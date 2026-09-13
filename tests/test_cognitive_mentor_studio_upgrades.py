import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.connection import SessionLocal
from backend.app.models.schema import Student, StudentConceptMastery, Concept, Prerequisite
from backend.app.student_model.numerical_guards import OutputNumericalGuard
from backend.app.student_model.error_classifier import CodeTraceDissector
from backend.app.student_model.akt import AttentionKnowledgeTracing
from backend.app.student_model.irt import MultidimensionalIRT
from backend.app.student_model.bkt import BayesianKnowledgeTracing
from backend.app.student_model.fsrs_engine import FSRSEngine
from backend.app.ai.omni_context import CognitiveStateAccumulator, OmniContextHarvester
from backend.app.ai.socratic_agents import PedagogicalPolicyRouter, SocraticCoordinator

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


def test_output_numerical_guard_arithmetic():
    valid_text = "The calculated acceleration is derived as 15 / 3 = 5 and the force is 4 * 12 = 48."
    ok, issues = OutputNumericalGuard.verify_arithmetic_expressions(valid_text)
    assert ok is True
    assert len(issues) == 0

    invalid_text = "Clearly, from basic division 12 / 4 = 4 and also 5 + 7 = 13."
    ok, issues = OutputNumericalGuard.verify_arithmetic_expressions(invalid_text)
    assert ok is False
    assert len(issues) == 2


def test_output_numerical_guard_units_and_leakage():
    bad_unit_text = "We obtain 9.8 m/s^2 for velocity at the bottom of the incline."
    ok, issues = OutputNumericalGuard.verify_unit_consistency(bad_unit_text)
    assert ok is False
    assert any("Velocity cannot have units of acceleration" in iss for iss in issues)

    leaked_text = "Therefore, the correct answer is Option B."
    leak_ok, leak_issues = OutputNumericalGuard.validate_explanation_invariants(leaked_text, mode="scaffolding")
    assert leak_ok is False
    assert any("Option B" in iss for iss in leak_issues)

    report = OutputNumericalGuard.guard_llm_output(bad_unit_text, mode="socratic")
    assert report["passed"] is False


def test_code_trace_dissector_syntax_and_delimiters():
    valid_code = "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)"
    res = CodeTraceDissector.dissect_code(valid_code)
    assert res["is_code"] is True
    assert res["valid_syntax"] is True
    assert res["ast_metrics"]["has_recursion"] is True
    assert "fib" in res["ast_metrics"]["functions"]

    broken_code = "def broken(x):\n    return x + (10 * 2"
    res_broken = CodeTraceDissector.dissect_code(broken_code)
    assert res_broken["valid_syntax"] is False
    assert res_broken["fault_category"] == "UNCLOSED_DELIMITER"


def test_code_trace_dissector_traceback():
    sample_trace = """Traceback (most recent call last):
  File "solver.py", line 42, in calculate_flux
    flux = B * A * math.cos(theta[idx])
IndexError: list index out of range"""
    tb = CodeTraceDissector.dissect_traceback(sample_trace)
    assert tb["is_traceback"] is True
    assert tb["exception_type"] == "IndexError"
    assert tb["failing_frame"]["line"] == 42
    assert tb["failing_frame"]["scope"] == "calculate_flux"
    assert "out of range" in tb["exception_message"]


def test_psychometric_control_signals():
    # AKT predictive signals
    akt = AttentionKnowledgeTracing()
    interactions = [("q1", True), ("q2", False), ("q3", False), ("q4", False)]
    akt_res = akt.predict_next_interaction(interactions)
    assert "p_next" in akt_res
    assert 0.01 <= akt_res["p_next"] <= 0.99
    assert akt_res["cognitive_momentum"] == "DECLINING"
    assert akt_res["scaffolding_depth"] in ["STEP_BY_STEP", "GUIDED_HINTS", "INDEPENDENT_PROMPT"]

    # MIRT cognitive control vector
    mirt_sig = MultidimensionalIRT.get_cognitive_control_vector([-0.8, 0.5, -0.2, 0.1])
    assert "dimensions" in mirt_sig
    assert mirt_sig["primary_vulnerability"] == "calculation"
    assert mirt_sig["pedagogical_focus"] == "ALGEBRAIC_STEPS_FOCUS"

    # BKT slip vs guess evaluation
    bkt = BayesianKnowledgeTracing()
    slip_res = bkt.evaluate_slip_vs_guess(p_known=0.85, is_correct=False)
    assert slip_res["diagnosis"] == "CARELESS_SLIP"
    assert slip_res["slip_probability"] > 0.40

    guess_res = bkt.evaluate_slip_vs_guess(p_known=0.10, is_correct=True)
    assert guess_res["diagnosis"] == "LUCKY_GUESS"
    assert guess_res["guess_probability"] > 0.40


def test_cognitive_state_accumulator_entropy_and_thrashing():
    # Rapid guessing thrashing loop
    rapid_wrong = [
        {"is_correct": False, "error_type": "CALCULATION_ERROR", "time_taken_seconds": 8},
        {"is_correct": False, "error_type": "SIGN_ERROR", "time_taken_seconds": 11},
        {"is_correct": False, "error_type": "CONCEPTUAL_ERROR", "time_taken_seconds": 9}
    ]
    diag = CognitiveStateAccumulator.compute_student_cognitive_entropy(rapid_wrong)
    assert diag["is_thrashing"] is True
    assert diag["thrashing_mode"] == "RAPID_GUESSING"
    assert diag["entropy_score"] > 0.8

    # Nominal state
    steady = [
        {"is_correct": True, "error_type": None, "time_taken_seconds": 60},
        {"is_correct": True, "error_type": None, "time_taken_seconds": 55}
    ]
    diag_steady = CognitiveStateAccumulator.compute_student_cognitive_entropy(steady)
    assert diag_steady["is_thrashing"] is False
    assert diag_steady["thrashing_mode"] == "NOMINAL"


