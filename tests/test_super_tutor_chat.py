import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.pydantic_models import AIChatRequest, AIChatResponse
from backend.app.ai.templates import format_concept_explanation

client = TestClient(app)

def test_super_tutor_scaffold_templates():
    """Verify that the 5-part Super-Tutor scaffold is present in offline concept explanations."""
    # Test Simple Harmonic Motion scaffold
    shm_text = format_concept_explanation("Simple Harmonic Motion", "JEE")
    assert "💡 1. Intuitive Mental Model" in shm_text
    assert "📐 2. Canonical Analytical Formulation" in shm_text
    assert "🔬 3. Step-by-Step Derivation" in shm_text
    assert "⚠️ 4. Exam Trap Radar" in shm_text
    assert "🎯 5. Quick Micro-Check" in shm_text

    # Test Acidic Buffers scaffold
    buffer_text = format_concept_explanation("Acidic Buffers", "JEE")
    assert "💡 1. Intuitive Mental Model" in buffer_text
    assert "Henderson-Hasselbalch" in buffer_text
    assert "⚠️ 4. Exam Trap Radar" in buffer_text
    assert "🎯 5. Quick Micro-Check" in buffer_text

    # Test Meiosis / Cell Division scaffold
    meiosis_text = format_concept_explanation("Meiosis Stages", "NEET")
    assert "💡 1. Intuitive Mental Model" in meiosis_text
    assert "Centromere Splitting Trap" in meiosis_text
    assert "🎯 5. Quick Micro-Check" in meiosis_text

def test_api_chat_multi_turn_history():
    """Verify that multi-turn conversation history is accepted and processed by the API."""
    req_payload = {
        "prompt": "Now explain the restoring force equation",
        "mode": "pedagogical",
        "history": [
            {"role": "user", "text": "What is simple harmonic motion?"},
            {"role": "coach", "text": "SHM is a periodic oscillation governed by F = -kx."}
        ]
    }
    response = client.post("/api/ai/chat/stu_dev_01", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    assert "suggested_chips" in data
    assert isinstance(data["suggested_chips"], list)
    assert len(data["suggested_chips"]) > 0

def test_api_chat_inchat_quiz_agent():
    """Verify that when a user asks for a quiz or practice question, an interactive quiz card is returned."""
    req_payload = {
        "prompt": "Quiz me on this concept with a practice question",
        "concept_id": "phy_shm_01"
    }
    response = client.post("/api/ai/chat/stu_dev_01", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("source") == "INTERACTIVE_QUIZ_AGENT"
    assert "structured_card" in data
    card = data["structured_card"]
    assert card is not None
    assert card.get("type") == "quiz"
    assert "question_id" in card
    assert "content" in card
    assert "options" in card
    assert len(card["options"]) >= 2
    assert "correct_answer" in card

def test_api_chat_quiz_intent_flag():
    """Verify that setting quiz_intent=True directly triggers the interactive quiz card."""
    req_payload = {
        "prompt": "Give me something to test my understanding",
        "quiz_intent": True
    }
    response = client.post("/api/ai/chat/stu_dev_01", json=req_payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("source") == "INTERACTIVE_QUIZ_AGENT"
    assert data.get("structured_card") is not None
    assert data["structured_card"].get("type") == "quiz"

def test_rotational_and_optics_scaffolds():
    """Verify that newly added high-yield topics also have the complete 5-part Super-Tutor scaffold."""
    rot_text = format_concept_explanation("Rotational Dynamics and Inertia", "JEE")
    assert "💡 1. Intuitive Mental Model" in rot_text
    assert "📐 2. Canonical Analytical Formulation" in rot_text
    assert "🔬 3. Step-by-Step Rolling Derivation" in rot_text
    assert "⚠️ 4. Exam Trap Radar" in rot_text
    assert "🎯 5. Quick Micro-Check" in rot_text

    optics_text = format_concept_explanation("Lens Maker Formula and Optics", "JEE")
    assert "💡 1. Intuitive Mental Model" in optics_text
    assert "📐 2. Canonical Analytical Formulation" in optics_text
    assert "⚠️ 4. Exam Trap Radar" in optics_text
    assert "🎯 5. Quick Micro-Check" in optics_text
