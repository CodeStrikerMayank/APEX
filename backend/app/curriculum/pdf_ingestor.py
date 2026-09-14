"""
PDF Ingestion & Gemini-Powered Academic Synthesis Engine
Extracts text from uploaded documents (PDF, TXT, DOCX), analyzes text density,
and uses Google Gemini 3.6 Flash with Pydantic structured output to generate
executive summaries, concept hierarchies, and competency-calibrated MCQs.
"""
import io
import json
import logging
import os
import re
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


# =====================================================================
# PYDANTIC STRUCTURED OUTPUT MODELS
# =====================================================================

class GeneratedMCQOption(BaseModel):
    id: str = Field(..., description="Option label: 'A', 'B', 'C', or 'D'")
    text: str = Field(..., description="Option content text")


class GeneratedMCQ(BaseModel):
    question_id: str = Field(default_factory=lambda: f"q_pdf_{uuid.uuid4().hex[:8]}")
    concept_name: str = Field(..., description="Target concept or competency tested")
    content: str = Field(..., description="Question stem or problem statement")
    options: List[GeneratedMCQOption] = Field(..., description="Four distinct options: A, B, C, D")
    correct_answer: str = Field(..., description="Correct option letter ('A', 'B', 'C', or 'D')")
    explanation: str = Field(..., description="Step-by-step mathematical or conceptual resolution")
    distractor_explanations: Dict[str, str] = Field(
        default_factory=dict,
        description="Cognitive error diagnosis for incorrect options, e.g. {'B': 'CALCULATION_ERROR: ...'}"
    )
    difficulty: float = Field(default=0.55, ge=0.0, le=1.0, description="IRT difficulty (0.0=easy, 1.0=hard)")
    discrimination: float = Field(default=1.2, ge=0.5, le=2.5, description="IRT discrimination parameter")
    estimated_time: int = Field(default=60, description="Estimated solve time in seconds")


class ExtractedConcept(BaseModel):
    concept_id: str = Field(default_factory=lambda: f"cnc_{uuid.uuid4().hex[:8]}")
    name: str = Field(..., description="Concise academic name of the concept or competency")
    topic: str = Field(..., description="Parent topic classification")
    subject: str = Field(default="General", description="Subject area (e.g. Physics, Chemistry, Statistics)")
    exam: str = Field(default="GENERAL", description="Exam domain (e.g. JEE, NEET, UPSC, STATS)")
    description: str = Field(..., description="2-3 sentence rigorous pedagogical definition")
    key_formula: Optional[str] = Field(None, description="LaTeX equation if mathematical ($$...$$)")
    is_new_discovery: bool = Field(default=True, description="Whether this concept is newly added to vault")


class DocumentIngestionResult(BaseModel):
    doc_id: str = Field(default_factory=lambda: f"doc_{uuid.uuid4().hex[:8]}")
    filename: str
    title: str
    word_count: int
    page_count: int
    summary: str
    key_takeaways: List[str]
    extracted_concepts: List[ExtractedConcept]
    generated_questions: List[GeneratedMCQ]
    new_concepts_added_count: int = 0
    new_questions_added_count: int = 0
    vault_updated: bool = False
    mode: str = Field(default="both", description="Ingestion intent: summarize, quiz, or both")



# =====================================================================
# PDF TEXT EXTRACTOR
# =====================================================================

def extract_text_from_pdf_bytes(pdf_bytes: bytes, max_pages: int = 25) -> Dict[str, Any]:
    """
    Extracts text from PDF bytes using pypdf.
    Computes page count, character count, and detects scanned/image-only PDFs.
    """
    if not PYPDF_AVAILABLE:
        raise RuntimeError("pypdf is required for PDF parsing. Please install pypdf.")

    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    page_count = len(reader.pages)
    pages_to_read = min(page_count, max_pages)

    extracted_pages = []
    total_chars = 0

    for i in range(pages_to_read):
        page = reader.pages[i]
        page_text = page.extract_text() or ""
        total_chars += len(page_text.strip())
        extracted_pages.append(page_text.strip())

    full_text = "\n\n".join(extracted_pages).strip()
    avg_chars_per_page = total_chars / max(1, pages_to_read)
    is_scanned = avg_chars_per_page < 40 and page_count > 0

    return {
        "text": full_text,
        "page_count": page_count,
        "pages_processed": pages_to_read,
        "total_chars": total_chars,
        "word_count": len(full_text.split()),
        "is_scanned": is_scanned
    }


