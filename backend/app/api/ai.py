from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from backend.app.database.connection import get_db
from backend.app.models.schema import (
    Student, StudentConceptMastery, Concept, Question,
    AssessmentAttempt, StudentAttemptItem, Roadmap, RoadmapAction
)
from backend.app.schemas.pydantic_models import AIChatRequest, AIChatResponse, AIQuestionGenRequest
from backend.app.ai.local_llm import LocalLLMClient
from backend.app.ai.explanation import ExplanationGenerator
from backend.app.ai.question_generator import AIQuestionGenerator
from backend.app.ai.omni_context import OmniContextHarvester
from backend.app.ai.intent_classifier import (
    IntentClassifier,
    INTENT_GREETING,
    INTENT_OFF_TOPIC,
    INTENT_ANALYZE_MISTAKES,
    INTENT_EXPLAIN_ROADMAP,
    INTENT_STRATEGY_TIPS,
    INTENT_EXPLAIN_CONCEPT
)
from backend.app.ai.templates import format_greeting, format_off_topic_response

router = APIRouter(prefix="/ai", tags=["Offline AI Assistant & Tools"])

@router.get("/telemetry-hud/{student_id}")
async def get_student_telemetry_hud(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Returns live student cognitive telemetry: IRT ability, weak concepts, DAG bottlenecks, and FineWeb citations."""
    hud_data = OmniContextHarvester.harvest_full_context(student_id, db)
    return hud_data

@router.post("/chat/{student_id}", response_model=AIChatResponse)
async def chat_with_assistant(
    student_id: str,
    req: AIChatRequest,
    db: Session = Depends(get_db)
):
    llm = LocalLLMClient()

    student_context: Dict[str, Any] = {}
    context_str = ""

    student = db.query(Student).filter(Student.student_id == student_id).first()
    latest_attempt = None
    if student:
        student_context["student_name"] = student.name
        student_context["target_exam"] = student.target_exam

        # Masteries
        masteries = db.query(StudentConceptMastery).filter(StudentConceptMastery.student_id == student_id).all()
        avg_m = (sum(m.mastery for m in masteries) / max(len(masteries), 1)) if masteries else 0.0
        avg_theta = (sum(m.irt_ability for m in masteries) / max(len(masteries), 1)) if masteries else 0.0
        student_context["overall_mastery"] = round(avg_m * 100, 1)
        student_context["latent_ability_theta"] = round(avg_theta, 2)

        # Latest Quiz Attempt
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
            quiz_items = []
            mistakes = []
            subject_breakdown: Dict[str, Dict[str, int]] = {}

            for item, q in items:
                sub = q.subject or "General"
                if sub not in subject_breakdown:
                    subject_breakdown[sub] = {"total": 0, "correct": 0}
                subject_breakdown[sub]["total"] += 1
                if item.is_correct:
                    subject_breakdown[sub]["correct"] += 1

                distractor_note = None
                if not item.is_correct and q.distractor_explanations and item.student_answer:
                    distractor_note = q.distractor_explanations.get(item.student_answer)

                item_info = {
                    "question_id": q.question_id,
                    "subject": q.subject,
                    "concept_id": q.concept_id,
                    "is_correct": item.is_correct,
                    "student_answer": item.student_answer,
                    "correct_answer": q.correct_answer,
                    "error_type": item.error_type,
                    "explanation": q.explanation,
                    "distractor_note": distractor_note,
                    "content_snippet": q.content[:140] + "..." if len(q.content) > 140 else q.content
                }
                quiz_items.append(item_info)
                if not item.is_correct:
                    mistakes.append(item_info)

            student_context["latest_quiz"] = {
                "score_percentage": latest_attempt.score_percentage,
                "correct_count": latest_attempt.correct_count,
                "total_questions": latest_attempt.total_questions,
                "time_taken_seconds": latest_attempt.time_taken_seconds,
                "subject_breakdown": subject_breakdown,
                "items": quiz_items,
                "mistakes": mistakes
            }

        # Latest Roadmap
        latest_roadmap = (
            db.query(Roadmap)
            .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
            .order_by(Roadmap.version.desc())
            .first()
        )
        if not latest_roadmap:
            try:
                from backend.app.roadmap.generator import RoadmapGenerator
                gen = RoadmapGenerator(db, exam_id=student.target_exam)
                latest_roadmap = gen.generate_roadmap(student_id, trigger_event="AI_STANDBY_INIT")
                db.commit()
            except Exception:
                db.rollback()

        if latest_roadmap:
            actions = (
                db.query(RoadmapAction)
                .filter(RoadmapAction.roadmap_id == latest_roadmap.roadmap_id)
                .order_by(RoadmapAction.sequence_order)
                .limit(6)
                .all()
            )
            student_context["roadmap_actions"] = []
            for a in actions:
                c = db.query(Concept).filter(Concept.concept_id == a.concept_id).first()
                student_context["roadmap_actions"].append({
                    "order": a.sequence_order,
                    "concept_id": a.concept_id,
                    "title": c.name if c else a.concept_id,
                    "action_type": a.action_type,
                    "priority_score": a.priority_score,
                    "reasons": a.reasons,
                    "target_questions": a.target_questions_count,
                    "estimated_minutes": a.estimated_minutes
                })

    # Harvest deep omni-context across psychometrics, weak concepts, DAG bottlenecks, and FineWeb readings
    try:
        omni_ctx = OmniContextHarvester.harvest_full_context(student_id, db, req.get_prompt())
        for k, v in omni_ctx.items():
            if k not in student_context or not student_context[k]:
                student_context[k] = v
    except Exception as e:
        pass

    from backend.app.ai.socratic_agents import PedagogicalPolicyRouter, SocraticCoordinator, SocraticProberAgent, PsychologistAgent
    from backend.app.student_model.error_classifier import CodeTraceDissector
    from backend.app.student_model.numerical_guards import OutputNumericalGuard

    raw_mode = (req.mode or "auto").lower()
    cog_state = student_context.get("cognitive_state") or {}

    if raw_mode in ["auto", "adaptive", ""]:
        route = PedagogicalPolicyRouter.determine_route(
            entropy_score=cog_state.get("entropy_score", 0.0),
            mastery=student_context.get("overall_mastery", 50.0),
            theta=student_context.get("latent_ability_theta", 0.0),
            is_thrashing=cog_state.get("is_thrashing", False),
            has_broken_prereq=bool(cog_state.get("prerequisite_subtrees", {}).get("has_broken_ancestors") if isinstance(cog_state.get("prerequisite_subtrees"), dict) else False),
            recent_error_count=len(student_context.get("recent_mistakes", []))
        )
        mode = route["mode"].lower()
        student_context["pedagogical_route"] = route
    else:
        mode = raw_mode
    student_context["mode"] = mode

    prompt_raw = req.get_prompt()
    prompt_lower = prompt_raw.lower()

    # --- Intent Classification Pre-Check & Domain Protocol Engine ---
    from backend.app.ai.domain_protocols import DomainProtocolEngine
    from backend.app.ai.cloud_llm import build_unified_system_prompt

    user_intent, intent_confidence, topic_hint = IntentClassifier.classify(prompt_raw)
    exam_label = student.target_exam if student and student.target_exam else "JEE"
    student_name = student.name if student else "Aspirant"

    domain_diag = DomainProtocolEngine.classify_query_domain(prompt_raw, target_exam=exam_label)
    is_solve = domain_diag["is_solve"] or raw_mode == "solve" or "solve" in prompt_lower.split()

    # 1. Pure Greeting Handler (Warm, Intellectually Grounded, Cold-Start Aware)
    if user_intent == INTENT_GREETING:
        greeting_text = format_greeting(student_context)
        is_cold_start = (student_context.get("total_assessments", 0) == 0 and not latest_attempt)
        greeting_chips = [
            "⚡ Take 3-Min Diagnostic",
            "🗺️ Explore My Roadmap",
            "🔬 Explain SHM & Oscillations",
            "📊 Speed & Pacing Tips"
        ] if is_cold_start else [
            "📊 What mistakes am I making?",
            "🗺️ Why is my roadmap ordered this way?",
            "⚡ Speed & Pacing Tips",
            "🎯 Give Me a Challenge Question"
        ]
        return AIChatResponse(
            response=greeting_text,
            source="ACADEMIC_MENTOR_GREETING",
            suggested_chips=greeting_chips,
            domain_protocol=domain_diag["domain"]
        )

    # 2. Purely Non-Academic Casual Chat (Movies, pop culture, trivia)
    # If the user asks ANY STEM, Science, Math, Biology, Tech, UPSC or GK query, let the Cloud LLM answer it directly!
    if user_intent == INTENT_OFF_TOPIC and domain_diag["category"] == "CASUAL_OFF_TOPIC":
        off_topic_text = format_off_topic_response(topic_hint, exam_label, student_name)
        return AIChatResponse(
            response=off_topic_text,
            source="SYLLABUS_GUARD_ROUTER",
            suggested_chips=[
                "🔬 Explain High-Yield Concepts",
                "⚡ Pacing & Strategy Tips",
                "🎯 Take Practice Drill",
                "🗺️ View Exam Roadmap"
            ],
            domain_protocol="OFF_TOPIC"
        )

    # --- Structured AST & Error Trace Preprocessing ---
    troubleshoot_diag = CodeTraceDissector.preprocess_troubleshooting_input(prompt_raw)
    troubleshoot_str = ""
    if troubleshoot_diag["type"] == "TRACEBACK":
        tb = troubleshoot_diag["dissection"]
        troubleshoot_str = (
            f"\n[TECHNICAL TRACEBACK DISSECTION]\n"
            f"Exception Type: {tb.get('exception_type')}\n"
            f"Failing Frame: {tb.get('failing_frame')}\n"
            f"Root Cause Message: {tb.get('exception_message')}\n"
            "INSTRUCTION: Target this exact exception and frame. Explain why this error occurred in the execution flow.\n"
        )
    elif troubleshoot_diag["type"] == "CODE_SNIPPET":
        cd = troubleshoot_diag["dissection"]
        if not cd.get("valid_syntax"):
            troubleshoot_str = (
                f"\n[TECHNICAL CODE AST DISSECTION]\n"
                f"Syntax Fault: {cd.get('fault_category')} at line {cd.get('fault_line')}, offset {cd.get('fault_offset')}\n"
                f"Offending text: '{cd.get('fault_line_text')}'\n"
                f"Message: {cd.get('fault_message')}\n"
                "INSTRUCTION: Guide the student to identify this exact syntax issue without rewriting their entire program.\n"
            )
        else:
            metrics = cd.get("ast_metrics") or {}
            troubleshoot_str = (
                f"\n[TECHNICAL CODE AST METRICS]\n"
                f"Valid Syntax: True | Nodes: {metrics.get('total_nodes')} | Loops: {metrics.get('has_loops')} | Recursion: {metrics.get('has_recursion')}\n"
            )


    # --- Pillar 3: In-Chat Interactive Quiz Agent ---
    is_quiz_req = bool(req.quiz_intent) or any(k in prompt_lower for k in [
        "quiz me", "test me", "micro-check", "micro check",
        "practice question", "give me a question", "targeted recovery drill",
        "quick drill", "practice problem", "interactive quiz",
        "retest", "re-test", "retest mistakes", "recovery drill", "test my mistakes"
    ])

    if is_quiz_req:
        exam_filter = student.target_exam if student and student.target_exam else "JEE"
        target_cid = req.concept_id

        if not target_cid:
            # First check if student prompt mentions any concept directly
            all_c = db.query(Concept).all()
            for c in all_c:
                if c.name and (c.name.lower() in prompt_lower or c.concept_id.lower() in prompt_lower):
                    target_cid = c.concept_id
                    break

        if not target_cid:
            # Prioritize targeting missed concepts from student's recent test attempt
            recent_m = student_context.get("latest_quiz", {}).get("mistakes") or student_context.get("recent_mistakes") or []
            for m in recent_m:
                if m.get("concept_id"):
                    target_cid = m.get("concept_id")
                    break

        if not target_cid:
            # Check if any weak concepts match or use the first weak concept
            weak_list = student_context.get("weak_concepts") or []
            if weak_list and len(weak_list) > 0:
                target_cid = weak_list[0].get("concept_id")

        q_target = None
        q_query = db.query(Question).filter(Question.exam == exam_filter)
        if target_cid:
            q_target = q_query.filter(Question.concept_id == target_cid).first()
        if not q_target:
            # Try matching chapter or subject from prompt
            all_q = q_query.all()
            for q_cand in all_q:
                if (q_cand.chapter and q_cand.chapter.lower() in prompt_lower) or (q_cand.subject and q_cand.subject.lower() in prompt_lower):
                    q_target = q_cand
                    break
        if not q_target:
            q_target = q_query.first()

        if q_target:
            raw_opts = q_target.options or []
            formatted_opts = []
            if isinstance(raw_opts, list):
                for o in raw_opts:
                    if isinstance(o, dict):
                        formatted_opts.append(o)
                    elif isinstance(o, str):
                        opt_id = o[:1].upper() if o[:1].isalpha() else str(len(formatted_opts) + 1)
                        formatted_opts.append({"id": opt_id, "text": o})
            if not formatted_opts:
                formatted_opts = [
                    {"id": "A", "text": "Option A"},
                    {"id": "B", "text": "Option B"},
                    {"id": "C", "text": "Option C"},
                    {"id": "D", "text": "Option D"}
                ]

            c_name = q_target.concept_id
            c_obj = db.query(Concept).filter(Concept.concept_id == q_target.concept_id).first()
            if c_obj:
                c_name = c_obj.name

            structured_card = {
                "type": "quiz",
                "question_id": q_target.question_id,
                "subject": q_target.subject,
                "chapter": q_target.chapter,
                "concept_id": q_target.concept_id,
                "concept_name": c_name,
                "content": q_target.content,
                "options": formatted_opts,
                "correct_answer": q_target.correct_answer,
                "explanation": q_target.explanation,
                "distractor_explanations": q_target.distractor_explanations or {}
            }

            theta_val = student_context.get("latent_ability_theta", 0.0)
            resp_msg = (
                f"🎯 **Interactive Micro-Challenge: {c_name}**\n\n"
                f"I've generated a high-yield question calibrated to your latent ability "
                f"($\\theta = {theta_val:+.2f}$). Test your conceptual understanding directly below:"
            )

            return AIChatResponse(
                response=resp_msg,
                source="INTERACTIVE_QUIZ_AGENT",
                structured_card=structured_card,
                suggested_chips=[
                    "📐 Unpack Derivation",
                    "⚠️ Common Traps",
                    "💡 Numerical Example",
                    "🔄 Another Question"
                ]
            )

    # --- Multi-Turn Rolling History Ingestion ---
    history_str = ""
    if req.history and isinstance(req.history, list):
        recent_turns = req.history[-6:]
        turn_lines = []
        for turn in recent_turns:
            role_name = turn.get("role", "user").upper()
            msg_txt = turn.get("text", "")
            if msg_txt and role_name in ["USER", "COACH", "ASSISTANT"]:
                clean_txt = msg_txt[:200].replace("\n", " ")
                turn_lines.append(f"{role_name}: {clean_txt}")
        if turn_lines:
            history_str = "\n[RECENT CONVERSATION HISTORY]\n" + "\n".join(turn_lines) + "\n"

    # Build unified single-statement multi-tier system prompt with domain protocol
    system_prompt = build_unified_system_prompt(
        student_context=student_context,
        exam=domain_diag["domain"],
        mode=mode,
        is_solve=is_solve,
        troubleshoot_str=troubleshoot_str,
        history_str=history_str
    )

    # Determine active session duration for Agent 3 (Psychologist)
    active_minutes = 0.0
    from backend.app.models.schema import utc_now
    if student and student.last_active:
        diff_secs = (utc_now() - student.last_active).total_seconds()
        if 0 <= diff_secs <= 86400:
            active_minutes = diff_secs / 60.0
    if latest_attempt and latest_attempt.time_taken_seconds:
        active_minutes = max(active_minutes, latest_attempt.time_taken_seconds / 60.0)

    is_explicit_socratic = raw_mode in ["socratic", "scaffolding", "diagnostic"]
    is_troubleshoot = troubleshoot_diag.get("type") in ["TRACEBACK", "CODE_SNIPPET"]
    is_mistake_review = (
        user_intent == INTENT_ANALYZE_MISTAKES or
        any(k in prompt_lower for k in [
            "mistake", "mistakes", "error", "errors", "wrong", "last test",
            "past test", "previous test", "review my test", "performance correction",
            "retest", "how did i do", "what did i miss"
        ])
    )

    structured_card = None
    if is_mistake_review and (latest_attempt or student_context.get("latest_quiz") or student_context.get("recent_mistakes")):
        l_quiz = student_context.get("latest_quiz") or {}
        test_title = l_quiz.get("test_title") or (latest_attempt.assessment.title if (latest_attempt and latest_attempt.assessment) else "Last Completed Assessment")
        mistakes_list = l_quiz.get("mistakes") or student_context.get("recent_mistakes") or []

        score_val = l_quiz.get("score_percentage")
        if score_val is None and latest_attempt:
            score_val = latest_attempt.score_percentage
        score_val = round(score_val or 0.0, 1)

        c_count = l_quiz.get("correct_count") if l_quiz.get("correct_count") is not None else (latest_attempt.correct_count if latest_attempt else 0)
        t_count = l_quiz.get("total_questions") if l_quiz.get("total_questions") is not None else (latest_attempt.total_questions if latest_attempt else len(mistakes_list))
        time_sec = l_quiz.get("time_taken_seconds") if l_quiz.get("time_taken_seconds") is not None else (latest_attempt.time_taken_seconds if latest_attempt else 0)

        structured_card = {
            "type": "test_review",
            "test_title": test_title,
            "score_percentage": score_val,
            "correct_count": c_count,
            "total_questions": t_count,
            "time_taken_seconds": time_sec,
            "can_retest": True,
            "retest_concept_ids": [m["concept_id"] for m in mistakes_list if m.get("concept_id")],
            "mistakes": [
                {
                    "topic": m.get("topic") or m.get("chapter") or "Curriculum Area",
                    "chapter": m.get("chapter", ""),
                    "concept_name": m.get("concept_name") or m.get("concept_id"),
                    "concept_id": m.get("concept_id"),
                    "question_text": m.get("content"),
                    "content_snippet": m.get("content_snippet") or ((m.get("content") or "")[:140] + "..."),
                    "student_answer": m.get("student_answer"),
                    "correct_answer": m.get("correct_answer"),
                    "options": m.get("options"),
                    "trap_explanation": m.get("distractor_note"),
                    "solution_explanation": m.get("explanation"),
                    "error_type": m.get("error_type")
                }
                for m in mistakes_list
            ]
        }

    if is_explicit_socratic or (mode in ["socratic", "scaffolding", "diagnostic"] and is_troubleshoot and user_intent != INTENT_EXPLAIN_CONCEPT):
        concept_name = "Core Conceptual Foundation"
        if latest_attempt and student_context.get("latest_quiz", {}).get("mistakes"):
            first_mistake = student_context["latest_quiz"]["mistakes"][0]
            concept_name = first_mistake.get("concept_name") or first_mistake.get("concept_id", concept_name)
            error_type = first_mistake.get("error_type")
            explanation = first_mistake.get("explanation")
        else:
            error_type = "CONCEPTUAL_ERROR"
            explanation = None

        socratic_bundle = SocraticCoordinator.coordinate_response(
            student_id=student_id,
            db=db,
            concept_name=concept_name,
            error_type=error_type,
            explanation=explanation,
            session_duration_minutes=active_minutes,
            student_name=student.name if student else "Aspirant",
            cognitive_state=cog_state
        )
        final_text = socratic_bundle["text"]
        source = socratic_bundle["source"]
    else:
        res = await llm.generate_text(
            prompt=req.get_prompt(),
            system_prompt=system_prompt,
            student_context=student_context
        )
        final_text = res["text"]
        source = res["source"]

    # Prepend advisory note for cross-disciplinary or advanced STEM exploration
    if domain_diag.get("advisory_note") and not final_text.startswith("> 💡"):
        final_text = f"> 💡 **{domain_diag['advisory_note']}**\n\n" + final_text

    # Deterministic output verification & guard
    guard_report = OutputNumericalGuard.guard_llm_output(final_text, mode=mode)
    if not guard_report["passed"] and not guard_report["leakage_free"]:
        final_text = SocraticProberAgent.sanitize_scaffolding(final_text)

    # Attach Knowledge Vault preview badge links if articles exist and not already present
    vault_readings = student_context.get("vault_readings", [])
    if vault_readings and "vault:" not in final_text.lower() and not is_explicit_socratic:
        vault_links = []
        for v in vault_readings[:2]:
            v_title = v.get("title", "Academic Reading")
            v_score = v.get("score", 4.5)
            vault_links.append(f"- [📚 **{v_title}** (FineWeb-Edu Score: {v_score})](vault:{v['id']})")
        if vault_links:
            final_text += "\n\n**📚 Relevant Knowledge Vault Readings:**\n" + "\n".join(vault_links)

    # Construct Dynamic Interactive Chips in Asking Form
    suggested_chips = []
    if is_solve:
        suggested_chips = [
            "⚡ Step-by-Step Hint: Guide me through Step 1",
            "📐 Check Formula & Units: What is the exact formula?",
            "🎯 Give me another practice problem on this"
        ]
    else:
        # Extract topic keyword if available
        topic_term = topic_hint or ""
        if not topic_term and prompt_raw:
            stopwords = {
                "what", "is", "are", "define", "explain", "about", "the", "this", "that", "you", "tell",
                "how", "does", "connect", "connecting", "next", "topic", "topics", "syllabus",
                "would", "like", "deep", "dive", "into", "derivation", "derive", "practice", "solve",
                "question", "exam", "drill", "challenge", "please", "show", "step", "steps"
            }
            cleaned_words = [
                w for w in prompt_raw.lower().replace("?", "").replace("!", "").replace(":", "").replace(".", "").split()
                if len(w) > 2 and w not in stopwords
            ]
            topic_term = cleaned_words[0] if cleaned_words else ""

        # If still no topic keyword but history exists, check prior user turns
        if not topic_term and req.history and isinstance(req.history, list):
            for turn in reversed(req.history):
                if turn.get("role") == "user" and turn.get("text"):
                    prev_words = [
                        w for w in turn.get("text", "").lower().replace("?", "").replace("!", "").split()
                        if len(w) > 2 and w not in {
                            "what", "is", "are", "define", "explain", "about", "the", "this", "that",
                            "how", "does", "connect", "next", "topic", "syllabus", "would", "like"
                        }
                    ]
                    if prev_words:
                        topic_term = prev_words[0]
                        break

        def _clean_chip_topic(raw_text: str) -> str:
            if not raw_text:
                return ""
            raw_s = raw_text.strip()
            stop_phrases = [
                "and give me", "give me", "and provide", "and test", "and show", "with 4 options",
                "with options", "multiple choice", "mcq", "to test my understanding", "to test my",
                "to test", "for me", "please", "quick", "options", "question", "connect to the next topic",
                "in my syllabus", "deep dive into the derivation of", "deep dive into", "derivation of",
                "would you like to", "would you like", "how does", "connect to", "next topic",
                "solve a practice", "practice jee question", "practice question", "practice problem",
                "can you explain", "tell me about", "what is", "what are"
            ]
            lower_s = raw_s.lower()
            for sp in stop_phrases:
                idx = lower_s.find(sp)
                if idx >= 0:
                    raw_s = raw_s[:idx] + " " + raw_s[idx + len(sp):]
                    lower_s = raw_s.lower()

            words = [w for w in raw_s.split() if len(w) > 1 and w.lower() not in {
                "and", "the", "a", "an", "of", "in", "on", "to", "for", "with", "by", "from", "at"
            }]
            if len(words) > 3:
                words = words[:3]
            clean_result = " ".join(words).strip()
            if len(clean_result) > 22:
                clean_result = clean_result[:22].strip()
            return clean_result.title() if clean_result else "Key Principle"

        if is_mistake_review:
            suggested_chips = [
                "🎯 Retest Mistakes Drill",
                "📐 Step Derivation",
                f"🗺️ Next {exam_label} Goal"
            ]
        elif topic_term:
            topic_clean = _clean_chip_topic(topic_term)
            suggested_chips = [
                f"📐 Derive {topic_clean}",
                f"🗺️ Next Topic in Syllabus",
                f"🎯 Practice {exam_label} Drill"
            ]
        else:
            suggested_chips = [
                "📐 Key Mathematical Proof",
                "🗺️ Next Topic in Syllabus",
                f"🎯 Practice {exam_label} Drill"
            ]

    # ONLY if genuine, high-relevance Knowledge Vault files exist in the database, attach as bonus chip
    for v in vault_readings[:2]:
        c_title = v.get("title", "")
        short_t = c_title[:24] + "..." if len(c_title) > 24 else c_title
        chip_label = f"📚 Vault: {short_t}"
        if chip_label not in suggested_chips:
            suggested_chips.append(chip_label)

    return AIChatResponse(
        response=final_text,
        source=source,
        model_used=res.get("model") if ("res" in locals() and isinstance(res, dict)) else None,
        structured_card=structured_card,
        suggested_chips=suggested_chips,
        vault_readings=vault_readings[:3] if vault_readings else None,
        domain_protocol=domain_diag["domain"]
    )


@router.post("/generate-question")
async def generate_practice_question(
    req: AIQuestionGenRequest,
    db: Session = Depends(get_db)
):
    concept = db.query(Concept).filter(Concept.concept_id == req.concept_id).first()
    concept_name = concept.name if concept else req.concept_id

    gen = AIQuestionGenerator()
    q_data = await gen.generate_candidate_question(
        exam=req.exam,
        subject=req.subject,
        chapter=req.chapter,
        concept_id=req.concept_id,
        concept_name=concept_name,
        target_difficulty=req.difficulty
    )
    return q_data


@router.get("/engine-status")
async def get_engine_status():
    from backend.app.ai.cloud_llm import CloudLLMHub
    from backend.app.ai.local_llm import LocalLLMClient
    
    hub = CloudLLMHub()
    gemini_avail = hub.is_gemini_available()
    grok_avail = hub.is_grok_available()
    hf_avail = hub.is_hf_available()
    custom_avail = hub.is_custom_available()
    
    llm = LocalLLMClient()
    ollama_ok = await llm.is_available()
    
    gemini_keys = hub.get_gemini_keys()
    grok_keys = hub.get_grok_keys()
    hf_tokens = hub.get_hf_tokens()
    
    if gemini_avail:
        active_gem_key = next((k.to_dict()["masked"] for k in gemini_keys if k.is_available()), "")
        tier = f"RANK_1_GEMINI ({hub.gemini_model} • {active_gem_key})"
    elif grok_avail:
        active_grok_key = next((k.to_dict()["masked"] for k in grok_keys if k.is_available()), "")
        tier = f"RANK_2_GROK ({hub.grok_model} • {active_grok_key})"
    elif hf_avail:
        active_hf_tok = next((k.to_dict()["masked"] for k in hf_tokens if k.is_available()), "")
        tier = f"RANK_3_HF_QWEN_72B ({hub.hf_72b_model} • {active_hf_tok})"
    elif custom_avail:
        tier = f"CUSTOM_PROVIDER ({hub.custom_model})"
    elif ollama_ok:
        tier = "RANK_6_LOCAL_OLLAMA"
    else:
        tier = "RANK_7_DETERMINISTIC_SCAFFOLD"
        
    return {
        "active_tier": tier,
        "gemini_available": gemini_avail,
        "gemini_keys": [k.to_dict() for k in gemini_keys],
        "grok_available": grok_avail,
        "grok_keys": [k.to_dict() for k in grok_keys],
        "huggingface_available": hf_avail,
        "huggingface_tokens": [k.to_dict() for k in hf_tokens],
        "huggingface_model": hub.hf_model if hf_avail else None,
        "custom_available": custom_avail,
        "ollama_available": ollama_ok,
        "mentor_failsafe_active": True,
        "supported_exams": ["JEE", "NEET", "UPSC"],
        "hierarchy": [
            "Rank 1: Google Gemini (gemini-3.6-flash / gemini-3.7-flash with multi-key pool)",
            "Rank 2: xAI Grok (grok-2-latest)",
            "Rank 3: Hugging Face Qwen 2.5 72B (Qwen/Qwen2.5-72B-Instruct)",
            "Rank 4: Hugging Face Qwen 2.5 Coder 32B (Qwen/Qwen2.5-Coder-32B-Instruct)",
            "Rank 5: Hugging Face Qwen 2.5 Coder 7B (Qwen/Qwen2.5-Coder-7B-Instruct)",
            "Rank 6: Local Ollama (qwen2.5:0.5b / localhost:11434)",
            "Rank 7: Deterministic Pedagogical Scaffold & FineWeb Knowledge Vault"
        ],
        "message": "Power-Ranked AI Hierarchy with Auto-Cooldown Recharge & Failover active."
    }


class KeyConfigRequest(BaseModel):
    hf_token: Optional[str] = None
    gemini_api_key: Optional[str] = None
    grok_api_key: Optional[str] = None
    custom_provider: Optional[str] = None
    custom_api_key: Optional[str] = None
    custom_base_url: Optional[str] = None
    custom_model: Optional[str] = None
    persist_to_env: bool = False


class KeyTestRequest(BaseModel):
    provider: str
    key: str
    base_url: Optional[str] = None
    model: Optional[str] = None


@router.get("/keys-config")
async def get_keys_config():
    """Returns safe masked configuration of currently active AI provider keys."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    return CloudLLMHub.get_masked_config()


@router.post("/keys-config")
async def update_keys_config(req: KeyConfigRequest):
    """Dynamically applies new AI provider keys to runtime without server restart."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    res = CloudLLMHub.update_keys(
        hf_token=req.hf_token,
        gemini_key=req.gemini_api_key,
        grok_key=req.grok_api_key,
        custom_provider=req.custom_provider,
        custom_api_key=req.custom_api_key,
        custom_base_url=req.custom_base_url,
        custom_model=req.custom_model,
        persist_to_env=req.persist_to_env
    )
    return res


@router.post("/test-key")
async def test_provider_key(req: KeyTestRequest):
    """Tests live validity of a provided key."""
    from backend.app.ai.cloud_llm import CloudLLMHub
    return await CloudLLMHub.test_key(
        provider=req.provider,
        key=req.key,
        base_url=req.base_url,
        model=req.model
    )


@router.get("/fineweb/readings")
async def get_fineweb_readings_endpoint(
    course: Optional[str] = None,
    subject: Optional[str] = None,
    sub_category: Optional[str] = None,
    min_score: float = 0.0,
    db: Session = Depends(get_db)
):
    """
    Returns comprehensive educational readings across ALL curriculum topics extracted from the API,
    divided into primary categories (Subjects) and granular subcategories (e.g., Mechanics, Electrodynamics, Calculus).
    """
    from backend.app.knowledge_graph.fineweb_vault import get_fineweb_readings, extract_all_curriculum_readings

    # Fetch all readings for this course to extract available subcategories
    all_course_readings = extract_all_curriculum_readings(course=course or "ALL", db=db)

    # Compute subcategories list for dynamic frontend pills
    subcat_counts = {}
    for r in all_course_readings:
        sc = r.get("sub_category", "General")
        subcat_counts[sc] = subcat_counts.get(sc, 0) + 1

    subcat_emoji_map = {
        "Mechanics": "⚙️ Mechanics",
        "Electrodynamics": "⚡ Electrodynamics",
        "Optics": "🔍 Optics",
        "Modern Physics": "⚛️ Modern Physics",
        "Thermal Physics": "🔥 Thermal Physics",
        "Calculus & Analysis": "📐 Calculus & Analysis",
        "Algebra": "📊 Algebra",
        "Vectors & 3D Geometry": "📐 Vectors & 3D Geometry",
        "Physical Chemistry": "🧪 Physical Chemistry",
        "Organic Chemistry": "⚗️ Organic Chemistry",
        "Biochemistry & Biomolecules": "🧬 Biomolecules",
        "Inorganic Chemistry": "🧱 Inorganic Chemistry",
        "Cell Biology": "🔬 Cell Biology",
        "Genetics & Evolution": "🧬 Genetics & Evolution",
        "Human Physiology": "🫀 Human Physiology",
        "Plant Physiology": "🌱 Plant Physiology",
        "Ecology & Environment": "🌍 Ecology & Environment",
        "Polity & Governance": "🏛️ Polity & Governance",
        "Economy & Development": "📈 Economy & Development",
        "Environment & Ecology": "🌿 Environment & Ecology",
        "Ethics & Integrity": "⚖️ Ethics & Integrity",
        "Modern History & Culture": "📜 Modern History",
        "CSAT & Aptitude": "🧩 CSAT & Aptitude"
    }

    sub_categories_list = [
        {"id": "all", "label": "All Subcategories", "count": len(all_course_readings)}
    ] + [
        {
            "id": sc,
            "label": f"{subcat_emoji_map.get(sc, sc)} ({count})",
            "name": sc,
            "count": count
        }
        for sc, count in sorted(subcat_counts.items())
    ]

    # Filtered readings based on query params
    readings = get_fineweb_readings(
        course=course,
        subject=subject,
        sub_category=sub_category,
        min_score=min_score,
        db=db
    )

    return {
        "dataset": "HuggingFaceFW/fineweb-edu & APEX Curriculum Graph",
        "total_tokens_dataset": "1.3T",
        "course": course or "ALL",
        "count": len(readings),
        "total_topics": len(all_course_readings),
        "sub_categories": sub_categories_list,
        "readings": readings
    }


@router.get("/fineweb/reading/{reading_id}")
async def get_single_fineweb_reading(reading_id: str, db: Session = Depends(get_db)):
    """Fetches full academic excerpt by reading ID."""
    from backend.app.knowledge_graph.fineweb_vault import get_reading_by_id
    reading = get_reading_by_id(reading_id, db=db)
    if not reading:
        raise HTTPException(status_code=404, detail=f"Reading {reading_id} not found")
    return reading





@router.post("/brain-briefing/{student_id}")

async def get_brain_briefing(
    student_id: str,
    page_context: str = "DAILY_PRACTICE",
    concept_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Powers the global Brain Icon Copilot:
    - Real-time page context
    - Performance state
    - Hidden prerequisite gap assessment (from DAG)
    - Actionable cover-up drill
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam = student.target_exam if student else "JEE"

    masteries = db.query(StudentConceptMastery).filter(StudentConceptMastery.student_id == student_id).all()
    avg_m = (sum(m.mastery for m in masteries) / max(len(masteries), 1)) if masteries else 0.50
    avg_theta = (sum(m.irt_ability for m in masteries) / max(len(masteries), 1)) if masteries else 0.0

    target_concept = None
    if concept_id:
        target_concept = db.query(Concept).filter(Concept.concept_id == concept_id).first()

    concept_name = target_concept.name if target_concept else "Current Core Module"

    # Evaluate gap from DAG
    broken_prereqs = []
    if concept_id:
        from backend.app.knowledge_graph.prerequisites import PrerequisiteEngine
        pe = PrerequisiteEngine(db)
        status = pe.check_prerequisites_status(student_id, concept_id)
        broken_prereqs = status.get("missing_prerequisites", [])

    coverup_steps = [
        f"Review 2-minute visual breakdown of {concept_name}",
        f"Solve 2 guided warm-up questions to secure foundational mastery"
    ]
    if broken_prereqs:
        coverup_steps.insert(0, f"Prerequisite Bridge: Quick revision of {broken_prereqs[0]}")

    # Generate sharp mentor advice using Cloud / Local LLM
    from backend.app.ai.cloud_llm import CloudLLMHub
    hub = CloudLLMHub()
    prompt = (
        f"Act as a master tutor for an Indian {exam} student. "
        f"The student is on the {page_context} page studying '{concept_name}'. "
        f"Their overall mastery is {round(avg_m * 100, 1)}%. "
        f"Prerequisite gaps flagged: {', '.join(broken_prereqs) if broken_prereqs else 'None'}. "
        "Give a 2-sentence sharp, highly motivating, and actionable tutor briefing explaining their exact immediate focus."
    )
    cloud_res = await hub.generate_best(prompt)
    mentor_quote = cloud_res.get("text") if cloud_res.get("text") else (
        f"You're in the zone for {concept_name}. Focus on setting up coordinate axes clearly before diving into algebra!"
    )

    return {
        "page_context": page_context,
        "concept_name": concept_name,
        "performance": {
            "overall_mastery_pct": round(avg_m * 100, 1),
            "latent_ability_theta": round(avg_theta, 2),
            "readiness_tier": "READY_FOR_DRILL" if avg_m >= 0.50 else "NEEDS_FOUNDATION_BRIDGE"
        },
        "gap_assessment": {
            "symptom": f"Friction in {concept_name}",
            "prerequisite_gaps": broken_prereqs,
            "root_severity": "MODERATE" if broken_prereqs else "LOW"
        },
        "coverup_strategy": coverup_steps,
        "mentor_quote": mentor_quote,
        "engine_source": cloud_res.get("source", "LOCAL_LLM")
    }


@router.get("/diagnostics/history/{student_id}")
async def get_lifetime_diagnostics(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns full lifetime diagnostics, historical scores, error distributions,
    and recurring distractor traps across all assessments taken by the student.
    """
    data = OmniContextHarvester.harvest_lifetime_diagnostics(student_id, db)
    return data


@router.get("/smartboard/topic/{concept_id}")
async def get_smartboard_topic(
    concept_id: str,
    db: Session = Depends(get_db)
):
    """
    Fetches full Smart Board topic details:
    - Concept metadata, difficulty, estimated time
    - Upstream & downstream prerequisites
    - FineWeb-Edu textbook excerpt, summary, and LaTeX formula box
    - Sample practice questions for live derivation/drilling
    """
    concept = db.query(Concept).filter(Concept.concept_id == concept_id).first()
    if not concept:
        # Fallback 1: match by substring or alias (e.g. phy_shm_01 -> shm)
        clean_key = concept_id.lower().replace("_01", "").replace("_02", "").replace("_basic", "").strip()
        concept = db.query(Concept).filter(
            (Concept.concept_id.ilike(f"%{clean_key}%")) | 
            (Concept.name.ilike(f"%{clean_key}%"))
        ).first()
    if not concept and "shm" in concept_id.lower():
        concept = db.query(Concept).filter(Concept.concept_id.ilike("%shm%")).first()
    if not concept:
        concept = db.query(Concept).first()
    if not concept:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")

    resolved_cid = concept.concept_id

    from backend.app.models.schema import Prerequisite
    upstream_prereqs = (
        db.query(Prerequisite, Concept)
        .join(Concept, Prerequisite.from_concept_id == Concept.concept_id)
        .filter(Prerequisite.to_concept_id == resolved_cid)
        .all()
    )
    upstream_list = [
        {"concept_id": c.concept_id, "name": c.name, "strength": p.strength, "relationship": p.relationship_type}
        for p, c in upstream_prereqs
    ]

    downstream_prereqs = (
        db.query(Prerequisite, Concept)
        .join(Concept, Prerequisite.to_concept_id == Concept.concept_id)
        .filter(Prerequisite.from_concept_id == resolved_cid)
        .all()
    )
    downstream_list = [
        {"concept_id": c.concept_id, "name": c.name, "strength": p.strength}
        for p, c in downstream_prereqs
    ]

    topic_name = concept.topic.name if concept.topic else None
    chapter_name = concept.topic.chapter.name if (concept.topic and concept.topic.chapter) else None
    subject_name = (
        concept.topic.chapter.subject.name
        if (concept.topic and concept.topic.chapter and concept.topic.chapter.subject)
        else None
    )

    from backend.app.knowledge_graph.fineweb_vault import FINEWEB_READINGS
    matched_reading = None
    cname_lower = concept.name.lower()
    for r in FINEWEB_READINGS:
        title_lower = (r.get("title") or "").lower()
        chap_lower = (r.get("chapter") or "").lower()
        if cname_lower in title_lower or cname_lower in chap_lower:
            matched_reading = r
            break
    if not matched_reading and FINEWEB_READINGS:
        for r in FINEWEB_READINGS:
            if subject_name and subject_name.lower() in (r.get("subject") or "").lower():
                matched_reading = r
                break
        if not matched_reading:
            matched_reading = FINEWEB_READINGS[0]

    sample_qs = (
        db.query(Question)
        .filter(Question.concept_id == resolved_cid)
        .limit(3)
        .all()
    )
    questions_list = []
    for q in sample_qs:
        questions_list.append({
            "question_id": q.question_id,
            "content": q.content,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "skill": q.skill
        })

    return {
        "concept_id": concept.concept_id,
        "name": concept.name,
        "description": concept.description,
        "difficulty_weight": concept.difficulty_weight,
        "exam_relevance": concept.exam_relevance,
        "estimated_minutes": concept.estimated_minutes,
        "topic_name": topic_name,
        "chapter_name": chapter_name,
        "subject_name": subject_name,
        "upstream_prerequisites": upstream_list,
        "downstream_unlocked": downstream_list,
        "fineweb_reading": {
            "title": matched_reading.get("title") if matched_reading else concept.name,
            "chapter": matched_reading.get("chapter") if matched_reading else chapter_name,
            "subject": matched_reading.get("subject") if matched_reading else subject_name,
            "summary": matched_reading.get("summary") if matched_reading else "Core concept foundational principles.",
            "formula_box": matched_reading.get("formula_box", {}) if matched_reading else {},
            "key_takeaways": matched_reading.get("key_takeaways", []) if matched_reading else []
        } if matched_reading else None,
        "sample_questions": questions_list
    }


@router.get("/smartboard/mistakes/{student_id}")
async def get_smartboard_mistakes(
    student_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Returns student's complete historical failed questions across all tests
    with question details, options, student choice vs correct answer,
    distractor notes, and mathematical explanations for the Smart Board inspector.
    """
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.student_id == student_id, AssessmentAttempt.is_completed == True)
        .all()
    )
    if not attempts:
        return {"total_mistakes": 0, "mistakes": []}

    attempt_map = {a.attempt_id: a for a in attempts}
    attempt_ids = list(attempt_map.keys())

    items = (
        db.query(StudentAttemptItem, Question)
        .join(Question, StudentAttemptItem.question_id == Question.question_id)
        .filter(StudentAttemptItem.attempt_id.in_(attempt_ids), StudentAttemptItem.is_correct == False)
        .order_by(StudentAttemptItem.timestamp.desc())
        .limit(limit)
        .all()
    )

    mistakes_list = []
    for item, q in items:
        att = attempt_map.get(item.attempt_id)
        distractor_note = None
        if q.distractor_explanations and item.student_answer:
            distractor_note = q.distractor_explanations.get(item.student_answer)

        mistakes_list.append({
            "attempt_id": item.attempt_id,
            "test_title": (att.assessment.title if att and att.assessment else "Practice Assessment"),
            "date": item.timestamp.strftime("%b %d, %Y %H:%M") if item.timestamp else "Recent",
            "question_id": q.question_id,
            "subject": q.subject,
            "chapter": q.chapter,
            "concept_id": q.concept_id,
            "concept_name": q.concept.name if q.concept else q.concept_id,
            "content": q.content,
            "options": q.options,
            "student_answer": item.student_answer,
            "correct_answer": q.correct_answer,
            "error_type": item.error_type or "CONCEPTUAL_ERROR",
            "distractor_note": distractor_note,
            "explanation": q.explanation,
            "time_taken_seconds": item.time_taken_seconds,
            "difficulty": q.difficulty
        })

    return {
        "student_id": student_id,
        "total_mistakes": len(mistakes_list),
        "mistakes": mistakes_list
    }


