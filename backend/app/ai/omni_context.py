"""
Omni-Context Grounding Engine
Harvests full internal cognitive telemetry:
- IRT Latent Ability (\\theta) and BKT Concept Masteries
- Critical Weak Concepts & Decaying Topics (FSRS retrievability)
- Curriculum DAG Bottlenecks & Prerequisite Chains
- Mistake Forensics & Distractor Traps
- FineWeb-Edu Textbook Citations & Formula Grounding
- Roadmap Status & Next-Best Action (NBA)
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept, Question,
    AssessmentAttempt, StudentAttemptItem, Roadmap, RoadmapAction, Prerequisite
)
from backend.app.knowledge_graph.fineweb_vault import FINEWEB_READINGS


class OmniContextHarvester:
    @staticmethod
    def harvest_full_context(student_id: str, db: Session, prompt: str = "") -> Dict[str, Any]:
        """
        Harvests student's full internal cognitive telemetry across all engines.
        Returns a rich dictionary ready for AI prompt grounding and HUD rendering.
        """
        context: Dict[str, Any] = {
            "student_id": student_id,
            "student_name": "Aspirant",
            "target_exam": "JEE",
            "overall_mastery": 0.0,
            "latent_ability_theta": 0.0,
            "ability_tier": "Diagnostic Baseline (Standby)",
            "subject_mastery": {},
            "bkt_distribution": {
                "mastered_count": 0,
                "progressing_count": 0,
                "needs_review_count": 0,
                "total_tracked": 0
            },
            "weak_concepts": [],
            "decaying_concepts": [],
            "mastered_concepts": [],
            "prerequisite_bottlenecks": [],
            "recent_mistakes": [],
            "latest_quiz": None,
            "active_roadmap": None,
            "fineweb_citations": [],
            "lifetime_diagnostics": None
        }

        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            context["student_name"] = student.name
            context["target_exam"] = student.target_exam or "JEE"

        exam = context["target_exam"]

        # 1. PSYCHOMETRICS: BKT Concept Masteries, FSRS Retrievability & IRT Latent Ability (theta)
        masteries = db.query(StudentConceptMastery).filter(StudentConceptMastery.student_id == student_id).all()
        if masteries:
            total_m = sum(m.mastery for m in masteries)
            total_theta = sum(m.irt_ability for m in masteries)
            n_m = max(len(masteries), 1)
            context["overall_mastery"] = round((total_m / n_m) * 100, 1)
            avg_theta = round(total_theta / n_m, 2)
            context["latent_ability_theta"] = avg_theta

            # Ability Tier Description
            if avg_theta >= 1.5:
                context["ability_tier"] = "Advanced Scholar (Top 1% Percentile)"
            elif avg_theta >= 0.7:
                context["ability_tier"] = "Proficient Problem Solver (Top 5-10%)"
            elif avg_theta >= 0.0:
                context["ability_tier"] = "Core Conceptual Competence (Median)"
            elif avg_theta >= -0.8:
                context["ability_tier"] = "Developing Baseline (Foundation Phase)"
            else:
                context["ability_tier"] = "Needs Guided Prerequisite Repair"

            # Subject Breakdown & Categorization
            subj_totals: Dict[str, List[float]] = {}
            weak_list = []
            decaying_list = []
            mastered_list = []

            m_count = 0
            p_count = 0
            nr_count = 0

            for m in masteries:
                concept = db.query(Concept).filter(Concept.concept_id == m.concept_id).first()
                c_name = concept.name if concept else m.concept_id

                # Safe subject extraction without requiring direct column
                sub = "General"
                if concept:
                    if hasattr(concept, "subject") and getattr(concept, "subject", None):
                        sub = concept.subject
                    elif concept.topic and concept.topic.chapter and concept.topic.chapter.subject:
                        sub = concept.topic.chapter.subject.name

                if sub not in subj_totals:
                    subj_totals[sub] = []
                subj_totals[sub].append(m.mastery)

                retrievability = getattr(m, "fsrs_retrievability", 1.0) or 1.0
                forgetting = getattr(m, "forgetting_risk", 0.0) or 0.0

                item_summary = {
                    "concept_id": m.concept_id,
                    "name": c_name,
                    "subject": sub,
                    "mastery": round(m.mastery * 100, 1),
                    "bkt_mastery": round((getattr(m, "bkt_mastery", m.mastery) or m.mastery) * 100, 1),
                    "theta": round(m.irt_ability, 2),
                    "confidence": round(m.confidence * 100, 1) if m.confidence else 50.0,
                    "retrievability": round(retrievability * 100, 1),
                    "forgetting_risk": round(forgetting * 100, 1)
                }

                if m.mastery >= 0.80:
                    m_count += 1
                    mastered_list.append(item_summary)
                elif m.mastery >= 0.50:
                    p_count += 1
                else:
                    nr_count += 1

                if m.mastery < 0.60:
                    weak_list.append(item_summary)

                # Decaying concepts: low retrievability (< 70%) or high forgetting risk (> 40%)
                if (retrievability < 0.70 or forgetting > 0.40) and m.mastery >= 0.30:
                    decaying_list.append(item_summary)

            context["bkt_distribution"] = {
                "mastered_count": m_count,
                "progressing_count": p_count,
                "needs_review_count": nr_count,
                "total_tracked": len(masteries)
            }

            weak_list.sort(key=lambda x: x["mastery"])
            decaying_list.sort(key=lambda x: x["retrievability"])
            mastered_list.sort(key=lambda x: x["mastery"], reverse=True)

            context["weak_concepts"] = weak_list[:6]
            context["decaying_concepts"] = decaying_list[:4]
            context["mastered_concepts"] = mastered_list[:6]

            for s, vals in subj_totals.items():
                context["subject_mastery"][s] = round((sum(vals) / len(vals)) * 100, 1)

        # 2. CURRICULUM DAG BOTTLENECKS
        if context["weak_concepts"]:
            for wc in context["weak_concepts"][:3]:
                cid = wc["concept_id"]
                # Use to_concept_id matching Prerequisite schema
                prereqs = db.query(Prerequisite).filter(Prerequisite.to_concept_id == cid).all()
                for p in prereqs:
                    prereq_mastery = (
                        db.query(StudentConceptMastery)
                        .filter(StudentConceptMastery.student_id == student_id,
                                StudentConceptMastery.concept_id == p.from_concept_id)
                        .first()
                    )
                    pm_val = prereq_mastery.mastery if prereq_mastery else 0.25
                    if pm_val < 0.70:
                        p_concept = db.query(Concept).filter(Concept.concept_id == p.from_concept_id).first()
                        context["prerequisite_bottlenecks"].append({
                            "target_concept": wc["name"],
                            "blocking_prerequisite": p_concept.name if p_concept else p.from_concept_id,
                            "prerequisite_mastery": round(pm_val * 100, 1),
                            "relationship": p.relationship_type
                        })

        # 3. MISTAKE FORENSICS & DISTRACTOR LOGBOOK
        latest_attempt = (
            db.query(AssessmentAttempt)
            .filter(AssessmentAttempt.student_id == student_id, AssessmentAttempt.is_completed == True)
            .order_by(AssessmentAttempt.submitted_at.desc())
            .first()
        )
        if latest_attempt:
            items = (
                db.query(StudentAttemptItem, Question)
                .join(Question, StudentAttemptItem.question_id == Question.question_id)
                .filter(StudentAttemptItem.attempt_id == latest_attempt.attempt_id)
                .all()
            )
            mistakes = []
            for item, q in items:
                if not item.is_correct:
                    distractor_note = None
                    if q.distractor_explanations and item.student_answer:
                        distractor_note = q.distractor_explanations.get(item.student_answer)

                    mistakes.append({
                        "question_id": q.question_id,
                        "subject": q.subject,
                        "concept_id": q.concept_id,
                        "student_answer": item.student_answer,
                        "correct_answer": q.correct_answer,
                        "error_type": item.error_type or "CONCEPTUAL_GAP",
                        "distractor_note": distractor_note,
                        "time_taken_seconds": item.time_taken_seconds,
                        "content_snippet": (q.content[:120] + "...") if q.content and len(q.content) > 120 else q.content
                    })

            context["latest_quiz"] = {
                "score_percentage": latest_attempt.score_percentage,
                "correct_count": latest_attempt.correct_count,
                "total_questions": latest_attempt.total_questions,
                "time_taken_seconds": latest_attempt.time_taken_seconds,
                "mistakes": mistakes
            }
            context["recent_mistakes"] = mistakes[:5]

        # 4. ROADMAP STATUS & NEXT-BEST ACTION (NBA)
        latest_roadmap = (
            db.query(Roadmap)
            .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
            .order_by(Roadmap.version.desc())
            .first()
        )
        if latest_roadmap:
            actions = (
                db.query(RoadmapAction)
                .filter(RoadmapAction.roadmap_id == latest_roadmap.roadmap_id)
                .order_by(RoadmapAction.sequence_order)
                .limit(4)
                .all()
            )
            act_list = []
            for a in actions:
                c = db.query(Concept).filter(Concept.concept_id == a.concept_id).first()
                act_list.append({
                    "order": a.sequence_order,
                    "title": c.name if c else a.concept_id,
                    "action_type": a.action_type,
                    "estimated_minutes": a.estimated_minutes,
                    "reasons": a.reasons
                })
            context["active_roadmap"] = {
                "version": latest_roadmap.version,
                "actions": act_list,
                "next_action": act_list[0] if act_list else None
            }

        # 5. FINEWEB-EDU CITATIONS & KNOWLEDGE MATCHING
        query_terms = (prompt or "").lower().split()
        relevant_readings = []
        for r in FINEWEB_READINGS:
            if r.get("course") == exam or (exam == "JEE" and r.get("course") == "JEE"):
                score = 0
                title_lower = (r.get("title") or "").lower()
                chap_lower = (r.get("chapter") or "").lower()
                summary_lower = (r.get("summary") or "").lower()

                for term in query_terms:
                    if len(term) > 3:
                        if term in title_lower or term in chap_lower:
                            score += 3
                        elif term in summary_lower:
                            score += 1

                if score == 0 and context["weak_concepts"]:
                    top_weak_name = context["weak_concepts"][0]["name"].lower()
                    if top_weak_name in title_lower or top_weak_name in chap_lower:
                        score += 2

                if score > 0 or len(relevant_readings) == 0:
                    relevant_readings.append({
                        "id": r.get("id"),
                        "title": r.get("title"),
                        "chapter": r.get("chapter"),
                        "subject": r.get("subject"),
                        "formula": r.get("formula_box", {}).get("latex"),
                        "summary": r.get("summary"),
                        "reading_time_mins": r.get("reading_time_mins", 3)
                    })
                if len(relevant_readings) >= 2:
                    break

        context["fineweb_citations"] = relevant_readings[:2]
        # 6. LIFETIME DIAGNOSTIC MEMORY (All Quizzes & Practice History)
        context["lifetime_diagnostics"] = OmniContextHarvester.harvest_lifetime_diagnostics(student_id, db)
        return context

    @staticmethod
    def harvest_lifetime_diagnostics(student_id: str, db: Session) -> Dict[str, Any]:
        """
        Harvests student's complete historical record across all completed assessments,
        quizzes, and student attempt items.
        Returns:
            - total_assessments: total completed attempts
            - total_questions_attempted: total items answered
            - total_correct: correct count
            - overall_accuracy_pct: percentage
            - total_time_spent_seconds: sum of time
            - error_breakdown: { "CALCULATION_ERROR": count, "CONCEPTUAL_ERROR": count, ... }
            - top_error_types: sorted list of {"error_type": ..., "count": ...}
            - subject_breakdown: { "Physics": {"total": x, "correct": y, "accuracy_pct": z}, ... }
            - recurring_traps: list of distinct distractor trap messages
            - chronological_scores: list of attempts with date, score, correct_count, total_questions
            - lifetime_mistakes: recent mistakes across all tests
        """
        diagnostics: Dict[str, Any] = {
            "total_assessments": 0,
            "total_questions_attempted": 0,
            "total_correct": 0,
            "overall_accuracy_pct": 0.0,
            "total_time_spent_seconds": 0,
            "error_breakdown": {},
            "top_error_types": [],
            "subject_breakdown": {},
            "recurring_traps": [],
            "chronological_scores": [],
            "lifetime_mistakes": []
        }

        attempts = (
            db.query(AssessmentAttempt)
            .filter(AssessmentAttempt.student_id == student_id, AssessmentAttempt.is_completed == True)
            .order_by(AssessmentAttempt.started_at.asc())
            .all()
        )
        if not attempts:
            return diagnostics

        diagnostics["total_assessments"] = len(attempts)
        diagnostics["total_time_spent_seconds"] = sum(a.time_taken_seconds or 0 for a in attempts)

        chronological = []
        attempt_ids = []
        for a in attempts:
            attempt_ids.append(a.attempt_id)
            title = "Practice Assessment"
            if a.assessment and a.assessment.title:
                title = a.assessment.title
            date_str = a.started_at.strftime("%b %d, %H:%M") if a.started_at else "Recent"
            chronological.append({
                "attempt_id": a.attempt_id,
                "title": title,
                "score_percentage": round(a.score_percentage or 0.0, 1),
                "correct_count": a.correct_count or 0,
                "total_questions": a.total_questions or 0,
                "date": date_str
            })
        diagnostics["chronological_scores"] = chronological

        # Query all items
        items = (
            db.query(StudentAttemptItem, Question)
            .join(Question, StudentAttemptItem.question_id == Question.question_id)
            .filter(StudentAttemptItem.attempt_id.in_(attempt_ids))
            .all()
        )

        total_q = len(items)
        correct_q = sum(1 for item, _ in items if item.is_correct)
        diagnostics["total_questions_attempted"] = total_q
        diagnostics["total_correct"] = correct_q
        if total_q > 0:
            diagnostics["overall_accuracy_pct"] = round((correct_q / total_q) * 100, 1)

        err_counts: Dict[str, int] = {}
        trap_notes: Dict[str, int] = {}
        subject_stats: Dict[str, Dict[str, int]] = {}
        all_mistakes = []

        for item, q in items:
            sub = q.subject or "General"
            if sub not in subject_stats:
                subject_stats[sub] = {"total": 0, "correct": 0}
            subject_stats[sub]["total"] += 1
            if item.is_correct:
                subject_stats[sub]["correct"] += 1
            else:
                etype = item.error_type or "CONCEPTUAL_ERROR"
                err_counts[etype] = err_counts.get(etype, 0) + 1

                distractor_note = None
                if q.distractor_explanations and item.student_answer:
                    distractor_note = q.distractor_explanations.get(item.student_answer)
                    if distractor_note:
                        trap_notes[distractor_note] = trap_notes.get(distractor_note, 0) + 1

                all_mistakes.append({
                    "question_id": q.question_id,
                    "subject": q.subject,
                    "concept_id": q.concept_id,
                    "student_answer": item.student_answer,
                    "correct_answer": q.correct_answer,
                    "error_type": etype,
                    "distractor_note": distractor_note,
                    "time_taken_seconds": item.time_taken_seconds,
                    "content_snippet": (q.content[:120] + "...") if q.content and len(q.content) > 120 else q.content,
                    "explanation": q.explanation
                })

        diagnostics["error_breakdown"] = err_counts
        diagnostics["top_error_types"] = sorted(
            [{"error_type": k, "count": v} for k, v in err_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )

        for sub, sdata in subject_stats.items():
            tot = sdata["total"]
            cor = sdata["correct"]
            pct = round((cor / tot) * 100, 1) if tot > 0 else 0.0
            diagnostics["subject_breakdown"][sub] = {
                "total": tot,
                "correct": cor,
                "accuracy_pct": pct
            }

        diagnostics["recurring_traps"] = sorted(
            [{"note": k, "frequency": v} for k, v in trap_notes.items()],
            key=lambda x: x["frequency"],
            reverse=True
        )[:5]

        diagnostics["lifetime_mistakes"] = all_mistakes[-20:]
        return diagnostics

    @staticmethod
    def format_grounding_block(context: Dict[str, Any], mode: str = "pedagogical") -> str:
        """
        Formats the harvested omni-context into a concise, rich grounding string for LLMs.
        """
        lines = []
        lines.append(f"Student: {context.get('student_name', 'Aspirant')} | Target Exam: {context.get('target_exam', 'JEE')}")
        lines.append(f"IRT Latent Ability theta: {context.get('latent_ability_theta', 0.0)} ({context.get('ability_tier', 'Standard')})")
        lines.append(f"Overall Mastery: {context.get('overall_mastery', 0.0)}%")

        life = context.get("lifetime_diagnostics")
        if life and life.get("total_questions_attempted", 0) > 0:
            lines.append(
                f"Lifetime History: {life['total_questions_attempted']} Qs across {life['total_assessments']} assessments ({life['overall_accuracy_pct']}% overall accuracy)"
            )
            top_errs = life.get("top_error_types", [])
            if top_errs:
                err_str = ", ".join(f"{e['error_type']} ({e['count']}x)" for e in top_errs[:3])
                lines.append(f"Dominant Lifetime Error Modes: {err_str}")
            rec_traps = life.get("recurring_traps", [])
            if rec_traps:
                trap_str = "; ".join(f"'{t['note']}' (x{t['frequency']})" for t in rec_traps[:2])
                lines.append(f"Recurring Distractor Traps: {trap_str}")

        weak = context.get("weak_concepts", [])
        if weak:
            weak_str = ", ".join(f"{w['name']} ({w['mastery']}%)" for w in weak[:3])
            lines.append(f"Critical Weak Concepts: {weak_str}")

        decay = context.get("decaying_concepts", [])
        if decay:
            decay_str = ", ".join(f"{d['name']} (R={d['retrievability']}%)" for d in decay[:2])
            lines.append(f"Decaying Memory (FSRS): {decay_str}")

        bottlenecks = context.get("prerequisite_bottlenecks", [])
        if bottlenecks:
            b_str = ", ".join(f"{b['target_concept']} blocked by {b['blocking_prerequisite']} ({b['prerequisite_mastery']}%)" for b in bottlenecks[:2])
            lines.append(f"DAG Bottlenecks: {b_str}")

        mistakes = context.get("recent_mistakes", [])
        if mistakes:
            m_str = "; ".join(
                f"Q: {m['question_id']} Choice: {m['student_answer']} Correct: {m['correct_answer']} (Trap: {m.get('distractor_note') or m['error_type']})"
                for m in mistakes[:2]
            )
            lines.append(f"Recent Mistake Forensics: {m_str}")

        citations = context.get("fineweb_citations", [])
        if citations:
            c_str = " | ".join(f"[{c['chapter']}: {c['title']}] Formula: {c.get('formula') or 'N/A'}" for c in citations)
            lines.append(f"Academic Reference Passages: {c_str}")

        return "\n".join(lines)
