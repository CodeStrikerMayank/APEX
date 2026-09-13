"""
Multi-Agent Socratic Runtime Isolation Architecture
===================================================
Platform Upgrade Phase 5:
  - Agent 1 (Diagnostician): Pure read-only consumer of StudentErrorLog, latency telemetry, and mistake patterns.
  - Agent 2 (Socratic Prober): Generates scaffolding prompts without outputting correct option letters (A, B, C, D).
  - Agent 3 (Psychologist): Monitors session duration; if active time > 45 minutes without a break, injects an encouragement and micro-break prompt.
  - Zero-hallucination, psychometrically isolated runtime.
"""
from __future__ import annotations

import re
import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.orm import Session

from backend.app.models.schema import Student, StudentErrorLog, StudentAttemptItem, AssessmentAttempt, Question, Concept


class DiagnosticianAgent:
    """
    Agent 1 (Diagnostician):
    Pure read-only consumer of StudentErrorLog and response latency telemetry.
    Synthesizes cognitive failure modes and diagnostic profile.
    """

    @classmethod
    def diagnose_student(
        cls,
        student_id: str,
        db: Session,
        limit_errors: int = 10
    ) -> Dict[str, Any]:
        """
        Pure read-only query of historical error logs and latency telemetry.
        """
        errors = (
            db.query(StudentErrorLog)
            .filter(StudentErrorLog.student_id == student_id)
            .order_by(StudentErrorLog.timestamp.desc())
            .limit(limit_errors)
            .all()
        )

        error_taxonomy_counts: Dict[str, int] = {}
        for err in errors:
            etype = err.error_type or "UNSPECIFIED"
            error_taxonomy_counts[etype] = error_taxonomy_counts.get(etype, 0) + 1

        # Fetch recent attempt latency telemetry
        recent_items = (
            db.query(StudentAttemptItem)
            .filter(StudentAttemptItem.attempt.has(student_id=student_id))
            .order_by(StudentAttemptItem.timestamp.desc())
            .limit(15)
            .all()
        )

        total_time = sum(item.time_taken_seconds for item in recent_items)
        avg_time = (total_time / len(recent_items)) if recent_items else 60.0
        rushed_count = sum(1 for item in recent_items if item.time_taken_seconds < 25 and not item.is_correct)
        overtime_count = sum(1 for item in recent_items if item.time_taken_seconds > 120 and not item.is_correct)

        primary_vulnerability = "CONCEPTUAL_APPLICATION"
        if error_taxonomy_counts:
            primary_vulnerability = max(error_taxonomy_counts, key=error_taxonomy_counts.get)

        speed_profile = "BALANCED"
        if rushed_count >= 3:
            speed_profile = "IMPULSIVE_RUSHING"
        elif overtime_count >= 3:
            speed_profile = "OVERTHINKING_BOTTLENECK"

        return {
            "error_count": len(errors),
            "taxonomy_breakdown": error_taxonomy_counts,
            "primary_vulnerability": primary_vulnerability,
            "average_latency_seconds": round(avg_time, 1),
            "speed_profile": speed_profile,
            "recent_items_evaluated": len(recent_items)
        }


class SocraticProberAgent:
    """
    Agent 2 (Socratic Prober):
    Generates conceptual scaffolding prompts and hints.
    STRICT INVARIANT: Never outputs raw correct option letters (A, B, C, D) or direct answers.
    """

    ANSWER_LETTER_REGEX = re.compile(
        r'\b(?:option|answer|choice|correct\s+is|key\s+is|select)\s+[:=]?\s*([A-D])\b',
        re.IGNORECASE
    )
    STANDALONE_LETTER_REGEX = re.compile(
        r'(?:^|\s)\(([A-D])\)(?:\s|$)|(?:\b[A-D]\s+is\s+the\s+correct\b)',
        re.IGNORECASE
    )

    @classmethod
    def sanitize_scaffolding(cls, text: str) -> str:
        """
        Enforces strict leakage prevention: strips or masks any raw correct option letters (A, B, C, D)
        or direct option revelations to protect Socratic discovery.
        """
        # 1. Scrub "The [correct] answer is [Option] X"
        sanitized = re.sub(
            r'(?:The\s+)?(?:correct\s+)?answer\s+is\s+(?:option\s+)?([A-D])\.?',
            "The key relationship is governed by the underlying principle:",
            text,
            flags=re.IGNORECASE
        )
        # 2. Scrub "Select X" or "Choice X" or "Option X"
        sanitized = re.sub(
            r'\b(?:option|choice|select)\s+([A-D])\b',
            "the intended option",
            sanitized,
            flags=re.IGNORECASE
        )
        # 3. Scrub standalone "(X) is correct" or "X is [the] correct/right"
        sanitized = re.sub(
            r'(?:\(([A-D])\)|\b([A-D]))\s+is\s+(?:the\s+)?(?:correct|right)\b',
            "This governing deduction is sound",
            sanitized,
            flags=re.IGNORECASE
        )
        # 4. Fallback scrub for any residual "Option X"
        sanitized = re.sub(r'\bOption\s+[A-D]\b', "the relevant option", sanitized, flags=re.IGNORECASE)
        return sanitized

    @classmethod
    def generate_scaffolding_probe(
        cls,
        concept_name: str,
        student_mistake: Optional[str] = None,
        error_type: Optional[str] = None,
        explanation: Optional[str] = None,
    ) -> str:
        """
        Constructs a pure Socratic probing question without revealing option letters.
        """
        probe_lines = []

        if error_type == "CALCULATION_ERROR":
            probe_lines.append(f"🔍 **Socratic Diagnostic Probe on {concept_name}**:")
            probe_lines.append("Look closely at the dimensional units and scaling factor in your intermediate step.")
            probe_lines.append("• *Probing Question*: What happens to the final value if the boundary condition or constant is inverted?")
            probe_lines.append("• Re-verify your arithmetic before substituting into the primary formula.")

        elif error_type == "FORMULA_SELECTION_ERROR":
            probe_lines.append(f"📐 **Socratic Diagnostic Probe on {concept_name}**:")
            probe_lines.append("Notice the physical constraints of this scenario:")
            probe_lines.append("• *Probing Question*: Is this system operating under dynamic first-order kinetics, or in equilibrium steady-state?")
            probe_lines.append("• Which conservation theorem applies when non-conservative dissipative forces are absent?")

        else:
            probe_lines.append(f"🧠 **Socratic Diagnostic Probe on {concept_name}**:")
            probe_lines.append("Let's break down the underlying mechanism step-by-step:")
            probe_lines.append("• *Probing Question*: What is the governing relationship between the input state and the resulting observation?")
            probe_lines.append("• Where does the standard textbook assumption differ from this specific scenario?")

        if explanation:
            # Provide gentle conceptual hint without letter leakage
            clean_hint = cls.sanitize_scaffolding(explanation[:240])
            probe_lines.append(f"\n💡 *Conceptual Scaffolding*: {clean_hint}...")

        raw_output = "\n".join(probe_lines)
        return cls.sanitize_scaffolding(raw_output)


