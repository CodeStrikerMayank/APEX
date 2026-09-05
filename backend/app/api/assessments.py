import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.app.database.connection import get_db
from backend.app.models.schema import AssessmentAttempt, Assessment, Question, Student, CatSessionState
from backend.app.schemas.pydantic_models import (
    AssessmentStartRequest, AssessmentSessionResponse,
    AssessmentSubmitRequest, AssessmentResultResponse,
    CatStartRequest, CatNextQuestionRequest, CatNextQuestionResponse,
    DrillStartRequest, FullScanStartRequest, AdvancedStartRequest
)
from backend.app.assessment.quiz_engine import QuizEngine
from backend.app.roadmap.generator import RoadmapGenerator
from backend.app.student_model.cat_engine import CATEngine
from backend.app.student_model.irt import ItemResponseTheory

router = APIRouter(prefix="/assessments", tags=["Assessments & Testing"])

@router.post("/start", response_model=AssessmentSessionResponse)
def start_assessment(
    req: AssessmentStartRequest,
    student_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    target_student_id = req.student_id or student_id
    if not target_student_id:
        raise HTTPException(status_code=422, detail="student_id is required either in request body or as query parameter")

    engine = QuizEngine(db)
    session_data = engine.start_assessment(
        student_id=target_student_id,
        exam=req.exam,
        assessment_type=req.assessment_type,
        stage=req.stage,
        duration_minutes=req.duration_minutes or 30,
        target_concept_id=req.target_concept_id
    )
    return session_data

@router.post("/start-drill", response_model=AssessmentSessionResponse)
def start_drill_assessment(
    req: Optional[DrillStartRequest] = None,
    student_id: Optional[str] = None,
    subject: Optional[str] = None,
    exam: Optional[str] = None,
    chapter_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    target_student_id = (req.student_id if req and req.student_id else None) or student_id
    target_subject = (req.subject if req and req.subject else None) or subject
    target_exam = (req.exam if req and req.exam else None) or exam or "JEE"
    target_chapter_id = (req.chapter_id if req and req.chapter_id else None) or chapter_id

    if not target_student_id:
        raise HTTPException(status_code=422, detail="student_id is required in body or query parameters")
    if not target_subject:
        raise HTTPException(status_code=422, detail="subject is required in body or query parameters")

    duration = req.duration_minutes if req and req.duration_minutes else 15

    engine = QuizEngine(db)
    session_data = engine.start_drill_assessment(
        student_id=target_student_id,
        exam=target_exam,
        subject=target_subject,
        chapter_id=target_chapter_id,
        duration_minutes=duration
    )
    return session_data

@router.post("/start-full-scan", response_model=AssessmentSessionResponse)
def start_full_scan_assessment(
    req: Optional[FullScanStartRequest] = None,
    student_id: Optional[str] = None,
    exam: Optional[str] = None,
    db: Session = Depends(get_db)
):
    target_student_id = (req.student_id if req and req.student_id else None) or student_id
    target_exam = (req.exam if req and req.exam else None) or exam or "JEE"

    if not target_student_id:
        raise HTTPException(status_code=422, detail="student_id is required in body or query parameters")

    duration = req.duration_minutes if req and req.duration_minutes else 40

    engine = QuizEngine(db)
    session_data = engine.start_full_scan_assessment(
        student_id=target_student_id,
        exam=target_exam,
        duration_minutes=duration
    )
    return session_data

@router.post("/start-advanced", response_model=AssessmentSessionResponse)
def start_advanced_assessment(
    req: Optional[AdvancedStartRequest] = None,
    student_id: Optional[str] = None,
    exam: Optional[str] = None,
    subject: Optional[str] = None,
    db: Session = Depends(get_db)
):
    target_student_id = (req.student_id if req and req.student_id else None) or student_id
    target_exam = (req.exam if req and req.exam else None) or exam or "JEE"
    target_subject = (req.subject if req and req.subject else None) or subject

    if not target_student_id:
        raise HTTPException(status_code=422, detail="student_id is required in body or query parameters")

    duration = req.duration_minutes if req and req.duration_minutes else 20

    engine = QuizEngine(db)
    session_data = engine.start_advanced_challenge(
        student_id=target_student_id,
        exam=target_exam,
        subject=target_subject,
        duration_minutes=duration
    )
    return session_data

@router.post("/submit", response_model=AssessmentResultResponse)
def submit_assessment(
    req: AssessmentSubmitRequest,
    db: Session = Depends(get_db)
):
    engine = QuizEngine(db)
    responses_list = [r.model_dump() for r in req.responses]
    result = engine.submit_assessment(
        attempt_id=req.attempt_id,
        responses=responses_list
    )

    attempt = db.query(AssessmentAttempt).filter(AssessmentAttempt.attempt_id == req.attempt_id).first()
    # Regenerate dynamic roadmap immediately after assessment
    generator = RoadmapGenerator(db, exam_id=attempt.assessment.exam)
    new_roadmap = generator.generate_roadmap(
        student_id=attempt.student_id,
        trigger_event="ASSESSMENT_COMPLETED"
    )

    result["new_roadmap_summary"] = {
        "roadmap_id": new_roadmap.roadmap_id,
        "version": new_roadmap.version,
        "actions_count": len(new_roadmap.actions)
    }

    return result

@router.get("/history/{student_id}")
def get_assessment_history(student_id: str, db: Session = Depends(get_db)):
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.student_id == student_id)
        .order_by(AssessmentAttempt.started_at.desc())
        .all()
    )

    history = []
    for a in attempts:
        asmt = a.assessment
        history.append({
            "attempt_id": a.attempt_id,
            "title": asmt.title if asmt else "Diagnostic Quiz",
            "exam": asmt.exam if asmt else "JEE",
            "score_percentage": a.score_percentage,
            "correct_count": a.correct_count,
            "total_questions": a.total_questions,
            "time_taken_seconds": a.time_taken_seconds,
            "status": a.status,
            "started_at": a.started_at,
            "submitted_at": a.submitted_at
        })

    return history


