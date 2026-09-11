from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
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
from backend.app.ai.omni_context import OmniContextHarvester

router = APIRouter(prefix="/ai", tags=["Offline AI Assistant & Tools"])

@router.get("/telemetry-hud/{student_id}")
async def get_student_telemetry_hud(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Returns live student cognitive telemetry: IRT ability, weak concepts, DAG bottlenecks, and FineWeb citations."""
    hud_data = OmniContextHarvester.harvest_full_context(student_id, db)
    return hud_data

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
    latest_attempt = None
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

    # Harvest deep omni-context across psychometrics, weak concepts, DAG bottlenecks, and FineWeb readings
    try:
        omni_ctx = OmniContextHarvester.harvest_full_context(student_id, db, req.get_prompt())
        for k, v in omni_ctx.items():
            if k not in student_context or not student_context[k]:
                student_context[k] = v
    except Exception as e:
        pass

    mode = (req.mode or "pedagogical").lower()
    student_context["mode"] = mode

    # Build omni-context grounding block
    grounding_str = OmniContextHarvester.format_grounding_block(student_context, mode=mode)

    mode_instructions = {
        "socratic": (
            "Mode: SOCRATIC COACH. Do NOT provide direct full solutions immediately. "
            "Ask probing conceptual questions, guide the student step-by-step to deduce formulas or identify errors, "
            "and encourage active problem solving."
        ),
        "forensics": (
            "Mode: MISTAKE FORENSICS & STRATEGIST. Focus specifically on analyzing error patterns, "
            "explaining why particular distractor traps were fallen for, contrasting student answers with correct keys, "
            "and giving pacing and negative marking defense guidelines."
        ),
        "pedagogical": (
            "Mode: PEDAGOGICAL MENTOR. Deliver clear, academically rigorous derivations, "
            "explain theoretical foundations step-by-step, format all formulas with standard LaTeX ($...$ and $$...$$), "
            "and provide structured concept summaries."
        )
    }
    mode_guidance = mode_instructions.get(mode, mode_instructions["pedagogical"])

    exam_label = student.target_exam if student and student.target_exam else "JEE"
    system_prompt = (
        f"You are an offline pedagogical AI study mentor for {exam_label}.\n"
        f"{mode_guidance}\n\n"
        f"Real-Time Student Cognitive Grounding:\n{grounding_str}\n\n"
        "Your role is to guide the student, explain concepts and error patterns, "
        "explain why their dynamic roadmap was sequenced the way it was, and give direct, rigorous guidance. "
        "All adaptive diagnostic engines are active on standby with zero compulsory barriers."
    )

    from backend.app.ai.socratic_agents import SocraticCoordinator, SocraticProberAgent, PsychologistAgent

    # Determine active session duration for Agent 3 (Psychologist)
    active_minutes = 0.0
    from backend.app.models.schema import utc_now
    if student and student.last_active:
        diff_secs = (utc_now() - student.last_active).total_seconds()
        if 0 <= diff_secs <= 86400:
            active_minutes = diff_secs / 60.0
    if latest_attempt and latest_attempt.time_taken_seconds:
        active_minutes = max(active_minutes, latest_attempt.time_taken_seconds / 60.0)

    if mode == "socratic":
        concept_name = "Core Conceptual Foundation"
        if latest_attempt and student_context.get("latest_quiz", {}).get("mistakes"):
            first_mistake = student_context["latest_quiz"]["mistakes"][0]
            concept_name = first_mistake.get("concept_id", concept_name)
            error_type = first_mistake.get("error_type")
            explanation = first_mistake.get("explanation")
        else:
            error_type = "CONCEPTUAL_ERROR"
            explanation = None

        socratic_bundle = SocraticCoordinator.coordinate_response(
            student_id=student_id,
            db=db,
            concept_name=concept_name,
            error_type=error_type,
            explanation=explanation,
            session_duration_minutes=active_minutes,
            student_name=student.name if student else "Aspirant"
        )
        final_text = socratic_bundle["text"]
        source = socratic_bundle["source"]
    else:
        res = await llm.generate_text(
            prompt=req.get_prompt(),
            system_prompt=system_prompt,
            student_context=student_context
        )
        final_text = res["text"]
        source = res["source"]

        # Agent 3 (Psychologist) fatigue check for long sessions
        break_prompt = PsychologistAgent.check_and_inject_break_prompt(
            active_duration_minutes=active_minutes,
            student_name=student.name if student else "Aspirant"
        )
        if break_prompt:
            final_text += break_prompt

    return AIChatResponse(response=final_text, source=source)

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


@router.get("/engine-status")
async def get_engine_status():
    from backend.app.ai.cloud_llm import CloudLLMHub
    from backend.app.ai.local_llm import LocalLLMClient
    
    hub = CloudLLMHub()
    gemini_avail = hub.is_gemini_available()
    grok_avail = hub.is_grok_available()
    custom_avail = hub.is_custom_available()
    
    llm = LocalLLMClient()
    ollama_ok = await llm.is_available()
    
    tier = "CLOUD_PRIMARY"
    if not gemini_avail and not grok_avail:
        if custom_avail:
            tier = "CLOUD_CUSTOM"
        else:
            tier = "LOCAL_OLLAMA" if ollama_ok else "DETERMINISTIC_MENTOR"
        
    return {
        "active_tier": tier,
        "gemini_available": gemini_avail,
        "grok_available": grok_avail,
        "custom_available": custom_avail,
        "ollama_available": ollama_ok,
        "mentor_failsafe_active": True,
        "supported_exams": ["JEE", "NEET", "UPSC"],
        "message": "Cloud LLM (Gemini/Grok/Custom) primary with local Ollama fallback and deterministic mentor fail-safe."
    }


class KeyConfigRequest(BaseModel):
    gemini_api_key: Optional[str] = None
    grok_api_key: Optional[str] = None
    custom_provider: Optional[str] = None
    custom_api_key: Optional[str] = None
    custom_base_url: Optional[str] = None
    custom_model: Optional[str] = None
    persist_to_env: bool = False


class KeyTestRequest(BaseModel):
    provider: str
    key: str
    base_url: Optional[str] = None
    model: Optional[str] = None


@router.get("/keys-config")
async def get_keys_config():
    """Returns safe masked configuration of currently active AI provider keys."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    return CloudLLMHub.get_masked_config()


@router.post("/keys-config")
async def update_keys_config(req: KeyConfigRequest):
    """Dynamically applies new AI provider keys to runtime without server restart."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    res = CloudLLMHub.update_keys(
        gemini_key=req.gemini_api_key,
        grok_key=req.grok_api_key,
        custom_provider=req.custom_provider,
        custom_api_key=req.custom_api_key,
        custom_base_url=req.custom_base_url,
        custom_model=req.custom_model,
        persist_to_env=req.persist_to_env
    )
    return res


@router.post("/test-key")
async def test_provider_key(req: KeyTestRequest):
    """Tests live validity of a provided key."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    return await CloudLLMHub.test_key(
        provider=req.provider,
        key=req.key,
        base_url=req.base_url,
        model=req.model
    )


