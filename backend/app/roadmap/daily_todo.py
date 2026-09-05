import datetime
import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.models.schema import (
    DailyTodoList, Student, StudentConceptMastery, Concept, Roadmap, RoadmapAction, utc_now
)
from backend.app.roadmap.priority import PriorityEngine
from backend.app.events.collector import EventCollector

class DailyTodoEngine:
    """
    Locked Daily Mission Generator & Manager:
    1. Reads student's current memory state, forgetting decay, and active roadmap.
    2. Curates 3-5 high-leverage tasks totaling 60-90 mins.
    3. Locks the list in LOCKED_ACTIVE status — no algorithm updates until all items are completed.
    4. Upon 100% completion, triggers achievement event and marks COMPLETED.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_daily_todo(
        self,
        student_id: str,
        target_date: Optional[str] = None,
        force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves today's locked todo list, or generates a new one if none exists for today.
        """
        today_str = target_date or datetime.date.today().isoformat()

        existing = (
            self.db.query(DailyTodoList)
            .filter(
                DailyTodoList.student_id == student_id,
                DailyTodoList.todo_date == today_str
            )
            .first()
        )

        if existing and not force_regenerate:
            return self._format_response(existing)

        student = self.db.query(Student).filter(Student.student_id == student_id).first()
        exam = student.target_exam if student else "JEE"

        # Assemble balanced task list:
        tasks = []

        # 1. Memory Guard / Flashcard review (from decaying concepts)
        decaying = (
            self.db.query(StudentConceptMastery)
            .filter(StudentConceptMastery.student_id == student_id, StudentConceptMastery.retention_score < 0.65)
            .first()
        )
        if decaying:
            c = self.db.query(Concept).filter(Concept.concept_id == decaying.concept_id).first()
            c_name = c.name if c else decaying.concept_id
            tasks.append({
                "task_id": "T1",
                "type": "MEMORY_GUARD",
                "title": f"Flashcard Retention Review: {c_name}",
                "description": f"Memory stability dipped to {int(decaying.retention_score * 100)}%. Review key definitions & boundary formulas.",
                "concept_id": decaying.concept_id,
                "estimated_minutes": 10,
                "is_completed": False
            })
        else:
            tasks.append({
                "task_id": "T1",
                "type": "MEMORY_GUARD",
                "title": "5-Minute Memory Calibration",
                "description": "Quick spaced-retention check across high-yield formulas.",
                "concept_id": None,
                "estimated_minutes": 10,
                "is_completed": False
            })

        # 2. Next Best Roadmap Action (Core Lecture or Incline Drill)
        active_rm = (
            self.db.query(Roadmap)
            .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
            .order_by(Roadmap.version.desc())
            .first()
        )
        if active_rm and active_rm.actions:
            incomplete_actions = [a for a in active_rm.actions if not a.is_completed][:2]
            for idx, act in enumerate(incomplete_actions):
                c = self.db.query(Concept).filter(Concept.concept_id == act.concept_id).first()
                c_name = c.name if c else act.concept_id
                t_type = "CORE_LECTURE" if idx == 0 else "TARGETED_PRACTICE"
                tasks.append({
                    "task_id": f"T{len(tasks) + 1}",
                    "type": t_type,
                    "title": f"{act.action_type.replace('_', ' ').title()}: {c_name}",
                    "description": "; ".join(act.reasons or ["High-yield curriculum milestone"]),
                    "concept_id": act.concept_id,
                    "estimated_minutes": act.estimated_minutes or 25,
                    "is_completed": False
                })

        # 3. Daily 3-Subject Assignment Anchor
        tasks.append({
            "task_id": f"T{len(tasks) + 1}",
            "type": "DAILY_ASSIGNMENT",
            "title": f"Daily Practice Assignment ({exam})",
            "description": "Solve your customized daily questions with immediate step-by-step mentor reasoning.",
            "concept_id": None,
            "estimated_minutes": 30,
            "is_completed": False
        })

        # 4. Micro-Check Wrap-up
        tasks.append({
            "task_id": f"T{len(tasks) + 1}",
            "type": "MICRO_CHECK",
            "title": "Wrap-up Diagnostic Pulse",
            "description": "3 quick confidence checkpoints to lock today's learning into permanent memory.",
            "concept_id": None,
            "estimated_minutes": 10,
            "is_completed": False
        })

        total_mins = sum(t["estimated_minutes"] for t in tasks)
        todo_id = f"todo_{student_id}_{today_str.replace('-', '')}_{uuid.uuid4().hex[:4]}"

        if existing and force_regenerate:
            existing.tasks_payload = tasks
            existing.total_tasks = len(tasks)
            existing.completed_tasks = 0
            existing.total_estimated_minutes = total_mins
            existing.status = "LOCKED_ACTIVE"
            self.db.commit()
            return self._format_response(existing)

        new_todo = DailyTodoList(
            todo_id=todo_id,
            student_id=student_id,
            todo_date=today_str,
            status="LOCKED_ACTIVE",
            total_tasks=len(tasks),
            completed_tasks=0,
            total_estimated_minutes=total_mins,
            tasks_payload=tasks,
            created_at=utc_now()
        )
        self.db.add(new_todo)
        self.db.commit()

        EventCollector.log_event(
            db=self.db,
            student_id=student_id,
            session_id=f"sess_{todo_id}",
            event_type="DAILY_TODO_LOCKED",
            resource_id=todo_id,
            metadata={"date": today_str, "tasks_count": len(tasks), "total_minutes": total_mins}
        )
        self.db.commit()

        return self._format_response(new_todo)

    def complete_task(self, student_id: str, task_id: str, target_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Marks a task in today's locked list as completed.
        Checks if entire day's mission is finished.
        """
        today_str = target_date or datetime.date.today().isoformat()

        todo = (
            self.db.query(DailyTodoList)
            .filter(
                DailyTodoList.student_id == student_id,
                DailyTodoList.todo_date == today_str
            )
            .first()
        )
        if not todo:
            return {"status": "ERROR", "message": "No active todo list found for today"}

        tasks = list(todo.tasks_payload or [])
        updated = False
        for t in tasks:
            if t["task_id"] == task_id:
                t["is_completed"] = True
                updated = True
                break

        if not updated:
            return {"status": "ERROR", "message": f"Task {task_id} not found in today's mission"}

        todo.tasks_payload = tasks
        todo.completed_tasks = sum(1 for t in tasks if t.get("is_completed"))

        # If all tasks finished, switch to COMPLETED
        if todo.completed_tasks >= todo.total_tasks:
            todo.status = "COMPLETED"
            todo.completed_at = utc_now()
            EventCollector.log_event(
                db=self.db,
                student_id=student_id,
                session_id=f"sess_{todo.todo_id}",
                event_type="DAILY_MISSION_ACCOMPLISHED",
                resource_id=todo.todo_id,
                metadata={"date": today_str, "total_tasks": todo.total_tasks}
            )

        self.db.commit()
        return self._format_response(todo)

    def _format_response(self, todo: DailyTodoList) -> Dict[str, Any]:
        progress = round((todo.completed_tasks / max(todo.total_tasks, 1)) * 100, 1)
        return {
            "todo_id": todo.todo_id,
            "student_id": todo.student_id,
            "date": todo.todo_date,
            "status": todo.status,
            "is_locked": todo.status == "LOCKED_ACTIVE",
            "total_tasks": todo.total_tasks,
            "completed_tasks": todo.completed_tasks,
            "total_estimated_minutes": todo.total_estimated_minutes,
            "progress_percentage": progress,
            "tasks": todo.tasks_payload,
            "completed_at": todo.completed_at.isoformat() if todo.completed_at else None
        }
