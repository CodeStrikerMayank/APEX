import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.connection import SessionLocal
from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept,
    Assessment, AssessmentAttempt, StudentAttemptItem, Question
)
from backend.app.ai.omni_context import OmniContextHarvester

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_lifetime_diagnostics_harvester(db_session):
    student_id = "test_hist_student_001"
    student = db_session.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(
            student_id=student_id,
            name="History Aspirant",
            email="hist@aspirant.test",
            password_hash="mock_password_hash",
            target_exam="JEE"
        )
        db_session.add(student)
        db_session.commit()

    # Find or use existing question
    q = db_session.query(Question).first()
    assert q is not None, "Need at least one question in database"

    # Find or use existing assessment
    assessment = db_session.query(Assessment).first()
    if not assessment:
        assessment = Assessment(
            assessment_id="test_assessment_hist_01",
            exam="JEE",
            title="Diagnostic Baseline Exam",
            duration_minutes=30
        )
        db_session.add(assessment)
        db_session.commit()

    # Create completed assessment attempt
    attempt_id = f"attempt_hist_{student_id}"
    attempt = db_session.query(AssessmentAttempt).filter(AssessmentAttempt.attempt_id == attempt_id).first()
    if not attempt:
        attempt = AssessmentAttempt(
            attempt_id=attempt_id,
            assessment_id=assessment.assessment_id,
            student_id=student_id,
            session_id="session_hist_01",
            total_questions=2,
            correct_count=1,
            score_percentage=50.0,
            is_completed=True,
            time_taken_seconds=120
        )
        db_session.add(attempt)
        db_session.flush()

        # Add 1 correct item and 1 mistake item
        item_correct = StudentAttemptItem(
            attempt_id=attempt_id,
            question_id=q.question_id,
            concept_id=q.concept_id,
            student_answer=q.correct_answer,
            is_correct=True,
            time_taken_seconds=45,
            difficulty=0.5
        )
        item_wrong = StudentAttemptItem(
            attempt_id=attempt_id,
            question_id=q.question_id,
            concept_id=q.concept_id,
            student_answer="WRONG_A",
            is_correct=False,
            time_taken_seconds=60,
            difficulty=0.7,
            error_type="CALCULATION_ERROR"
        )
        db_session.add_all([item_correct, item_wrong])
        db_session.commit()

    # Harvest lifetime diagnostics
    diagnostics = OmniContextHarvester.harvest_lifetime_diagnostics(student_id, db_session)
    assert diagnostics["total_assessments"] >= 1
    assert diagnostics["total_questions_attempted"] >= 2
    assert diagnostics["total_correct"] >= 1
    assert "CALCULATION_ERROR" in diagnostics["error_breakdown"]
    assert len(diagnostics["top_error_types"]) >= 1
    assert len(diagnostics["chronological_scores"]) >= 1

    # Test full omni-context inclusion
    full_ctx = OmniContextHarvester.harvest_full_context(student_id, db_session)
    assert "lifetime_diagnostics" in full_ctx
    assert full_ctx["lifetime_diagnostics"]["total_assessments"] >= 1

    # Test formatting string
    grounding = OmniContextHarvester.format_grounding_block(full_ctx)
    assert "Lifetime History" in grounding or "Dominant Lifetime Error Modes" in grounding

def test_api_diagnostics_history(client, db_session):
    student = db_session.query(Student).first()
    sid = student.student_id if student else "general"
    res = client.get(f"/api/ai/diagnostics/history/{sid}")
    assert res.status_code == 200
    data = res.json()
    assert "total_assessments" in data
    assert "error_breakdown" in data
    assert "chronological_scores" in data

def test_api_smartboard_topic(client, db_session):
    concept = db_session.query(Concept).first()
    assert concept is not None
    res = client.get(f"/api/ai/smartboard/topic/{concept.concept_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["concept_id"] == concept.concept_id
    assert "name" in data
    assert "upstream_prerequisites" in data
    assert "downstream_unlocked" in data
    assert "fineweb_reading" in data
    assert "sample_questions" in data

def test_api_smartboard_mistakes(client, db_session):
    student = db_session.query(Student).first()
    sid = student.student_id if student else "general"
    res = client.get(f"/api/ai/smartboard/mistakes/{sid}")
    assert res.status_code == 200
    data = res.json()
    assert "total_mistakes" in data
    assert "mistakes" in data
