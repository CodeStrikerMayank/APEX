import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.open_mm_rl_service import OpenMMRLService


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def service():
    return OpenMMRLService()


def test_keyword_classification(service):
    """Test heuristic STEM keyword classification across all 4 disciplines."""
    # Mathematics
    math_res = service.classify_stem_problem(
        "Determine the number of monic primitive irreducible polynomials of degree d",
        domain="Math"
    )
    assert math_res["category"] == "Mathematics"
    assert "math_" in math_res["concept_id"]

    # Physics
    phy_res = service.classify_stem_problem(
        "A charged particle experiences a Lorentz magnetic force in a uniform magnetic field of B = 0.5 T",
        domain="Physics"
    )
    assert phy_res["category"] == "Physics"
    assert phy_res["concept_id"] == "phy_lorentz_force_circular_motion"

    # Chemistry
    chem_res = service.classify_stem_problem(
        "Calculate the cell potential and emf using the Nernst equation for a galvanic cell at 298 K",
        domain="Chemistry"
    )
    assert chem_res["category"] == "Chemistry"
    assert chem_res["concept_id"] == "chem_nernst_equation"

    # Biology
    bio_res = service.classify_stem_problem(
        "Compare the proton gradient in chloroplast thylakoid lumen with mitochondria during photosynthesis",
        domain="Biology"
    )
    assert bio_res["category"] == "Biology"
    assert "bio_" in bio_res["concept_id"]


def test_resilience_fallback_on_network_failure(service):
    """Test Tier 2 local cache fallback when network times out or fails."""
    # Force timeout=0.0001 to simulate instant network timeout
    res = service.fetch_live_rows(offset=0, length=5, timeout=0.0001)
    assert res["source"] == "cache_fallback"
    assert res["total"] > 0
    assert len(res["problems"]) <= 5
    first = res["problems"][0]
    assert "question" in first
    assert "answer" in first
    assert "concept_id" in first
    assert "category" in first


def test_api_endpoint_curriculum_open_mm_rl(client):
    """Test GET /api/curriculum/open-mm-rl/sample."""
    response = client.get("/api/curriculum/open-mm-rl/sample?offset=0&length=3")
    assert response.status_code == 200
    data = response.json()
    assert "problems" in data
    assert "total" in data
    assert len(data["problems"]) == 3
    for p in data["problems"]:
        assert "id" in p
        assert "question" in p
        assert "answer" in p
        assert "concept_id" in p
        assert "category" in p


def test_api_v1_endpoint_curriculum_open_mm_rl(client):
    """Test GET /api/v1/curriculum/open-mm-rl/sample."""
    response = client.get("/api/v1/curriculum/open-mm-rl/sample?offset=1&length=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["problems"]) == 2
    assert data["offset"] == 1
    assert data["length"] == 2
