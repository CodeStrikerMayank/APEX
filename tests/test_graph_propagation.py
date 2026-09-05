"""
Unit Test Suite: Graph-Wide Knowledge Propagation (GKT) Engine
==============================================================
Verifies:
  1. Exponential decay of mastery deltas over topological distance (gamma^d)
  2. Upstream ancestor propagation reinforcement (w_upstream = 0.70)
  3. Downstream descendant forward readiness propagation (w_downstream = 0.50)
  4. Gating: Negative or zero delta does NOT propagate downstream
  5. Mathematical bounds: P(L) strictly clamped in [0.01, 0.99]
  6. Multi-level prerequisite chain propagation
  7. Database-backed propagation in StudentConceptMastery
"""
import pytest
import networkx as nx
from backend.app.knowledge_graph.propagation import GKTPropagator
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.curriculum.loader import seed_curriculum_and_questions
from backend.app.models.schema import Student, StudentConceptMastery, Concept

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_curriculum_and_questions(db)
    yield db
    db.close()

@pytest.fixture
def linear_dag():
    """
    Linear prerequisite chain:
    A (foundational) -> B (intermediate) -> C (target) -> D (advanced) -> E (mastery)
    """
    dag = nx.DiGraph()
    dag.add_edge("A", "B")
    dag.add_edge("B", "C")
    dag.add_edge("C", "D")
    dag.add_edge("D", "E")
    return dag

def test_upstream_ancestor_propagation(linear_dag):
    propagator = GKTPropagator(graph=linear_dag, gamma=0.40, w_upstream=0.70, w_downstream=0.50)
    target = "C"
    delta = 0.30

    deltas = propagator.calculate_deltas(target_concept_id=target, delta_mastery=delta)

    # Target gets full delta
    assert abs(deltas["C"] - 0.30) < 1e-6

    # B is 1 hop upstream (d=1): delta * 0.40 * 0.70 = delta * 0.28
    expected_b = 0.30 * 0.40 * 0.70  # 0.084
    assert abs(deltas["B"] - expected_b) < 1e-6

    # A is 2 hops upstream (d=2): delta * (0.40^2) * 0.70 = delta * 0.16 * 0.70 = delta * 0.112
    expected_a = 0.30 * (0.40 ** 2) * 0.70  # 0.0336
    assert abs(deltas["A"] - expected_a) < 1e-6

    # Verify exponential decay: hop 1 delta > hop 2 delta
    assert deltas["B"] > deltas["A"] > 0

def test_downstream_descendant_propagation_positive_progress(linear_dag):
    propagator = GKTPropagator(graph=linear_dag, gamma=0.40, w_upstream=0.70, w_downstream=0.50)
    target = "C"
    delta = 0.20

    deltas = propagator.calculate_deltas(target_concept_id=target, delta_mastery=delta)

    # D is 1 hop downstream (d=1): delta * 0.40 * 0.50 = delta * 0.20
    expected_d = 0.20 * 0.40 * 0.50  # 0.04
    assert abs(deltas["D"] - expected_d) < 1e-6

    # E is 2 hops downstream (d=2): delta * 0.16 * 0.50 = delta * 0.08
    expected_e = 0.20 * (0.40 ** 2) * 0.50  # 0.016
    assert abs(deltas["E"] - expected_e) < 1e-6

    assert deltas["D"] > deltas["E"] > 0

def test_downstream_gating_on_negative_delta(linear_dag):
    propagator = GKTPropagator(graph=linear_dag, gamma=0.40, w_upstream=0.70, w_downstream=0.50)
    target = "C"
    delta_negative = -0.25

    deltas = propagator.calculate_deltas(target_concept_id=target, delta_mastery=delta_negative)

    # Upstream ancestors receive negative delta
    assert deltas["B"] < 0
    assert deltas["A"] < 0

    # Downstream descendants MUST NOT receive updates when delta <= 0
    assert "D" not in deltas
    assert "E" not in deltas

def test_probability_clamping_boundaries(linear_dag):
    propagator = GKTPropagator(graph=linear_dag)
    current_masteries = {
        "A": 0.95,
        "B": 0.90,
        "C": 0.85,
        "D": 0.05,
    }
    # Large positive surge
    updated = propagator.propagate(target_concept_id="C", delta_mastery=0.40, current_masteries=current_masteries)
    for node, val in updated.items():
        assert 0.01 <= val <= 0.99

    # Large negative surge
    low_masteries = {"A": 0.05, "B": 0.05, "C": 0.05}
    updated_low = propagator.propagate(target_concept_id="C", delta_mastery=-0.50, current_masteries=low_masteries)
    for node, val in updated_low.items():
        assert 0.01 <= val <= 0.99

def test_gkt_db_propagation(test_db):
    concepts = test_db.query(Concept).limit(3).all()
    assert len(concepts) >= 3
    c_base, c_target, c_adv = concepts[0].concept_id, concepts[1].concept_id, concepts[2].concept_id

    dag = nx.DiGraph()
    dag.add_edge(c_base, c_target)
    dag.add_edge(c_target, c_adv)

    propagator = GKTPropagator(graph=dag)
    student_id = "gkt_test_student_01"

    student = test_db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        student = Student(student_id=student_id, name="GKT Student", email="gkt@test.local", password_hash="pw", target_exam="JEE")
        test_db.add(student)
        test_db.commit()

    # Pre-seed records or update existing
    base_rec = test_db.query(StudentConceptMastery).filter(
        StudentConceptMastery.student_id == student_id,
        StudentConceptMastery.concept_id == c_base
    ).first()
    if not base_rec:
        base_rec = StudentConceptMastery(student_id=student_id, concept_id=c_base, bkt_mastery=0.50, mastery=0.50)
        test_db.add(base_rec)
    else:
        base_rec.bkt_mastery = 0.50
        base_rec.mastery = 0.50

    target_rec = test_db.query(StudentConceptMastery).filter(
        StudentConceptMastery.student_id == student_id,
        StudentConceptMastery.concept_id == c_target
    ).first()
    if not target_rec:
        target_rec = StudentConceptMastery(student_id=student_id, concept_id=c_target, bkt_mastery=0.40, mastery=0.40)
        test_db.add(target_rec)
    else:
        target_rec.bkt_mastery = 0.40
        target_rec.mastery = 0.40

    test_db.commit()

    results = propagator.propagate_db(target_concept_id=c_target, delta_mastery=0.30, student_id=student_id, db=test_db)
    test_db.commit()

    # c_target should increase by 0.30 -> 0.70
    assert results[c_target] == pytest.approx(0.70, abs=0.01)
    # c_base is upstream (d=1): 0.50 + (0.30 * 0.40 * 0.70) = 0.50 + 0.084 = 0.584
    assert results[c_base] == pytest.approx(0.584, abs=0.01)
    # c_adv was created and updated downstream
    assert c_adv in results

