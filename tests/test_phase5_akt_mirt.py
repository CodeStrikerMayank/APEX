"""
Tests for Phase 5 Psychometric Upgrades:
  1. Attention-Based Knowledge Tracing (AKT) Runtime Engine
  2. 4-Dimensional Multi-Dimensional IRT (MIRT) Engine
"""
import pytest
import numpy as np
from backend.app.student_model.akt import AttentionKnowledgeTracing
from backend.app.student_model.bkt import BayesianKnowledgeTracing
from backend.app.student_model.irt import ItemResponseTheory, MultiDimensionalIRT


def test_akt_sequence_attention():
    akt = AttentionKnowledgeTracing(embed_dim=16, p_init=0.20)

    # Historical interaction sequence: [question_id, is_correct]
    interactions = [
        ("q_phys_001", True),
        ("q_phys_002", True),
        ("q_phys_003", False),
        ("q_phys_004", True),
        ("q_phys_005", True),
    ]

    posterior = akt.forward_sequence(interactions)
    # Must be within [0.01, 0.99]
    assert 0.01 <= posterior <= 0.99
    # Multiple correct answers should produce high posterior knowledge
    assert posterior > 0.50

    # Low correctness sequence
    poor_interactions = [
        ("q_chem_001", False),
        ("q_chem_002", False),
        ("q_chem_003", False),
    ]
    poor_posterior = akt.forward_sequence(poor_interactions)
    assert 0.01 <= poor_posterior <= 0.99
    assert poor_posterior < posterior


def test_akt_batch_processing_shape():
    akt = AttentionKnowledgeTracing(embed_dim=16)

    # Batch tensor of shape (Batch=3, SequenceLength=4, Features=2)
    # [question_id_hash, correctness]
    batch_data = np.array([
        [[101, 1], [102, 1], [103, 1], [104, 1]], # High mastery student
        [[201, 0], [202, 0], [203, 0], [204, 0]], # Struggling student
        [[301, 1], [302, 0], [303, 1], [304, 0]], # Moderate student
    ], dtype=np.float64)

    posteriors = akt.forward_batch(batch_data)
    assert posteriors.shape == (3,)
    assert all(0.01 <= p <= 0.99 for p in posteriors)
    assert posteriors[0] > posteriors[1]


def test_bkt_akt_integration():
    bkt = BayesianKnowledgeTracing(p_init=0.20)

    # Standard BKT sequence
    p_bkt = bkt.compute_sequence_mastery([True, True, True])
    assert 0.01 <= p_bkt <= 0.99

    # Augmented AKT sequence
    p_akt = bkt.compute_akt_sequence_mastery([
        ("q_math_01", True),
        ("q_math_02", True),
        ("q_math_03", True)
    ])
    assert 0.01 <= p_akt <= 0.99


def test_mirt_4d_vector_estimation():
    initial_theta = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float64)

    # Observations specifically exercising calculation and spatial dimensions
    observations = [
        {
            "is_correct": True,
            "difficulty_01": 0.70,
            "skill": "numerical_calculation",
            "content": "Calculate the magnitude of acceleration and velocity integral",
            "time_taken_seconds": 45,
            "estimated_time": 60,
            "discrimination": 1.2
        },
        {
            "is_correct": True,
            "difficulty_01": 0.65,
            "skill": "spatial_reasoning",
            "content": "Determine the prism refraction angle and geometric path",
            "time_taken_seconds": 40,
            "estimated_time": 60,
            "discrimination": 1.1
        },
        {
            "is_correct": False,
            "difficulty_01": 0.40,
            "skill": "conceptual",
            "content": "State the fundamental definition theorem",
            "time_taken_seconds": 95,
            "estimated_time": 60,
            "discrimination": 0.9
        }
    ]

    updated_theta = MultiDimensionalIRT.update_ability_vector(initial_theta, observations)

    # Check 4 dimensions: [calc, concept, spatial, pacing]
    assert updated_theta.shape == (4,)
    # Calculation ability should have increased
    assert updated_theta[0] > 0.0
    # Spatial ability should have increased
    assert updated_theta[2] > 0.0
    # Pacing should be elevated from rapid answers
    assert updated_theta[3] > -1.0
    # Values bounded in [-3.0, 3.0]
    assert all(-3.0 <= th <= 3.0 for th in updated_theta)

    # Composite scalar projection
    composite = MultiDimensionalIRT.composite_scalar_ability(updated_theta)
    assert -3.0 <= composite <= 3.0


def test_numerical_guards_stability():
    from backend.app.student_model.numerical_guards import (
        safe_clamp_prob, safe_div, safe_log, safe_exp, safe_softmax
    )

    # Extreme edge cases
    assert safe_div(1.0, 0.0) == 1e7 or safe_div(1.0, 0.0) > 0.0
    assert safe_div(1.0, 1e-12) == 1e7 or safe_div(1.0, 1e-12) > 0.0
    assert safe_clamp_prob(-5.0) == 1e-7
    assert safe_clamp_prob(15.0) == 1.0 - 1e-7
    assert safe_log(0.0) == np.log(1e-7)

    probs = safe_softmax([1000.0, -1000.0, 0.0])
    assert probs.shape == (3,)
    assert not np.isnan(probs).any()
    assert np.isclose(np.sum(probs), 1.0, atol=1e-4)
