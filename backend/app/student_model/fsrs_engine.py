"""
Modern FSRS-5 Spaced Repetition Engine
======================================
Platform Upgrade: Mathematical implementation of the Free Spaced Repetition Scheduler (FSRS-5).
Provides:
  - Power-Law Retrievability Forgetting Curve R(t, S)
  - Stability Update on Recall (Y = 1)
  - Stability Update on Lapse (Y = 0)
  - Continuous Difficulty Calibration D in [1.0, 10.0]
  - Optimal Review Trigger (R < 0.90) and Interval Computation
"""
from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple


class FSRSEngine:
    """
    FSRS-5 (Free Spaced Repetition Scheduler v5) Engine.
    Deterministic, offline, psychometrically calibrated.
    """

    DECAY: float = -0.5
    FACTOR: float = 19.0 / 81.0  # approximately 0.2345679
    TARGET_RETRIEVABILITY: float = 0.90

    DEFAULT_STABILITY: float = 1.0
    DEFAULT_DIFFICULTY: float = 5.0
    MIN_STABILITY: float = 0.40
    MIN_DIFFICULTY: float = 1.0
    MAX_DIFFICULTY: float = 10.0

    @classmethod
    def retrievability(cls, elapsed_days: float, stability: float) -> float:
        """
        Computes Power-Law Retrievability Forgetting Curve:
            R(t, S) = (1 + FACTOR * (t / S))^DECAY
        Where:
            t = elapsed time in days (t >= 0)
            S = memory stability in days (S > 0)
            DECAY = -0.5
            FACTOR = 19 / 81
        """
        t = max(float(elapsed_days), 0.0)
        s = max(float(stability), 0.01)

        base = 1.0 + cls.FACTOR * (t / s)
        # base >= 1.0, so base^(-0.5) is strictly in (0, 1]
        r = math.pow(base, cls.DECAY)
        return min(max(r, 0.0), 1.0)

    @classmethod
    def update_stability_recall(
        cls,
        stability: float,
        difficulty: float,
        retrievability: float,
    ) -> float:
        """
        Stability update after successful recall (Y = 1):
            S_new = S * (1 + (11 - D) * 0.15 * S^(-0.2) * (exp(1 - R) - 1))
        """
        s = max(float(stability), 0.01)
        d = min(max(float(difficulty), cls.MIN_DIFFICULTY), cls.MAX_DIFFICULTY)
        r = min(max(float(retrievability), 0.0), 1.0)

        boost_factor = (11.0 - d) * 0.15 * math.pow(s, -0.2) * (math.exp(1.0 - r) - 1.0)
        s_new = s * (1.0 + max(boost_factor, 0.0))
        return max(s_new, cls.MIN_STABILITY)

    @classmethod
    def update_stability_lapse(
        cls,
        stability: float,
        difficulty: float,
        retrievability: float,
    ) -> float:
        """
        Stability update after memory lapse / incorrect response (Y = 0):
            S_new = max(0.40, min(S * 0.50, 0.25 * D^(-0.3) * S^0.2 * exp(1 - R)))
        """
        s = max(float(stability), 0.01)
        d = min(max(float(difficulty), cls.MIN_DIFFICULTY), cls.MAX_DIFFICULTY)
        r = min(max(float(retrievability), 0.0), 1.0)

        lapse_calc = 0.25 * math.pow(d, -0.3) * math.pow(s, 0.2) * math.exp(1.0 - r)
        s_candidate = min(s * 0.50, lapse_calc)
        s_new = max(cls.MIN_STABILITY, s_candidate)
        return s_new

    @classmethod
    def update_difficulty(cls, difficulty: float, is_correct: bool) -> float:
        """
        Difficulty updating rule:
            - Correct:   D_new = max(1.0, min(10.0, D - 0.2))
            - Incorrect: D_new = max(1.0, min(10.0, D + 0.8))
        """
        d = float(difficulty)
        if is_correct:
            d_new = d - 0.2
        else:
            d_new = d + 0.8

        return min(max(d_new, cls.MIN_DIFFICULTY), cls.MAX_DIFFICULTY)

    @classmethod
    def calculate_interval(
        cls,
        stability: float,
        target_retrievability: float = TARGET_RETRIEVABILITY,
    ) -> float:
        """
        Calculates optimal review interval (in days) to achieve target retrievability.
        Solving: (1 + FACTOR * (I / S))^DECAY = r_target
        Yields:
            I = (S / FACTOR) * (r_target^(1/DECAY) - 1)
        For r_target = 0.90 and DECAY = -0.5:
            r^(-2) - 1 = (0.90)^(-2) - 1 = (100/81) - 1 = 19/81 = FACTOR.
            Thus I = (S / FACTOR) * FACTOR = S.
        """
        s = max(float(stability), cls.MIN_STABILITY)
        r = min(max(float(target_retrievability), 0.01), 0.99)

        # r^(1 / -0.5) = r^(-2)
        r_term = math.pow(r, 1.0 / cls.DECAY) - 1.0
        interval = (s / cls.FACTOR) * max(r_term, 0.0)
        return max(interval, 0.1)

    @classmethod
    def is_overdue(
        cls,
        elapsed_days: float,
        stability: float,
        threshold: float = TARGET_RETRIEVABILITY,
    ) -> bool:
        """
        Checks if concept memory has decayed below target retention (R < 0.90).
        """
        r = cls.retrievability(elapsed_days, stability)
        return r < threshold

    @classmethod
    def step(
        cls,
        stability: float,
        difficulty: float,
        elapsed_days: float,
        is_correct: bool,
    ) -> Dict[str, float]:
        """
        Full state transition for a concept review step.
        Returns:
            {
                "stability": S_new,
                "difficulty": D_new,
                "retrievability": R_current,
                "next_interval_days": interval
            }
        """
        current_r = cls.retrievability(elapsed_days, stability)
        d_new = cls.update_difficulty(difficulty, is_correct)

        if is_correct:
            s_new = cls.update_stability_recall(stability, difficulty, current_r)
        else:
            s_new = cls.update_stability_lapse(stability, difficulty, current_r)

        next_interval = cls.calculate_interval(s_new, cls.TARGET_RETRIEVABILITY)

        return {
            "stability": round(s_new, 4),
            "difficulty": round(d_new, 4),
            "retrievability": round(current_r, 4),
            "next_interval_days": round(next_interval, 2),
        }

    @classmethod
    def find_decay_remediation_candidates(
        cls,
        masteries: Any,
        threshold: float = 0.70
    ) -> Optional[Dict[str, Any]]:
        """
        Scans tracked concepts to identify the single most critical memory-decay candidate
        for proactive Socratic interleaving during active troubleshooting sessions.
        """
        candidates = []
        for m in masteries:
            # Safely read retrievability and mastery
            retrievability = getattr(m, "fsrs_retrievability", 1.0)
            if retrievability is None:
                retrievability = 1.0
            raw_mastery = getattr(m, "mastery", 0.0) or 0.0

            # Only select concepts that were once partially learned but are decaying
            if retrievability < threshold and raw_mastery >= 0.30:
                cid = getattr(m, "concept_id", "concept")
                candidates.append({
                    "concept_id": cid,
                    "retrievability": round(float(retrievability), 3),
                    "mastery": round(float(raw_mastery), 3),
                    "forgetting_risk": round(1.0 - float(retrievability), 3)
                })

        if not candidates:
            return None

        # Sort by lowest retrievability (highest urgency)
        candidates.sort(key=lambda x: x["retrievability"])
        top = candidates[0]
        return {
            "candidate_concept_id": top["concept_id"],
            "retrievability": top["retrievability"],
            "urgency": "HIGH" if top["retrievability"] < 0.50 else "MODERATE",
            "interleaving_instruction": (
                f"Proactive FSRS Memory Rescue: Concept '{top['concept_id']}' memory retrievability is at {round(top['retrievability']*100)}%. "
                f"Before concluding this session, interleave a 10-second rapid micro-check question on this concept to reset the forgetting curve."
            )
        }