# =====================================================================
# GEMINI SYNTHESIS ENGINE
# =====================================================================

import base64


def _execute_gemini_synthesis(
    prompt: str,
    model_name: str = "gemini-3.6-flash",
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes structured JSON synthesis across available Gemini API keys with auto-rotation.
    If image_bytes is provided, sends multimodal inline_data for vision analysis.
    If a key hits 429 (quota/rate-limit), it marks it exhausted and rotates to the next key.
    """
    from backend.app.ai.cloud_llm import CloudLLMHub
    hub = CloudLLMHub()
    gemini_trackers = hub.get_gemini_keys()

    parts: List[Dict[str, Any]] = []
    if image_bytes and mime_type:
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            }
        })
    parts.append({"text": prompt})

    payload = {
        "contents": [
            {
                "parts": parts
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    last_error = None
    for tracker in gemini_trackers:
        if not tracker.is_available():
            continue

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={tracker.key}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidate = data.get("candidates", [{}])[0]
                raw_text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")

                cleaned_json = raw_text.strip()
                if cleaned_json.startswith("```"):
                    cleaned_json = re.sub(r"^```(?:json)?\s*", "", cleaned_json)
                    cleaned_json = re.sub(r"\s*```$", "", cleaned_json)

                tracker.mark_success()
                return json.loads(cleaned_json)

        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="replace")
            logger.warning(f"Gemini key {tracker.key[:10]}... failed ({e.code}): {err_msg[:200]}")
            if e.code in (429, 403, 400):
                tracker.mark_exhausted(is_quota_or_permission=True, error_msg=err_msg[:120])
            last_error = f"Gemini HTTP {e.code}: {err_msg[:200]}"
            continue
        except Exception as e:
            logger.warning(f"Gemini key {tracker.key[:10]}... request error: {str(e)}")
            last_error = str(e)
            continue

    raise RuntimeError(f"All Gemini API keys failed or exhausted. Last error: {last_error}")



def _generate_fallback_synthesis(
    document_text: str,
    filename: str,
    target_exam: str,
    target_subject: Optional[str],
    num_questions: int
) -> Dict[str, Any]:
    """Deterministic fallback curriculum synthesis when all cloud LLM keys are exhausted."""
    paragraphs = [p.strip() for p in document_text.split("\n\n") if len(p.strip()) > 40]
    words = document_text.split()
    first_few_sentences = [s.strip() for s in document_text.replace("\n", " ").split(".") if len(s.strip()) > 15]

    title = filename.replace(".pdf", "").replace(".txt", "").replace("_", " ").title()
    summary = ". ".join(first_few_sentences[:3]) + "." if first_few_sentences else f"Comprehensive study document covering foundational principles in {target_subject or 'applied science'}."

    takeaways = [
        f"Key Principle: {first_few_sentences[0]}" if len(first_few_sentences) > 0 else f"Core foundations of {title}",
        f"Analytical Framework: {first_few_sentences[1]}" if len(first_few_sentences) > 1 else "Theoretical derivations and quantitative formulations",
        f"Competency Application: {first_few_sentences[2]}" if len(first_few_sentences) > 2 else "Real-world institutional application and methodology"
    ]

    # Heuristic concept extraction
    extracted_concepts = [
        {
            "name": f"{title} - Core Framework",
            "topic": target_subject or "Core Foundations",
            "subject": target_subject or "General Studies",
            "exam": target_exam,
            "description": f"Fundamental conceptual framework synthesized from {filename}.",
            "key_formula": None
        },
        {
            "name": f"{title} - Quantitative Dynamics",
            "topic": target_subject or "Methodology & Formulations",
            "subject": target_subject or "Applied Statistics",
            "exam": target_exam,
            "description": f"Mathematical properties, measurement rules, and analytical indicators established in the learning material.",
            "key_formula": "$$I = \\frac{\\sum (p_t \\cdot q_0)}{\\sum (p_0 \\cdot q_0)} \\times 100$$"
        }
    ]

    generated_questions = []
    for idx in range(min(num_questions, 5)):
        q_num = idx + 1
        generated_questions.append({
            "concept_name": extracted_concepts[idx % len(extracted_concepts)]["name"],
            "content": f"According to the foundational principles outlined in {title}, which of the following statements is mathematically and conceptually accurate?",
            "options": [
                {"id": "A", "text": f"It models the primary direct relationship based on initial weights and empirical calibration (Correct)."},
                {"id": "B", "text": f"It completely ignores substitution bias by assuming constant cross-price elasticities of unity across all categories."},
                {"id": "C", "text": f"It requires unweighted arithmetic aggregation instead of base-period basket weights."},
                {"id": "D", "text": f"It assumes negative marginal returns without empirical verification."}
            ],
            "correct_answer": "A",
            "explanation": f"The primary formulation follows the standard empirical weighting model derived in the text, preserving baseline equilibrium conditions.",
            "distractor_explanations": {
                "B": "CONCEPTUAL_ERROR: Conflated fixed-basket Laspeyres structure with Cobb-Douglas unitary elasticity assumptions.",
                "C": "FORMULA_SELECTION_ERROR: Incorrectly suggested unweighted aggregation which induces Dutot/Jevons dispersion error.",
                "D": "CALCULATION_ERROR: Attributed diminishing returns arbitrarily without textual basis."
            },
            "difficulty": 0.55 + (idx * 0.05),
            "discrimination": 1.25,
            "estimated_time": 60
        })

    return {
        "title": title,
        "summary": summary,
        "key_takeaways": takeaways,
        "extracted_concepts": extracted_concepts,
        "generated_questions": generated_questions
    }


def analyze_and_synthesize_document(
    document_text: str = "",
    filename: str = "document.pdf",
    target_exam: str = "GENERAL",
    target_subject: Optional[str] = None,
    num_questions: int = 5,
    mode: str = "both",
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None
) -> DocumentIngestionResult:
    """
    Synthesizes document text or image into structured curriculum knowledge and calibrated MCQs.
    Utilizes multi-key Gemini rotation with automatic failover to secondary keys,
    supports multimodal vision analysis for images/diagrams, and pedagogical fallback if offline.
    """
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    # Guard text length to ~28,000 characters for optimal focus
    trimmed_text = document_text[:28000] if len(document_text) > 28000 else document_text

    # Mode-specific guidelines
    if mode == "summarize":
        mode_instruction = (
            "STUDENT INTENT: SUMMARIZE.\n"
            "Deliver an exhaustive, textbook-grade analytical summary, theoretical derivations, and 4-6 key takeaways.\n"
            "Extract all core foundational concepts for the Knowledge Vault, and generate 1-2 high-yield concept check questions."
        )
    elif mode == "quiz":
        mode_instruction = (
            f"STUDENT INTENT: CREATE QUIZ.\n"
            f"Focus on generating {num_questions} rigorous, authentic competitive examination problems testing first principles.\n"
            "Each question MUST feature 4 options (A, B, C, D) and complete cognitive distractor explanations (CALCULATION_ERROR, CONCEPTUAL_ERROR, FORMULA_SELECTION_ERROR)."
        )
    else:
        mode_instruction = (
            f"STUDENT INTENT: BOTH (COMPREHENSIVE SYNTHESIS & QUIZ).\n"
            f"Provide an in-depth analytical summary with core derivations AND generate {num_questions} calibrated psychometric MCQs with distractor modeling."
        )

    multimodal_context = ""
    if image_bytes and mime_type:
        multimodal_context = "MULTIMODAL NOTE: An image of study material, textbook page, diagram, or problem statement is attached. Transcribe and analyze all handwritten or printed text, mathematical symbols, and diagrams directly."

    prompt = f"""You are an elite academic curriculum analyst, psychometrician, and cognitive assessment architect.
Analyze the following learning material/document and produce a rigorous structured learning package.

{mode_instruction}
{multimodal_context}

Target Context:
- Filename: {filename}
- Target Exam Track: {target_exam}
- Target Subject: {target_subject or 'Inferred from content'}
- Required MCQ Count: {num_questions if mode != 'summarize' else 2}

Material Content:
\"\"\"
{trimmed_text or '(Image input provided via multimodal channel)'}
\"\"\"

Output MUST be 100% valid JSON matching this exact structure:
{{
  "title": "Clear, professional academic title of the document",
  "summary": "Comprehensive 3-5 sentence executive summary of the core concepts, principles, and findings",
  "key_takeaways": [
    "Takeaway 1: core formula or theorem",
    "Takeaway 2: key insight or relationship",
    "Takeaway 3: practical application or caveat"
  ],
  "extracted_concepts": [
    {{
      "name": "Academic Concept Name",
      "topic": "Broad Topic Name",
      "subject": "{target_subject or 'General Studies'}",
      "exam": "{target_exam}",
      "description": "2-3 sentence rigorous pedagogical definition suitable for textbooks",
      "key_formula": "$$E = mc^2$$ or null if non-mathematical"
    }}
  ],
  "generated_questions": [
    {{
      "concept_name": "Matching Concept Name from extracted_concepts",
      "content": "A rigorous, authentic multiple-choice problem testing first principles",
      "options": [
        {{"id": "A", "text": "Option text"}},
        {{"id": "B", "text": "Option text"}},
        {{"id": "C", "text": "Option text"}},
        {{"id": "D", "text": "Option text"}}
      ],
      "correct_answer": "A",
      "explanation": "Step-by-step mathematical or conceptual resolution proving why the correct option is true",
      "distractor_explanations": {{
        "B": "CALCULATION_ERROR: Inverted divisor or arithmetic slip",
        "C": "CONCEPTUAL_ERROR: Misapplied theorem boundary condition",
        "D": "FORMULA_SELECTION_ERROR: Used zero-order approximation"
      }},
      "difficulty": 0.55,
      "discrimination": 1.25,
      "estimated_time": 60
    }}
  ]
}}

CRITICAL REQUIREMENTS:
1. Every question MUST have 4 options: A, B, C, D.
2. The distractor_explanations MUST diagnose all 3 incorrect options with error tags (CONCEPTUAL_ERROR, CALCULATION_ERROR, FORMULA_SELECTION_ERROR).
3. Generate between 3 and 5 distinct concepts that represent the core pillars of the text.
4. Return ONLY the raw JSON object. No Markdown code fences, no extra text.
"""

    parsed_payload = None
    try:
        parsed_payload = _execute_gemini_synthesis(
            prompt,
            model_name=model_name,
            image_bytes=image_bytes,
            mime_type=mime_type
        )
    except Exception as e:
        logger.warning(f"Gemini synthesis failed, switching to pedagogical fallback: {str(e)}")
        fallback_text = document_text or f"Visual and textual study notes from {filename} regarding {target_subject or 'applied science'}."
        parsed_payload = _generate_fallback_synthesis(
            document_text=fallback_text,
            filename=filename,
            target_exam=target_exam,
            target_subject=target_subject,
            num_questions=num_questions if mode != 'summarize' else 2
        )

    # Build Pydantic models
    concepts = [
        ExtractedConcept(
            concept_id=f"cnc_{uuid.uuid4().hex[:8]}",
            name=c.get("name", "Unknown Concept"),
            topic=c.get("topic", "General Topic"),
            subject=c.get("subject", target_subject or "General Studies"),
            exam=c.get("exam", target_exam),
            description=c.get("description", ""),
            key_formula=c.get("key_formula")
        )
        for c in parsed_payload.get("extracted_concepts", [])
    ]

    questions = []
    for q in parsed_payload.get("generated_questions", []):
        opts = [
            GeneratedMCQOption(id=opt.get("id", "A"), text=opt.get("text", ""))
            for opt in q.get("options", [])
        ]
        questions.append(GeneratedMCQ(
            question_id=f"q_pdf_{uuid.uuid4().hex[:8]}",
            concept_name=q.get("concept_name", concepts[0].name if concepts else "General"),
            content=q.get("content", ""),
            options=opts,
            correct_answer=q.get("correct_answer", "A"),
            explanation=q.get("explanation", ""),
            distractor_explanations=q.get("distractor_explanations", {}),
            difficulty=float(q.get("difficulty", 0.55)),
            discrimination=float(q.get("discrimination", 1.2)),
            estimated_time=int(q.get("estimated_time", 60))
        ))

    word_count = len(document_text.split()) if document_text else 250
    return DocumentIngestionResult(
        doc_id=f"doc_{uuid.uuid4().hex[:8]}",
        filename=filename,
        title=parsed_payload.get("title", f"Summary of {filename}"),
        word_count=word_count,
        page_count=1,
        summary=parsed_payload.get("summary", "Document analyzed successfully."),
        key_takeaways=parsed_payload.get("key_takeaways", []),
        extracted_concepts=concepts,
        generated_questions=questions,
        mode=mode
    )

