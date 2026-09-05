"""
Comprehensive End-to-End REST API Test Suite
============================================
Verifies the complete backend API surface across all subsystems:
  1. System Health & Root Info (/ and /api/health)
  2. Student Authentication Flow (Register, Case-normalization, Duplicates, Login, Profile)
  3. Curriculum Tree & Knowledge Graph for JEE, NEET, UPSC + 404 validation
  4. Standard Assessments (Start, Drill, Full Scan, Advanced, Submit, History)
  5. Real-Time Adaptive CAT Session (Start, Stepwise Item Responses, Convergence/Termination)
  6. Daily 3-Subject Interleaved Assignments for JEE, NEET, UPSC (Today, Progress, Submit, Streaks)
  7. Dynamic Roadmap & Learning Intelligence (Active, Next-Action, Action-Complete, Weaknesses, Priorities, Regenerate)
  8. Pedagogical AI Tutor (/chat, /generate-question)
  9. Append-Only Telemetry (/log, /stream, Event Validation)
 10. Supporting Analytics & Admin DB Reset with FK Integrity (/review-queue, /error-trends, /report-card, /admin/stats, /admin/reset-db)
 11. UPSC Civil Services Subsystem (/mains-prompts, /prelims-quiz, /evaluate-written, /history)
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.connection import SessionLocal, Base, engine
from backend.app.curriculum.loader import seed_curriculum_and_questions
from backend.app.models.schema import Student, Question, Concept

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_curriculum_and_questions(db)
    yield


# ---------------------------------------------------------------------------
# 1. System Health & Root Endpoints
# ---------------------------------------------------------------------------
def test_system_status_and_health():
    # Root
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "online"
    assert "health_url" in data
    assert data["docs_url"] == "/docs"

    # Health check
    resp_h = client.get("/api/health")
    assert resp_h.status_code == 200
    data_h = resp_h.json()
    assert data_h["status"] == "HEALTHY"
    assert "JEE" in data_h["supported_exams"]
    assert "NEET" in data_h["supported_exams"]
    assert "UPSC" in data_h["supported_exams"]


# ---------------------------------------------------------------------------
# 2. Authentication Flow & Email Normalization
# ---------------------------------------------------------------------------
def test_auth_full_lifecycle():
    raw_email = f"  Student_{uuid.uuid4().hex[:6]}@DOMAIN.COM  "
    expected_email = raw_email.strip().lower()

    # 1. Registration
    reg_payload = {
        "name": "Arjun Singhania",
        "email": raw_email,
        "password": "SecurePassword123",
        "target_exam": "JEE",
        "target_track": "JEE_MAIN",
        "daily_available_hours": 3.5
    }
    resp_reg = client.post("/api/auth/register", json=reg_payload)
    assert resp_reg.status_code == 200
    student_data = resp_reg.json()
    student_id = student_data["student_id"]
    assert student_data["email"] == expected_email
    assert student_data["name"] == "Arjun Singhania"

    # 2. Duplicate registration (same email in lowercase)
    resp_dup = client.post("/api/auth/register", json=reg_payload)
    assert resp_dup.status_code == 400
    assert "already registered" in resp_dup.json()["detail"].lower()

    # 3. Login with mixed case email
    login_payload = {
        "email": raw_email.upper(),
        "password": "SecurePassword123"
    }
    resp_login = client.post("/api/auth/login", json=login_payload)
    assert resp_login.status_code == 200
    assert resp_login.json()["student_id"] == student_id

    # 4. Login with invalid password
    resp_invalid = client.post("/api/auth/login", json={
        "email": expected_email,
        "password": "WrongPassword"
    })
    assert resp_invalid.status_code == 401

    # 5. Fetch profile
    resp_prof = client.get(f"/api/auth/profile/{student_id}")
    assert resp_prof.status_code == 200
    assert resp_prof.json()["email"] == expected_email

    # 6. Fetch non-existent profile
    resp_404 = client.get("/api/auth/profile/std_non_existent_999")
    assert resp_404.status_code == 404


# ---------------------------------------------------------------------------
# 3. Curriculum & Knowledge Graph across Streams
# ---------------------------------------------------------------------------
def test_curriculum_and_knowledge_graph_endpoints():
    # Exams list
    resp_exams = client.get("/api/curriculum/exams")
    assert resp_exams.status_code == 200
    exam_ids = [e["exam_id"] for e in resp_exams.json()]
    assert "JEE" in exam_ids
    assert "NEET" in exam_ids
    assert "UPSC" in exam_ids

    # JEE Tree
    resp_jee = client.get("/api/curriculum/tree/JEE")
    assert resp_jee.status_code == 200
    jee_subs = [s["name"] for s in resp_jee.json()["subjects"]]
    assert "Physics" in jee_subs
    assert "Chemistry" in jee_subs
    assert "Mathematics" in jee_subs

    # NEET Tree
    resp_neet = client.get("/api/curriculum/tree/NEET")
    assert resp_neet.status_code == 200
    neet_subs = [s["name"] for s in resp_neet.json()["subjects"]]
    assert "Biology" in neet_subs
    assert "Physics" in neet_subs
    assert "Chemistry" in neet_subs

    # UPSC Tree
    resp_upsc = client.get("/api/curriculum/tree/UPSC")
    assert resp_upsc.status_code == 200
    upsc_subs = [s["name"] for s in resp_upsc.json()["subjects"]]
    assert "Indian Polity & Governance" in upsc_subs
    assert "Economy, Environment & Technology" in upsc_subs
    assert "Ethics, Integrity & Aptitude" in upsc_subs

    # Invalid Exam Tree
    resp_invalid_tree = client.get("/api/curriculum/tree/INVALID_EXAM")
    assert resp_invalid_tree.status_code == 404

    # Knowledge Graph
    resp_graph_jee = client.get("/api/curriculum/graph/JEE")
    assert resp_graph_jee.status_code == 200
    assert "nodes" in resp_graph_jee.json()
    assert "edges" in resp_graph_jee.json()

    resp_graph_upsc = client.get("/api/curriculum/graph/UPSC")
    assert resp_graph_upsc.status_code == 200

    resp_graph_all = client.get("/api/curriculum/graph/ALL")
    assert resp_graph_all.status_code == 200

    # Non-existent Exam Graph returns 404
    resp_graph_404 = client.get("/api/curriculum/graph/NOT_AN_EXAM")
    assert resp_graph_404.status_code == 404


# ---------------------------------------------------------------------------
# 4. Standard Assessment Endpoints (Body & Query Parameter Flexibility)
# ---------------------------------------------------------------------------
def test_standard_assessments_flexibility_and_lifecycle():
    # Register student
    reg = client.post("/api/auth/register", json={
        "name": "Kavya Patel",
        "email": f"kavya_{uuid.uuid4().hex[:6]}@example.com",
        "password": "pass123kavya",
        "target_exam": "JEE",
        "daily_available_hours": 3.0
    }).json()
    sid = reg["student_id"]

    # 1. Start via JSON body
    resp_start_body = client.post("/api/assessments/start", json={
        "student_id": sid,
        "exam": "JEE",
        "assessment_type": "DIAGNOSTIC",
        "stage": 1,
        "duration_minutes": 25
    })
    assert resp_start_body.status_code == 200
    asmt_data = resp_start_body.json()
    assert "attempt_id" in asmt_data
    assert len(asmt_data["questions"]) > 0

    # 2. Start via Query parameter
    resp_start_query = client.post(f"/api/assessments/start?student_id={sid}", json={
        "exam": "JEE",
        "assessment_type": "DIAGNOSTIC"
    })
    assert resp_start_query.status_code == 200

    # 3. Start Drill via body
    resp_drill_body = client.post("/api/assessments/start-drill", json={
        "student_id": sid,
        "subject": "Physics",
        "exam": "JEE",
        "duration_minutes": 15
    })
    assert resp_drill_body.status_code == 200

    # 4. Start Drill via query params
    resp_drill_query = client.post(f"/api/assessments/start-drill?student_id={sid}&subject=Physics&exam=JEE")
    assert resp_drill_query.status_code == 200

    # 5. Start Full Scan via body and query
    resp_scan_body = client.post("/api/assessments/start-full-scan", json={"student_id": sid, "exam": "JEE"})
    assert resp_scan_body.status_code == 200

    resp_scan_query = client.post(f"/api/assessments/start-full-scan?student_id={sid}&exam=JEE")
    assert resp_scan_query.status_code == 200

    # 6. Start Advanced challenge via body and query
    resp_adv_body = client.post("/api/assessments/start-advanced", json={"student_id": sid, "exam": "JEE"})
    assert resp_adv_body.status_code == 200

    resp_adv_query = client.post(f"/api/assessments/start-advanced?student_id={sid}&exam=JEE")
    assert resp_adv_query.status_code == 200

    # 7. Submit Assessment
    attempt_id = asmt_data["attempt_id"]
    responses = []
    for q in asmt_data["questions"]:
        responses.append({
            "question_id": q["question_id"],
            "student_answer": "A",
            "time_taken_seconds": 45,
            "confidence_estimate": 0.8
        })

    resp_sub = client.post("/api/assessments/submit", json={
        "attempt_id": attempt_id,
        "responses": responses
    })
    assert resp_sub.status_code == 200
    res = resp_sub.json()
    assert res["attempt_id"] == attempt_id
    assert "score_percentage" in res
    assert "new_roadmap_summary" in res

    # 8. Assessment History
    resp_hist = client.get(f"/api/assessments/history/{sid}")
    assert resp_hist.status_code == 200
    hist = resp_hist.json()
    assert len(hist) >= 1
    attempt_ids = [h["attempt_id"] for h in hist]
    assert attempt_id in attempt_ids


# ---------------------------------------------------------------------------
# 5. Real-Time Computerized Adaptive Testing (CAT) Engine
# ---------------------------------------------------------------------------
def test_cat_adaptive_session_loop():
    reg = client.post("/api/auth/register", json={
        "name": "CAT Tester",
        "email": f"cat_{uuid.uuid4().hex[:6]}@example.com",
        "password": "pass123cat",
        "target_exam": "JEE"
    }).json()
    sid = reg["student_id"]

    # Start CAT session
    start_res = client.post("/api/assessments/cat/start", json={
        "student_id": sid,
        "exam": "JEE",
        "subject": "Physics"
    })
    assert start_res.status_code == 200
    cat_session = start_res.json()
    session_id = cat_session["session_id"]
    current_q = cat_session["question"]
    assert current_q is not None
    assert cat_session["current_theta"] == 0.0

    # Step through CAT questions until termination or up to 6 iterations
    steps = 0
    while not cat_session.get("is_complete") and steps < 6 and current_q:
        step_res = client.post("/api/assessments/cat/next-question", json={
            "session_id": session_id,
            "last_question_id": current_q["question_id"],
            "student_answer": "A",
            "time_taken_seconds": 50
        })
        assert step_res.status_code == 200
        cat_session = step_res.json()
        current_q = cat_session.get("question")
        steps += 1

    assert steps > 0
    assert "current_theta" in cat_session
    assert "sem" in cat_session


# ---------------------------------------------------------------------------
# 6. Daily 3-Subject Interleaved Assignments across JEE, NEET, and UPSC
# ---------------------------------------------------------------------------
def test_daily_assignments_across_all_streams():
    streams = [
        ("JEE", ["Physics", "Chemistry", "Mathematics"]),
        ("NEET", ["Biology", "Physics", "Chemistry"]),
        ("UPSC", [
            "Indian Polity & Governance",
            "Economy, Environment & Technology",
            "Ethics, Integrity & Aptitude"
        ])
    ]

    for exam, expected_subjects in streams:
        reg = client.post("/api/auth/register", json={
            "name": f"Student {exam}",
            "email": f"daily_{exam.lower()}_{uuid.uuid4().hex[:6]}@example.com",
            "password": "password1234",
            "target_exam": exam
        }).json()
        sid = reg["student_id"]

        # Fetch / generate today's assignment
        resp_today = client.get(f"/api/assignments/today/{sid}?questions_per_subject=10")
        assert resp_today.status_code == 200
        asgn = resp_today.json()
        assert asgn["exam"] == exam
        assert "subjects" in asgn
        assert set(expected_subjects).issubset(set(asgn["subjects"]))

        # Gather questions
        all_items = []
        for sub_qs in asgn["questions_by_subject"].values():
            all_items.extend(sub_qs)
        assert len(all_items) > 0

        assignment_id = asgn["assignment_id"]

        # Save progress
        sample_q = all_items[0]["question_id"]
        save_resp = client.post("/api/assignments/save-progress", json={
            "assignment_id": assignment_id,
            "responses": [
                {"question_id": sample_q, "student_answer": "B", "is_marked_review": False, "time_taken_seconds": 30}
            ]
        })
        assert save_resp.status_code == 200
        assert save_resp.json()["status"] in ["SAVED", "SUCCESS"]

        # Submit assignment
        sub_resp = client.post("/api/assignments/submit", json={
            "assignment_id": assignment_id,
            "responses": [
                {"question_id": it["question_id"], "student_answer": "B", "is_marked_review": False, "time_taken_seconds": 25}
                for it in all_items
            ]
        })
        assert sub_resp.status_code == 200
        grade_data = sub_resp.json()
        assert grade_data["status"] == "COMPLETED"
        assert "subject_scores" in grade_data

        # Check history & streaks
        hist_resp = client.get(f"/api/assignments/history/{sid}")
        assert hist_resp.status_code == 200
        h_data = hist_resp.json()
        assert h_data["streak_days"] >= 1
        assert len(h_data["assignments"]) >= 1


# ---------------------------------------------------------------------------
# 7. Dynamic Roadmap & Intelligence Endpoints
# ---------------------------------------------------------------------------
def test_roadmap_and_learning_intelligence():
    reg = client.post("/api/auth/register", json={
        "name": "Roadmap Learner",
        "email": f"roadmap_{uuid.uuid4().hex[:6]}@example.com",
        "password": "pass123roadmap",
        "target_exam": "JEE"
    }).json()
    sid = reg["student_id"]

    # 1. Active roadmap
    rm_resp = client.get(f"/api/roadmap/active/{sid}")
    assert rm_resp.status_code == 200
    rm = rm_resp.json()
    assert rm["student_id"] == sid
    assert len(rm["actions"]) > 0

    # 2. Next best action
    next_resp = client.get(f"/api/roadmap/next-action/{sid}")
    assert next_resp.status_code == 200

    # 3. Complete action
    first_action = rm["actions"][0]
    action_id = first_action.get("id") or first_action.get("action_id") or 1
    comp_resp = client.post(f"/api/roadmap/action/complete/{action_id}")
    assert comp_resp.status_code == 200
    assert comp_resp.json()["status"] == "SUCCESS"

    # 4. Detect weaknesses
    weak_resp = client.get(f"/api/roadmap/weaknesses/{sid}")
    assert weak_resp.status_code == 200
    assert isinstance(weak_resp.json(), list)

    # 5. Ranked priorities
    prior_resp = client.get(f"/api/roadmap/priorities/{sid}")
    assert prior_resp.status_code == 200
    assert isinstance(prior_resp.json(), list)

    # 6. Regenerate roadmap
    regen_resp = client.post(f"/api/roadmap/regenerate/{sid}")
    assert regen_resp.status_code == 200
    assert regen_resp.json()["version"] >= rm["version"]


# ---------------------------------------------------------------------------
# 8. AI Pedagogical Assistant & Synthetic Question Generator
# ---------------------------------------------------------------------------
def test_ai_tutor_and_question_generation():
    reg = client.post("/api/auth/register", json={
        "name": "AI Study Student",
        "email": f"ai_stud_{uuid.uuid4().hex[:6]}@example.com",
        "password": "passwordai123",
        "target_exam": "JEE"
    }).json()
    sid = reg["student_id"]

    # Chat with pedagogical tutor
    chat_resp = client.post(f"/api/ai/chat/{sid}", json={
        "prompt": "Why is resolving components along the inclined plane important in Newton's laws?"
    })
    assert chat_resp.status_code == 200
    data = chat_resp.json()
    assert "response" in data
    assert len(data["response"]) > 20

    # Generate synthetic question
    with SessionLocal() as db:
        concept = db.query(Concept).first()
        cid = concept.concept_id if concept else "c_kinematics_1d"

    qgen_resp = client.post("/api/ai/generate-question", json={
        "exam": "JEE",
        "subject": "Physics",
        "chapter": "Kinematics",
        "concept_id": cid,
        "difficulty": 0.65
    })
    assert qgen_resp.status_code == 200
    q_data = qgen_resp.json()
    assert "content" in q_data
    assert "correct_answer" in q_data


# ---------------------------------------------------------------------------
# 9. Telemetry Event Collection & Stream
# ---------------------------------------------------------------------------
def test_telemetry_event_logging():
    reg = client.post("/api/auth/register", json={
        "name": "Telemetry Student",
        "email": f"telem_{uuid.uuid4().hex[:6]}@example.com",
        "password": "passtelem123",
        "target_exam": "JEE"
    }).json()
    sid = reg["student_id"]

    # Valid event 1: ASSIGNMENT_GENERATED
    ev1 = client.post(f"/api/telemetry/log/{sid}", json={
        "session_id": "sess_001",
        "event_type": "ASSIGNMENT_GENERATED",
        "metadata": {"assignment_id": "asgn_test_123"}
    })
    assert ev1.status_code == 200
    assert ev1.json()["status"] == "LOGGED"

    # Valid event 2: ASSIGNMENT_SUBMITTED
    ev2 = client.post(f"/api/telemetry/log/{sid}", json={
        "session_id": "sess_001",
        "event_type": "ASSIGNMENT_SUBMITTED",
        "metadata": {"score": 85.0}
    })
    assert ev2.status_code == 200

    # Invalid event type
    ev_inv = client.post(f"/api/telemetry/log/{sid}", json={
        "session_id": "sess_001",
        "event_type": "UNREGISTERED_BOGUS_EVENT"
    })
    assert ev_inv.status_code == 400

    # Retrieve telemetry stream
    stream_resp = client.get(f"/api/telemetry/stream/{sid}")
    assert stream_resp.status_code == 200
    events = stream_resp.json()
    assert len(events) >= 2


# ---------------------------------------------------------------------------
# 10. Supporting Features & Admin Security
# ---------------------------------------------------------------------------
def test_supporting_features_and_admin_endpoints():
    reg = client.post("/api/auth/register", json={
        "name": "Support Test Student",
        "email": f"support_{uuid.uuid4().hex[:6]}@example.com",
        "password": "passsupport123",
        "target_exam": "JEE"
    }).json()
    sid = reg["student_id"]

    # Review queue
    rq = client.get(f"/api/supporting/review-queue/{sid}")
    assert rq.status_code == 200
    assert "queue" in rq.json()

    # Error trends
    et = client.get(f"/api/supporting/error-trends/{sid}")
    assert et.status_code == 200
    assert "by_error_type" in et.json()

    # Report card
    rc = client.get(f"/api/supporting/report-card/{sid}")
    assert rc.status_code == 200
    assert "overall_performance" in rc.json()

    # Admin stats unauthorized
    st_unauth = client.get("/api/admin/stats")
    assert st_unauth.status_code == 403

    # Admin stats authorized
    st_auth = client.get("/api/admin/stats", headers={"x-admin-key": "1234admin"})
    assert st_auth.status_code == 200
    stats = st_auth.json()
    assert "total_students" in stats
    assert "total_assignments" in stats
    assert "total_cat_sessions" in stats
    assert "total_upsc_submissions" in stats

    # Reset DB unauthorized
    reset_unauth = client.post("/api/admin/reset-db")
    assert reset_unauth.status_code == 403

    # Reset DB authorized (wipes student records cleanly while maintaining FK integrity)
    reset_auth = client.post("/api/admin/reset-db", headers={"x-admin-key": "1234admin"})
    assert reset_auth.status_code == 200
    assert reset_auth.json()["status"] == "RESET_COMPLETE"

    # Confirm students table is reset
    st_after = client.get("/api/admin/stats", headers={"x-admin-key": "1234admin"}).json()
    assert st_after["total_students"] == 0


# ---------------------------------------------------------------------------
# 11. UPSC Civil Services Subsystem
# ---------------------------------------------------------------------------
def test_upsc_civil_services_subsystem():
    # Register UPSC student after reset
    reg = client.post("/api/auth/register", json={
        "name": "Meera Rao",
        "email": f"meera_{uuid.uuid4().hex[:6]}@upsc.gov.in",
        "password": "upscpassword123",
        "target_exam": "UPSC",
        "target_track": "UPSC_MAINS"
    }).json()
    sid = reg["student_id"]

    # 1. Fetch UPSC Mains prompts
    mains_resp = client.get("/api/upsc/mains-prompts")
    assert mains_resp.status_code == 200
    prompts = mains_resp.json()
    assert len(prompts) >= 4
    prompt_sample = prompts[0]

    # 2. Fetch UPSC Prelims quiz
    prelims_resp = client.get("/api/upsc/prelims-quiz")
    assert prelims_resp.status_code == 200
    prelims_data = prelims_resp.json()
    assert isinstance(prelims_data, list)
    assert len(prelims_data) >= 2

    # 3. Evaluate Written Answer (Mains)
    eval_resp = client.post("/api/upsc/evaluate-written", json={
        "student_id": sid,
        "question_id": prompt_sample["question_id"],
        "student_answer": (
            "The basic structure doctrine, propounded in Kesavananda Bharati (1973), limits parliamentary amending power under Article 368. "
            "It safeguards judicial review, rule of law, and democratic separation of powers while maintaining constitutional equilibrium."
        ),
        "time_taken_seconds": 480
    })
    assert eval_resp.status_code == 200
    eval_data = eval_resp.json()
    assert "total_score" in eval_data
    assert "rubric_scores" in eval_data
    assert "ai_feedback_summary" in eval_data or "feedback_summary" in eval_data

    # 4. Fetch student's UPSC written submission history
    hist_resp = client.get(f"/api/upsc/history/{sid}")
    assert hist_resp.status_code == 200
    upsc_history = hist_resp.json()
    assert len(upsc_history) >= 1
    assert upsc_history[0]["question_id"] == prompt_sample["question_id"]


# ---------------------------------------------------------------------------
# 12. Zero Compulsory Gating & Standby Engine Operation (Minute Zero Access)
# ---------------------------------------------------------------------------
def test_zero_compulsory_gating_and_standby_engines():
    """
    Verifies that a newly registered student has immediate, unrestricted access
    to all intelligence and study engines without having to take a compulsory quiz first.
    """
    reg = client.post("/api/auth/register", json={
        "name": "Zero Gate Candidate",
        "email": f"standby_{uuid.uuid4().hex[:6]}@example.com",
        "password": "pass_standby_123",
        "target_exam": "NEET",
        "daily_available_hours": 4.0
    }).json()
    sid = reg["student_id"]

    # 1. Active Roadmap is immediately ready upon registration
    rm_resp = client.get(f"/api/roadmap/active/{sid}")
    assert rm_resp.status_code == 200
    rm_data = rm_resp.json()
    assert "roadmap_id" in rm_data
    assert len(rm_data["actions"]) >= 1
    assert rm_data["actions"][0]["subject"] in ["Biology", "Physics", "Chemistry", "General"]

    # 2. Next Best Action is immediately available
    nba_resp = client.get(f"/api/roadmap/next-action/{sid}")
    assert nba_resp.status_code == 200
    nba_data = nba_resp.json()
    assert nba_data is not None
    assert "action_type" in nba_data
    assert "concept_id" in nba_data

    # 3. AI Mentor provides Standby Diagnostic Profile (no compulsory demand)
    ai_mistake = client.post(f"/api/ai/chat/{sid}", json={
        "message": "Analyze my mistakes and test errors"
    })
    assert ai_mistake.status_code == 200
    m_reply = ai_mistake.json()["response"]
    assert "Standby Diagnostic Profile" in m_reply
    assert "No compulsory quiz is required" in m_reply or "standby" in m_reply.lower()

    # 4. AI Mentor explains Roadmap without quiz requirement
    ai_rm = client.post(f"/api/ai/chat/{sid}", json={
        "message": "Explain my study roadmap and next steps"
    })
    assert ai_rm.status_code == 200
    rm_reply = ai_rm.json()["response"]
    assert "Dynamic DAG Priority Engine" in rm_reply or "Roadmap" in rm_reply

    # 5. Daily 3-Subject Interleaved Assignment is immediately accessible
    daily_resp = client.get(f"/api/assignments/today/{sid}?questions_per_subject=5")
    assert daily_resp.status_code == 200
    daily_data = daily_resp.json()
    assert daily_data["exam"] == "NEET"
    assert len(daily_data["subjects"]) >= 3

    # 6. Report Card is immediately viewable with populated milestones
    report_resp = client.get(f"/api/supporting/report-card/{sid}")
    assert report_resp.status_code == 200
    report_data = report_resp.json()
    assert report_data["student"]["name"] == "Zero Gate Candidate"
    assert len(report_data["upcoming_milestones"]) >= 1

    # 7. Priorities and foundational gaps are calculated out-of-the-box
    prio_resp = client.get(f"/api/roadmap/priorities/{sid}")
    assert prio_resp.status_code == 200
    prios = prio_resp.json()
    assert len(prios) >= 1

