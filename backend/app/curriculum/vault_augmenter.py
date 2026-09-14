"""
Knowledge Vault Auto-Augmenter & Self-Evolving Database Synchronization
Compares newly extracted concepts and MCQs against the existing curriculum database.
If new concepts or questions are discovered, it dynamically provisions:
- Subject, Chapter, Topic, and Concept hierarchy in SQLite
- Persists new MCQs with cognitive distractor modeling in SQLite
- Augments FineWeb-Edu Knowledge Vault in-memory store so readings appear immediately
"""
import logging
import uuid
import re
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session

from backend.app.models.schema import (
    Exam, Subject, Chapter, Topic, Concept, Question
)
from backend.app.curriculum.pdf_ingestor import DocumentIngestionResult, ExtractedConcept, GeneratedMCQ
from backend.app.knowledge_graph.fineweb_vault import FINEWEB_READINGS

logger = logging.getLogger(__name__)


def _sanitize_id(text: str, prefix: str = "id") -> str:
    """Generates a clean URL/DB-safe alphanumeric ID string."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', text.strip().lower())
    clean = re.sub(r'_+', '_', clean)[:40]
    return f"{prefix}_{clean}" if clean else f"{prefix}_{uuid.uuid4().hex[:8]}"


def augment_vault_and_database(
    db: Session,
    ingestion_result: DocumentIngestionResult,
    default_exam: str = "JEE"
) -> DocumentIngestionResult:
    """
    Persists new concepts and questions into SQLite and augments the Knowledge Vault.
    Guarantees idempotency: existing concepts and questions are linked rather than duplicated.
    """
    exam_code = ingestion_result.extracted_concepts[0].exam if ingestion_result.extracted_concepts else default_exam
    if exam_code.upper() in ["JEE", "IIT-JEE", "PCM"]:
        exam_id = "JEE"
    elif exam_code.upper() in ["NEET", "PCB"]:
        exam_id = "NEET"
    elif exam_code.upper() in ["UPSC", "CIVIL_SERVICES"]:
        exam_id = "UPSC"
    else:
        exam_id = "JEE"

    # 1. Ensure Exam exists
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if not exam:
        exam = Exam(exam_id=exam_id, name=f"{exam_id} Curriculum Track", tracks=[])
        db.add(exam)
        db.flush()

    new_concepts_count = 0
    new_questions_count = 0
    concept_map: Dict[str, Concept] = {}

    for ec in ingestion_result.extracted_concepts:
        # Check if concept exists by name (case-insensitive)
        existing_concept = db.query(Concept).filter(
            Concept.name.ilike(ec.name.strip())
        ).first()

        if existing_concept:
            ec.is_new_discovery = False
            ec.concept_id = existing_concept.concept_id
            concept_map[ec.name.lower()] = existing_concept
            continue

        # 2. Provision Subject
        subj_name = ec.subject.strip().capitalize() or "General"
        subj_id = _sanitize_id(f"{exam_id}_{subj_name}", prefix="subj")
        subject = db.query(Subject).filter(Subject.subject_id == subj_id).first()
        if not subject:
            subject = db.query(Subject).filter(
                Subject.exam_id == exam_id,
                Subject.name.ilike(subj_name)
            ).first()
        if not subject:
            subject = Subject(subject_id=subj_id, exam_id=exam_id, name=subj_name)
            db.add(subject)
            db.flush()

        # 3. Provision Chapter (under dynamic Ingested Materials chapter)
        chap_name = f"Ingested: {ingestion_result.title[:45]}"
        chap_id = _sanitize_id(f"{subject.subject_id}_{ingestion_result.doc_id}", prefix="chap")
        chapter = db.query(Chapter).filter(Chapter.chapter_id == chap_id).first()
        if not chapter:
            chapter = Chapter(chapter_id=chap_id, subject_id=subject.subject_id, name=chap_name)
            db.add(chapter)
            db.flush()

        # 4. Provision Topic
        topic_name = ec.topic.strip() or "Core Foundations"
        topic_id = _sanitize_id(f"{chapter.chapter_id}_{topic_name}", prefix="top")
        topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()
        if not topic:
            topic = Topic(topic_id=topic_id, chapter_id=chapter.chapter_id, name=topic_name)
            db.add(topic)
            db.flush()

        # 5. Provision Concept
        new_concept_id = _sanitize_id(f"cnc_{ec.name}", prefix="cnc")
        existing_concept_by_id = db.query(Concept).filter(
            (Concept.concept_id == new_concept_id) | (Concept.name.ilike(ec.name.strip()))
        ).first()

        if existing_concept_by_id:
            ec.is_new_discovery = False
            ec.concept_id = existing_concept_by_id.concept_id
            concept_map[ec.name.lower()] = existing_concept_by_id
            continue

        # If ID somehow exists with different name, append unique suffix
        if db.query(Concept).filter(Concept.concept_id == new_concept_id).first():
            new_concept_id = f"{new_concept_id[:32]}_{uuid.uuid4().hex[:6]}"

        new_concept = Concept(
            concept_id=new_concept_id,
            topic_id=topic.topic_id,
            name=ec.name.strip(),
            estimated_minutes=30,
            exam_relevance=0.90,
            difficulty_weight=0.50,
            description=ec.description
        )
        db.add(new_concept)
        db.flush()

        ec.is_new_discovery = True
        ec.concept_id = new_concept.concept_id
        concept_map[ec.name.lower()] = new_concept
        new_concepts_count += 1

        # Also augment in-memory FineWeb Knowledge Vault so it displays immediately
        vault_entry = {
            "id": f"VAULT-AUG-{new_concept.concept_id.upper()}",
            "course": exam_id,
            "subject": subj_name,
            "chapter": chap_name,
            "title": f"{ec.name}: Conceptual Overview & Derivation",
            "score": 4.90,
            "source": f"User Ingested: {ingestion_result.filename}",
            "word_count": len(ec.description.split()) + 150,
            "reading_time_mins": 3,
            "summary": ec.description,
            "formula_box": {
                "title": f"Key Formula: {ec.name}",
                "latex": ec.key_formula or "N/A",
                "plain": ec.key_formula or "N/A",
                "terms": [["Core", ec.name]]
            },
            "content": f"### Overview\n{ec.description}\n\n### Theoretical Formulation\n{ec.key_formula or 'Pure conceptual foundation.'}\n\n### Academic Takeaways\n- Extracted directly from: {ingestion_result.filename}\n- Added to dynamic knowledge graph.",
            "didactic_notes": {
                "axiom": f"Core competency in {ec.name} derived from uploaded material.",
                "trap": "Verify first-principles reasoning when solving related assessment problems.",
                "mnemonic": f"Review key formula: {ec.key_formula or 'Defined conceptually'}"
            },
            "key_takeaways": ingestion_result.key_takeaways[:3]
        }
        FINEWEB_READINGS.append(vault_entry)

    # 6. Save newly generated questions into SQLite
    for gq in ingestion_result.generated_questions:
        # Check if question content or ID already exists
        existing_q = db.query(Question).filter(
            (Question.question_id == gq.question_id) | (Question.content == gq.content.strip())
        ).first()

        if existing_q:
            gq.question_id = existing_q.question_id
            continue

        if db.query(Question).filter(Question.question_id == gq.question_id).first():
            gq.question_id = f"q_pdf_{uuid.uuid4().hex[:10]}"

        # Match to concept
        matched_concept = concept_map.get(gq.concept_name.lower())
        if not matched_concept and concept_map:
            matched_concept = list(concept_map.values())[0]

        if not matched_concept:
            # Fallback to any existing concept
            matched_concept = db.query(Concept).first()

        concept_id = matched_concept.concept_id if matched_concept else "cnc_general"
        topic = matched_concept.topic if matched_concept else None
        chapter = topic.chapter if topic else None
        subject = chapter.subject if chapter else None

        new_question = Question(
            question_id=gq.question_id,
            exam=exam_id,
            paper=f"{exam_id}_INGESTED",
            subject=subject.name if subject else "General",
            chapter=chapter.name if chapter else "Ingested Materials",
            topic=topic.name if topic else "General Topic",
            chapter_id=chapter.chapter_id if chapter else None,
            topic_id=topic.topic_id if topic else None,
            concept_id=concept_id,
            skill="conceptual",
            difficulty=gq.difficulty,
            discrimination=gq.discrimination,
            guessing=0.25,
            estimated_time=gq.estimated_time,
            question_type="multiple_choice",
            content=gq.content.strip(),
            options=[{"id": o.id, "text": o.text} for o in gq.options],
            correct_answer=gq.correct_answer.strip().upper(),
            explanation=gq.explanation.strip(),
            distractor_explanations=gq.distractor_explanations,
            tier="STANDARD"
        )
        db.add(new_question)
        new_questions_count += 1

    db.commit()

    ingestion_result.new_concepts_added_count = new_concepts_count
    ingestion_result.new_questions_added_count = new_questions_count
    ingestion_result.vault_updated = True

    logger.info(
        f"Vault successfully augmented: +{new_concepts_count} new concepts, "
        f"+{new_questions_count} new questions from '{ingestion_result.filename}'."
    )

    return ingestion_result
