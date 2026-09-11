"""
Bayesian Knowledge Tracing (BKT) & Attention-Based Knowledge Tracing (AKT)
==========================================================================
Psychometric Core Upgrade Phase 5:
  - Standard BKT state updates with Rule 1 floating-point underflow/division protection
  - Sequence self-attention AKT extension for attention-based latent knowledge estimation
  - 100% backward compatible with historical response telemetry
"""
from typing import List, Optional, Sequence, Tuple, Union
from backend.app.student_model.numerical_guards import safe_clamp_prob, safe_div
from backend.app.student_model.akt import AttentionKnowledgeTracing


class BayesianKnowledgeTracing:
    """
    Bayesian Knowledge Tracing (BKT) augmented with Attention-Based Knowledge Tracing (AKT).
    Tracks hidden latent knowledge state transitions P(L) with numerical stability guarantees.
    """
    def __init__(
        self,
        p_init: float = 0.20,  # P(L_0) prior probability of knowing concept
        p_transit: float = 0.15,  # P(T) transition probability from unlearned to learned
        p_guess: float = 0.25,  # P(G) probability of guessing correctly
        p_slip: float = 0.10   # P(S) probability of slipping (wrong answer despite knowing)
    ):
        self.p_init = safe_clamp_prob(p_init)
        self.p_transit = safe_clamp_prob(p_transit)
        self.p_guess = safe_clamp_prob(p_guess)
        self.p_slip = safe_clamp_prob(p_slip)
        self._akt_engine: Optional[AttentionKnowledgeTracing] = None

    @property
    def akt_engine(self) -> AttentionKnowledgeTracing:
        if self._akt_engine is None:
            self._akt_engine = AttentionKnowledgeTracing(p_init=self.p_init)
        return self._akt_engine

    def update_single_step(self, current_p_known: float, is_correct: bool) -> float:
        """
        Updates knowledge probability after a single binary attempt observation.
        Bounded by strict clamps and safe denominator floors.
        """
        p_known = safe_clamp_prob(current_p_known)
        if is_correct:
            # P(L | correct) = P(L)*(1 - S) / [P(L)*(1 - S) + (1 - P(L))*G]
            numerator = p_known * (1.0 - self.p_slip)
            denominator = numerator + (1.0 - p_known) * self.p_guess
        else:
            # P(L | incorrect) = P(L)*S / [P(L)*S + (1 - P(L))*(1 - G)]
            numerator = p_known * self.p_slip
            denominator = numerator + (1.0 - p_known) * (1.0 - self.p_guess)

        p_learned_given_obs = safe_div(numerator, max(denominator, 1e-7))
        p_learned_given_obs = safe_clamp_prob(p_learned_given_obs)

        # Transition step: P(L_next) = P(L|obs) + (1 - P(L|obs)) * P(T)
        p_next = p_learned_given_obs + (1.0 - p_learned_given_obs) * self.p_transit
        return round(min(max(p_next, 0.01), 0.99), 3)

    def compute_sequence_mastery(self, response_sequence: List[bool]) -> float:
        """
        Feeds a historical boolean response sequence through BKT to compute current state.
        """
        p = self.p_init
        for is_correct in response_sequence:
            p = self.update_single_step(p, is_correct)
        return p

    def compute_akt_sequence_mastery(
        self,
        interactions: Sequence[Union[bool, Tuple[str, bool]]]
    ) -> float:
        """
        Computes dynamic mastery using the Attention-Based Knowledge Tracing (AKT) self-attention encoder.
        Accepts list of bools or list of (question_id, is_correct) tuples.
        """
        if not interactions:
            return self.p_init

        normalized: List[Tuple[str, bool]] = []
        for idx, item in enumerate(interactions):
            if isinstance(item, (tuple, list)):
                normalized.append((str(item[0]), bool(item[1])))
            else:
                normalized.append((f"q_seq_{idx}", bool(item)))

        return self.akt_engine.forward_sequence(normalized)
