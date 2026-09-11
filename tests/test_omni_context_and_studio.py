import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.connection import SessionLocal
from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept, Prerequisite,
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

def test_omni_context_harvester_unit(db_session):
    # Setup test student
    student_id = "test_omni_student_001"
    student = db_session.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(
            student_id=student_id,
            name="Omni Aspirant",
            email="omni@aspirant.test",
            password_hash="mock_password_hash",
            target_exam="JEE"
        )
        db_session.add(student)
        db_session.commit()

    # Query existing concepts or create sample concept mastery
    concept = db_session.query(Concept).first()
    assert concept is not None, "At least one concept should exist in seed database"

    mastery = db_session.query(StudentConceptMastery).filter(
        StudentConceptMastery.student_id == student_id,
        StudentConceptMastery.concept_id == concept.concept_id
    ).first()

    if not mastery:
        mastery = StudentConceptMastery(
            student_id=student_id,
            concept_id=concept.concept_id,
            mastery=0.45,
            bkt_mastery=0.45,
            irt_ability=-0.35,
            confidence=0.8,
            fsrs_retrievability=0.62,
            forgetting_risk=0.48
        )
        db_session.add(mastery)
        db_session.commit()

    # Harvest context
    ctx = OmniContextHarvester.harvest_full_context(student_id, db_session, prompt="explain vectors derivation")

    assert ctx["student_id"] == student_id
    assert ctx["target_exam"] == "JEE"
    assert "overall_mastery" in ctx
    assert "latent_ability_theta" in ctx
    assert "ability_tier" in ctx
    assert "bkt_distribution" in ctx
    assert "weak_concepts" in ctx
    assert "fineweb_citations" in ctx

    # Test grounding block formatting
    grounding_ped = OmniContextHarvester.format_grounding_block(ctx, mode="pedagogical")
    assert "Student: Omni Aspirant" in grounding_ped
    assert "Target Exam: JEE" in grounding_ped
    assert "IRT Latent Ability" in grounding_ped

    grounding_soc = OmniContextHarvester.format_grounding_block(ctx, mode="socratic")
    assert "Omni Aspirant" in grounding_soc

def test_telemetry_hud_api_endpoint(client, db_session):
    student_id = "test_omni_student_001"
    response = client.get(f"/api/ai/telemetry-hud/{student_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["student_id"] == student_id
    assert "latent_ability_theta" in data
    assert "ability_tier" in data
    assert "overall_mastery" in data
    assert "weak_concepts" in data
    assert "prerequisite_bottlenecks" in data
    assert "fineweb_citations" in data

def test_ai_chat_with_modes_and_omni_grounding(client):
    student_id = "test_omni_student_001"

    # 1. Test Pedagogical Mode
    res_ped = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": "Explain the formula for kinetic energy and work-energy theorem",
        "mode": "pedagogical",
        "include_student_state": True
    })
    assert res_ped.status_code == 200
    data_ped = res_ped.json()
    assert "response" in data_ped
    assert len(data_ped["response"]) > 20

    # 2. Test Socratic Mode
    res_soc = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": "How do I derive the acceleration in circular motion?",
        "mode": "socratic",
        "include_student_state": True
    })
    assert res_soc.status_code == 200
    data_soc = res_soc.json()
    assert "response" in data_soc
    assert len(data_soc["response"]) > 20

    # 3. Test Mistake Forensics Mode
    res_forensics = client.post(f"/api/ai/chat/{student_id}", json={
        "prompt": "Analyze my exam mistakes and traps",
        "mode": "forensics",
        "include_student_state": True
    })
    assert res_forensics.status_code == 200
    data_forensics = res_forensics.json()
    assert "response" in data_forensics
    assert len(data_forensics["response"]) > 20