def _format_cat_question(q: Question) -> Dict[str, Any]:
    return {
        "question_id": q.question_id,
        "content": q.content,
        "options": q.options,
        "difficulty": q.difficulty,
        "subject": q.subject,
        "chapter": q.chapter,
        "topic": q.topic,
        "concept_id": q.concept_id,
        "estimated_time": q.estimated_time,
        "image_url": q.image_url,
    }


@router.post("/cat/start", response_model=CatNextQuestionResponse)
def start_cat_assessment(
    req: CatStartRequest,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.student_id == req.student_id).first()
    if not student:
        student = Student(
            student_id=req.student_id,
            name="Aspirant",
            email=f"{req.student_id}@adaptive.local",
            password_hash="temp_hash",
            target_exam=req.exam,
        )
        db.add(student)
        db.flush()

    query = db.query(Question).filter(Question.exam == req.exam)
    if req.subject:
        query = query.filter(Question.subject == req.subject)
    questions = query.all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available for this exam/subject.")

    candidate_ids = [q.question_id for q in questions]
    candidate_items = [
        {
            "question_id": q.question_id,
            "difficulty_b": ItemResponseTheory.difficulty_to_b_parameter(q.difficulty),
            "discrimination_a": q.discrimination or 1.0,
            "guessing_c": q.guessing or 0.25,
        }
        for q in questions
    ]

    session_id = f"cat_{uuid.uuid4().hex[:16]}"
    first_item_meta = CATEngine.select_next_item(0.0, candidate_items, candidate_ids)
    first_q_id = first_item_meta["question_id"] if first_item_meta else candidate_ids[0]

    session = CatSessionState(
        session_id=session_id,
        student_id=req.student_id,
        exam=req.exam,
        subject=req.subject,
        current_theta=0.0,
        current_sem=1.50,
        items_answered_count=0,
        is_terminated=False,
        answered_history=[],
        unvisited_question_ids=[qid for qid in candidate_ids if qid != first_q_id]
    )
    db.add(session)
    db.commit()

    first_q = db.query(Question).filter(Question.question_id == first_q_id).first()
    return CatNextQuestionResponse(
        session_id=session_id,
        is_complete=False,
        current_theta=0.0,
        sem=1.50,
        items_answered_count=0,
        question=_format_cat_question(first_q) if first_q else None
    )


