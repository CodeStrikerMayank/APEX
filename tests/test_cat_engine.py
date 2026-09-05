"""
Unit Test Suite: Real-Time Computerized Adaptive Testing (CAT) Engine
====================================================================
Verifies:
  1. 2PL/3PL probability curves P_i(theta)
  2. Fisher Information I_i(theta) peaks near theta = b
  3. Item selection picks maximum information item
  4. Ability estimates converge accurately via EAP
  5. SEM decreases monotonically as items are added
  6. Termination criteria (SEM <= 0.25 or N >= 12, min N=5)
  7. CAT API Endpoints (/api/assessments/cat/start, /api/assessments/cat/next-question)
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.student_model.cat_engine import CATEngine
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.curriculum.loader import seed_curriculum_and_questions
from backend.app.models.schema import Student, Question, CatSessionState
from backend.app.main import app

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_curriculum_and_questions(db)
    yield db
    db.close()

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def test_cat_probability_curve_2pl_and_3pl():
    # At theta == b, 2PL probability is exactly 0.5
    p_2pl = CATEngine.probability_correct(theta=0.0, difficulty_b=0.0, discrimination_a=1.0, guessing_c=0.0)
    assert abs(p_2pl - 0.5) < 1e-4

    # Higher theta -> higher probability
    p_high = CATEngine.probability_correct(theta=1.5, difficulty_b=0.0, discrimination_a=1.0, guessing_c=0.0)
    p_low = CATEngine.probability_correct(theta=-1.5, difficulty_b=0.0, discrimination_a=1.0, guessing_c=0.0)
    assert p_high > 0.5
    assert p_low < 0.5
    assert p_high > p_low

    # 3PL with guessing c=0.25 at extreme negative theta approaches c
    p_extreme_low = CATEngine.probability_correct(theta=-10.0, difficulty_b=0.0, discrimination_a=1.0, guessing_c=0.25)
    assert abs(p_extreme_low - 0.25) < 1e-3

def test_fisher_information_peaks_near_difficulty():
    b = 0.5
    a = 1.2
    c = 0.0  # 2PL peak is exactly at theta = b

    info_peak = CATEngine.fisher_information(theta=b, difficulty_b=b, discrimination_a=a, guessing_c=c)
    info_left = CATEngine.fisher_information(theta=b - 0.5, difficulty_b=b, discrimination_a=a, guessing_c=c)
    info_right = CATEngine.fisher_information(theta=b + 0.5, difficulty_b=b, discrimination_a=a, guessing_c=c)

    assert info_peak > info_left
    assert info_peak > info_right

    # 3PL peak is also close to b
    info_3pl_peak = CATEngine.fisher_information(theta=b + 0.1, difficulty_b=b, discrimination_a=a, guessing_c=0.25)
    info_3pl_far = CATEngine.fisher_information(theta=b + 3.0, difficulty_b=b, discrimination_a=a, guessing_c=0.25)
    assert info_3pl_peak > info_3pl_far

def test_dynamic_item_selection_maximizes_information():
    current_theta = 1.0
    candidates = [
        {"question_id": "Q_EASY", "difficulty_b": -1.5, "discrimination_a": 1.0, "guessing_c": 0.0},
        {"question_id": "Q_MATCH", "difficulty_b": 1.0, "discrimination_a": 1.0, "guessing_c": 0.0},
        {"question_id": "Q_HARD", "difficulty_b": 2.5, "discrimination_a": 1.0, "guessing_c": 0.0},
    ]
    unvisited = ["Q_EASY", "Q_MATCH", "Q_HARD"]

    best = CATEngine.select_next_item(current_theta, candidates, unvisited)
    assert best is not None
    assert best["question_id"] == "Q_MATCH"

def test_eap_ability_estimation_convergence():
    # Strong student: answers hard items correctly
    strong_responses = [
        {"is_correct": True, "difficulty_b": -0.5, "discrimination_a": 1.2, "guessing_c": 0.20},
        {"is_correct": True, "difficulty_b": 0.0, "discrimination_a": 1.2, "guessing_c": 0.20},
        {"is_correct": True, "difficulty_b": 0.8, "discrimination_a": 1.2, "guessing_c": 0.20},
        {"is_correct": True, "difficulty_b": 1.5, "discrimination_a": 1.2, "guessing_c": 0.20},
    ]
    theta_strong, sd_strong = CATEngine.estimate_theta_eap(strong_responses)
    assert theta_strong > 0.8

    # Struggling student: answers items incorrectly
    weak_responses = [
        {"is_correct": False, "difficulty_b": -0.5, "discrimination_a": 1.2, "guessing_c": 0.20},
        {"is_correct": False, "difficulty_b": 0.0, "discrimination_a": 1.2, "guessing_c": 0.20},
        {"is_correct": False, "difficulty_b": -1.0, "discrimination_a": 1.2, "guessing_c": 0.20},
    ]
    theta_weak, sd_weak = CATEngine.estimate_theta_eap(weak_responses)
    assert theta_weak < -0.5
    assert theta_strong > theta_weak

def test_sem_decreases_as_items_added():
    theta = 0.0
    items = []
    sems = []

    for i in range(1, 10):
        items.append({"difficulty_b": 0.0, "discrimination_a": 1.2, "guessing_c": 0.0})
        sem = CATEngine.calculate_sem(theta, items)
        sems.append(sem)

    # Verify monotonic decrease of SEM
    for i in range(len(sems) - 1):
        assert sems[i] > sems[i + 1]

def test_cat_termination_criteria():
    # Less than minimum items (N < 5) should NEVER terminate even if SEM <= 0.25
    term, reason = CATEngine.evaluate_termination(items_answered_count=3, current_sem=0.20)
    assert not term
    assert reason == "CONTINUE_TESTING"

    # Minimum items satisfied (N >= 5) and SEM <= 0.25 -> TERMINATE
    term, reason = CATEngine.evaluate_termination(items_answered_count=6, current_sem=0.24)
    assert term
    assert "SEM_PRECISION_ACHIEVED" in reason

    # Max items reached (N = 12) -> TERMINATE regardless of SEM
    term, reason = CATEngine.evaluate_termination(items_answered_count=12, current_sem=0.35)
    assert term
    assert "MAX_ITEMS_REACHED" in reason

def test_cat_api_lifecycle(client, test_db):
    # 1. Start CAT assessment
    start_resp = client.post("/api/assessments/cat/start", json={
        "student_id": "cat_test_student_01",
        "exam": "JEE",
        "subject": "Physics"
    })
    assert start_resp.status_code == 200
    data = start_resp.json()
    assert not data["is_complete"]
    assert data["session_id"].startswith("cat_")
    assert data["question"] is not None
    assert "question_id" in data["question"]
    session_id = data["session_id"]
    q1_id = data["question"]["question_id"]

    # 2. Answer question 1
    next_resp = client.post("/api/assessments/cat/next-question", json={
        "session_id": session_id,
        "last_question_id": q1_id,
        "student_answer": "B",
        "time_taken_seconds": 35
    })
    assert next_resp.status_code == 200
    data2 = next_resp.json()
    assert data2["items_answered_count"] == 1
    assert data2["current_theta"] is not None
    assert data2["sem"] is not None