class PsychologistAgent:
    """
    Agent 3 (Psychologist):
    Monitors session active duration. If active session time > 45 minutes (2700s)
    without a break, injects an empathetic encouragement and micro-break reminder.
    """

    TIREDNESS_THRESHOLD_MINUTES: float = 45.0
    TIREDNESS_THRESHOLD_SECONDS: float = 2700.0

    @classmethod
    def check_and_inject_break_prompt(
        cls,
        active_duration_minutes: float,
        student_name: str = "Aspirant"
    ) -> Optional[str]:
        """
        Evaluates active session duration. Returns an empathetic break prompt if > 45 min.
        """
        if active_duration_minutes < cls.TIREDNESS_THRESHOLD_MINUTES:
            return None

        mins = int(active_duration_minutes)
        return (
            f"\n\n🧘 **Mental Energy & Focus Protocol ({student_name})**:\n"
            f"You have been engaged in continuous high-intensity problem solving for **{mins} minutes**! "
            f"Neuroscience shows that working memory efficiency declines significantly past 45 minutes of sustained focus.\n"
            f"• **Recommendation**: Take a 5-minute micro-break (stand up, drink a glass of water, rest your eyes off the screen).\n"
            f"• Your brain consolidates conceptual neural pathways during brief downtime. Step back for 5 minutes, then return with 100% clarity!"
        )


