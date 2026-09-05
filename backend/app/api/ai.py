from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from backend.app.database.connection import get_db
from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept, Question,
    AssessmentAttempt, StudentAttemptItem, Roadmap, RoadmapAction
)
from backend.app.schemas.pydantic_models import AIChatRequest, AIChatResponse, AIQuestionGenRequest
from backend.app.ai.local_llm import LocalLLMClient
from backend.app.ai.explanation import ExplanationGenerator
from backend.app.ai.question_generator import AIQuestionGenerator

router = APIRouter(prefix="/ai", tags=["Offline AI Assistant & Tools"])

@router.post("/chat/{student_id}", response_model=AIChatResponse)
async def chat_with_assistant(
    student_id: str,
    req: AIChatRequest,
    db: Session = Depends(get_db)
):
    llm = LocalLLMClient()

    student_context: Dict[str, Any] = {}
    context_str = ""

    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student:
        student_context["student_name"] = student.name
        student_context["target_exam"] = student.target_exam

        # Masteries
        masteries = db.query(StudentConceptMastery).filter(StudentConceptMastery.student_id == student_id).all()
        avg_m = (sum(m.mastery for m in masteries) / max(len(masteries), 1)) if masteries else 0.0
        avg_theta = (sum(m.irt_ability for m in masteries) / max(len(masteries), 1)) if masteries else 0.0
        student_context["overall_mastery"] = round(avg_m * 100, 1)
        student_context["latent_ability_theta"] = round(avg_theta, 2)

        # Latest Quiz Attempt
        latest_attempt = (
            db.query(AssessmentAttempt)
            .filter(AssessmentAttempt.student_id == student_id, AssessmentAttempt.is_completed == True)
            .order_by(AssessmentAttempt.submitted_at.desc())
            .first()
        )
        if latest_attempt:
            items = (
                db.query(StudentAttemptItem, Question)
                .join(Question, StudentAttemptItem.question_id == Question.question_id)
                .filter(StudentAttemptItem.attempt_id == latest_attempt.attempt_id)
                .all()
            )
            quiz_items = []
            mistakes = []
            subject_breakdown: Dict[str, Dict[str, int]] = {}

            for item, q in items:
                sub = q.subject or "General"
                if sub not in subject_breakdown:
                    subject_breakdown[sub] = {"total": 0, "correct": 0}
                subject_breakdown[sub]["total"] += 1
                if item.is_correct:
                    subject_breakdown[sub]["correct"] += 1

                distractor_note = None
                if not item.is_correct and q.distractor_explanations and item.student_answer:
                    distractor_note = q.distractor_explanations.get(item.student_answer)

                item_info = {
                    "question_id": q.question_id,
                    "subject": q.subject,
                    "concept_id": q.concept_id,
                    "is_correct": item.is_correct,
                    "student_answer": item.student_answer,
                    "correct_answer": q.correct_answer,
                    "error_type": item.error_type,
                    "explanation": q.explanation,
                    "distractor_note": distractor_note,
                    "content_snippet": q.content[:140] + "..." if len(q.content) > 140 else q.content
                }
                quiz_items.append(item_info)
                if not item.is_correct:
                    mistakes.append(item_info)

            student_context["latest_quiz"] = {
                "score_percentage": latest_attempt.score_percentage,
                "correct_count": latest_attempt.correct_count,
                "total_questions": latest_attempt.total_questions,
                "time_taken_seconds": latest_attempt.time_taken_seconds,
                "subject_breakdown": subject_breakdown,
                "items": quiz_items,
                "mistakes": mistakes
            }

        # Latest Roadmap
        latest_roadmap = (
            db.query(Roadmap)
            .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
            .order_by(Roadmap.version.desc())
            .first()
        )
        if not latest_roadmap:
            try:
                from backend.app.roadmap.generator import RoadmapGenerator
                gen = RoadmapGenerator(db, exam_id=student.target_exam)
                latest_roadmap = gen.generate_roadmap(student_id, trigger_event="AI_STANDBY_INIT")
                db.commit()
            except Exception:
                db.rollback()

        if latest_roadmap:
            actions = (
                db.query(RoadmapAction)
                .filter(RoadmapAction.roadmap_id == latest_roadmap.roadmap_id)
                .order_by(RoadmapAction.sequence_order)
                .limit(6)
                .all()
            )
            student_context["roadmap_actions"] = []
            for a in actions:
                c = db.query(Concept).filter(Concept.concept_id == a.concept_id).first()
                student_context["roadmap_actions"].append({
                    "order": a.sequence_order,
                    "concept_id": a.concept_id,
                    "title": c.name if c else a.concept_id,
                    "action_type": a.action_type,
                    "priority_score": a.priority_score,
                    "reasons": a.reasons,
                    "target_questions": a.target_questions_count,
                    "estimated_minutes": a.estimated_minutes
                })

    system_prompt = (
        f"You are an offline pedagogical AI study mentor for {student.target_exam if student else 'JEE/NEET'}. "
        "Your role is to guide the student, explain concepts and error patterns, "
        "explain why their dynamic roadmap was sequenced the way it was, and give direct, rigorous guidance. "
        "All adaptive diagnostic engines are active on standby with zero compulsory barriers."
    )

    res = await llm.generate_text(
        prompt=req.get_prompt(),
        system_prompt=system_prompt,
        student_context=student_context
    )

    return AIChatResponse(response=res["text"], source=res["source"])

