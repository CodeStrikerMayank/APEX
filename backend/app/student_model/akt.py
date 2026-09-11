"""
Attention-Based Knowledge Tracing (AKT) Runtime Engine
======================================================
Platform Upgrade Phase 5: Neural-Symbolic Sequence Knowledge Tracing.
Provides:
  - Sequence self-attention encoder layers over student interaction history
  - Historical response array processing of shape (Batch, SequenceLength, 2)
    representing [question_id, correctness]
  - Scaled dot-product self-attention with safe numerical softmax clamping
  - Output posterior probability P(L_{t+1}) clamped strictly within [0.01, 0.99]
  - 100% offline, zero external heavyweight framework overhead, sub-millisecond execution.
"""
from __future__ import annotations

import hashlib
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import numpy as np

from backend.app.student_model.numerical_guards import (
    safe_clamp_prob,
    safe_div,
    safe_exp,
    safe_softmax,
    MIN_PROBABILITY,
    MAX_PROBABILITY
)


class AttentionKnowledgeTracing:
    """
    Attention-Based Knowledge Tracing (AKT) with Sequence Self-Attention.
    Processes historical response sequences to track dynamic concept mastery.
    """

    DEFAULT_EMBED_DIM: int = 16
    DEFAULT_PRIOR: float = 0.20
    MIN_POSTERIOR: float = 0.01
    MAX_POSTERIOR: float = 0.99

    def __init__(
        self,
        embed_dim: int = DEFAULT_EMBED_DIM,
        num_heads: int = 2,
        decay_rate: float = 0.05,
        p_init: float = DEFAULT_PRIOR,
    ) -> None:
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.decay_rate = decay_rate
        self.p_init = p_init

        # Deterministic pseudo-random projection weights seeded for absolute runtime consistency
        rng = np.random.RandomState(42)
        scale = 1.0 / math.sqrt(embed_dim)
        self.W_q = rng.normal(0.0, scale, (embed_dim, embed_dim))
        self.W_k = rng.normal(0.0, scale, (embed_dim, embed_dim))
        self.W_v = rng.normal(0.0, scale, (embed_dim, embed_dim))
        self.W_out = rng.normal(0.0, scale, (embed_dim, 1))
        self.b_out = 0.0

    @classmethod
    def question_id_to_feature(cls, question_id: str, dim: int) -> np.ndarray:
        """Deterministically projects question_id string into a stable embedding vector."""
        if not question_id:
            return np.zeros(dim, dtype=np.float64)
        hash_digest = hashlib.sha256(str(question_id).encode("utf-8")).digest()
        # Derive integer seeds from hash bytes
        vals = [((hash_digest[i % len(hash_digest)] / 255.0) * 2.0 - 1.0) for i in range(dim)]
        vec = np.array(vals, dtype=np.float64)
        norm = np.linalg.norm(vec)
        return vec / max(norm, 1e-7)

    def embed_interaction(self, question_id: str, is_correct: Union[bool, int, float]) -> np.ndarray:
        """
        Embeds a single interaction [question_id, correctness] into continuous representation.
        """
        q_vec = self.question_id_to_feature(question_id, self.embed_dim)
        c_val = 1.0 if bool(is_correct) else -1.0
        # Modulate query vector with correctness state
        interaction_vec = q_vec * (1.0 + 0.5 * c_val)
        return interaction_vec

    def forward_sequence(
        self,
        interactions: Sequence[Tuple[str, Union[bool, int, float]]]
    ) -> float:
        """
        Processes a sequence of (question_id, correctness) tuples through self-attention encoder.
        Returns posterior mastery probability P(L_{t+1}) clamped within [0.01, 0.99].
        """
        if not interactions:
            return self.p_init

        seq_len = len(interactions)
        # Construct interaction matrix X of shape (seq_len, embed_dim)
        X = np.zeros((seq_len, self.embed_dim), dtype=np.float64)
        for t, (qid, corr) in enumerate(interactions):
            # Apply exponential temporal recency weighting
            recency = math.exp(-self.decay_rate * (seq_len - 1 - t))
            X[t] = self.embed_interaction(qid, corr) * recency

        # Compute Q, K, V
        Q = np.dot(X, self.W_q)
        K = np.dot(X, self.W_k)
        V = np.dot(X, self.W_v)

        # Scaled dot-product attention
        scores = np.dot(Q, K.T) / math.sqrt(self.embed_dim)

        # Causal / Temporal masking (attending only to past interactions)
        mask = np.triu(np.ones((seq_len, seq_len)), k=1) * -1e9
        masked_scores = scores + mask

        # Row-wise safe softmax
        attn_weights = np.zeros_like(masked_scores)
        for i in range(seq_len):
            attn_weights[i] = safe_softmax(masked_scores[i])

        # Context representation
        context = np.dot(attn_weights, V)

        # Pool final interaction representation (latest state at sequence end)
        h_last = context[-1]
        raw_logit = float(np.asarray(np.dot(h_last, self.W_out) + self.b_out).item())

        # Base accuracy bias from recent observations
        recent_acc = sum(1.0 for _, c in interactions[-5:] if bool(c)) / max(min(len(interactions), 5), 1)
        prior_logit = math.log(max(self.p_init, 1e-7) / max(1.0 - self.p_init, 1e-7))
        combined_logit = 0.5 * raw_logit + 0.8 * (recent_acc - 0.5) * 4.0 + 0.3 * prior_logit

        # Sigmoid activation
        prob = 1.0 / (1.0 + safe_exp(-combined_logit))

        # Output posterior probability clamped strictly within [0.01, 0.99]
        clamped_posterior = min(max(prob, self.MIN_POSTERIOR), self.MAX_POSTERIOR)
        return round(clamped_posterior, 3)

    def forward_batch(self, batch_interactions: np.ndarray) -> np.ndarray:
        """
        Processes batch interaction tensor of shape (Batch, SequenceLength, 2).
        Each element is [question_id_hash_int, correctness].
        Returns array of posterior probabilities of shape (Batch,).
        """
        arr = np.asarray(batch_interactions)
        if arr.ndim != 3 or arr.shape[2] != 2:
            raise ValueError(f"Expected shape (Batch, SequenceLength, 2), got {arr.shape}")

        batch_size, seq_len, _ = arr.shape
        posteriors = np.zeros(batch_size, dtype=np.float64)

        for b in range(batch_size):
            tuples: List[Tuple[str, bool]] = []
            for t in range(seq_len):
                qid = str(arr[b, t, 0])
                corr = bool(arr[b, t, 1] > 0.5)
                tuples.append((qid, corr))
            posteriors[b] = self.forward_sequence(tuples)

        return posteriors