def test_pedagogical_policy_router():
    # Diagnostic mode on high entropy
    r_diag = PedagogicalPolicyRouter.determine_route(entropy_score=1.6, mastery=40.0, theta=-0.4, is_thrashing=True)
    assert r_diag["mode"] == PedagogicalPolicyRouter.MODE_DIAGNOSTIC

    # Challenge mode on high mastery and high theta
    r_chal = PedagogicalPolicyRouter.determine_route(entropy_score=0.4, mastery=88.0, theta=1.2, is_thrashing=False)
    assert r_chal["mode"] == PedagogicalPolicyRouter.MODE_CHALLENGE

    # Scaffolding mode on moderate developing mastery
    r_scaff = PedagogicalPolicyRouter.determine_route(entropy_score=0.9, mastery=55.0, theta=0.1, is_thrashing=False)
    assert r_scaff["mode"] == PedagogicalPolicyRouter.MODE_SCAFFOLDING


def test_fsrs_decay_remediation_candidate():
    class DummyMastery:
        def __init__(self, cid, r, m):
            self.concept_id = cid
            self.fsrs_retrievability = r
            self.mastery = m

    masteries = [
        DummyMastery("c_solid", 0.95, 0.9),
        DummyMastery("c_decaying", 0.52, 0.65),
        DummyMastery("c_unlearned", 0.30, 0.10)
    ]
    cand = FSRSEngine.find_decay_remediation_candidates(masteries, threshold=0.70)
    assert cand is not None
    assert cand["candidate_concept_id"] == "c_decaying"
    assert cand["urgency"] == "MODERATE"
    assert "c_decaying" in cand["interleaving_instruction"]


def test_e2e_ai_chat_and_telemetry_hud_cognitive_state(client, db_session):
    student_id = "test_cognitive_upgrade_student"
    student = db_session.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(
            student_id=student_id,
            name="Cognitive Aspirant",
            email="cognitive@aspirant.test",
            password_hash="mock_hash",
            target_exam="JEE"
        )
        db_session.add(student)
        db_session.commit()

    # 1. Telemetry HUD returns cognitive state
    res_hud = client.get(f"/api/ai/telemetry-hud/{student_id}")
    assert res_hud.status_code == 200
    hud_data = res_hud.json()
    assert "cognitive_state" in hud_data
    cog = hud_data["cognitive_state"]
    assert "entropy_score" in cog
    assert "thrashing_mode" in cog
    assert "cognitive_control_signals" in cog

    # 2. Chat with code snippet troubleshooting
    code_prompt = """Why is my function crashing?
```python
def solve_ke(m, v):
    return 0.5 * m * (v ** 2
```"""
    chat_res = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": code_prompt,
        "mode": "auto"
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["response"] is not None
    assert len(chat_data["response"]) > 20
    assert "suggested_chips" in chat_data


def test_zero_exam_cold_start_greeting(client, db_session):
    """
    Test zero-exam cold start intelligence:
    When a student has 0 tests/assessments, typing 'hi' returns an encouraging explanation
    of their standby diagnostic profile and recommends taking a baseline test.
    """
    cold_student_id = "test_cold_start_newbie"
    student = db_session.query(Student).filter(Student.student_id == cold_student_id).first()
    if not student:
        student = Student(
            student_id=cold_student_id,
            name="New Aspirant",
            email="newbie@aspirant.test",
            password_hash="mock_hash",
            target_exam="JEE"
        )
        db_session.add(student)
        db_session.commit()

    # User types 'hi'
    res = client.post(f"/api/ai/chat/{cold_student_id}", json={
        "prompt": "hi",
        "mode": "auto"
    })
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    # Must NOT generate an absurd Socratic session or fake masterclass
    assert "awaiting initial calibration" in resp_text or "standby" in resp_text.lower()
    assert "3-Minute Baseline Diagnostic" in resp_text or "diagnostic" in resp_text.lower()
    assert "Take 3-Min Diagnostic" in data["suggested_chips"][0]


def test_casual_off_topic_query_handling(client, db_session):
    """
    Test casual / out-of-syllabus query intelligence:
    Asking 'what is apple' or 'who is batman' must NOT trigger a fake masterclass or socratic drill.
    It must politely identify that it is off-syllabus, answer concisely, and redirect to high-yield topics.
    """
    student_id = "test_cold_start_newbie"
    res = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": "what is apple",
        "mode": "auto"
    })
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    # Must recognize out of syllabus
    assert "is not a tested concept" in resp_text or "outside" in resp_text.lower() or "not on your syllabus" in resp_text.lower()
    # Mentions Newton / Physics or High-Yield JEE topics
    assert "Physics" in resp_text or "Gravitation" in resp_text or "SHM" in resp_text
    assert any("High-Yield" in chip or "Concepts" in chip for chip in data["suggested_chips"])


def test_in_syllabus_concept_query_handling(client, db_session):
    """
    Test in-syllabus query:
    Asking 'explain SHM and oscillations' should deliver an academically rigorous Masterclass.
    """
    student_id = "test_cold_start_newbie"
    res = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": "explain SHM and oscillations",
        "mode": "auto"
    })
    assert res.status_code == 200
    data = res.json()
    resp_text = data["response"]

    assert "Simple Harmonic Motion" in resp_text or "SHM" in resp_text
    assert any(k in resp_text for k in ["Mental Model", "Picture", "Oscillation", "oscillation", "restoring", "bowl", "marble", "spring"])
    assert any(k in resp_text for k in ["Analytical Formulation", "\\omega", "omega", "F =", "k", "x(t)"])

