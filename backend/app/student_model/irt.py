"""
Item Response Theory (IRT) & Multi-Dimensional IRT (MIRT) Engine
================================================================
Platform Upgrade Phase 5:
  - Psychometrically grounded 2PL/3PL IRT with Rule 1 floating-point protection
  - Multi-Dimensional IRT (4D MIRT) Vector Estimation:
      vec(theta) = [theta_calc, theta_concept, theta_spatial, theta_pacing]
  - Dynamic item dimension discrimination vector a = [a_calc, a_concept, a_spatial, a_pacing]
  - Multi-dimensional Fisher information and Newton-Raphson vector updates
  - 100% backward compatible with scalar theta estimation.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import numpy as np

from backend.app.student_model.numerical_guards import (
    safe_clamp_prob,
    safe_div,
    safe_exp,
    safe_log,
    MIN_PROBABILITY,
    MAX_PROBABILITY,
    EPSILON
)


class ItemResponseTheory:
    """
    Standard Unidimensional Item Response Theory (IRT) 2PL/3PL module.
    Estimates student latent ability (theta) and question information gain with numerical protection.
    """
    @staticmethod
    def difficulty_to_b_parameter(difficulty_01: float) -> float:
        """Converts normalized [0, 1] difficulty to IRT b parameter in [-2.5, +2.5]."""
        clamped = safe_clamp_prob(difficulty_01, 0.05, 0.95)
        # Logit scaling
        ratio = safe_div(clamped, 1.0 - clamped)
        return round(safe_log(ratio) * 1.5, 3)

    @staticmethod
    def probability_correct(
        theta: float,
        difficulty_b: float,
        discrimination_a: float = 1.0,
        guessing_c: float = 0.25
    ) -> float:
        """
        3PL IRT probability curve: P(theta) = c + (1-c) / (1 + exp(-a*(theta - b)))
        """
        a = max(float(discrimination_a), 0.01)
        c = safe_clamp_prob(guessing_c, 0.0, 0.99)
        z = a * (float(theta) - float(difficulty_b))
        # Numerical stability clamp
        z = max(min(z, 20.0), -20.0)
        p_logistic = 1.0 / (1.0 + safe_exp(-z))
        p_total = c + (1.0 - c) * p_logistic
        return safe_clamp_prob(p_total)

    @staticmethod
    def item_information(
        theta: float,
        difficulty_b: float,
        discrimination_a: float = 1.0,
        guessing_c: float = 0.25
    ) -> float:
        """
        Fisher Information of a question at ability level theta.
        Higher information indicates higher diagnostic power.
        """
        a = max(float(discrimination_a), 0.01)
        c = safe_clamp_prob(guessing_c, 0.0, 0.99)
        P = ItemResponseTheory.probability_correct(theta, difficulty_b, a, c)
        z = a * (float(theta) - float(difficulty_b))
        z = max(min(z, 20.0), -20.0)
        p_logistic = 1.0 / (1.0 + safe_exp(-z))
        q_logistic = 1.0 - p_logistic

        numerator = (a ** 2) * ((1.0 - c) ** 2) * (p_logistic ** 2) * (q_logistic ** 2)
        denominator = max(P * (1.0 - P), EPSILON)
        return safe_div(numerator, denominator)

    @classmethod
    def estimate_student_ability(
        cls,
        responses: List[Tuple[bool, float, float]],  # List of (is_correct, difficulty_01, discrimination)
        initial_theta: float = 0.0,
        max_iterations: int = 25
    ) -> float:
        """
        Estimates latent student ability theta using Newton-Raphson maximum likelihood.
        """
        if not responses:
            return initial_theta

        theta = float(initial_theta)
        for _ in range(max_iterations):
            score_sum = 0.0
            info_sum = 0.0

            for is_correct, diff_01, disc in responses:
                b = cls.difficulty_to_b_parameter(diff_01)
                a = disc if disc > 0 else 1.0
                P = cls.probability_correct(theta, b, a, guessing_c=0.20)
                u = 1.0 if is_correct else 0.0

                score_sum += a * (u - P)
                info_sum += (a ** 2) * P * (1.0 - P)

            if info_sum <= 1e-5:
                break

            delta = safe_div(score_sum, info_sum)
            # Step size dampening for stability
            delta = max(min(delta, 0.75), -0.75)
            theta += delta

            if abs(delta) < 0.01:
                break

        return round(min(max(theta, -3.0), 3.0), 3)


class MultiDimensionalIRT:
    """
    4-Dimensional Multi-Dimensional Item Response Theory (MIRT) Engine.
    Vectorized Latent Ability:
        vec(theta) = [theta_calc, theta_concept, theta_spatial, theta_pacing]
    """

    DIMENSIONS: Tuple[str, str, str, str] = ("calc", "concept", "spatial", "pacing")
    DIM_COUNT: int = 4
    MIN_THETA: float = -3.0
    MAX_THETA: float = 3.0

    @classmethod
    def extract_discrimination_vector(
        cls,
        skill: Optional[str] = "conceptual",
        content: Optional[str] = "",
        time_taken_seconds: Optional[int] = 60,
        estimated_time: Optional[int] = 60,
        base_discrimination: float = 1.0,
    ) -> np.ndarray:
        """
        Derives a 4D item discrimination vector a = [a_calc, a_concept, a_spatial, a_pacing]
        dynamically based on item skill taxonomy, textual tokens, and pacing ratio.
        """
        base = max(float(base_discrimination), 0.2)
        skill_str = (skill or "").lower()
        content_str = (content or "").lower()

        # Dimension 1: Calculation / Numerical
        is_calc = (
            "numerical" in skill_str or
            "multi_step" in skill_str or
            any(w in content_str for w in ["calculate", "magnitude", "ratio", "velocity", "moles", "integral", "matrix", "equilibrium constant"])
        )
        a_calc = base * (1.4 if is_calc else 0.4)

        # Dimension 2: Conceptual / Deductive
        is_concept = (
            "conceptual" in skill_str or
            "reasoning" in skill_str or
            "factual" in skill_str or
            any(w in content_str for w in ["principle", "theorem", "definition", "explain", "because", "identify"])
        )
        a_concept = base * (1.3 if is_concept else 0.5)

        # Dimension 3: Spatial / Visual / Structural
        is_spatial = (
            any(w in content_str for w in ["geometry", "angle", "diagram", "figure", "projection", "orbital", "stereochemistry", "circuit", "optics", "ray", "prism"]) or
            "spatial" in skill_str
        )
        a_spatial = base * (1.5 if is_spatial else 0.3)

        # Dimension 4: Pacing / Latency
        est = max(float(estimated_time or 60), 10.0)
        taken = max(float(time_taken_seconds or 60), 1.0)
        pacing_ratio = taken / est
        # Higher discrimination on pacing when item tests rapid response
        a_pacing = base * (1.2 if pacing_ratio < 0.7 or pacing_ratio > 1.4 else 0.6)

        vec = np.array([a_calc, a_concept, a_spatial, a_pacing], dtype=np.float64)
        # Normalize so Euclidean magnitude is calibrated around base
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = (vec / norm) * (base * 2.0)
        return vec

    @classmethod
    def probability_correct_multidimensional(
        cls,
        theta_vec: Union[Sequence[float], np.ndarray],
        a_vec: Union[Sequence[float], np.ndarray],
        difficulty_b: float,
        guessing_c: float = 0.20,
    ) -> float:
        """
        Multidimensional Compensatory IRT Model:
            P(vec(theta)) = c + (1 - c) / (1 + exp(-(sum_k(a_k * theta_k) - b)))
        """
        theta_arr = np.asarray(theta_vec, dtype=np.float64)
        a_arr = np.asarray(a_vec, dtype=np.float64)
        c = safe_clamp_prob(guessing_c, 0.0, 0.99)

        # Dot product a . theta - b
        z = float(np.dot(a_arr, theta_arr) - float(difficulty_b))
        z = max(min(z, 20.0), -20.0)

        p_logistic = 1.0 / (1.0 + safe_exp(-z))
        p_total = c + (1.0 - c) * p_logistic
        return safe_clamp_prob(p_total)

    @classmethod
    def update_ability_vector(
        cls,
        current_theta_vec: Union[Sequence[float], np.ndarray],
        item_observations: Sequence[Dict[str, Any]],
        learning_rate: float = 0.30,
    ) -> np.ndarray:
        """
        Updates 4D latent ability vector from a sequence of item attempt records.
        Each item observation dict contains:
            - is_correct: bool
            - difficulty_01: float
            - skill: str
            - content: str
            - time_taken_seconds: int
            - estimated_time: int
            - discrimination: float
        """
        theta = np.array(current_theta_vec, dtype=np.float64)
        if theta.shape != (cls.DIM_COUNT,):
            theta = np.zeros(cls.DIM_COUNT, dtype=np.float64)

        if not item_observations:
            return theta

        for obs in item_observations:
            is_correct = bool(obs.get("is_correct", False))
            diff_01 = float(obs.get("difficulty_01", obs.get("difficulty", 0.5)))
            b = ItemResponseTheory.difficulty_to_b_parameter(diff_01)
            disc = float(obs.get("discrimination", 1.0))

            a_vec = cls.extract_discrimination_vector(
                skill=obs.get("skill", "conceptual"),
                content=obs.get("content", ""),
                time_taken_seconds=obs.get("time_taken_seconds", 60),
                estimated_time=obs.get("estimated_time", 60),
                base_discrimination=disc
            )

            P = cls.probability_correct_multidimensional(theta, a_vec, b, guessing_c=0.20)
            u = 1.0 if is_correct else 0.0
            error = u - P

            # Multi-dimensional gradient update
            info_denom = max(float(np.sum(a_vec ** 2) * P * (1.0 - P)), EPSILON)
            step = (a_vec * error) / info_denom
            step = np.clip(step, -0.60, 0.60)

            # Extra pacing dimension adjustment based on speed
            taken = float(obs.get("time_taken_seconds", 60))
            est = float(obs.get("estimated_time", 60))
            if is_correct and taken <= est:
                step[3] += 0.05
            elif not is_correct and taken > est * 1.5:
                step[3] -= 0.05

            theta = theta + learning_rate * step
            theta = np.clip(theta, cls.MIN_THETA, cls.MAX_THETA)

        return np.round(theta, 3)

    @classmethod
    def composite_scalar_ability(cls, theta_vec: Union[Sequence[float], np.ndarray]) -> float:
        """
        Projects 4D MIRT ability vector back to a unified scalar theta in [-3.0, +3.0]
        for backward compatibility with unidimensional consumers.
        Weights: Calc (0.35), Concept (0.35), Spatial (0.15), Pacing (0.15)
        """
        arr = np.asarray(theta_vec, dtype=np.float64)
        if arr.size != cls.DIM_COUNT:
            return 0.0
        weights = np.array([0.35, 0.35, 0.15, 0.15], dtype=np.float64)
        scalar = float(np.dot(arr, weights))
        return round(min(max(scalar, cls.MIN_THETA), cls.MAX_THETA), 3)

    @classmethod
    def get_cognitive_control_vector(
        cls,
        theta_val: Union[float, Sequence[float], np.ndarray]
    ) -> Dict[str, Any]:
        """
        Translates raw IRT/MIRT abilities into explicit control signals for the LLM mentor:
          - Calculation strength vs vulnerability
          - Conceptual understanding vs arithmetic slips
          - Spatial/geometric intuition requirements
          - Pacing / cognitive load management
        """
        if isinstance(theta_val, (list, tuple, np.ndarray)) and len(theta_val) == cls.DIM_COUNT:
            vec = [float(v) for v in theta_val]
            scalar = cls.composite_scalar_ability(vec)
        else:
            s = float(theta_val) if theta_val is not None else 0.0
            vec = [s, s, s, s]
            scalar = s

        dim_names = ["calculation", "conceptual", "spatial", "pacing"]
        dim_dict = dict(zip(dim_names, [round(v, 2) for v in vec]))

        min_dim = min(dim_dict, key=dim_dict.get)
        max_dim = max(dim_dict, key=dim_dict.get)

        if dim_dict["calculation"] < -0.4 and dim_dict["conceptual"] >= 0.0:
            pedagogical_focus = "ALGEBRAIC_STEPS_FOCUS"
            mentor_directive = "Student grasps underlying physical concept but slips on algebraic/calculation steps. Emphasize line-by-line algebraic tracking and unit cancellation."
        elif dim_dict["conceptual"] < -0.4:
            pedagogical_focus = "INTUITIVE_CONCEPT_FOCUS"
            mentor_directive = "Student exhibits conceptual gaps. Provide physical intuition, Feynman-style analogies, and first-principles definitions before formulas."
        elif dim_dict["spatial"] < -0.4:
            pedagogical_focus = "SPATIAL_GEOMETRY_FOCUS"
            mentor_directive = "Student struggles with spatial or vector orientation. Describe geometry, coordinate axes, and free-body directions explicitly."
        elif dim_dict["pacing"] < -0.4:
            pedagogical_focus = "PACING_AND_DECISION_FOCUS"
            mentor_directive = "Student is overthinking or rushing. Guide them on time allocation, option elimination, and negative marking prevention."
        else:
            pedagogical_focus = "BALANCED_RIGOR"
            mentor_directive = "Maintain high standard academic rigor with clean derivation and competitive exam trap warnings."

        return {
            "scalar_theta": scalar,
            "dimensions": dim_dict,
            "primary_vulnerability": min_dim,
            "dominant_strength": max_dim,
            "pedagogical_focus": pedagogical_focus,
            "mentor_directive": mentor_directive
        }


# Alias for flexible case-insensitive import
MultidimensionalIRT = MultiDimensionalIRT


