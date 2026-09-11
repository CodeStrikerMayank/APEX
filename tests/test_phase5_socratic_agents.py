"""
Tests for Phase 5 Multi-Agent Socratic Runtime Isolation
  - Agent 1: Diagnostician (Read-only error & latency telemetry consumer)
  - Agent 2: Socratic Prober (Zero answer letter leakage)
  - Agent 3: Psychologist (Active duration fatigue detector > 45 min)
"""
import pytest
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.models.schema import Student, StudentErrorLog, StudentAttemptItem, AssessmentAttempt, Question, Concept
from backend.app.ai.socratic_agents import (
    DiagnosticianAgent, SocraticProberAgent, PsychologistAgent, SocraticCoordinator
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


def test_diagnostician_read_only_telemetry(db_session):
    student_id = "std_socratic_diag_01"

    # Setup student with error logs and attempt items
    student = Student(
        student_id=student_id,
        name="Test Aspirant",
        email="socratic_aspirant@apex.engine",
        password_hash="pass",
        target_exam="JEE"
    )
    db_session.add(student)

    # Add error logs
    for err_type in ["CALCULATION_ERROR", "CALCULATION_ERROR", "CONCEPTUAL_ERROR"]:
        err = StudentErrorLog(
            student_id=student_id,
            question_id="q_dummy_01",
            concept_id="c_dummy_01",
            error_type=err_type,
            details="Boundary calculation failure"
        )
        db_session.add(err)

    db_session.flush()

    diagnosis = DiagnosticianAgent.diagnose_student(student_id, db_session)

    assert diagnosis["error_count"] >= 3
    assert diagnosis["primary_vulnerability"] == "CALCULATION_ERROR"
    assert "speed_profile" in diagnosis
    assert isinstance(diagnosis["average_latency_seconds"], float)


def test_socratic_prober_zero_answer_leakage():
    # Attempt to leak option letters
    leaky_texts = [
        "The correct answer is Option A because of conservation of energy.",
        "Select B: it solves the boundary condition.",
        "Choice C is right for this reaction mechanism.",
        "The answer is D.",
        "(A) is correct.",
    ]

    for raw in leaky_texts:
        sanitized = SocraticProberAgent.sanitize_scaffolding(raw)
        # Check that explicit option letters were scrubbed
        assert "Option A" not in sanitized
        assert "Select B" not in sanitized
        assert "Choice C" not in sanitized
        assert "The answer is D" not in sanitized

    # Verify generated probe is purely Socratic
    probe = SocraticProberAgent.generate_scaffolding_probe(
        concept_name="Bernoulli Theorem",
        error_type="CALCULATION_ERROR",
        explanation="Option B is correct because total head is conserved."
    )
    assert "Bernoulli Theorem" in probe
    assert "Option B is correct" not in probe
    assert "?" in probe  # Contains a probing question


def test_psychologist_fatigue_injection():
    # Session under 45 minutes: no break injection
    short_session = PsychologistAgent.check_and_inject_break_prompt(
        active_duration_minutes=25.0,
        student_name="Arjun"
    )
    assert short_session is None

    # Session over 45 minutes (e.g. 50 minutes): break injected
    long_session = PsychologistAgent.check_and_inject_break_prompt(
        active_duration_minutes=50.0,
        student_name="Arjun"
    )
    assert long_session is not None
    assert "5-minute micro-break" in long_session
    assert "50 minutes" in long_session


def test_socratic_coordinator_bundle(db_session):
    student_id = "std_socratic_coord_01"

    student = Student(
        student_id=student_id,
        name="Priya",
        email="priya@apex.engine",
        password_hash="pass",
        target_exam="NEET"
    )
    db_session.add(student)
    db_session.flush()

    res = SocraticCoordinator.coordinate_response(
        student_id=student_id,
        db=db_session,
        concept_name="DNA Replication",
        error_type="CONCEPTUAL_ERROR",
        explanation="Option C is correct because DNA Polymerase III operates 5' to 3'.",
        session_duration_minutes=55.0,
        student_name="Priya"
    )

    assert "DNA Replication" in res["text"]
    assert "Option C is correct" not in res["text"]
    assert res["fatigue_break_triggered"] is True
    assert "micro-break" in res["text"]
    assert res["source"] == "SOCRATIC_MULTI_AGENT"