@router.post("/generate-question")
async def generate_practice_question(
    req: AIQuestionGenRequest,
    db: Session = Depends(get_db)
):
    concept = db.query(Concept).filter(Concept.concept_id == req.concept_id).first()
    concept_name = concept.name if concept else req.concept_id

    gen = AIQuestionGenerator()
    q_data = await gen.generate_candidate_question(
        exam=req.exam,
        subject=req.subject,
        chapter=req.chapter,
        concept_id=req.concept_id,
        concept_name=concept_name,
        target_difficulty=req.difficulty
    )
    return q_data


@router.post("/brain-briefing/{student_id}")
async def get_brain_briefing(
    student_id: str,
    page_context: str = "DAILY_PRACTICE",
    concept_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Powers the global Brain Icon Copilot:
    - Real-time page context
    - Performance state
    - Hidden prerequisite gap assessment (from DAG)
    - Actionable cover-up drill
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam = student.target_exam if student else "JEE"

    masteries = db.query(StudentConceptMastery).filter(StudentConceptMastery.student_id == student_id).all()
    avg_m = (sum(m.mastery for m in masteries) / max(len(masteries), 1)) if masteries else 0.50
    avg_theta = (sum(m.irt_ability for m in masteries) / max(len(masteries), 1)) if masteries else 0.0

    target_concept = None
    if concept_id:
        target_concept = db.query(Concept).filter(Concept.concept_id == concept_id).first()

    concept_name = target_concept.name if target_concept else "Current Core Module"

    # Evaluate gap from DAG
    broken_prereqs = []
    if concept_id:
        from backend.app.knowledge_graph.prerequisites import PrerequisiteEngine
        pe = PrerequisiteEngine(db)
        status = pe.check_prerequisites_status(student_id, concept_id)
        broken_prereqs = status.get("missing_prerequisites", [])

    coverup_steps = [
        f"Review 2-minute visual breakdown of {concept_name}",
        f"Solve 2 guided warm-up questions to secure foundational mastery"
    ]
    if broken_prereqs:
        coverup_steps.insert(0, f"Prerequisite Bridge: Quick revision of {broken_prereqs[0]}")

    # Generate sharp mentor advice using Cloud / Local LLM
    from backend.app.ai.cloud_llm import CloudLLMHub
    hub = CloudLLMHub()
    prompt = (
        f"Act as a master tutor for an Indian {exam} student. "
        f"The student is on the {page_context} page studying '{concept_name}'. "
        f"Their overall mastery is {round(avg_m * 100, 1)}%. "
        f"Prerequisite gaps flagged: {', '.join(broken_prereqs) if broken_prereqs else 'None'}. "
        "Give a 2-sentence sharp, highly motivating, and actionable tutor briefing explaining their exact immediate focus."
    )
    cloud_res = await hub.generate_best(prompt)
    mentor_quote = cloud_res.get("text") if cloud_res.get("text") else (
        f"You're in the zone for {concept_name}. Focus on setting up coordinate axes clearly before diving into algebra!"
    )

    return {
        "page_context": page_context,
        "concept_name": concept_name,
        "performance": {
            "overall_mastery_pct": round(avg_m * 100, 1),
            "latent_ability_theta": round(avg_theta, 2),
            "readiness_tier": "READY_FOR_DRILL" if avg_m >= 0.50 else "NEEDS_FOUNDATION_BRIDGE"
        },
        "gap_assessment": {
            "symptom": f"Friction in {concept_name}",
            "prerequisite_gaps": broken_prereqs,
            "root_severity": "MODERATE" if broken_prereqs else "LOW"
        },
        "coverup_strategy": coverup_steps,
        "mentor_quote": mentor_quote,
        "engine_source": cloud_res.get("source", "LOCAL_LLM")
    }