class PedagogicalPolicyRouter:
    """
    Multi-Tier Pedagogical Routing Pipeline:
    Automatically switches between Diagnostic, Scaffolding, and Challenge modes
    based on live student entropy scores, error frequencies, and mastery indices.
    """

    MODE_DIAGNOSTIC = "DIAGNOSTIC"
    MODE_SCAFFOLDING = "SCAFFOLDING"
    MODE_CHALLENGE = "CHALLENGE"

    @classmethod
    def determine_route(
        cls,
        entropy_score: float = 0.0,
        mastery: float = 50.0,
        theta: float = 0.0,
        is_thrashing: bool = False,
        has_broken_prereq: bool = False,
        recent_error_count: int = 1
    ) -> Dict[str, Any]:
        """
        Determines the optimal pedagogical route based on psychometric signals:
          - DIAGNOSTIC: High entropy (> 1.3), erratic guessing, or unclassified gap.
          - SCAFFOLDING: Thrashing detected, developing mastery (< 70%), or broken prerequisite.
          - CHALLENGE: Solid mastery (>= 75%), high ability (theta >= 0.7), and low entropy.
        """
        if entropy_score > 1.35 or (is_thrashing and recent_error_count >= 3):
            mode = cls.MODE_DIAGNOSTIC
            reason = "High cognitive entropy / thrashing trajectory indicates fundamental ambiguity in student mental model."
            directive = (
                "MODE: DIAGNOSTIC PROBING. Do NOT deliver lengthy derivations or reveal formulas. "
                "Ask a single discriminatory diagnostic question to isolate whether the confusion is dimensional, "
                "algebraic, or a misconception of boundary conditions."
            )
        elif mastery >= 75.0 and theta >= 0.70 and not is_thrashing and entropy_score <= 1.0:
            mode = cls.MODE_CHALLENGE
            reason = "Student has demonstrated solid conceptual mastery and stable latent ability theta."
            directive = (
                "MODE: COGNITIVE CHALLENGE & STRESS-TEST. Avoid basic textbook definitions. "
                "Pose an extreme boundary case, a counterfactual limit (e.g., m -> infinity or t -> 0), "
                "or an Olympiad-level multi-concept synthesis linking this concept to another chapter."
            )
        else:
            mode = cls.MODE_SCAFFOLDING
            reason = "Student is in the Zone of Proximal Development (ZPD) requiring stepped guidance."
            directive = (
                "MODE: FADED SCAFFOLDING. Break the derivation or solution into 3 sequential micro-steps. "
                "Explicitly lay out Step 1, then prompt the student with a guided hint to deduce Step 2. "
                "Never reveal final numerical answers or multiple-choice letters."
            )

        return {
            "mode": mode,
            "reason": reason,
            "system_directive": directive,
            "temperature_recommendation": 0.15 if mode != cls.MODE_CHALLENGE else 0.35
        }

    @classmethod
    def generate_pedagogical_prompt_prefix(
        cls,
        route: Dict[str, Any],
        concept_name: str,
        broken_prereq_name: Optional[str] = None
    ) -> str:
        """
        Generates mode-specific pedagogical framing for the LLM mentor.
        """
        mode = route["mode"]
        if mode == cls.MODE_DIAGNOSTIC:
            prefix = f"🔍 **Diagnostic Probe Mode — {concept_name}**\n"
            prefix += "Before jumping into calculations, let's pinpoint where the conceptual disconnect lies.\n"
            if broken_prereq_name:
                prefix += f"💡 *Prerequisite Alert*: Root foundation '{broken_prereq_name}' needs clarification.\n"
        elif mode == cls.MODE_CHALLENGE:
            prefix = f"⚡ **Advanced Master Challenge — {concept_name}**\n"
            prefix += "Your conceptual foundation is solid! Let's stress-test your mastery with an advanced boundary problem:\n"
        else:
            prefix = f"🧗 **Stepped Scaffolding — {concept_name}**\n"
            prefix += "Let's deconstruct this challenge step-by-step so you discover the solution yourself:\n"
        return prefix


class SocraticCoordinator:
    """
    Runtime Orchestrator coordinating Agent 1, Agent 2, and Agent 3
    into a unified, isolated Socratic dialogue response, augmented with PedagogicalPolicyRouter.
    """

    @classmethod
    def coordinate_response(
        cls,
        student_id: str,
        db: Session,
        concept_name: str,
        error_type: Optional[str] = None,
        explanation: Optional[str] = None,
        session_duration_minutes: float = 0.0,
        student_name: str = "Aspirant",
        cognitive_state: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Runs the multi-agent pedagogical pipeline:
          1. Diagnostician reads telemetry & error distribution
          2. PedagogicalPolicyRouter determines mode (Diagnostic vs Scaffolding vs Challenge)
          3. Socratic Prober generates guided question (zero answer-letter leakage)
          4. Psychologist monitors session duration and injects fatigue breaks
        """
        # 1. Diagnostician (Read-only)
        diagnosis = DiagnosticianAgent.diagnose_student(student_id, db)

        # Extract cognitive state if provided
        entropy = 0.0
        is_thrashing = False
        broken_prereq_name = None

        if cognitive_state:
            entropy = cognitive_state.get("entropy_score", 0.0)
            is_thrashing = cognitive_state.get("is_thrashing", False)
            subtrees = cognitive_state.get("prerequisite_subtrees")
            if subtrees and subtrees.get("root_broken_ancestor"):
                broken_prereq_name = subtrees["root_broken_ancestor"].get("name")

        # 2. Pedagogical Route Selection
        route = PedagogicalPolicyRouter.determine_route(
            entropy_score=entropy,
            mastery=50.0,
            theta=0.0,
            is_thrashing=is_thrashing,
            has_broken_prereq=broken_prereq_name is not None,
            recent_error_count=diagnosis.get("error_count", 1)
        )

        # 3. Socratic Prober (Answer letter masked)
        actual_error = error_type or diagnosis.get("primary_vulnerability")
        socratic_probe = SocraticProberAgent.generate_scaffolding_probe(
            concept_name=concept_name,
            error_type=actual_error,
            explanation=explanation
        )

        prefix = PedagogicalPolicyRouter.generate_pedagogical_prompt_prefix(
            route=route,
            concept_name=concept_name,
            broken_prereq_name=broken_prereq_name
        )

        # 4. Psychologist (Fatigue check)
        psych_break = PsychologistAgent.check_and_inject_break_prompt(
            active_duration_minutes=session_duration_minutes,
            student_name=student_name
        )

        combined_text = prefix + socratic_probe
        if psych_break:
            combined_text += psych_break

        return {
            "text": combined_text,
            "diagnosis": diagnosis,
            "pedagogical_route": route,
            "fatigue_break_triggered": psych_break is not None,
            "source": "SOCRATIC_MULTI_AGENT",
            "tier": "NEURAL_SYMBOLIC_PHASE5"
        }

