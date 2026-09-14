import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database.connection import Base
from backend.app.models.schema import (
    Exam, Subject, Chapter, Topic, Concept, Prerequisite,
    StudentConceptMastery, Student, Roadmap, RoadmapAction
)
from backend.app.roadmap.generator import RoadmapGenerator
from backend.app.roadmap.next_action import NextActionEngine

@pytest.fixture
def roadmap_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    exam = Exam(exam_id="JEE", name="JEE")
    sub = Subject(subject_id="JEE_MATH", exam_id="JEE", name="Math")
    chap = Chapter(chapter_id="MATH_CALC", subject_id="JEE_MATH", name="Calculus")
    top = Topic(topic_id="MATH_LCD", chapter_id="MATH_CALC", name="LCD")
    session.add_all([exam, sub, chap, top])
    session.flush()

    c1 = Concept(concept_id="c_limits", topic_id="MATH_LCD", name="Limits", exam_relevance=0.95)
    c2 = Concept(concept_id="c_cont", topic_id="MATH_LCD", name="Continuity", exam_relevance=0.92)
    c3 = Concept(concept_id="c_diff", topic_id="MATH_LCD", name="Differentiability", exam_relevance=0.98)
    session.add_all([c1, c2, c3])
    session.flush()

    p1 = Prerequisite(from_concept_id="c_limits", to_concept_id="c_cont", strength=0.95)
    p2 = Prerequisite(from_concept_id="c_cont", to_concept_id="c_diff", strength=0.95)
    session.add_all([p1, p2])

    student = Student(student_id="s1", name="Rohan", email="rohan@example.com", password_hash="hash", target_exam="JEE")
    session.add(student)
    session.commit()

    yield session
    session.close()

def test_dynamic_roadmap_regeneration_on_mastery_change(roadmap_db):
    generator = RoadmapGenerator(roadmap_db, exam_id="JEE")
    next_engine = NextActionEngine(roadmap_db)

    # Initial state: student is weak on Limits (0.25)
    m1 = StudentConceptMastery(student_id="s1", concept_id="c_limits", mastery=0.25)
    m2 = StudentConceptMastery(student_id="s1", concept_id="c_cont", mastery=0.30)
    m3 = StudentConceptMastery(student_id="s1", concept_id="c_diff", mastery=0.20)
    roadmap_db.add_all([m1, m2, m3])
    roadmap_db.commit()

    # Generate initial roadmap
    rm1 = generator.generate_roadmap("s1")
    nba1 = next_engine.get_next_best_action("s1")

    # The Next-Best-Action MUST be Limits (foundational prerequisite)
    assert nba1["concept_id"] == "c_limits"
    assert nba1["action_type"] in ["LEARN_CONCEPT", "BASIC_PRACTICE", "JEE_FOUNDATION_REBUILD"]

    # Student now studies and masters Limits (mastery updates to 0.85)
    m1.mastery = 0.85
    roadmap_db.commit()

    # Re-generate roadmap after mastery improvement
    rm2 = generator.generate_roadmap("s1", trigger_event="PRACTICE_COMPLETED")
    nba2 = next_engine.get_next_best_action("s1")

    # Next-Best-Action MUST automatically advance to Continuity
    assert nba2["concept_id"] == "c_cont"
    assert rm2.version == rm1.version + 1


def test_unified_adaptive_study_roadmap_endpoints(roadmap_db):
    from backend.app.api.roadmap import (
        get_unified_study_roadmap, get_concept_roadmap_detail, recalculate_study_roadmap
    )

    # Initial state: student has varied mastery
    m1 = StudentConceptMastery(student_id="s1", concept_id="c_limits", mastery=0.35, fsrs_retrievability=0.60)
    m2 = StudentConceptMastery(student_id="s1", concept_id="c_cont", mastery=0.20, fsrs_retrievability=0.85)
    m3 = StudentConceptMastery(student_id="s1", concept_id="c_diff", mastery=0.10, fsrs_retrievability=0.90)
    roadmap_db.add_all([m1, m2, m3])
    roadmap_db.commit()

    # 1. Test Unified Roadmap single-source-of-truth payload
    res = get_unified_study_roadmap("s1", roadmap_db)
    assert res.student["id"] == "s1"
    assert res.student["exam"] == "JEE"
    assert res.overview.conceptsTotal == 3
    assert res.overview.conceptsMastered == 0
    assert res.overview.criticalGaps == 3  # all < 0.40
    assert res.overview.reviewsDue >= 1   # c_limits retrievability 0.60 < 0.70

    # Next Best Step should be Limits (prerequisite for downstream)
    assert res.currentFocus is not None
    assert res.currentFocus.conceptId == "c_limits"
    assert len(res.currentFocus.reasons) >= 1

    # Milestones and nodes validation
    assert len(res.milestones) >= 1
    assert len(res.nodes) == 3
    
    # Check DAG prerequisites & unlocks in nodes
    limits_node = next(n for n in res.nodes if n.id == "c_limits")
    cont_node = next(n for n in res.nodes if n.id == "c_cont")
    diff_node = next(n for n in res.nodes if n.id == "c_diff")

    assert len(limits_node.unlocks) >= 1
    assert limits_node.unlocks[0].id == "c_cont"
    assert len(cont_node.prerequisites) == 1
    assert cont_node.prerequisites[0].id == "c_limits"
    assert cont_node.prerequisites[0].isSatisfied is False  # 0.35 < 0.70
    assert cont_node.status == "LOCKED"  # Locked due to unsatisfied prerequisite

    # Today's path items
    assert len(res.today) >= 2

    # Graph topology export
    assert res.graph is not None
    assert len(res.graph["nodes"]) == 3
    assert len(res.graph["edges"]) == 2

    # 2. Test Concept Detail Drawer Endpoint
    detail = get_concept_roadmap_detail("s1", "c_cont", roadmap_db)
    assert detail["name"] == "Continuity"
    assert detail["mastery"] == 0.20
    assert len(detail["prerequisites"]) == 1
    assert detail["prerequisites"][0]["id"] == "c_limits"
    assert detail["prerequisites"][0]["is_satisfied"] is False
    assert len(detail["unlocks"]) == 1
    assert detail["unlocks"][0]["id"] == "c_diff"

    # 3. Test Recalculate Roadmap Endpoint
    recalc_res = recalculate_study_roadmap("s1", roadmap_db)
    assert recalc_res.overview.conceptsTotal == 3
    assert recalc_res.currentFocus.conceptId == "c_limits"
