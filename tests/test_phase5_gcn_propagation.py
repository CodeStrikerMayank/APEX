"""
Tests for Phase 5 GCN Knowledge Graph Message Passing Engine
"""
import pytest
import networkx as nx
import numpy as np
from backend.app.knowledge_graph.propagation import GKTPropagator, GCNPropagator


@pytest.fixture
def sample_dag():
    """
    Constructs a 3-tier prerequisite DAG:
    A (Limits) -> B (Continuity) -> C (Differentiability)
    """
    g = nx.DiGraph()
    g.add_node("A", name="Limits")
    g.add_node("B", name="Continuity")
    g.add_node("C", name="Differentiability")
    g.add_edge("A", "B", relationship="prerequisite")
    g.add_edge("B", "C", relationship="prerequisite")
    return g


def test_gcn_upstream_ancestor_solidity_credit(sample_dag):
    gcn = GCNPropagator(sample_dag)

    # When student demonstrates mastery gain on C (Differentiability)
    delta_u = 0.20
    deltas = gcn.compute_message_passing_deltas("C", delta_u)

    assert deltas["C"] == pytest.approx(0.20)

    # Upstream ancestor B (d = 1):
    # Delta P(L_B) = Delta P(L_C) * (0.40)^1 * 0.70 = 0.20 * 0.40 * 0.70 = 0.056
    expected_delta_b = 0.20 * 0.40 * 0.70
    assert deltas["B"] == pytest.approx(expected_delta_b, rel=1e-4)

    # Upstream ancestor A (d = 2):
    # Delta P(L_A) = Delta P(L_C) * (0.40)^2 * 0.70 = 0.20 * 0.16 * 0.70 = 0.0224
    expected_delta_a = 0.20 * (0.40 ** 2) * 0.70
    assert deltas["A"] == pytest.approx(expected_delta_a, rel=1e-4)


def test_gcn_downstream_readiness_gating(sample_dag):
    gcn = GCNPropagator(sample_dag)

    # Case 1: Positive mastery gain on A (Limits) unlocks downstream concepts
    deltas_pos = gcn.compute_message_passing_deltas("A", 0.30)
    assert "B" in deltas_pos
    assert "C" in deltas_pos

    # Downstream descendant B (d = 1):
    # Delta P(L_B) = 0.30 * 0.40 * 0.50 = 0.060
    assert deltas_pos["B"] == pytest.approx(0.30 * 0.40 * 0.50, rel=1e-4)

    # Case 2: Negative delta (failure on foundational concept A)
    # Strictly must NOT propagate downstream readiness
    deltas_neg = gcn.compute_message_passing_deltas("A", -0.25)
    assert deltas_neg["A"] == -0.25
    assert "B" not in deltas_neg
    assert "C" not in deltas_neg


def test_gcn_feature_layer_convolution(sample_dag):
    gcn = GCNPropagator(sample_dag)

    # 3 nodes, feature dimension 4
    features = np.ones((3, 4), dtype=np.float64)
    H_next = gcn.compute_gcn_layer(features)

    assert H_next.shape == (3, 4)
    assert not np.isnan(H_next).any()
    assert (H_next >= 0.0).all()