@router.get("/fineweb/readings")
async def get_fineweb_readings_endpoint(
    course: Optional[str] = None,
    subject: Optional[str] = None,
    sub_category: Optional[str] = None,
    min_score: float = 0.0,
    db: Session = Depends(get_db)
):
    """
    Returns comprehensive educational readings across ALL curriculum topics extracted from the API,
    divided into primary categories (Subjects) and granular subcategories (e.g., Mechanics, Electrodynamics, Calculus).
    """
    from backend.app.knowledge_graph.fineweb_vault import get_fineweb_readings, extract_all_curriculum_readings

    # Fetch all readings for this course to extract available subcategories
    all_course_readings = extract_all_curriculum_readings(course=course or "ALL", db=db)

    # Compute subcategories list for dynamic frontend pills
    subcat_counts = {}
    for r in all_course_readings:
        sc = r.get("sub_category", "General")
        subcat_counts[sc] = subcat_counts.get(sc, 0) + 1

    subcat_emoji_map = {
        "Mechanics": "⚙️ Mechanics",
        "Electrodynamics": "⚡ Electrodynamics",
        "Optics": "🔍 Optics",
        "Modern Physics": "⚛️ Modern Physics",
        "Thermal Physics": "🔥 Thermal Physics",
        "Calculus & Analysis": "📐 Calculus & Analysis",
        "Algebra": "📊 Algebra",
        "Vectors & 3D Geometry": "📐 Vectors & 3D Geometry",
        "Physical Chemistry": "🧪 Physical Chemistry",
        "Organic Chemistry": "⚗️ Organic Chemistry",
        "Biochemistry & Biomolecules": "🧬 Biomolecules",
        "Inorganic Chemistry": "🧱 Inorganic Chemistry",
        "Cell Biology": "🔬 Cell Biology",
        "Genetics & Evolution": "🧬 Genetics & Evolution",
        "Human Physiology": "🫀 Human Physiology",
        "Plant Physiology": "🌱 Plant Physiology",
        "Ecology & Environment": "🌍 Ecology & Environment",
        "Polity & Governance": "🏛️ Polity & Governance",
        "Economy & Development": "📈 Economy & Development",
        "Environment & Ecology": "🌿 Environment & Ecology",
        "Ethics & Integrity": "⚖️ Ethics & Integrity",
        "Modern History & Culture": "📜 Modern History",
        "CSAT & Aptitude": "🧩 CSAT & Aptitude"
    }

    sub_categories_list = [
        {"id": "all", "label": "All Subcategories", "count": len(all_course_readings)}
    ] + [
        {
            "id": sc,
            "label": f"{subcat_emoji_map.get(sc, sc)} ({count})",
            "name": sc,
            "count": count
        }
        for sc, count in sorted(subcat_counts.items())
    ]

    # Filtered readings based on query params
    readings = get_fineweb_readings(
        course=course,
        subject=subject,
        sub_category=sub_category,
        min_score=min_score,
        db=db
    )

    return {
        "dataset": "HuggingFaceFW/fineweb-edu & APEX Curriculum Graph",
        "total_tokens_dataset": "1.3T",
        "course": course or "ALL",
        "count": len(readings),
        "total_topics": len(all_course_readings),
        "sub_categories": sub_categories_list,
        "readings": readings
    }


@router.get("/fineweb/reading/{reading_id}")
async def get_single_fineweb_reading(reading_id: str, db: Session = Depends(get_db)):
    """Fetches full academic excerpt by reading ID."""
    from backend.app.knowledge_graph.fineweb_vault import get_reading_by_id
    reading = get_reading_by_id(reading_id, db=db)
    if not reading:
        raise HTTPException(status_code=404, detail=f"Reading {reading_id} not found")
    return reading





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

