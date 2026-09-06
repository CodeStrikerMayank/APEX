import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.app.database.connection import get_db
from backend.app.models.schema import Roadmap, RoadmapAction, Concept, Chapter, Subject, Topic, Student, utc_now
from backend.app.schemas.pydantic_models import RoadmapResponse, NextActionResponse, WeaknessDetail, PriorityItem
from backend.app.roadmap.next_action import NextActionEngine
from backend.app.roadmap.generator import RoadmapGenerator
from backend.app.roadmap.weakness import WeaknessDetector
from backend.app.roadmap.priority import PriorityEngine
from backend.app.events.collector import EventCollector

router = APIRouter(prefix="/roadmap", tags=["Dynamic Roadmap & Intelligence"])

@router.get("/active/{student_id}", response_model=RoadmapResponse)
def get_active_roadmap(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    next_engine = NextActionEngine(db)
    nba = next_engine.get_next_best_action(student_id)

    active_rm = (
        db.query(Roadmap)
        .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
        .order_by(Roadmap.version.desc())
        .first()
    )

    needs_regen = False
    if active_rm and active_rm.actions:
        first_c = db.query(Concept).filter(Concept.concept_id == active_rm.actions[0].concept_id).first()
        sub = first_c.topic.chapter.subject if (first_c and first_c.topic and first_c.topic.chapter) else None
        if sub and sub.exam_id != student.target_exam:
            needs_regen = True

    if not active_rm or needs_regen:
        generator = RoadmapGenerator(db, exam_id=student.target_exam)
        active_rm = generator.generate_roadmap(student_id, trigger_event="API_REQUEST_EXAM_SYNC")

    actions_list = []
    for act in active_rm.actions:
        concept = db.query(Concept).filter(Concept.concept_id == act.concept_id).first()
        topic = concept.topic if concept else None
        chapter = topic.chapter if topic else None
        subject = chapter.subject if chapter else None

        actions_list.append({
            "id": act.id,
            "action_id": act.id,
            "sequence_order": act.sequence_order,
            "action_type": act.action_type,
            "concept_id": act.concept_id,
            "concept_name": concept.name if concept else act.concept_id,
            "subject": subject.name if subject else "General",
            "priority_score": act.priority_score,
            "reasons": act.reasons or [],
            "target_questions_count": act.target_questions_count,
            "estimated_minutes": act.estimated_minutes,
            "target_difficulty": act.target_difficulty,
            "is_completed": act.is_completed
        })

    return RoadmapResponse(
        roadmap_id=active_rm.roadmap_id,
        student_id=student_id,
        version=active_rm.version,
        created_at=active_rm.created_at,
        next_best_action=nba,
        actions=actions_list
    )

@router.get("/next-action/{student_id}", response_model=Optional[NextActionResponse])
def get_next_action(student_id: str, db: Session = Depends(get_db)):
    next_engine = NextActionEngine(db)
    return next_engine.get_next_best_action(student_id)

@router.post("/action/complete/{action_id}")
def mark_action_completed(action_id: int, db: Session = Depends(get_db)):
    action = db.query(RoadmapAction).filter(RoadmapAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Roadmap action not found.")

    action.is_completed = True
    action.completed_at = utc_now()
    db.commit()

    student_id = action.roadmap.student_id if action.roadmap else None
    if student_id:
        EventCollector.log_event(
            db=db,
            student_id=student_id,
            session_id="roadmap",
            event_type="ROADMAP_ITEM_COMPLETED",
            concept_id=action.concept_id,
            metadata={"action_type": action.action_type}
        )
        db.commit()

    return {"status": "SUCCESS", "action_id": action_id}

@router.get("/weaknesses/{student_id}", response_model=List[WeaknessDetail])
def get_student_weaknesses(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam_id = student.target_exam if student else "JEE"

    detector = WeaknessDetector(db, exam_id=exam_id)
    return detector.detect_weaknesses(student_id)

@router.get("/priorities/{student_id}", response_model=List[PriorityItem])
def get_student_priorities(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam_id = student.target_exam if student else "JEE"

    engine = PriorityEngine(db, exam_id=exam_id)
    return engine.rank_all_priorities(student_id)

@router.post("/regenerate/{student_id}", response_model=RoadmapResponse)
def regenerate_roadmap(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    generator = RoadmapGenerator(db, exam_id=student.target_exam)
    generator.generate_roadmap(student_id, trigger_event="USER_REGENERATE_REQUEST")

    return get_active_roadmap(student_id, db)


# --- Locked Daily Mission To-Do Endpoints ---

@router.get("/daily-todo/{student_id}")
def get_daily_todo(
    student_id: str,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieves or locks today's 3-5 mission tasks for the student.
    Does not allow algorithm reshuffling mid-day.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.get_or_create_daily_todo(student_id, target_date=target_date)


@router.post("/daily-todo/complete/{student_id}/{task_id}")
def complete_daily_task(
    student_id: str,
    task_id: str,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Marks a specific task completed in today's locked mission.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.complete_task(student_id, task_id, target_date=target_date)


@router.post("/ai-customize-todo/{student_id}")
def ai_customize_todo(
    student_id: str,
    prompt: Optional[str] = None,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    AI-Customized Daily Mission Generator:
    Analyzes student cognitive gaps, Ebbinghaus forgetting rate, and target exam
    to generate a student-centric locked mission with clear pedagogical reasoning.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.ai_customize_daily_todo(student_id, custom_prompt=prompt, target_date=target_date)

