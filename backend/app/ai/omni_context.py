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
from typing import Dict, Any, List, Optional, Tuple, Sequence
import math
from sqlalchemy.orm import Session

from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept, Question,
    AssessmentAttempt, StudentAttemptItem, Roadmap, RoadmapAction, Prerequisite
)
from backend.app.knowledge_graph.fineweb_vault import FINEWEB_READINGS, get_fineweb_readings
from backend.app.student_model.akt import AttentionKnowledgeTracing
from backend.app.student_model.irt import MultidimensionalIRT
from backend.app.student_model.bkt import BayesianKnowledgeTracing
from backend.app.student_model.fsrs_engine import FSRSEngine


class CognitiveStateAccumulator:
    """
    Dynamic Cognitive State Accumulator:
    Calculates student cognitive entropy scores, tracks compilation/error thrashing trajectories,
    extracts recursive prerequisite DAG subtrees, and synthesizes live control signals.
    """

    @staticmethod
    def compute_student_cognitive_entropy(items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates Shannon entropy H(S) over student error categories and response latency variance.
        High entropy indicates erratic guessing or thrashing; low entropy indicates localized misconceptions.
        """
        if not items:
            return {
                "entropy_score": 0.0,
                "normalized_entropy": 0.0,
                "is_thrashing": False,
                "thrashing_mode": "NOMINAL",
                "latency_spread_seconds": 0.0,
                "state": "BASELINE_STANDBY"
            }

        error_counts: Dict[str, int] = {}
        latencies: List[float] = []
        total_errors = 0
        rapid_wrong_count = 0
        freeze_wrong_count = 0

        for it in items:
            t = float(it.get("time_taken_seconds") or 45.0)
            latencies.append(t)
            is_corr = bool(it.get("is_correct", False))

            if not is_corr:
                etype = it.get("error_type") or "CONCEPTUAL_ERROR"
                error_counts[etype] = error_counts.get(etype, 0) + 1
                total_errors += 1
                if t < 15.0:
                    rapid_wrong_count += 1
                elif t > 150.0:
                    freeze_wrong_count += 1

        if total_errors == 0:
            std_dev = 0.0
            if len(latencies) > 1:
                m_lat = sum(latencies) / len(latencies)
                var_lat = sum((l - m_lat) ** 2 for l in latencies) / len(latencies)
                std_dev = round(math.sqrt(var_lat), 1)
            return {
                "entropy_score": 0.0,
                "normalized_entropy": 0.0,
                "is_thrashing": False,
                "thrashing_mode": "NOMINAL",
                "latency_spread_seconds": std_dev,
                "state": "HIGH_STABILITY_MASTERY"
            }

        # Shannon Entropy H = - sum(p * log2(p))
        entropy = 0.0
        for count in error_counts.values():
            p = count / total_errors
            if p > 0:
                entropy -= p * math.log2(p)

        k = max(len(error_counts), 1)
        max_possible_entropy = math.log2(k) if k > 1 else 1.0
        normalized_entropy = round(min(entropy / max(max_possible_entropy, 1.0), 1.0), 2)

        avg_lat = sum(latencies) / len(latencies)
        variance = sum((l - avg_lat) ** 2 for l in latencies) / len(latencies)
        lat_spread = math.sqrt(variance)

        is_thrashing = False
        thrashing_mode = "NOMINAL"

        if rapid_wrong_count >= 2:
            is_thrashing = True
            thrashing_mode = "RAPID_GUESSING"
        elif freeze_wrong_count >= 2:
            is_thrashing = True
            thrashing_mode = "COGNITIVE_FREEZE"
        elif entropy > 1.5 and lat_spread > 40.0:
            is_thrashing = True
            thrashing_mode = "OSCILLATING_CONFUSION"

        return {
            "entropy_score": round(entropy, 2),
            "normalized_entropy": normalized_entropy,
            "is_thrashing": is_thrashing,
            "thrashing_mode": thrashing_mode,
            "latency_spread_seconds": round(lat_spread, 1),
            "rapid_wrong_count": rapid_wrong_count,
            "freeze_wrong_count": freeze_wrong_count,
            "error_distribution": error_counts
        }

    @staticmethod
    def extract_prerequisite_subtrees(
        target_concept_id: str,
        student_id: str,
        db: Session,
        max_depth: int = 3
    ) -> Dict[str, Any]:
        """
        Recursively extracts multi-hop prerequisite ancestral subtrees from the knowledge graph
        and pinpoints the deepest broken foundation node blocking the student.
        """
        visited = set()
        subtree_nodes = []
        root_broken_ancestor = None

        def traverse_ancestors(cid: str, depth: int):
            if depth > max_depth or cid in visited:
                return
            visited.add(cid)

            # Query direct prerequisites (to_concept_id == cid means from_concept_id is the prerequisite parent)
            prereqs = db.query(Prerequisite).filter(Prerequisite.to_concept_id == cid).all()
            for p in prereqs:
                parent_id = p.from_concept_id
                parent_concept = db.query(Concept).filter(Concept.concept_id == parent_id).first()
                p_name = parent_concept.name if parent_concept else parent_id

                mastery_rec = (
                    db.query(StudentConceptMastery)
                    .filter(StudentConceptMastery.student_id == student_id,
                            StudentConceptMastery.concept_id == parent_id)
                    .first()
                )
                m_val = mastery_rec.mastery if mastery_rec else 0.25
                retrievability = getattr(mastery_rec, "fsrs_retrievability", 1.0) or 1.0

                node_entry = {
                    "concept_id": parent_id,
                    "name": p_name,
                    "depth": depth,
                    "mastery": round(m_val * 100, 1),
                    "retrievability": round(retrievability * 100, 1),
                    "is_broken": m_val < 0.60 or retrievability < 0.65,
                    "blocks": cid
                }
                subtree_nodes.append(node_entry)

                nonlocal root_broken_ancestor
                if node_entry["is_broken"]:
                    if not root_broken_ancestor or depth > root_broken_ancestor["depth"]:
                        root_broken_ancestor = node_entry

                traverse_ancestors(parent_id, depth + 1)

        traverse_ancestors(target_concept_id, 1)

        return {
            "target_concept_id": target_concept_id,
            "has_broken_ancestors": root_broken_ancestor is not None,
            "root_broken_ancestor": root_broken_ancestor,
            "total_ancestors_tracked": len(subtree_nodes),
            "subtree_nodes": subtree_nodes
        }


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
            all_items = []
            for item, q in items:
                distractor_note = None
                if q.distractor_explanations and item.student_answer:
                    distractor_note = q.distractor_explanations.get(item.student_answer)

                c_name = q.concept.name if (q.concept and q.concept.name) else q.concept_id
                item_dict = {
                    "question_id": q.question_id,
                    "subject": q.subject,
                    "chapter": q.chapter or "Core Syllabus",
                    "topic": q.topic or q.chapter or "General",
                    "concept_id": q.concept_id,
                    "concept_name": c_name,
                    "student_answer": item.student_answer,
                    "correct_answer": q.correct_answer,
                    "is_correct": bool(item.is_correct),
                    "error_type": item.error_type or "CONCEPTUAL_GAP",
                    "distractor_note": distractor_note,
                    "explanation": q.explanation or "Apply fundamental governing equations step-by-step.",
                    "options": q.options,
                    "time_taken_seconds": item.time_taken_seconds,
                    "content": q.content,
                    "content_snippet": (q.content[:140] + "...") if q.content and len(q.content) > 140 else q.content
                }
                all_items.append(item_dict)
                if not item.is_correct:
                    mistakes.append(item_dict)

            test_title = latest_attempt.assessment.title if (latest_attempt.assessment and latest_attempt.assessment.title) else "Diagnostic Assessment"
            attempt_dict = {
                "assessment_id": latest_attempt.assessment_id,
                "attempt_id": latest_attempt.attempt_id,
                "test_title": test_title,
                "score_percentage": round(latest_attempt.score_percentage, 1) if latest_attempt.score_percentage is not None else 0.0,
                "correct_count": latest_attempt.correct_count,
                "total_questions": latest_attempt.total_questions,
                "time_taken_seconds": latest_attempt.time_taken_seconds,
                "submitted_at": latest_attempt.submitted_at.isoformat() if latest_attempt.submitted_at else None,
                "items": all_items,
                "mistakes": mistakes
            }
            context["latest_attempt"] = attempt_dict
            context["latest_quiz"] = attempt_dict
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

        # 5. FINEWEB-EDU & KNOWLEDGE VAULT RETRIEVER
        vault_matches = OmniContextHarvester.find_vault_matches(
            prompt=prompt or "",
            exam=exam,
            db=db,
            limit=3
        )
        # Only return vault readings if there is an authentic match for the student query.
        # If the query does not match any file, do NOT suggest unsolicited files to the student!
        if not prompt or not prompt.strip():
            # Only provide baseline track readings when harvesting for the static telemetry HUD
            if not vault_matches:
                for r in FINEWEB_READINGS:
                    if r.get("course") == exam or exam == "JEE":
                        vault_matches.append({
                            "id": r.get("id"),
                            "title": r.get("title"),
                            "course": r.get("course", exam),
                            "subject": r.get("subject"),
                            "chapter": r.get("chapter"),
                            "summary": r.get("summary"),
                            "formula": (r.get("formula_box") or {}).get("latex"),
                            "formula_latex": (r.get("formula_box") or {}).get("latex"),
                            "formula_plain": (r.get("formula_box") or {}).get("plain"),
                            "reading_time_mins": r.get("reading_time_mins", 3),
                            "score": r.get("score", 4.8),
                            "preview_chip": f"📚 Vault: {r.get('title', '')[:28]}...",
                            "preview_url": f"vault:{r.get('id')}",
                            "didactic_notes": r.get("didactic_notes") or {},
                            "match_score": 1.0
                        })
                        break

        context["vault_readings"] = vault_matches
        context["fineweb_citations"] = vault_matches[:2]

        # 6. LIFETIME DIAGNOSTIC MEMORY (All Quizzes & Practice History)
        context["lifetime_diagnostics"] = OmniContextHarvester.harvest_lifetime_diagnostics(student_id, db)

        # 7. DYNAMIC COGNITIVE ACCUMULATION: Entropy, Thrashing & Prerequisite Subtrees
        all_recent_items = []
        if latest_attempt:
            for item, _ in items:
                all_recent_items.append({
                    "is_correct": item.is_correct,
                    "error_type": item.error_type or "CONCEPTUAL_ERROR",
                    "time_taken_seconds": item.time_taken_seconds or 45
                })
        elif context["lifetime_diagnostics"] and context["lifetime_diagnostics"].get("lifetime_mistakes"):
            for m in context["lifetime_diagnostics"]["lifetime_mistakes"]:
                all_recent_items.append({
                    "is_correct": False,
                    "error_type": m.get("error_type", "CONCEPTUAL_ERROR"),
                    "time_taken_seconds": m.get("time_taken_seconds", 45)
                })

        entropy_diag = CognitiveStateAccumulator.compute_student_cognitive_entropy(all_recent_items)

        # Extract recursive prerequisite subtree for top weak concept
        prereq_subtree = None
        if context["weak_concepts"]:
            top_weak_cid = context["weak_concepts"][0]["concept_id"]
            prereq_subtree = CognitiveStateAccumulator.extract_prerequisite_subtrees(top_weak_cid, student_id, db)

        # Expose live MIRT cognitive control vector
        mirt_signals = MultidimensionalIRT.get_cognitive_control_vector(context.get("latent_ability_theta", 0.0))

        # Expose AKT sequence predictive signals
        akt_tuples = [(m.get("question_id", f"q_{i}"), m.get("is_correct", False)) for i, m in enumerate(all_recent_items[-10:])]
        akt_engine = AttentionKnowledgeTracing()
        akt_prediction = akt_engine.predict_next_interaction(akt_tuples)

        # Expose BKT slip/guess signal on recent observation
        bkt_signal = None
        if all_recent_items:
            last_it = all_recent_items[-1]
            bkt = BayesianKnowledgeTracing()
            bkt_signal = bkt.evaluate_slip_vs_guess(
                p_known=context["overall_mastery"] / 100.0,
                is_correct=last_it["is_correct"]
            )

        # Expose proactive FSRS decay remediation candidate
        fsrs_candidate = FSRSEngine.find_decay_remediation_candidates(masteries)

        context["cognitive_state"] = {
            "entropy_score": entropy_diag["entropy_score"],
            "normalized_entropy": entropy_diag["normalized_entropy"],
            "is_thrashing": entropy_diag["is_thrashing"],
            "thrashing_mode": entropy_diag["thrashing_mode"],
            "latency_spread_seconds": entropy_diag["latency_spread_seconds"],
            "prerequisite_subtrees": prereq_subtree,
            "cognitive_control_signals": {
                "mirt": mirt_signals,
                "akt": akt_prediction,
                "bkt": bkt_signal
            },
            "decay_remediation": fsrs_candidate
        }

        return context


    @classmethod
    def find_vault_matches(
        cls,
        prompt: str,
        exam: str = "JEE",
        db: Optional[Session] = None,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Matches user query against local Knowledge Vault readings (curated FineWeb-Edu + dynamic curriculum).
        Computes weighted relevance score across titles, chapters, formulas, and content.
        Returns structured readings with preview metadata and interactive chip identifiers.
        """
        if not prompt or not prompt.strip():
            return []

        clean_p = prompt.lower()
        stopwords = {
            "what", "tell", "explain", "about", "this", "that", "these", "those",
            "please", "could", "would", "should", "with", "from", "into", "onto",
            "give", "show", "some", "more", "help", "need", "know", "want", "like",
            "have", "does", "will", "cant", "dont", "isnt", "arent", "the", "and",
            "for", "how", "why", "when", "where", "which", "can", "you", "me"
        }
        tokens = [t.strip("?,.:;!'\"()[]{}") for t in clean_p.split() if len(t.strip("?,.:;!'\"()[]{}")) >= 3]
        query_terms = [t for t in tokens if t not in stopwords]
        if not query_terms:
            query_terms = tokens

        # Fetch corpus: dynamic database readings + static readings
        corpus: List[Dict[str, Any]] = []
        try:
            corpus = get_fineweb_readings(course=exam or "ALL", db=db)
        except Exception:
            corpus = []

        if not corpus:
            corpus = FINEWEB_READINGS

        scored_candidates = []
        seen_ids = set()

        for r in corpus:
            rid = r.get("id")
            if not rid or rid in seen_ids:
                continue

            r_course = (r.get("course") or "").upper()
            course_match = (r_course == (exam or "JEE").upper() or (exam == "JEE" and r_course == "JEE"))

            title_l = (r.get("title") or "").lower()
            chap_l = (r.get("chapter") or "").lower()
            subj_l = (r.get("subject") or "").lower()
            summ_l = (r.get("summary") or "").lower()
            fbox = r.get("formula_box") or {}
            f_latex = (fbox.get("latex") or "").lower()
            f_plain = (fbox.get("plain") or "").lower()

            score = 0.0

            # Direct phrase match in title
            if clean_p in title_l or (len(title_l) > 6 and title_l in clean_p):
                score += 15.0

            # Term level matching
            for t in query_terms:
                if t in title_l:
                    score += 6.0
                elif t in chap_l:
                    score += 4.5
                elif t in subj_l:
                    score += 2.0
                elif t in f_plain or t in f_latex:
                    score += 3.5
                elif t in summ_l:
                    score += 1.5

            if score > 0:
                if course_match:
                    score += 3.0  # Track affinity boost

                seen_ids.add(rid)
                scored_candidates.append({
                    "id": rid,
                    "title": r.get("title") or "Academic Reading",
                    "course": r.get("course") or exam,
                    "subject": r.get("subject") or "General",
                    "chapter": r.get("chapter") or "Curriculum",
                    "summary": r.get("summary") or "",
                    "formula": fbox.get("latex"),
                    "formula_latex": fbox.get("latex"),
                    "formula_plain": fbox.get("plain"),
                    "reading_time_mins": r.get("reading_time_mins", 3),
                    "score": r.get("score", 4.5),
                    "preview_chip": f"📚 Vault: {r.get('title')[:30]}..." if len(r.get('title', '')) > 30 else f"📚 Vault: {r.get('title')}",
                    "preview_url": f"vault:{rid}",
                    "didactic_notes": r.get("didactic_notes") or {},
                    "match_score": round(score, 2)
                })

        scored_candidates.sort(key=lambda x: (x["match_score"], x["score"]), reverse=True)
        return scored_candidates[:limit]


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
            m_items = []
            for m in mistakes[:3]:
                top = m.get("topic") or m.get("chapter") or "Curriculum Area"
                cname = m.get("concept_name") or m.get("concept_id") or "Core Principle"
                prob = (m.get("content_snippet") or m.get("content") or "").replace("\n", " ")
                stud_ans = m.get("student_answer") or "Skipped"
                corr_ans = m.get("correct_answer") or "Key"
                trap = m.get("distractor_note") or m.get("error_type") or "Conceptual miscalculation"
                sol = m.get("explanation") or "Apply fundamental governing equations step-by-step."
                m_items.append(
                    f"• [Topic: {top} | Concept: {cname}]\n"
                    f"  - Problem Context: \"{prob}\"\n"
                    f"  - Student Selected: Option {stud_ans} (Cognitive Trap: {trap})\n"
                    f"  - Correct Answer: Option {corr_ans}\n"
                    f"  - Step-by-Step Resolution: {sol}"
                )
            lines.append("Recent Test Mistake Diagnostics (HUMAN ACADEMIC ANALYSIS — NO RAW IDs):\n" + "\n".join(m_items))

        vault = context.get("vault_readings") or context.get("fineweb_citations", [])
        if vault:
            v_items = []
            for v in vault[:2]:
                f_str = f" [Formula: {v.get('formula_latex') or v.get('formula')}]" if (v.get('formula_latex') or v.get('formula')) else ""
                v_items.append(f"[{v.get('chapter', 'Curriculum')}: {v.get('title')}]{f_str}")
            lines.append(f"Knowledge Vault Academic Grounding: {' | '.join(v_items)}")

        # 7. LIVE COGNITIVE ACCUMULATOR & CONTROL SIGNALS
        cog = context.get("cognitive_state")
        if cog:
            entropy_line = f"Cognitive Entropy H={cog.get('entropy_score', 0.0)} (Mode: {cog.get('thrashing_mode', 'NOMINAL')})"
            if cog.get("is_thrashing"):
                entropy_line += " ⚠️ [THRASHING TRAJECTORY DETECTED - APPLY SCAFFOLDING]"
            lines.append(entropy_line)

            subtrees = cog.get("prerequisite_subtrees")
            if subtrees and subtrees.get("has_broken_ancestors") and subtrees.get("root_broken_ancestor"):
                root = subtrees["root_broken_ancestor"]
                lines.append(
                    f"Knowledge Graph Root Cause: Deepest broken prerequisite is '{root['name']}' ({root['mastery']}%, depth {root['depth']}). Fix this node before advancing."
                )

            ctrl = cog.get("cognitive_control_signals", {})
            mirt = ctrl.get("mirt", {})
            if mirt.get("mentor_directive"):
                lines.append(f"Pedagogical Control Directive ({mirt.get('pedagogical_focus')}): {mirt['mentor_directive']}")

            decay = cog.get("decay_remediation")
            if decay and decay.get("interleaving_instruction"):
                lines.append(f"Proactive FSRS Decay Alert: {decay['interleaving_instruction']}")

        return "\n".join(lines)

