"""
Tests for PDF Ingestion, Gemini Academic Synthesis & Knowledge Vault Augmentation
"""
import io
import pytest
from pydantic import ValidationError
from pypdf import PdfWriter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database.connection import Base
from backend.app.curriculum.pdf_ingestor import (
    extract_text_from_pdf_bytes,
    ExtractedConcept,
    GeneratedMCQ,
    GeneratedMCQOption,
    DocumentIngestionResult
)
from backend.app.curriculum.vault_augmenter import augment_vault_and_database
from backend.app.models.schema import Concept, Question

client = TestClient(app)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def create_sample_pdf_bytes() -> bytes:
    """Helper creating a valid in-memory PDF with readable text."""
    writer = PdfWriter()
    # Add a blank page and annotations or standard page
    page = writer.add_blank_page(width=612, height=792)
    stream = io.BytesIO()
    writer.write(stream)
    return stream.getvalue()


def test_pydantic_models_validation():
    """Verify schema integrity of ExtractedConcept and GeneratedMCQ."""
    concept = ExtractedConcept(
        name="Sampling Error & Central Limit Theorem",
        topic="Survey Methodology",
        subject="Statistics",
        exam="UPSC",
        description="The deviation of the sample estimate from the true population parameter.",
        key_formula="$$SE = \\frac{\\sigma}{\\sqrt{n}}$$"
    )
    assert concept.name == "Sampling Error & Central Limit Theorem"
    assert concept.is_new_discovery is True

    opts = [
        GeneratedMCQOption(id="A", text="Standard Error decreases by half"),
        GeneratedMCQOption(id="B", text="Standard Error doubles"),
        GeneratedMCQOption(id="C", text="Standard Error remains invariant"),
        GeneratedMCQOption(id="D", text="Standard Error drops to zero")
    ]
    mcq = GeneratedMCQ(
        concept_name=concept.name,
        content="If the sample size n is quadrupled from 100 to 400, how does the Standard Error change?",
        options=opts,
        correct_answer="A",
        explanation="Since SE = sigma / sqrt(n), quadrupling n doubles the denominator, halving the SE.",
        distractor_explanations={
            "B": "CALCULATION_ERROR: Inverted the square root ratio",
            "C": "CONCEPTUAL_ERROR: Assumed SE is independent of sample size",
            "D": "FORMULA_SELECTION_ERROR: Assumed infinite sample limit"
        },
        difficulty=0.60
    )
    assert mcq.correct_answer == "A"
    assert len(mcq.options) == 4
    assert "CALCULATION_ERROR" in mcq.distractor_explanations["B"]


def test_vault_augmenter_provisions_sqlite_and_vault(db_session):
    """
    Verify that newly discovered concepts and questions are automatically
    provisioned in the SQLite database and augmented into the Knowledge Vault.
    """
    concept_name = "Kullback-Leibler Divergence in Statistical Estimation"
    concept = ExtractedConcept(
        concept_name=concept_name,
        name=concept_name,
        topic="Information Theory & Estimation",
        subject="Statistics",
        exam="JEE",
        description="A statistical measure of difference between two probability distributions P and Q.",
        key_formula="$$D_{KL}(P \\parallel Q) = \\sum P(x) \\log \\frac{P(x)}{Q(x)}$$"
    )

    opts = [
        GeneratedMCQOption(id="A", text="Non-negative D_KL >= 0 (Gibbs Inequality)"),
        GeneratedMCQOption(id="B", text="Strictly symmetric"),
        GeneratedMCQOption(id="C", text="Can be negative"),
        GeneratedMCQOption(id="D", text="Independent of distribution shape")
    ]

    mcq = GeneratedMCQ(
        concept_name=concept_name,
        content="Which fundamental mathematical property characterizes KL Divergence?",
        options=opts,
        correct_answer="A",
        explanation="By Gibbs inequality, KL divergence is always non-negative, equaling 0 iff P = Q almost everywhere.",
        distractor_explanations={
            "B": "CONCEPTUAL_ERROR: KL divergence is asymmetric (D_KL(P||Q) != D_KL(Q||P))",
            "C": "SIGN_ERROR: KL divergence cannot be negative",
            "D": "FORMULA_SELECTION_ERROR: Misunderstood entropy basis"
        }
    )

    mock_ingestion = DocumentIngestionResult(
        filename="statistical_inference_notes.pdf",
        title="Official Statistical Inference & Information Measures",
        word_count=450,
        page_count=2,
        summary="Foundations of relative entropy and minimum distance estimators in official sampling.",
        key_takeaways=["KL Divergence measures information loss", "Always non-negative via Gibbs inequality"],
        extracted_concepts=[concept],
        generated_questions=[mcq]
    )

    result = augment_vault_and_database(db=db_session, ingestion_result=mock_ingestion, default_exam="JEE")

    assert result.new_concepts_added_count == 1
    assert result.new_questions_added_count == 1
    assert result.vault_updated is True

    # Verify concept exists in SQLite
    saved_concept = db_session.query(Concept).filter(Concept.name == concept_name).first()
    assert saved_concept is not None
    assert "difference between two probability" in saved_concept.description

    # Verify question exists in SQLite
    saved_question = db_session.query(Question).filter(Question.content == mcq.content).first()
    assert saved_question is not None
    assert saved_question.correct_answer == "A"
    assert saved_question.concept_id == saved_concept.concept_id

    # Verify idempotency: running again should not duplicate
    repeat_result = augment_vault_and_database(db=db_session, ingestion_result=mock_ingestion, default_exam="JEE")
    assert repeat_result.new_concepts_added_count == 0
    assert repeat_result.new_questions_added_count == 0


def test_augmented_vault_endpoint():
    """Verify /api/materials/augmented-vault returns valid structure."""
    res = client.get("/api/materials/augmented-vault")
    assert res.status_code == 200
    data = res.json()
    assert "augmented_readings_count" in data
    assert "readings" in data
    assert isinstance(data["readings"], list)


def test_live_generate_from_text_end_to_end():
    """Verify end-to-end Gemini synthesis, Pydantic parsing and auto-save via /api/materials/generate-from-text."""
    sample_text = """
    The Consumer Price Index (CPI) and Macroeconomic Inflation dynamics measure changes over time in the general level of prices of goods and services that a reference
    population acquires, uses or pays for consumption. The Laspeyres Price Index formula with a fixed base year weighting scheme
    is predominantly utilized: I_L = (sum(p_t * q_0) / sum(p_0 * q_0)) * 100.
    A crucial challenge is Substitution Bias, where consumers shift towards relatively cheaper substitutes as prices diverge.
    """
    res = client.post("/api/materials/generate-from-text", json={
        "title": "Macroeconomics: Consumer Price Index & Laspeyres Formulation",
        "text": sample_text,
        "exam": "UPSC",
        "subject": "Economics & Public Policy",
        "num_questions": 2
    })
    assert res.status_code == 200
    data = res.json()
    assert "doc_id" in data
    assert "summary" in data
    assert len(data["extracted_concepts"]) >= 1
    assert len(data["generated_questions"]) >= 1
    assert data["vault_updated"] is True
    assert data["generated_questions"][0]["correct_answer"] in ["A", "B", "C", "D"]
    assert len(data["generated_questions"][0]["options"]) == 4

