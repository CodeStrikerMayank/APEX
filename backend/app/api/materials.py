"""
Materials Ingestion & Self-Evolving Knowledge Vault Router
Handles multipart/form-data PDF and document uploads, text extraction,
Gemini-powered concept synthesis, MCQ generation, and database auto-augmentation.
"""
import io
import logging
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.curriculum.pdf_ingestor import (
    extract_text_from_pdf_bytes,
    analyze_and_synthesize_document,
    DocumentIngestionResult
)
from backend.app.curriculum.vault_augmenter import augment_vault_and_database
from backend.app.knowledge_graph.fineweb_vault import FINEWEB_READINGS

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/materials",
    tags=["Materials & Knowledge Vault Ingestion"]
)


class TextIngestRequest(BaseModel):
    title: str = Field(default="Custom Learning Document")
    text: str = Field(..., min_length=50, description="Raw text of learning material or lecture notes")
    exam: str = Field(default="JEE", description="Target exam track: JEE, NEET, UPSC, STATS")
    subject: Optional[str] = Field(None, description="Optional subject classification")
    num_questions: int = Field(default=5, ge=1, le=10)


@router.post("/upload-pdf", response_model=DocumentIngestionResult)
@router.post("/upload-document", response_model=DocumentIngestionResult)
async def upload_pdf_and_augment_vault(
    file: UploadFile = File(...),
    exam: str = Form("JEE"),
    subject: Optional[str] = Form(None),
    num_questions: int = Form(5),
    mode: str = Form("both"),
    db: Session = Depends(get_db)
):
    """
    Accepts a PDF, Image (PNG, JPG, WEBP), or TXT document upload, extracts text/vision features,
    generates executive summaries, identifies newly discovered concepts/competencies,
    synthesizes calibrated MCQs, and automatically augments the SQLite database and Knowledge Vault.
    Supports modes: 'summarize', 'quiz', 'both'.
    """
    filename = file.filename or "uploaded_document.pdf"
    content_bytes = await file.read()

    if not content_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    lower_filename = filename.lower()
    document_text = ""
    image_bytes: Optional[bytes] = None
    mime_type: Optional[str] = None

    # 1. Image formats (PNG, JPG, JPEG, WEBP)
    if lower_filename.endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
        image_bytes = content_bytes
        if lower_filename.endswith(".png"):
            mime_type = "image/png"
        elif lower_filename.endswith((".jpg", ".jpeg")):
            mime_type = "image/jpeg"
        elif lower_filename.endswith(".webp"):
            mime_type = "image/webp"
        else:
            mime_type = "image/jpeg"
        document_text = f"Attached visual learning document: {filename}"

    # 2. PDF format
    elif lower_filename.endswith(".pdf"):
        try:
            extraction = extract_text_from_pdf_bytes(content_bytes)
            document_text = extraction["text"]
            if not document_text or len(document_text.strip()) < 20:
                # If PDF text is thin, check if it's a scanned/visual PDF
                document_text = f"Visual/Scanned PDF Material: {filename}. Synthesizing academic structure and concepts."
        except Exception as e:
            logger.error(f"PDF Parsing error on {filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to read PDF document: {str(e)}")

    # 3. Plain text / Markdown
    elif lower_filename.endswith((".txt", ".md", ".json")):
        try:
            document_text = content_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read text file: {str(e)}")

    # 4. Fallback decoding
    else:
        try:
            document_text = content_bytes.decode("utf-8", errors="replace")
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF, image (.png, .jpg, .webp), or plain text (.txt) document."
            )

    try:
        # Synthesize with Google Gemini Flash (multimodal or text)
        clean_mode = mode.lower().strip() if mode in ["summarize", "quiz", "both"] else "both"
        ingestion = analyze_and_synthesize_document(
            document_text=document_text,
            filename=filename,
            target_exam=exam,
            target_subject=subject,
            num_questions=min(max(num_questions, 1), 10),
            mode=clean_mode,
            image_bytes=image_bytes,
            mime_type=mime_type
        )

        # Auto-save to SQLite and augment Knowledge Vault
        augmented_result = augment_vault_and_database(
            db=db,
            ingestion_result=ingestion,
            default_exam=exam
        )

        return augmented_result

    except Exception as e:
        logger.error(f"Failed to synthesize and augment material: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Academic synthesis failed: {str(e)}")



@router.post("/generate-from-text", response_model=DocumentIngestionResult)
async def generate_from_raw_text(
    payload: TextIngestRequest,
    db: Session = Depends(get_db)
):
    """
    Accepts raw pasted text, extracts concepts, generates MCQs with distractor modeling,
    and automatically saves newly discovered concepts into the Knowledge Vault.
    """
    try:
        ingestion = analyze_and_synthesize_document(
            document_text=payload.text,
            filename=payload.title,
            target_exam=payload.exam,
            target_subject=payload.subject,
            num_questions=payload.num_questions
        )

        augmented_result = augment_vault_and_database(
            db=db,
            ingestion_result=ingestion,
            default_exam=payload.exam
        )

        return augmented_result

    except Exception as e:
        logger.error(f"Text synthesis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text synthesis failed: {str(e)}")


@router.get("/augmented-vault")
async def get_augmented_vault_items():
    """
    Retrieves all user-augmented and dynamic readings currently active in the Knowledge Vault.
    """
    augmented = [r for r in FINEWEB_READINGS if str(r.get("id", "")).startswith("VAULT-AUG-")]
    return {
        "augmented_readings_count": len(augmented),
        "readings": augmented
    }
