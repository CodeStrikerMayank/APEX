"""
Graph-Wide Knowledge Propagation (GKT) Engine
=============================================
Platform Upgrade: Topological message passing over curriculum prerequisite DAG.
Provides:
  - Upstream Ancestor Propagation (Foundational Solidity Credit):
      Delta P(L_v) = Delta P(L_u) * (gamma^d) * w_upstream
  - Downstream Descendant Propagation (Forward Readiness Gating):
      Delta P(L_k) = Delta P(L_u) * (gamma^d) * w_downstream (if Delta P(L_u) > 0)
  - Clamping all states to [0.01, 0.99]
  - Database-integrated and standalone in-memory execution
"""
from __future__ import annotations

import networkx as nx
from typing import Any, Dict, List, Optional, Set, Tuple
from sqlalchemy.orm import Session


class GKTPropagator:
    """
    Graph-Wide Knowledge Propagation engine over a Directed Acyclic Graph (DAG).
    Sub-millisecond execution, mathematically guaranteed bounded states.
    """

    DEFAULT_GAMMA: float = 0.40
    DEFAULT_W_UPSTREAM: float = 0.70
    DEFAULT_W_DOWNSTREAM: float = 0.50
    MIN_PROBABILITY: float = 0.01
    MAX_PROBABILITY: float = 0.99

    def __init__(
        self,
        graph: Optional[nx.DiGraph] = None,
        gamma: float = DEFAULT_GAMMA,
        w_upstream: float = DEFAULT_W_UPSTREAM,
        w_downstream: float = DEFAULT_W_DOWNSTREAM,
    ) -> None:
        self.graph = graph if graph is not None else nx.DiGraph()
        self.gamma = gamma
        self.w_upstream = w_upstream
        self.w_downstream = w_downstream

    def set_graph(self, graph: nx.DiGraph) -> None:
        """Sets the underlying NetworkX DAG."""
        self.graph = graph

    @classmethod
    def clamp_probability(cls, value: float) -> float:
        """Clamps mastery probability P(L) in [0.01, 0.99]."""
        return min(max(float(value), cls.MIN_PROBABILITY), cls.MAX_PROBABILITY)

    def calculate_deltas(
        self,
        target_concept_id: str,
        delta_mastery: float,
    ) -> Dict[str, float]:
        """
        Calculates propagation deltas for all affected nodes in the DAG:
          - Target node: delta_mastery
          - Upstream ancestors: delta_mastery * (gamma^d) * w_upstream
          - Downstream descendants (if delta > 0): delta_mastery * (gamma^d) * w_downstream
        Returns a dict mapping concept_id -> delta_P(L).
        """
        deltas: Dict[str, float] = {target_concept_id: delta_mastery}
        if target_concept_id not in self.graph:
            return deltas

        if abs(delta_mastery) < 1e-9:
            return deltas

        # 1. Upstream Ancestor Propagation
        # Ancestors are nodes from which a directed path leads to target_concept_id
        ancestors = nx.ancestors(self.graph, target_concept_id)
        for v in ancestors:
            try:
                # Topological distance: shortest path length from ancestor v to target u
                dist = nx.shortest_path_length(self.graph, source=v, target=target_concept_id)
                decay = math_power = self.gamma ** dist
                delta_v = delta_mastery * decay * self.w_upstream
                deltas[v] = delta_v
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

        # 2. Downstream Descendant Propagation
        # Forward readiness gating: only propagates if delta_mastery > 0
        if delta_mastery > 0.0:
            descendants = nx.descendants(self.graph, target_concept_id)
            for k in descendants:
                try:
                    # Topological distance: shortest path length from target u to descendant k
                    dist = nx.shortest_path_length(self.graph, source=target_concept_id, target=k)
                    decay = self.gamma ** dist
                    delta_k = delta_mastery * decay * self.w_downstream
                    deltas[k] = delta_k
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue

        return deltas

    def propagate(
        self,
        target_concept_id: str,
        delta_mastery: float,
        current_masteries: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Applies graph propagation to a dictionary of current concept masteries.
        Returns a dictionary of updated mastery values bounded to [0.01, 0.99].
        """
        deltas = self.calculate_deltas(target_concept_id, delta_mastery)
        updated: Dict[str, float] = dict(current_masteries)

        for cid, delta in deltas.items():
            curr = updated.get(cid, 0.10)  # default prior if not yet evaluated
            new_val = self.clamp_probability(curr + delta)
            updated[cid] = round(new_val, 4)

        return updated

    def propagate_db(
        self,
        target_concept_id: str,
        delta_mastery: float,
        student_id: str,
        db: Session,
    ) -> Dict[str, float]:
        """
        Applies GKT propagation directly across SQLAlchemy StudentConceptMastery records.
        """
        from backend.app.models.schema import StudentConceptMastery

        deltas = self.calculate_deltas(target_concept_id, delta_mastery)
        results: Dict[str, float] = {}

        if not deltas:
            return results

        # Query existing masteries for all affected concepts
        existing = (
            db.query(StudentConceptMastery)
            .filter(
                StudentConceptMastery.student_id == student_id,
                StudentConceptMastery.concept_id.in_(list(deltas.keys())),
            )
            .all()
        )
        existing_map = {m.concept_id: m for m in existing}

        # Include pending objects in current session to prevent duplicate creation
        for obj in db.new:
            if isinstance(obj, StudentConceptMastery) and getattr(obj, "student_id", None) == student_id:
                if obj.concept_id not in existing_map:
                    existing_map[obj.concept_id] = obj

        for cid, delta in deltas.items():
            rec = existing_map.get(cid)
            if rec is None:
                # If no record exists, create one with prior BKT mastery
                base_bkt = 0.10
                new_bkt = self.clamp_probability(base_bkt + delta)
                rec = StudentConceptMastery(
                    student_id=student_id,
                    concept_id=cid,
                    bkt_mastery=new_bkt,
                    mastery=new_bkt,
                )
                db.add(rec)
                existing_map[cid] = rec
            else:
                curr_bkt = rec.bkt_mastery if rec.bkt_mastery is not None else rec.mastery
                new_bkt = self.clamp_probability(curr_bkt + delta)
                rec.bkt_mastery = new_bkt
                # Also blend with overall mastery
                rec.mastery = round(min(max(rec.mastery + delta * 0.5, 0.01), 0.99), 4)

            results[cid] = rec.bkt_mastery

        db.flush()
        return results
