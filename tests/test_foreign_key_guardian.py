"""
Test Foreign Key Auto-Provisioning Guardian (Rule 2)
Verifies that persisting child records without existing parent records automatically provisions
the baseline parent records rather than throwing SQLite IntegrityError.
"""
import pytest
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.models.schema import (
    Student, Concept, Question, DailyAssignment, DailyAssignmentItem,
    AssessmentAttempt, StudentAttemptItem, StudentConceptMastery
)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

def test_auto_provision_student_concept_mastery(db_session):
    # Child record with totally non-existent student and concept IDs
    orphan_student_id = "orphan_std_9999"
    orphan_concept_id = "orphan_cpt_9999"

    mastery = StudentConceptMastery(
        student_id=orphan_student_id,
        concept_id=orphan_concept_id,
        mastery=0.75,
        attempts_count=3,
        correct_count=2
    )
    db_session.add(mastery)
    # This flush would fail with IntegrityError if guardian was not active
    db_session.flush()

    # Verify parent records were auto-provisioned
    student = db_session.query(Student).filter(Student.student_id == orphan_student_id).first()
    concept = db_session.query(Concept).filter(Concept.concept_id == orphan_concept_id).first()

    assert student is not None
    assert student.student_id == orphan_student_id
    assert concept is not None
    assert concept.concept_id == orphan_concept_id
    assert mastery.mastery == 0.75

def test_auto_provision_daily_assignment_item(db_session):
    orphan_assignment_id = "orphan_asgn_8888"
    orphan_question_id = "orphan_q_8888"

    item = DailyAssignmentItem(
        assignment_id=orphan_assignment_id,
        question_id=orphan_question_id,
        subject="Physics",
        sequence_index=1,
        student_answer="A",
        is_correct=True
    )
    db_session.add(item)
    db_session.flush()

    assignment = db_session.query(DailyAssignment).filter(DailyAssignment.assignment_id == orphan_assignment_id).first()
    question = db_session.query(Question).filter(Question.question_id == orphan_question_id).first()

    assert assignment is not None
    assert question is not None
    assert item.sequence_index == 1

def test_auto_provision_student_attempt_item(db_session):
    orphan_attempt_id = "orphan_att_7777"
    orphan_question_id = "orphan_q_7777"
    orphan_concept_id = "orphan_cpt_7777"

    item = StudentAttemptItem(
        attempt_id=orphan_attempt_id,
        question_id=orphan_question_id,
        concept_id=orphan_concept_id,
        student_answer="B",
        is_correct=False,
        time_taken_seconds=42,
        difficulty=0.65
    )
    db_session.add(item)
    db_session.flush()

    attempt = db_session.query(AssessmentAttempt).filter(AssessmentAttempt.attempt_id == orphan_attempt_id).first()
    question = db_session.query(Question).filter(Question.question_id == orphan_question_id).first()
    concept = db_session.query(Concept).filter(Concept.concept_id == orphan_concept_id).first()

    assert attempt is not None
    assert question is not None
    assert concept is not None
    assert item.time_taken_seconds == 42
