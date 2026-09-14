import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.app.database.connection import get_db
from backend.app.models.schema import Roadmap, RoadmapAction, Concept, Chapter, Subject, Topic, Student, utc_now
from backend.app.schemas.pydantic_models import RoadmapResponse, NextActionResponse, WeaknessDetail, PriorityItem
from backend.app.roadmap.next_action import NextActionEngine
from backend.app.roadmap.generator import RoadmapGenerator
from backend.app.roadmap.weakness import WeaknessDetector
from backend.app.roadmap.priority import PriorityEngine
from backend.app.events.collector import EventCollector

router = APIRouter(prefix="/roadmap", tags=["Dynamic Roadmap & Intelligence"])

@router.get("/active/{student_id}", response_model=RoadmapResponse)
def get_active_roadmap(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    next_engine = NextActionEngine(db)
    nba = next_engine.get_next_best_action(student_id)

    active_rm = (
        db.query(Roadmap)
        .filter(Roadmap.student_id == student_id, Roadmap.status == "ACTIVE")
        .order_by(Roadmap.version.desc())
        .first()
    )

    needs_regen = False
    if active_rm and active_rm.actions:
        first_c = db.query(Concept).filter(Concept.concept_id == active_rm.actions[0].concept_id).first()
        sub = first_c.topic.chapter.subject if (first_c and first_c.topic and first_c.topic.chapter) else None
        if sub and sub.exam_id != student.target_exam:
            needs_regen = True

    if not active_rm or needs_regen:
        generator = RoadmapGenerator(db, exam_id=student.target_exam)
        active_rm = generator.generate_roadmap(student_id, trigger_event="API_REQUEST_EXAM_SYNC")

    actions_list = []
    for act in active_rm.actions:
        concept = db.query(Concept).filter(Concept.concept_id == act.concept_id).first()
        topic = concept.topic if concept else None
        chapter = topic.chapter if topic else None
        subject = chapter.subject if chapter else None

        actions_list.append({
            "id": act.id,
            "action_id": act.id,
            "sequence_order": act.sequence_order,
            "action_type": act.action_type,
            "concept_id": act.concept_id,
            "concept_name": concept.name if concept else act.concept_id,
            "subject": subject.name if subject else "General",
            "priority_score": act.priority_score,
            "reasons": act.reasons or [],
            "target_questions_count": act.target_questions_count,
            "estimated_minutes": act.estimated_minutes,
            "target_difficulty": act.target_difficulty,
            "is_completed": act.is_completed
        })

    return RoadmapResponse(
        roadmap_id=active_rm.roadmap_id,
        student_id=student_id,
        version=active_rm.version,
        created_at=active_rm.created_at,
        next_best_action=nba,
        actions=actions_list
    )

@router.get("/next-action/{student_id}", response_model=Optional[NextActionResponse])
def get_next_action(student_id: str, db: Session = Depends(get_db)):
    next_engine = NextActionEngine(db)
    return next_engine.get_next_best_action(student_id)

@router.post("/action/complete/{action_id}")
def mark_action_completed(action_id: int, db: Session = Depends(get_db)):
    action = db.query(RoadmapAction).filter(RoadmapAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Roadmap action not found.")

    action.is_completed = True
    action.completed_at = utc_now()
    db.commit()

    student_id = action.roadmap.student_id if action.roadmap else None
    if student_id:
        EventCollector.log_event(
            db=db,
            student_id=student_id,
            session_id="roadmap",
            event_type="ROADMAP_ITEM_COMPLETED",
            concept_id=action.concept_id,
            metadata={"action_type": action.action_type}
        )
        db.commit()

    return {"status": "SUCCESS", "action_id": action_id}

@router.get("/weaknesses/{student_id}", response_model=List[WeaknessDetail])
def get_student_weaknesses(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam_id = student.target_exam if student else "JEE"

    detector = WeaknessDetector(db, exam_id=exam_id)
    return detector.detect_weaknesses(student_id)

@router.get("/priorities/{student_id}", response_model=List[PriorityItem])
def get_student_priorities(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    exam_id = student.target_exam if student else "JEE"

    engine = PriorityEngine(db, exam_id=exam_id)
    return engine.rank_all_priorities(student_id)

@router.post("/regenerate/{student_id}", response_model=RoadmapResponse)
def regenerate_roadmap(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    generator = RoadmapGenerator(db, exam_id=student.target_exam)
    generator.generate_roadmap(student_id, trigger_event="USER_REGENERATE_REQUEST")

    return get_active_roadmap(student_id, db)


# --- Locked Daily Mission To-Do Endpoints ---

@router.get("/daily-todo/{student_id}")
def get_daily_todo(
    student_id: str,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieves or locks today's 3-5 mission tasks for the student.
    Does not allow algorithm reshuffling mid-day.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.get_or_create_daily_todo(student_id, target_date=target_date)


@router.post("/daily-todo/complete/{student_id}/{task_id}")
def complete_daily_task(
    student_id: str,
    task_id: str,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Marks a specific task completed in today's locked mission.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.complete_task(student_id, task_id, target_date=target_date)


@router.post("/ai-customize-todo/{student_id}")
def ai_customize_todo(
    student_id: str,
    prompt: Optional[str] = None,
    target_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    AI-Customized Daily Mission Generator:
    Analyzes student cognitive gaps, Ebbinghaus forgetting rate, and target exam
    to generate a student-centric locked mission with clear pedagogical reasoning.
    """
    from backend.app.roadmap.daily_todo import DailyTodoEngine
    engine = DailyTodoEngine(db)
    return engine.ai_customize_daily_todo(student_id, custom_prompt=prompt, target_date=target_date)


# =====================================================================
# UNIFIED ADAPTIVE STUDY ROADMAP API (Single Source of Truth)
# =====================================================================

from backend.app.models.schema import StudentConceptMastery, StudentAttemptItem, AssessmentAttempt
from backend.app.knowledge_graph.graph import CurriculumGraph
from backend.app.schemas.pydantic_models import (
    UnifiedRoadmapResponse, UnifiedRoadmapOverview, UnifiedRoadmapFocus,
    UnifiedRoadmapTodayItem, UnifiedRoadmapNode, UnifiedPrereqItem,
    UnifiedUnlockItem, UnifiedRoadmapMilestone, UnifiedSubjectMastery,
    UnifiedChapterItem
)

@router.get("/{student_id}", response_model=UnifiedRoadmapResponse)
def get_unified_study_roadmap(student_id: str, db: Session = Depends(get_db)):
    """
    Unified Adaptive Study Roadmap:
    Returns the single source of truth for the adaptive roadmap UI,
    including real IRT/BKT mastery, FSRS-5 memory retention decay,
    prerequisite DAG graph interception, unlocks, Next Best Step,
    Today's Path, subject/chapter aggregates, and graph topology.
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    exam_id = student.target_exam or "JEE"

    # Query all concepts for this exam
    concepts = (
        db.query(Concept)
        .join(Topic, Concept.topic_id == Topic.topic_id)
        .join(Chapter, Topic.chapter_id == Chapter.chapter_id)
        .join(Subject, Chapter.subject_id == Subject.subject_id)
        .filter(Subject.exam_id == exam_id)
        .all()
    )

    if not concepts:
        # Fallback: query all concepts if exam_id not filtered
        concepts = db.query(Concept).all()

    # Query student concept masteries
    masteries = (
        db.query(StudentConceptMastery)
        .filter(StudentConceptMastery.student_id == student_id)
        .all()
    )
    mastery_map = {m.concept_id: m for m in masteries}

    # Query curriculum DAG
    curriculum_graph = CurriculumGraph(db, exam_id=exam_id)

    # Query student attempt items for real question stats and error categorization
    attempt_items = (
        db.query(StudentAttemptItem)
        .join(AssessmentAttempt, StudentAttemptItem.attempt_id == AssessmentAttempt.attempt_id)
        .filter(AssessmentAttempt.student_id == student_id)
        .all()
    )
    
    question_stats = {}
    for item in attempt_items:
        cid = item.concept_id
        if cid not in question_stats:
            question_stats[cid] = {
                "attempted": 0,
                "correct": 0,
                "errors": {}
            }
        question_stats[cid]["attempted"] += 1
        if item.is_correct:
            question_stats[cid]["correct"] += 1
        elif item.error_type:
            err = item.error_type
            question_stats[cid]["errors"][err] = question_stats[cid]["errors"].get(err, 0) + 1

    # Map of all concept names for fast lookup
    concept_name_map = {c.concept_id: c.name for c in concepts}

    nodes_list: List[UnifiedRoadmapNode] = []
    total_mastery_sum = 0.0
    mastered_count = 0
    developing_count = 0
    critical_count = 0
    reviews_due_count = 0

    subject_buckets: Dict[str, Dict[str, Any]] = {}
    chapter_buckets: Dict[str, Dict[str, Any]] = {}

    for c in concepts:
        cid = c.concept_id
        topic = c.topic
        chapter = topic.chapter if topic else None
        subject = chapter.subject if chapter else None

        sub_name = subject.name if subject else "General"
        ch_name = chapter.name if chapter else "General"
        ch_id = chapter.chapter_id if chapter else "ch_gen"

        m_rec = mastery_map.get(cid)
        m_val = round(m_rec.mastery, 3) if m_rec else 0.0
        ret_val = round(
            m_rec.fsrs_retrievability if (m_rec and m_rec.fsrs_retrievability is not None)
            else (m_rec.retention_score if m_rec else 1.0),
            3
        )
        exam_rel = round(c.exam_relevance if c.exam_relevance is not None else 0.80, 2)
        diff_val = round(c.difficulty_weight if c.difficulty_weight is not None else 0.50, 2)
        out_deg_impact = curriculum_graph.get_prerequisite_impact(cid)

        # Priority calculation from system architecture:
        # Priority = 0.40 * (1 - Mastery) + 0.35 * ExamRelevance + 0.25 * OutDegreeImpact
        calc_priority = round(0.40 * (1.0 - m_val) + 0.35 * exam_rel + 0.25 * out_deg_impact, 3)

        # Direct prerequisites
        direct_prereqs = curriculum_graph.get_direct_prerequisites(cid)
        prereq_items: List[UnifiedPrereqItem] = []
        all_prereqs_satisfied = True

        for pid in direct_prereqs:
            p_rec = mastery_map.get(pid)
            p_mastery = round(p_rec.mastery, 3) if p_rec else 0.0
            p_name = concept_name_map.get(pid, pid)
            is_sat = p_mastery >= 0.70
            if not is_sat:
                all_prereqs_satisfied = False
            prereq_items.append(UnifiedPrereqItem(
                id=pid,
                name=p_name,
                mastery=p_mastery,
                isSatisfied=is_sat
            ))

        # Downstream unlocks
        unlock_ids = curriculum_graph.get_dependents(cid)
        unlock_items: List[UnifiedUnlockItem] = []
        for uid in unlock_ids:
            u_rec = mastery_map.get(uid)
            u_mastery = round(u_rec.mastery, 3) if u_rec else 0.0
            u_name = concept_name_map.get(uid, uid)
            unlock_items.append(UnifiedUnlockItem(
                id=uid,
                name=u_name,
                mastery=u_mastery
            ))

        # Node status logic:
        # >= 0.70 -> MASTERED
        # prerequisites unsatisfied -> LOCKED
        # < 0.40 -> CRITICAL
        # 0.40 - 0.69 -> DEVELOPING
        if m_val >= 0.70:
            status = "MASTERED"
            mastered_count += 1
        elif not all_prereqs_satisfied and len(direct_prereqs) > 0:
            status = "LOCKED"
            if m_val < 0.40:
                critical_count += 1
            else:
                developing_count += 1
        elif m_val < 0.40:
            status = "CRITICAL"
            critical_count += 1
        else:
            status = "DEVELOPING"
            developing_count += 1

        total_mastery_sum += m_val

        # Check retention / review due
        if ret_val < 0.70 or (m_rec and m_rec.forgetting_risk and m_rec.forgetting_risk > 0.35):
            reviews_due_count += 1

        # Question stats
        q_stat = question_stats.get(cid, {"attempted": 0, "correct": 0, "errors": {}})
        att_cnt = q_stat["attempted"]
        cor_cnt = q_stat["correct"]
        acc = round((cor_cnt / att_cnt), 2) if att_cnt > 0 else 0.0

        # Cognitive error signal
        err_signal = None
        if q_stat["errors"]:
            sorted_errors = sorted(q_stat["errors"].items(), key=lambda x: x[1], reverse=True)
            top_err_type, top_err_count = sorted_errors[0]
            clean_err = top_err_type.replace("_", " ").title()
            err_signal = f"{clean_err}: {top_err_count} recent mistake{'s' if top_err_count > 1 else ''}"

        # Recommendation reasons
        reasons = []
        if not all_prereqs_satisfied and len(direct_prereqs) > 0:
            unsat_names = [p.name for p in prereq_items if not p.isSatisfied]
            reasons.append(f"Prerequisite gap: Complete {', '.join(unsat_names[:2])} first")
        if m_val < 0.40:
            reasons.append(f"Critical mastery gap ({int(m_val * 100)}%)")
        if exam_rel >= 0.80:
            reasons.append(f"High {exam_id} exam relevance ({int(exam_rel * 100)}%)")
        if len(unlock_items) > 0:
            reasons.append(f"Unlocks {len(unlock_items)} downstream concept{'s' if len(unlock_items) > 1 else ''}")
        if ret_val < 0.70:
            reasons.append("Memory retention decay — spaced review due")

        last_studied_str = None
        if m_rec and m_rec.last_practiced_at:
            last_studied_str = m_rec.last_practiced_at.strftime("%Y-%m-%d")

        node = UnifiedRoadmapNode(
            id=cid,
            name=c.name,
            subject=sub_name,
            chapter=ch_name,
            mastery=m_val,
            retention=ret_val,
            examRelevance=exam_rel,
            pyqFrequency=round(exam_rel * 0.92, 2),
            difficulty=diff_val,
            status=status,
            priority=calc_priority,
            prerequisites=prereq_items,
            unlocks=unlock_items,
            estimatedMinutes=c.estimated_minutes or 30,
            questionsAttempted=att_cnt,
            questionsCorrect=cor_cnt,
            accuracy=acc,
            lastStudied=last_studied_str,
            errorSignal=err_signal,
            recommendationReasons=reasons
        )
        nodes_list.append(node)

        # Subject aggregate
        if sub_name not in subject_buckets:
            subject_buckets[sub_name] = {
                "name": sub_name,
                "mastery_sum": 0.0,
                "total": 0,
                "mastered": 0,
                "critical": 0
            }
        subject_buckets[sub_name]["mastery_sum"] += m_val
        subject_buckets[sub_name]["total"] += 1
        if m_val >= 0.70:
            subject_buckets[sub_name]["mastered"] += 1
        elif m_val < 0.40:
            subject_buckets[sub_name]["critical"] += 1

        # Chapter aggregate
        if ch_id not in chapter_buckets:
            chapter_buckets[ch_id] = {
                "id": ch_id,
                "name": ch_name,
                "subject": sub_name,
                "mastery_sum": 0.0,
                "total": 0,
                "mastered": 0,
                "critical": 0,
                "topics_count": 1
            }
        chapter_buckets[ch_id]["mastery_sum"] += m_val
        chapter_buckets[ch_id]["total"] += 1
        if m_val >= 0.70:
            chapter_buckets[ch_id]["mastered"] += 1
        elif m_val < 0.40:
            chapter_buckets[ch_id]["critical"] += 1

    # Calculate overall overview
    total_concepts = len(nodes_list) or 1
    overall_mastery_pct = int(round((total_mastery_sum / total_concepts) * 100))

    overview = UnifiedRoadmapOverview(
        overallMastery=overall_mastery_pct,
        conceptsTotal=len(nodes_list),
        conceptsMastered=mastered_count,
        conceptsDeveloping=developing_count,
        criticalGaps=critical_count,
        reviewsDue=reviews_due_count
    )

    # Subject masteries response
    subjects_res: List[UnifiedSubjectMastery] = []
    for s_name, s_data in subject_buckets.items():
        s_total = s_data["total"] or 1
        s_pct = int(round((s_data["mastery_sum"] / s_total) * 100))
        subjects_res.append(UnifiedSubjectMastery(
            name=s_name,
            mastery=s_pct,
            conceptsTotal=s_data["total"],
            conceptsMastered=s_data["mastered"],
            criticalGaps=s_data["critical"]
        ))

    # Chapters response
    chapters_res: List[UnifiedChapterItem] = []
    for ch_id, ch_data in chapter_buckets.items():
        ch_total = ch_data["total"] or 1
        ch_pct = int(round((ch_data["mastery_sum"] / ch_total) * 100))
        chapters_res.append(UnifiedChapterItem(
            id=ch_id,
            name=ch_data["name"],
            subject=ch_data["subject"],
            mastery=ch_pct,
            conceptsTotal=ch_data["total"],
            conceptsMastered=ch_data["mastered"],
            criticalGaps=ch_data["critical"],
            topicsCount=ch_data["topics_count"]
        ))

    # Next Best Step calculation (Highest priority eligible concept)
    # Filter candidates that are NOT mastered
    candidates = [n for n in nodes_list if n.status != "MASTERED"]
    candidates.sort(key=lambda x: x.priority, reverse=True)

    focus_node = None
    # Prerequisite Interception: if highest priority node is LOCKED, find its broken prerequisite
    for cand in candidates:
        if cand.status == "LOCKED":
            # Find the unsatisfied prerequisite with lowest mastery
            broken_prereqs = [p for p in cand.prerequisites if not p.isSatisfied]
            if broken_prereqs:
                broken_prereqs.sort(key=lambda p: p.mastery)
                target_pid = broken_prereqs[0].id
                p_node = next((n for n in nodes_list if n.id == target_pid), None)
                if p_node:
                    focus_node = p_node
                    break
        elif cand.status in ("CRITICAL", "DEVELOPING", "READY"):
            focus_node = cand
            break

    if not focus_node and candidates:
        focus_node = candidates[0]
    elif not focus_node and nodes_list:
        focus_node = nodes_list[0]

    current_focus = None
    if focus_node:
        focus_node.status = "CURRENT"
        focus_reasons = focus_node.recommendationReasons.copy()
        if not focus_reasons:
            focus_reasons = [
                f"Calibrated for {exam_id} curriculum",
                "High leverage concept",
                "Optimized for score velocity"
            ]
        current_focus = UnifiedRoadmapFocus(
            conceptId=focus_node.id,
            concept=focus_node.name,
            chapter=focus_node.chapter,
            subject=focus_node.subject,
            mastery=focus_node.mastery,
            priority=focus_node.priority,
            status="CURRENT",
            reasons=focus_reasons[:3],
            estimatedMinutes=focus_node.estimatedMinutes or 25
        )

    # Today's Path (3-4 high-impact actionable items)
    today_items: List[UnifiedRoadmapTodayItem] = []
    
    # 1. Spaced Review task (if any concept has decaying retention)
    review_candidates = [n for n in nodes_list if n.retention < 0.75 and n.mastery >= 0.30]
    review_candidates.sort(key=lambda x: x.retention)
    if review_candidates:
        r_node = review_candidates[0]
        today_items.append(UnifiedRoadmapTodayItem(
            id=f"today_rev_{r_node.id}",
            taskType="REVIEW",
            title=f"Spaced Review: {r_node.name}",
            subtitle=f"{r_node.subject} · Retention {int(r_node.retention * 100)}% (FSRS Decay)",
            conceptId=r_node.id,
            conceptName=r_node.name,
            chapter=r_node.chapter,
            subject=r_node.subject,
            durationMinutes=10,
            retention=r_node.retention,
            mastery=r_node.mastery,
            status="PENDING",
            actionLabel="Quick Review →"
        ))

    # 2. Core Focus / Next Best Step
    if focus_node:
        today_items.append(UnifiedRoadmapTodayItem(
            id=f"today_focus_{focus_node.id}",
            taskType="LEARN",
            title=f"Core Concept: {focus_node.name}",
            subtitle=f"{focus_node.chapter} · Mastery {int(focus_node.mastery * 100)}%",
            conceptId=focus_node.id,
            conceptName=focus_node.name,
            chapter=focus_node.chapter,
            subject=focus_node.subject,
            durationMinutes=focus_node.estimatedMinutes or 25,
            retention=focus_node.retention,
            mastery=focus_node.mastery,
            status="PENDING",
            actionLabel="Learn Concept →"
        ))

    # 3. Practice Drill (5 Qs) on next priority critical gap or topic drill
    drill_candidate = next((n for n in candidates if n.id != (focus_node.id if focus_node else "")), None)
    if drill_candidate:
        today_items.append(UnifiedRoadmapTodayItem(
            id=f"today_drill_{drill_candidate.id}",
            taskType="PRACTICE",
            title=f"Targeted Drill: {drill_candidate.name}",
            subtitle=f"{drill_candidate.subject} · 5 PYQ adaptive questions",
            conceptId=drill_candidate.id,
            conceptName=drill_candidate.name,
            chapter=drill_candidate.chapter,
            subject=drill_candidate.subject,
            durationMinutes=15,
            retention=drill_candidate.retention,
            mastery=drill_candidate.mastery,
            status="PENDING",
            actionLabel="Practice Drill →"
        ))

    # Milestones: group concepts into 3-4 pedagogical milestones
    # Stage 1: Foundation & Primitives
    # Stage 2: Core Analysis & Mechanics/Equilibrium
    # Stage 3: Advanced Applications & Synthesis
    milestones: List[UnifiedRoadmapMilestone] = []
    
    # Partition nodes into chunks
    chunk_size = max(len(nodes_list) // 3, 1)
    stage_titles = [
        ("FOUNDATIONS & ESSENTIALS", "Prerequisites, coordinate setups, definitions & core vector calculus"),
        ("CORE PRINCIPLES & DYNAMICS", "Governing laws, conservation theorems, equilibrium & analytical solving"),
        ("ADVANCED SYNTHESIS & PROBLEM BENCHMARK", "Multi-concept problem transfer, olympiad PYQs & mock mastery")
    ]

    for idx, (title, desc) in enumerate(stage_titles):
        start_i = idx * chunk_size
        end_i = (idx + 1) * chunk_size if idx < 2 else len(nodes_list)
        chunk_concepts = nodes_list[start_i:end_i]
        if chunk_concepts:
            milestones.append(UnifiedRoadmapMilestone(
                milestoneId=f"milestone_{idx + 1}",
                title=title,
                stage=idx + 1,
                description=desc,
                concepts=chunk_concepts
            ))

    # Export graph topology for Knowledge Graph view
    graph_data = curriculum_graph.export_graph_json(
        student_masteries={n.id: n.mastery for n in nodes_list}
    )

    return UnifiedRoadmapResponse(
        student={
            "id": student.student_id,
            "name": student.name,
            "email": student.email,
            "exam": exam_id,
            "target_track": student.target_track or exam_id,
            "daily_available_hours": student.daily_available_hours or 3.0
        },
        overview=overview,
        currentFocus=current_focus,
        today=today_items,
        milestones=milestones,
        nodes=nodes_list,
        subjects=subjects_res,
        chapters=chapters_res,
        graph=graph_data
    )


@router.get("/{student_id}/concept/{concept_id}")
def get_concept_roadmap_detail(
    student_id: str,
    concept_id: str,
    db: Session = Depends(get_db)
):
    """
    Detailed diagnostic deep-dive for a single concept in the slide-out drawer:
    Returns mastery, retention, question history, error classifications,
    prerequisite breakdown, and unlocked downstream concepts.
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    concept = db.query(Concept).filter(Concept.concept_id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found.")

    exam_id = student.target_exam or "JEE"
    graph = CurriculumGraph(db, exam_id=exam_id)

    m_rec = (
        db.query(StudentConceptMastery)
        .filter(StudentConceptMastery.student_id == student_id, StudentConceptMastery.concept_id == concept_id)
        .first()
    )

    topic = concept.topic
    chapter = topic.chapter if topic else None
    subject = chapter.subject if chapter else None

    # Prerequisites with live mastery
    direct_prereqs = graph.get_direct_prerequisites(concept_id)
    prereq_details = []
    for pid in direct_prereqs:
        p_c = db.query(Concept).filter(Concept.concept_id == pid).first()
        p_m = db.query(StudentConceptMastery).filter(
            StudentConceptMastery.student_id == student_id,
            StudentConceptMastery.concept_id == pid
        ).first()
        p_val = round(p_m.mastery, 2) if p_m else 0.0
        prereq_details.append({
            "id": pid,
            "name": p_c.name if p_c else pid,
            "mastery": p_val,
            "is_satisfied": p_val >= 0.70
        })

    # Unlocks
    unlock_ids = graph.get_dependents(concept_id)
    unlock_details = []
    for uid in unlock_ids:
        u_c = db.query(Concept).filter(Concept.concept_id == uid).first()
        u_m = db.query(StudentConceptMastery).filter(
            StudentConceptMastery.student_id == student_id,
            StudentConceptMastery.concept_id == uid
        ).first()
        unlock_details.append({
            "id": uid,
            "name": u_c.name if u_c else uid,
            "mastery": round(u_m.mastery, 2) if u_m else 0.0
        })

    # Questions and error signals
    attempt_items = (
        db.query(StudentAttemptItem)
        .join(AssessmentAttempt, StudentAttemptItem.attempt_id == AssessmentAttempt.attempt_id)
        .filter(AssessmentAttempt.student_id == student_id, StudentAttemptItem.concept_id == concept_id)
        .all()
    )

    error_counts: Dict[str, int] = {}
    correct_count = 0
    recent_history = []
    for it in attempt_items[-10:]:
        recent_history.append({
            "is_correct": it.is_correct,
            "time_taken": it.time_taken_seconds,
            "error_type": it.error_type
        })
        if it.is_correct:
            correct_count += 1
        elif it.error_type:
            error_counts[it.error_type] = error_counts.get(it.error_type, 0) + 1

    return {
        "concept_id": concept_id,
        "name": concept.name,
        "subject": subject.name if subject else "General",
        "chapter": chapter.name if chapter else "General",
        "description": concept.description,
        "mastery": round(m_rec.mastery, 3) if m_rec else 0.0,
        "retention": round(m_rec.fsrs_retrievability if (m_rec and m_rec.fsrs_retrievability is not None) else 1.0, 3),
        "exam_relevance": round(concept.exam_relevance or 0.8, 2),
        "difficulty": round(concept.difficulty_weight or 0.5, 2),
        "estimated_minutes": concept.estimated_minutes or 30,
        "prerequisites": prereq_details,
        "unlocks": unlock_details,
        "attempted_count": len(attempt_items),
        "correct_count": correct_count,
        "accuracy": round(correct_count / max(len(attempt_items), 1), 2),
        "error_counts": error_counts,
        "recent_history": recent_history
    }


@router.post("/{student_id}/recalculate", response_model=UnifiedRoadmapResponse)
def recalculate_study_roadmap(student_id: str, db: Session = Depends(get_db)):
    """
    Forces recalculation of roadmap priorities, prerequisite graph,
    and BKT state, returning the fresh unified roadmap payload.
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    generator = RoadmapGenerator(db, exam_id=student.target_exam or "JEE")
    generator.generate_roadmap(student_id, trigger_event="USER_RECALCULATE_REQUEST")

    return get_unified_study_roadmap(student_id, db)

