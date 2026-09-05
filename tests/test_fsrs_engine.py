"""
Unit Test Suite: Modern FSRS-5 Spaced Repetition Engine
======================================================
Verifies:
  1. Power-law retrievability forgetting curve R(t, S)
  2. Exact 90% retention interval property: R(S, S) == 0.90
  3. Stability growth on successful recall (Y = 1)
  4. Stability penalty on memory lapse (Y = 0) with minimum clamp
  5. Continuous difficulty calibration in [1.0, 10.0]
  6. Overdue triggers (R < 0.90)
  7. Integration with review-queue endpoint in supporting.py
"""
import pytest
import datetime
from fastapi.testclient import TestClient
from backend.app.student_model.fsrs_engine import FSRSEngine
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.curriculum.loader import seed_curriculum_and_questions
from backend.app.models.schema import Student, StudentConceptMastery, Concept, utc_now
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

def test_power_law_retrievability_properties():
    stability = 5.0  # 5 days

    # At t = 0, R is strictly 1.0
    r_0 = FSRSEngine.retrievability(elapsed_days=0.0, stability=stability)
    assert abs(r_0 - 1.0) < 1e-6

    # At t = S, R is mathematically 0.90
    r_s = FSRSEngine.retrievability(elapsed_days=stability, stability=stability)
    assert abs(r_s - 0.90) < 1e-4

    # Monotonic decrease over time
    r_1 = FSRSEngine.retrievability(elapsed_days=1.0, stability=stability)
    r_5 = FSRSEngine.retrievability(elapsed_days=5.0, stability=stability)
    r_10 = FSRSEngine.retrievability(elapsed_days=10.0, stability=stability)
    assert 1.0 > r_1 > r_5 > r_10 > 0.0

def test_stability_update_recall_increases_stability():
    s_initial = 3.0
    d = 5.0
    r = 0.85

    s_new = FSRSEngine.update_stability_recall(stability=s_initial, difficulty=d, retrievability=r)
    assert s_new > s_initial

    # Spacing effect: recalling at lower retrievability (harder recall) yields larger stability boost
    s_boost_hard = FSRSEngine.update_stability_recall(stability=s_initial, difficulty=d, retrievability=0.70)
    s_boost_easy = FSRSEngine.update_stability_recall(stability=s_initial, difficulty=d, retrievability=0.95)
    assert s_boost_hard > s_boost_easy

def test_stability_update_lapse_penalizes_stability():
    s_initial = 6.0
    d = 6.0
    r = 0.60

    s_new = FSRSEngine.update_stability_lapse(stability=s_initial, difficulty=d, retrievability=r)
    assert s_new < s_initial
    assert s_new >= FSRSEngine.MIN_STABILITY

def test_difficulty_updating_and_clamping():
    d_initial = 5.0

    # Success decreases difficulty
    d_success = FSRSEngine.update_difficulty(d_initial, is_correct=True)
    assert abs(d_success - 4.8) < 1e-4

    # Failure increases difficulty
    d_fail = FSRSEngine.update_difficulty(d_initial, is_correct=False)
    assert abs(d_fail - 5.8) < 1e-4

    # Clamping boundaries
    d_min = FSRSEngine.update_difficulty(1.1, is_correct=True)
    assert d_min >= 1.0
    d_max = FSRSEngine.update_difficulty(9.8, is_correct=False)
    assert d_max <= 10.0

def test_target_interval_calculation():
    s = 4.0
    # For default 90% retrievability, interval equals S
    interval_90 = FSRSEngine.calculate_interval(stability=s, target_retrievability=0.90)
    assert abs(interval_90 - s) < 1e-4

    # Higher target retrievability (e.g. 95%) requires a shorter interval
    interval_95 = FSRSEngine.calculate_interval(stability=s, target_retrievability=0.95)
    assert interval_95 < interval_90

def test_fsrs_review_queue_integration(client, test_db):
    student_id = "fsrs_student_01"
    student = test_db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(
            student_id=student_id,
            name="FSRS Tester",
            email=f"{student_id}@test.local",
            password_hash="pw",
            target_exam="JEE"
        )
        test_db.add(student)
        test_db.flush()

    concept = test_db.query(Concept).first()
    assert concept is not None

    # Insert a concept with elapsed review (decayed retrievability)
    now = utc_now()
    past_date = now - datetime.timedelta(days=7)
    mastery = test_db.query(StudentConceptMastery).filter(
        StudentConceptMastery.student_id == student_id,
        StudentConceptMastery.concept_id == concept.concept_id
    ).first()

    if not mastery:
        mastery = StudentConceptMastery(
            student_id=student_id,
            concept_id=concept.concept_id,
            mastery=0.65,
            fsrs_stability=2.0,
            fsrs_difficulty=5.0,
            fsrs_retrievability=0.60,
            last_fsrs_review=past_date,
            last_practiced_at=past_date
        )
        test_db.add(mastery)
    else:
        mastery.fsrs_stability = 2.0
        mastery.last_fsrs_review = past_date
        mastery.last_practiced_at = past_date

    test_db.commit()

    resp = client.get(f"/api/supporting/review-queue/{student_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["student_id"] == student_id
    assert data["total_due"] >= 1
    found_item = next((item for item in data["queue"] if item["concept_id"] == concept.concept_id), None)
    assert found_item is not None
    assert "fsrs_retrievability" in found_item
    assert found_item["fsrs_retrievability"] < 0.90