@router.post("/cat/next-question", response_model=CatNextQuestionResponse)
def cat_next_question(
    req: CatNextQuestionRequest,
    db: Session = Depends(get_db)
):
    session = db.query(CatSessionState).filter(CatSessionState.session_id == req.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="CAT session not found.")

    if session.is_terminated:
        return CatNextQuestionResponse(
            session_id=session.session_id,
            is_complete=True,
            current_theta=session.current_theta,
            final_theta=session.current_theta,
            sem=session.current_sem,
            items_answered_count=session.items_answered_count,
            termination_reason=session.termination_reason or "SESSION_ALREADY_TERMINATED"
        )

    # Process response if last_question_id provided
    if req.last_question_id:
        last_q = db.query(Question).filter(Question.question_id == req.last_question_id).first()
        if last_q:
            is_correct = (req.student_answer == last_q.correct_answer)
            b = ItemResponseTheory.difficulty_to_b_parameter(last_q.difficulty)
            a = last_q.discrimination or 1.0
            c = last_q.guessing or 0.25

            # Update answered history
            history = list(session.answered_history or [])
            history.append({
                "question_id": last_q.question_id,
                "is_correct": is_correct,
                "difficulty_b": b,
                "discrimination_a": a,
                "guessing_c": c,
                "student_answer": req.student_answer,
                "correct_answer": last_q.correct_answer,
                "time_taken_seconds": req.time_taken_seconds or 0
            })
            session.answered_history = history
            session.items_answered_count = len(history)

            # Re-estimate ability via EAP
            new_theta, new_sd = CATEngine.estimate_theta_eap(history)
            session.current_theta = new_theta
            new_sem = CATEngine.calculate_sem(new_theta, history)
            session.current_sem = round(new_sem, 4)

            # Evaluate termination
            is_term, reason = CATEngine.evaluate_termination(
                session.items_answered_count,
                session.current_sem
            )
            if is_term:
                session.is_terminated = True
                session.termination_reason = reason
                db.commit()
                return CatNextQuestionResponse(
                    session_id=session.session_id,
                    is_complete=True,
                    current_theta=session.current_theta,
                    final_theta=session.current_theta,
                    sem=session.current_sem,
                    items_answered_count=session.items_answered_count,
                    termination_reason=reason
                )

    # Filter unvisited question IDs
    unvisited = [qid for qid in (session.unvisited_question_ids or []) if qid != req.last_question_id]
    if not unvisited:
        session.is_terminated = True
        session.termination_reason = "QUESTION_POOL_EXHAUSTED"
        db.commit()
        return CatNextQuestionResponse(
            session_id=session.session_id,
            is_complete=True,
            current_theta=session.current_theta,
            final_theta=session.current_theta,
            sem=session.current_sem,
            items_answered_count=session.items_answered_count,
            termination_reason="QUESTION_POOL_EXHAUSTED"
        )

    # Select next question maximizing Fisher Information
    candidate_qs = db.query(Question).filter(Question.question_id.in_(unvisited)).all()
    candidate_items = [
        {
            "question_id": q.question_id,
            "difficulty_b": ItemResponseTheory.difficulty_to_b_parameter(q.difficulty),
            "discrimination_a": q.discrimination or 1.0,
            "guessing_c": q.guessing or 0.25,
        }
        for q in candidate_qs
    ]

    best_item = CATEngine.select_next_item(session.current_theta, candidate_items, unvisited)
    if not best_item:
        session.is_terminated = True
        session.termination_reason = "NO_VALID_CANDIDATE_FOUND"
        db.commit()
        return CatNextQuestionResponse(
            session_id=session.session_id,
            is_complete=True,
            current_theta=session.current_theta,
            final_theta=session.current_theta,
            sem=session.current_sem,
            items_answered_count=session.items_answered_count,
            termination_reason="NO_VALID_CANDIDATE_FOUND"
        )

    chosen_qid = best_item["question_id"]
    session.unvisited_question_ids = [qid for qid in unvisited if qid != chosen_qid]
    db.commit()

    chosen_q = next((q for q in candidate_qs if q.question_id == chosen_qid), None)
    return CatNextQuestionResponse(
        session_id=session.session_id,
        is_complete=False,
        current_theta=session.current_theta,
        sem=session.current_sem,
        items_answered_count=session.items_answered_count,
        question=_format_cat_question(chosen_q) if chosen_q else None
    )
