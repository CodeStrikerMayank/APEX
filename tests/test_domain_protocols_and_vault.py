"""
Comprehensive Test Suite for Domain Protocols, Knowledge Vault Retrieval,
Multi-Tier Prompt Framework & Step-by-Step Problem Solving.
"""
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database.connection import SessionLocal
from backend.app.models.schema import Student, Subject, Chapter, Topic, Concept
from backend.app.ai.domain_protocols import (
    DomainProtocolEngine, JEEProtocol, NEETProtocol, UPSCProtocol, GeneralSTEMProtocol
)
from backend.app.ai.omni_context import OmniContextHarvester
from backend.app.ai.cloud_llm import build_unified_system_prompt


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_student(db_session):
    student = db_session.query(Student).filter(Student.student_id == "proto_test_student").first()
    if not student:
        student = Student(
            student_id="proto_test_student",
            name="Arjun Protocologist",
            email="arjun_proto@apex.ai",
            password_hash="hashed_pw_proto",
            target_exam="JEE"
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
    return student


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_domain_protocols_definitions():
    """Verify all 4 domain protocols implement required instructions and solve structure."""
    jee = DomainProtocolEngine.get_protocol("JEE")
    assert isinstance(jee, JEEProtocol)
    assert "IIT-JEE" in jee.get_system_instructions()
    assert jee.latex_required is True
    assert "PROBLEM SOLVING PROTOCOL" in jee.get_system_instructions(is_solve=True)

    neet = DomainProtocolEngine.get_protocol("NEET")
    assert isinstance(neet, NEETProtocol)
    assert "NEET-UG" in neet.get_system_instructions()
    assert "NCERT" in neet.get_system_instructions()

    upsc = DomainProtocolEngine.get_protocol("UPSC")
    assert isinstance(upsc, UPSCProtocol)
    assert "UPSC Civil Services" in upsc.get_system_instructions()

    stem = DomainProtocolEngine.get_protocol("GENERAL_STEM")
    assert isinstance(stem, GeneralSTEMProtocol)
    assert "GENERAL STEM" in stem.get_system_instructions()


def test_domain_classification_boundaries():
    """Verify boundary checks: IN_SYLLABUS, IN_DOMAIN_ADVANCED, CROSS_DISCIPLINARY, CASUAL_OFF_TOPIC."""
    # 1. In-Syllabus JEE query
    res_jee = DomainProtocolEngine.classify_query_domain("Explain Lenz's Law and magnetic flux", target_exam="JEE")
    assert res_jee["category"] == "IN_SYLLABUS"
    assert res_jee["domain"] == "JEE"
    assert res_jee["advisory_note"] is None

    # 2. Advanced STEM query for JEE student (e.g. quantum tunneling)
    res_adv = DomainProtocolEngine.classify_query_domain("What is quantum tunneling in modern physics?", target_exam="JEE")
    assert res_adv["category"] == "IN_DOMAIN_ADVANCED"
    assert res_adv["domain"] == "GENERAL_STEM"
    assert "Advanced collegiate STEM" in res_adv["advisory_note"]

    # 3. Cross-Disciplinary: JEE student asking Biology
    res_cross = DomainProtocolEngine.classify_query_domain("How does photosynthesis produce ATP in the Calvin cycle?", target_exam="JEE")
    assert res_cross["category"] == "CROSS_DISCIPLINARY"
    assert res_cross["domain"] == "NEET"
    assert "IIT-JEE" in res_cross["advisory_note"]

    # 4. Cross-Disciplinary: JEE student asking UPSC Polity
    res_polity = DomainProtocolEngine.classify_query_domain("Explain Article 21 and the right to life", target_exam="JEE")
    assert res_cross["category"] == "CROSS_DISCIPLINARY"
    assert "General Studies" in res_polity["advisory_note"]

    # 5. Casual Off-Topic: Pure entertainment
    res_off = DomainProtocolEngine.classify_query_domain("Who is the best Marvel actor in movies?", target_exam="JEE")
    assert res_off["category"] == "CASUAL_OFF_TOPIC"
    assert res_off["domain"] == "OFF_TOPIC"


def test_solve_intent_detection():
    """Verify solve intent is recognized for numerical calculations and explicit solve requests."""
    assert DomainProtocolEngine.detect_solve_intent("Solve: A block of mass 5 kg moves at 10 m/s") is True
    assert DomainProtocolEngine.detect_solve_intent("Calculate the moment of inertia about the center of mass") is True
    assert DomainProtocolEngine.detect_solve_intent("Find the value of torque when r = 2 m and F = 15 N") is True
    assert DomainProtocolEngine.detect_solve_intent("v = 20, t = 4, find acceleration") is True
    assert DomainProtocolEngine.detect_solve_intent("What is the definition of inertia?") is False


def test_knowledge_vault_retriever(db_session):
    """Verify OmniContextHarvester.find_vault_matches retrieves matching readings with previews."""
    matches = OmniContextHarvester.find_vault_matches("parallel axis theorem moment of inertia", exam="JEE", db=db_session, limit=2)
    assert len(matches) > 0
    top = matches[0]
    assert "Parallel Axis" in top["title"]
    assert top["id"] == "FW-JEE-PHY-01"
    assert top["course"] == "JEE"
    assert top["subject"] == "Physics"
    assert "preview_chip" in top
    assert top["preview_url"].startswith("vault:")
    assert "I = I" in str(top["formula_latex"])


def test_unified_system_prompt_builder():
    """Verify build_unified_system_prompt composes all 4 tiers."""
    ctx = {
        "student_name": "Rohan",
        "target_exam": "JEE",
        "latent_ability_theta": 0.85,
        "overall_mastery": 78.5,
        "weak_concepts": [{"name": "Rotational Dynamics", "mastery": 42.0}],
    }
    sys_prompt = build_unified_system_prompt(
        student_context=ctx,
        exam="JEE",
        mode="pedagogical",
        is_solve=True
    )
    assert "TIER 1: TONE, STYLE & ACCESSIBILITY" in sys_prompt
    assert "TIER 2: DOMAIN PROTOCOL INVARIANTS" in sys_prompt
    assert "TIER 3: COGNITIVE & PSYCHOMETRIC GROUNDING" in sys_prompt
    assert "TIER 4: STEP-BY-STEP PROBLEM SOLVER" in sys_prompt
    assert "Advanced Mastery (θ > 0.7)" in sys_prompt
    assert "IIT-JEE" in sys_prompt


def test_e2e_chat_with_domain_protocols_and_vault(client, test_student):
    """Verify /api/ai/chat/{student_id} returns enriched payload with chips and vault readings."""
    sid = test_student.student_id

    # 1. Test Solve Query
    solve_res = client.post(f"/api/ai/chat/{sid}", json={
        "prompt": "Solve: A disc of mass 4 kg and radius 0.5 m rotates about its central axis. Find its moment of inertia.",
        "mode": "pedagogical"
    })
    assert solve_res.status_code == 200
    data = solve_res.json()
    assert "response" in data
    assert data["domain_protocol"] == "JEE"
    assert len(data["suggested_chips"]) > 0
    assert any("Hint" in c or "Formula" in c or "Problem" in c for c in data["suggested_chips"])

    # 2. Test Knowledge Vault matched query
    vault_res = client.post(f"/api/ai/chat/{sid}", json={
        "prompt": "Explain the parallel axis theorem and its derivation",
        "mode": "pedagogical"
    })
    assert vault_res.status_code == 200
    v_data = vault_res.json()
    assert v_data["vault_readings"] is not None
    assert len(v_data["vault_readings"]) > 0
    assert any("Vault:" in c for c in v_data["suggested_chips"])
    assert "vault:FW-JEE-PHY-01" in v_data["response"]

    # 3. Test Cross-Disciplinary Query
    cross_res = client.post(f"/api/ai/chat/{sid}", json={
        "prompt": "Explain photosynthesis and the light dependent reactions in plants",
        "mode": "pedagogical"
    })
    assert cross_res.status_code == 200
    c_data = cross_res.json()
    assert c_data["domain_protocol"] == "NEET"
    assert "Note: You are currently enrolled in IIT-JEE" in c_data["response"]
