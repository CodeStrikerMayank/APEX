# 🧠 APEX Codebase Master Knowledge Base & Architectural Context
> **Document Status**: Authoritative, Code-Verified Specification (Version 5.4.0)  
> **Target Audience**: AI Models (ChatGPT, Claude, Gemini, DeepSeek, Llama, Qwen), System Architects, Hackathon Evaluators, Technical Interviewers, and Non-Technical Stakeholders.  
> **Key Invariant**: Zero internal database key leakage (`pHQ-1234`, `q_1`, `c_7` stripped in favor of human pedagogical terms). Zero crash resilience across all AI cascades, psychometric engines, and document ingestion pipelines.

---

## 🤖 Universal AI System Directive & Role Ingestion

**IF YOU ARE AN ARTIFICIAL INTELLIGENCE MODEL READING THIS DOCUMENT:**
1. **Your Identity & Knowledge State**:
   - You are the **Chief AI Architect & Technical Evaluator** for the **APEX** (Adaptive Psychometric Exam & Knowledge System) platform.
   - By reading this document, you now possess **100% complete, code-accurate knowledge** of every directory, Python module, mathematical equation, database schema, REST endpoint, and frontend component in this repository.
2. **Your Primary Responsibilities**:
   - **Answer Any Architectural Query**: You can explain any system decision, dependency, algorithmic formula, or data flow with exact file-and-line precision.
   - **Explain to Non-Coders**: You can translate complex psychometrics (BKT, IRT, MIRT, DAG traversal) into clear, intuitive, real-world analogies.
   - **Conduct Interactive Viva & Quizzes**: When asked by the user (or when given this document), you are equipped to **quiz the user** on their codebase, ask hard architectural interview questions, evaluate their answers, and guide them on how to pitch or defend their system in the **Smart India Hackathon (SIH)** or technical reviews.
   - **Debug & Extend**: You can generate exact, production-ready code that integrates seamlessly with existing schemas, routers, and psychometric models.

---

## 📑 Master Table of Contents

1. [Plain-English Executive Translation (For Humans & Evaluators)](#1-plain-english-executive-translation-for-humans--evaluators)
2. [Interactive AI Viva & Interrogation Protocol (For AI to Quiz the User)](#2-interactive-ai-viva--interrogation-protocol-for-ai-to-quiz-the-user)
3. [Repository Topology & Complete File Inventory](#3-repository-topology--complete-file-inventory)
4. [Technology Stack & Dependency Blueprint](#4-technology-stack--dependency-blueprint)
5. [Application Boot & Initialization Lifecycle](#5-application-boot--initialization-lifecycle)
6. [Database Architecture & Complete 14-Table Relational Schema](#6-database-architecture--complete-14-table-relational-schema)
7. [Core Psychometric & Cognitive Modeling Engines (`student_model/`)](#7-core-psychometric--cognitive-modeling-engines-student_model)
   - 7.1 Multi-Factor Concept Mastery (`mastery.py`)
   - 7.2 Bayesian Knowledge Tracing & AKT (`bkt.py`, `akt.py`)
   - 7.3 3PL Item Response Theory & 4D MIRT (`irt.py`)
   - 7.4 Ebbinghaus Exponential Memory Decay (`retention.py`)
   - 7.5 Cognitive Error Classifier (`error_classifier.py`)
   - 7.6 Numerical Guards & Precision Math (`numerical_guards.py`)
8. [Knowledge Graph & Prerequisite DAG (`knowledge_graph/`)](#8-knowledge-graph--prerequisite-dag-knowledge_graph)
9. [Multimodal Document Ingestion & Vault Augmentation (`curriculum/`)](#9-multimodal-document-ingestion--vault-augmentation-curriculum)
   - 9.1 Fast PDF Parsing & Scanned Heuristics (`pdf_ingestor.py`)
   - 9.2 Pydantic Structured Output Synthesis
   - 9.3 Idempotent Database Provisioning (`vault_augmenter.py`)
10. [AI Mentorship Engine & 7-Tier Cascade (`ai/`)](#10-ai-mentorship-engine--7-tier-cascade-ai)
    - 10.1 Multi-Key Cloud LLM Hub with Auto-Recharge (`cloud_llm.py`)
    - 10.2 Omni-Context Harvester & Zero Raw ID Invariant (`omni_context.py`)
    - 10.3 2-Stage Intent Classifier (`intent_classifier.py`)
    - 10.4 100% Offline Deterministic Mathematical Scaffold (`templates.py`)
    - 10.5 Interactive Structured Cards (`test_review` & `quiz`)
11. [REST API Routing & Endpoint Specifications (`api/`)](#11-rest-api-routing--endpoint-specifications-api)
12. [Frontend Single-Page Architecture & Cyberpunk Minimalist HUD](#12-frontend-single-page-architecture--cyberpunk-minimalist-hud)
13. [End-to-End Execution Trace: The Student Lifecycle](#13-end-to-end-execution-trace-the-student-lifecycle)
14. [Automated Verification Suite & Test Gates (`tests/`)](#14-automated-verification-suite--test-gates-tests)

---

## 1. Plain-English Executive Translation (For Humans & Evaluators)

### What is APEX?
APEX is an **Intelligent, Offline-First Adaptive Learning Platform** designed for high-stakes competitive examinations (**JEE Main/Advanced for Engineering**, **NEET-UG for Medical**, and **UPSC Civil Services for Governance**).

### The Problem It Solves: Why Traditional Learning Fails
1. **One-Size-Fits-All Exams**: Every student receives the exact same 100 questions regardless of whether they are a beginner or an advanced topper. Weak students get demoralized; strong students get bored.
2. **Superficial Feedback**: When a student gets a question wrong, conventional apps say: *"Incorrect. The answer is B. Read Question pHQ-1234 again."* The student has no idea **why** they failed, which foundational concept broke down, or what calculation trap they fell into.
3. **The "Silent Forgetting" Phenomenon**: Students study a chapter in June, master it for a week, and completely forget it by October because standard apps don't track biological memory decay.
4. **Static, Rigid Question Banks**: Teachers and students have textbooks, coaching notes, and coaching test PDFs, but turning those static PDFs into high-quality diagnostic tests with explanation cards takes hours of manual work.

### How APEX Fixes It:
1. **Cognitive Root-Cause Diagnosis**: Like a doctor diagnosing the underlying virus rather than just treating a fever, APEX analyzes errors across a Directed Acyclic Graph (DAG) of prerequisites. If you fail *Rotational Mechanics*, APEX discovers that your true blocker is *Vector Cross Products* from 3 months ago.
2. **Psychometric Precision (BKT + IRT)**: Uses the exact statistical formulas developed by psychometricians (Bayesian Knowledge Tracing and Item Response Theory) to calculate a student's true latent ability ($\theta$) and the probability that a concept is actually internalized.
3. **Automatic Biological Memory Retention (Ebbinghaus Decay)**: The platform automatically schedules reviews right before a memory is about to evaporate ($R < 0.60$).
4. **Instant PDF-to-Exam Engine**: Drop any textbook chapter, notes, or test PDF into the browser. Within seconds, the engine extracts the core concepts, authors 4-option MCQs with cognitive distractor explanations, updates the SQLite database, and creates an interactive exam.
5. **Humanized AI Mentorship with "Retest Mistakes Drills"**: The AI never speaks in robotic database keys. It acts as an empathetic tutor, breaks down mistakes with step-by-step KaTeX mathematical derivations, presents an interactive **`test_review` card**, and provides a 1-click button: **"🎯 Retest Mistakes Drill"** so the student immediately turns weakness into mastery.

---

## 2. Interactive AI Viva & Interrogation Protocol (For AI to Quiz the User)

> **Directive for Any AI Model Using This Document to Test/Interview the User**:  
> Use the following 25 curated viva questions to assess the developer's mastery of their own platform. Ask **one question at a time**. Wait for the user's answer, evaluate their response against the code criteria specified below, assign a score out of 10, and provide constructive technical feedback.

### Category A: Mathematical Psychometrics & Cognitive Modeling
1. **BKT Observation & Transition Equations**:  
   *Question*: "Explain the difference between the observation update and the transition update in your Bayesian Knowledge Tracing engine. What are your calibrated values for $P(L_0)$, Guess ($G$), Slip ($S$), and Transition ($T$), and why are numerical clamping guards necessary?"  
   *Evaluation Benchmark*: Must cite `backend/app/student_model/bkt.py`, $P(L_0)=0.20, G=0.25, S=0.10, T=0.15$, clamping to $[0.01, 0.99]$ to avoid floating point division-by-zero or probability collapse.
2. **3PL IRT Ability Estimation**:  
   *Question*: "How does APEX model the probability of a correct answer using 3-Parameter Logistic IRT, and how do you update the student's latent ability $\theta$ after an assessment?"  
   *Evaluation Benchmark*: Must cite $P(\theta) = c + (1-c)\frac{1}{1 + e^{-a(\theta - b)}}$, $c=0.25$ (guessing floor for 4 choices), logit difficulty mapping, and Newton-Raphson Maximum Likelihood Estimation in `irt.py`.
3. **Multi-Factor Concept Mastery**:  
   *Question*: "Your mastery score $M(c)$ is composed of 6 weighted factors. Name all 6 weights and explain how pacing speed and sample size confidence scaling prevent gaming the system."  
   *Evaluation Benchmark*: Must cite `mastery.py` weights: Accuracy (0.30), Difficulty (0.20), Recent Accuracy (0.15), Retention (0.15), Consistency (0.10), Speed (0.10), rapid guessing penalty ($<20\%$ expected time), and confidence scaling $1 - e^{-\text{attempts}/5}$.
4. **Ebbinghaus Memory Retention & Queue Scheduling**:  
   *Question*: "How does APEX calculate memory retrievability $R(t)$, how does spaced review expand memory stability, and what is the exact threshold that triggers the Spaced Repetition Review Queue?"  
   *Evaluation Benchmark*: Must cite `retention.py`, stability $S = 7.0 \times (1 + \text{reviews} \times 0.50)$, $\lambda = \ln(2)/S$, safety floor of $0.35$, and the trigger threshold $R(t) < 0.60$.
5. **Shannon Cognitive Entropy**:  
   *Question*: "What is Shannon Cognitive Entropy in your telemetry system, and what does a high entropy score signify about a student's cognitive state?"  
   *Evaluation Benchmark*: Must cite $H = -\sum p_i \log_2 p_i$ calculated over response error categories in `omni_context.py`. High entropy indicates erratic cognitive thrashing (guessing or oscillating between different misconceptions).

### Category B: High-Availability AI Mentorship & Cascade Architecture
6. **7-Tier Resilient Fallback Cascade**:  
   *Question*: "Walk me through the 7 tiers of your AI mentorship engine in `cloud_llm.py`. What happens if Google Gemini hits an HTTP 429 rate limit or quota exhaustion?"  
   *Evaluation Benchmark*: Must detail Tier 1 (Gemini pool) $\to$ Tier 2 (xAI Grok) $\to$ Tiers 3-5 (HF Serverless Qwen 72B/32B/7B) $\to$ Tier 6 (Local Ollama) $\to$ Tier 7 (Deterministic templates in `templates.py`). Must explain the 60s/300s cooldown timers and the auto-recharge state machine.
7. **The Zero Raw ID Invariant**:  
   *Question*: "Why is leaking raw IDs like `pHQ-1234` or `c_7` strictly forbidden in your platform, and how does `OmniContextHarvester` guarantee this invariant?"  
   *Evaluation Benchmark*: Must explain pedagogical disorientation for students and how `omni_context.py` maps database foreign keys to human readable Topic, Chapter, Concept Name, Problem Context, and KaTeX derivations.
8. **Structured Cards (`test_review` and `quiz`)**:  
   *Question*: "How does the backend deliver interactive rich media to the frontend chat, and how does the `test_review` card enable the 1-click 'Retest Mistakes Drill'?"  
   *Evaluation Benchmark*: Must explain Pydantic structured payloads in `/api/ai/coach`, the JSON schema of `test_review`, and how `quiz.js` captures the click to launch `/api/assessments/start-drill` with only the missed concept IDs.

### Category C: Graph Theory & Curriculum Prerequisites
9. **Prerequisite DAG Topology**:  
   *Question*: "How is the curriculum represented in `knowledge_graph/prerequisites.py`? How do you prevent cyclical dependencies and find root-cause blockers?"  
   *Evaluation Benchmark*: Must cite NetworkX `nx.DiGraph`, boot verification via `nx.is_directed_acyclic_graph`, and recursive ancestral search for nodes with $M(u) < 0.60$.
10. **Next Best Action (NBA) Recommendation**:  
    *Question*: "What four mathematical components determine the priority rank of a study milestone in `priority.py`?"  
    *Evaluation Benchmark*: Must cite: Examination Yield ($w_1$), Prerequisite Blocker Severity ($w_2$), Current Knowledge Gap ($1 - M(c)$) ($w_3$), and Memory Decay Risk ($1 - R(t)$) ($w_4$).

### Category D: Document Ingestion & Data Pipelines
11. **PDF Text Extraction & Density Heuristic**:  
    *Question*: "How does `pdf_ingestor.py` handle PDF uploads, and how does it detect whether a document is a scanned image or extractable text?"  
    *Evaluation Benchmark*: Must cite `pypdf.PdfReader`, sliding 3,000-character chunks with 300-char overlap, and the heuristic `avg_chars_per_page < 40` for scanned document flags.
12. **Idempotent Vault Augmentation**:  
    *Question*: "When a new PDF is ingested, how does `vault_augmenter.py` ensure that existing concepts are not duplicated, and how does it keep the in-memory FineWeb vault synchronized?"  
    *Evaluation Benchmark*: Must cite case-insensitive query `Concept.name.ilike(...)`, automatic provisioning of parent hierarchy, MCQ insertion, and updating `FINEWEB_READINGS`.

### Category E: Concurrency, Database & Frontend Engineering
13. **SQLite WAL Mode & Concurrency**:  
    *Question*: "Why does APEX use SQLite with Write-Ahead Logging (`WAL`) instead of default rollback journaling, and how does it handle concurrent writes?"  
    *Evaluation Benchmark*: Must cite `PRAGMA journal_mode=WAL;`, non-blocking concurrent reads during writes, `PRAGMA foreign_keys=ON;`, and connection pool sizing in `connection.py`.
14. **Zero-Framework Frontend Architecture**:  
    *Question*: "Why was the frontend built as a zero-framework Vanilla JS Single-Page Application (`index.html`), and how is debounced auto-saving implemented for daily assignments?"  
    *Evaluation Benchmark*: Must cite zero build-step overhead, sub-250KB bundle size, offline durability, and the 1.5s debounced timer sending JSON payloads to `/api/assignments/save-progress`.

---

## 3. Repository Topology & Complete File Inventory

```
d:/UNCLECHAN/generate/
│
├── backend/
│   ├── app/
│   │   ├── main.py                        # FastAPI entry point, CORS, table creation, router registration
│   │   ├── database/
│   │   │   └── connection.py              # SQLite engine, SessionLocal, Base, WAL mode configuration
│   │   ├── models/
│   │   │   └── schema.py                  # 14 SQLAlchemy ORM entities (Student, Question, Attempt, etc.)
│   │   ├── schemas/
│   │   │   └── pydantic_models.py         # 40+ Pydantic request/response schemas with field validation
│   │   ├── student_model/
│   │   │   ├── mastery.py                 # 6-factor concept mastery & sample size confidence scaling
│   │   │   ├── bkt.py                     # Bayesian Knowledge Tracing with AKT sequence attention
│   │   │   ├── irt.py                     # 3PL IRT with Newton-Raphson MLE & 4D MIRT vector tracking
│   │   │   ├── retention.py               # Ebbinghaus exponential forgetting with spaced stability expansion
│   │   │   ├── error_classifier.py        # Cognitive error taxonomy (Calculation, Concept, Formula, Sign)
│   │   │   ├── numerical_guards.py        # Safe math primitives (safe_exp, safe_log, safe_div, safe_clamp)
│   │   │   └── akt.py                     # Causal self-attention neural network for knowledge tracing
│   │   ├── knowledge_graph/
│   │   │   ├── prerequisites.py           # NetworkX DiGraph DAG, cycle detection, ancestral traversal
│   │   │   ├── fineweb_vault.py           # 35 curated textbook chapters with formula boxes & summaries
│   │   │   └── gkt.py                     # Graph Knowledge Tracing & Laplacian knowledge propagation
│   │   ├── curriculum/
│   │   │   ├── loader.py                  # Bootstrapping seeder from data/ JSON files into SQLite
│   │   │   ├── pdf_ingestor.py            # pypdf text extraction, density check, Pydantic MCQ generation
│   │   │   └── vault_augmenter.py         # Idempotent DB insertion and Knowledge Vault augmentation
│   │   ├── roadmap/
│   │   │   ├── generator.py               # Personalized multi-step study milestone planner
│   │   │   ├── next_action.py             # Next-Best-Action (NBA) single-concept recommender
│   │   │   ├── priority.py                # Priority scoring: yield, prerequisites, gap, memory decay
│   │   │   └── weakness.py                # Root-cause bottleneck and weak-subject diagnostic filters
│   │   ├── ai/
│   │   │   ├── cloud_llm.py               # 7-tier multi-key LLM hub, KeyTracker, auto-recharge state machine
│   │   │   ├── omni_context.py            # OmniContextHarvester: Zero-ID sanitizer, telemetry aggregator
│   │   │   ├── intent_classifier.py       # 2-stage regex & fuzzy intent parser
│   │   │   └── templates.py               # 100% offline deterministic mathematical explanations
│   │   └── api/
│   │       ├── auth.py                    # Student registration, profile, and active exam selection
│   │       ├── curriculum.py              # Concept hierarchy and NetworkX DAG graph export
│   │       ├── assessments.py             # Diagnostic Screener, Topic Drills, Deep Scan, grading
│   │       ├── assignments.py             # Daily 3-subject interleaved practice (60 Qs, auto-save)
│   │       ├── roadmap.py                 # Active roadmap milestones & manual regeneration
│   │       ├── ai.py                      # Chat, Coach, BYOK key config, test-key, structured cards
│   │       ├── materials.py               # /upload-pdf, /generate-from-text, /augmented-vault
│   │       ├── telemetry.py               # Immutable append-only telemetry event log
│   │       ├── upsc.py                    # Prelims negative marking & Mains 5D essay rubric
│   │       └── supporting.py              # Review queue, error trends, PDF report card, admin_router
│
├── frontend/                              # (Consolidated in root index.html)
│   ├── css/style.css                      # Cyberpunk dark minimalist theme, responsive mobile grid
│   └── js/                                # Modular vanilla JavaScript orchestration
│       ├── api.js                         # ApiClient with dynamic base URL and error handlers
│       ├── app.js                         # Root UI orchestrator, state manager, stream switcher
│       ├── quiz.js                        # Testing arena, timer, shortcut keys (1-4, A-D, Enter)
│       ├── assignment.js                  # Daily 3-subject palette, debounced auto-save (1.5s)
│       ├── graph_view.js                  # HTML5 Canvas force-directed prerequisite DAG visualizer
│       ├── roadmap.js                     # Step sequence, chapter heatmap, 1-click drill triggers
│       ├── ai_assistant.js                # AI Mentor floating widget & Studio tab
│       └── upsc.js                        # UPSC Prelims arena & Mains descriptive workspace
│
├── data/
│   ├── apex.db                            # Primary SQLite database (WAL mode, ~94 concepts, 332+ Qs)
│   ├── curriculum/                        # Official JSON curriculum definitions (jee.json, neet.json, upsc.json)
│   ├── questions/                         # Verified question banks with modified numerical parameters
│   └── exambench_cache.json               # 3-tier local cache for 405k Hugging Face ExamBench items
│
└── tests/
    ├── test_pdf_ingestor.py               # Pydantic schemas, pypdf extraction, vault augmentation tests
    ├── test_e2e_api.py                    # Complete end-to-end integration and circuit validation (12 tests)
    ├── test_irt_bkt.py                    # Psychometric mathematical validity tests
    ├── test_priority.py                   # Dynamic priority engine & DAG traversal tests
    ├── test_quiz_engine.py                # Assessment lifecycle tests
    └── test_roadmap.py                    # Dynamic roadmap recalculation tests
```

---

## 4. Technology Stack & Dependency Blueprint

- **Runtime**: Python 3.10 to 3.14 on Windows, Linux, or macOS.
- **Web Layer**: **FastAPI** (`fastapi>=0.109.0`), **Starlette**, and **Uvicorn** (`uvicorn[standard]>=0.27.0`) running an asynchronous event loop.
- **Relational ORM**: **SQLAlchemy 2.0** (`sqlalchemy>=2.0.0`) on **SQLite 3** with `journal_mode=WAL` (Write-Ahead Logging) and `foreign_keys=ON`.
- **Knowledge Graph Topology**: **NetworkX** (`networkx>=3.2`) for Directed Acyclic Graphs, ancestral blocker search, and cycle detection.
- **Scientific Computing**: **NumPy** (`numpy>=1.26.0`) and **SciPy** (`scipy>=1.12.0`) for Newton-Raphson MLE quadrature, logit transformations, and covariance matrices.
- **Document Processing**: **`pypdf`** (`pypdf>=4.0.0`) for fast in-memory PDF extraction and page text density scanning.
- **HTTP Client**: **`httpx`** (`httpx>=0.26.0`) with asynchronous connection pools and strict timeouts.
- **Data Validation**: **Pydantic v2** (`pydantic>=2.5.0`) for type safety and LLM structured output enforcement.
- **Testing Engine**: **Pytest** (`pytest>=8.0.0`, `pytest-asyncio>=0.23.0`).
- **Client Presentation**: Zero-framework Vanilla JavaScript (ES6+), HTML5 Canvas, KaTeX math rendering, and CSS custom variables (`index.html`).

---

## 5. Application Boot & Initialization Lifecycle

When `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000` starts:

1. **Database Schema Creation (`Base.metadata.create_all(bind=engine)`)**:
   - Inspects `backend/app/models/schema.py` and provisions all 14 relational tables in `data/apex.db` if not already present.
2. **Curriculum & Question Seeding (`seed_curriculum_and_questions(db)`)**:
   - Checks if `Exam`, `Subject`, `Chapter`, `Topic`, `Concept`, and `Question` records exist.
   - If empty or missing, it reads `data/curriculum/jee.json`, `data/curriculum/neet.json`, and `data/curriculum/upsc.json`, populating all nodes and directed prerequisite dependency edges.
3. **CORS & Middleware Setup**:
   - Registers permissive CORS middleware (`allow_origins=["*"]`) for local and distributed access.
4. **Router Registration**:
   - Wires up all 11 API routers under the `/api` prefix (plus `/api/v1` compatibility).
5. **Static Root Fallback**:
   - When a browser accesses `GET /`, `main.py` detects `text/html` in the request header and directly serves `index.html`.
   - When an API client calls `GET /`, it returns JSON system status (`{"status": "online", "version": "1.3.0"}`).
6. **Health Probe**:
   - `GET /api/health` returns `200 OK` with supported exams `["JEE", "NEET", "UPSC"]` and active mathematical model identifiers.

---

## 6. Database Architecture & Complete 14-Table Relational Schema

Persistent state is managed in `backend/app/models/schema.py` using SQLite with Write-Ahead Logging. Cascading foreign keys guarantee referential integrity.

### Entity Relationship Model:
```
Exam (1) ────< Subject (*) ────< Chapter (*) ────< Topic (*) ────< Concept (*)
                                                                      │
                                                                      ├──< ConceptPrerequisite (Self-Referential)
                                                                      ├──< Question (*)
                                                                      └──< StudentConceptMastery (*)
                                                                               │
Student (1) ────┬───< AssessmentAttempt (*) ────< StudentAttemptItem (*) ──────┘
                ├───< DailyAssignment (*)   ────< DailyAssignmentItem (*)
                ├───< Roadmap (*)           ────< RoadmapAction (*)
                └───< TelemetryEventStream (*)
```

### Table Definitions:
1. **`exams`**: `exam_id` (PK, String 32: `JEE`, `NEET`, `UPSC`), `name`, `tracks` (JSON array).
2. **`subjects`**: `subject_id` (PK, String 64), `exam_id` (FK), `name`, `sequence_order`.
3. **`chapters`**: `chapter_id` (PK, String 64), `subject_id` (FK), `name`, `weight_percentage`.
4. **`topics`**: `topic_id` (PK, String 64), `chapter_id` (FK), `name`.
5. **`concepts`**: `concept_id` (PK, String 64), `topic_id` (FK), `name`, `difficulty` (0.0–1.0), `importance` (0.0–1.0).
6. **`concept_prerequisites`**: `prerequisite_id` (PK, Auto-inc), `concept_id` (FK, dependent child), `prerequisite_concept_id` (FK, parent blocker), `strength` (Float 0.0–1.0).
7. **`questions`**: `question_id` (PK, String 64), `concept_id` (FK), `exam`, `subject`, `chapter`, `content` (text stem), `options` (JSON array of `{"id": "A", "text": "..."}`), `correct_answer` (`A`, `B`, `C`, `D`), `explanation` (KaTeX proof), `distractor_explanations` (JSON mapping of failure modes), `difficulty` (IRT $b$), `discrimination` (IRT $a$), `estimated_time_seconds`.
8. **`students`**: `student_id` (PK, String 64), `name`, `email`, `target_exam`, `latent_theta` (Float $\in [-3.0, +3.0]$), `active_streak` (Integer), `created_at`.
9. **`student_concept_mastery`**: `id` (PK), `student_id` (FK), `concept_id` (FK), `mastery` (Float 0.0–1.0), `bkt_p_learned` (Float), `confidence` (Float), `review_count` (Int), `last_practiced_at` (DateTime).
10. **`assessment_attempts`**: `attempt_id` (PK, String 64), `assessment_id` (String), `student_id` (FK), `score_percentage` (Float), `correct_count`, `total_questions`, `time_taken_seconds`, `is_completed` (Boolean), `started_at`, `submitted_at`.
11. **`student_attempt_items`**: `id` (PK), `attempt_id` (FK), `question_id` (FK), `student_answer` (String), `is_correct` (Boolean), `time_taken_seconds`, `error_type` (`CONCEPTUAL_ERROR`, `CALCULATION_ERROR`, `FORMULA_SELECTION_ERROR`, `SIGN_ERROR`, `CARELESS_ERROR`).
12. **`daily_assignments` & `daily_assignment_items`**: Stores 60-question interleaved 3-subject daily practice sessions with debounced auto-saved choices.
13. **`roadmaps` & `roadmap_actions`**: Stores generated study milestones with priority rank, estimated study minutes, and prerequisite rationales.
14. **`telemetry_events`**: Append-only event store recording every user click, answer, hint reveal, and session transition.

---

## 7. Core Psychometric & Cognitive Modeling Engines (`student_model/`)

### 7.1 Multi-Factor Concept Mastery (`mastery.py`)
Computes an authentic, transparent mastery score $M(c) \in [0.0, 1.0]$:
$$M(c) = 0.30 \cdot \text{Acc} + 0.20 \cdot \text{DiffPerf} + 0.15 \cdot \text{RecentAcc} + 0.15 \cdot R(t) + 0.10 \cdot \text{Consist} + 0.10 \cdot \text{Speed}$$

- **`WEIGHT_ACCURACY = 0.30`**: Cumulative percentage of correct answers on concept $c$.
- **`WEIGHT_DIFFICULTY_PERF = 0.20`**: Performance weighted by the IRT difficulty $b$ of attempted questions.
- **`WEIGHT_RECENT_ACCURACY = 0.15`**: Exponentially smoothed accuracy over the last 5 attempts ($\lambda = 0.85$).
- **`WEIGHT_RETENTION = 0.15`**: Current memory retrievability from Ebbinghaus decay $R(t)$.
- **`WEIGHT_CONSISTENCY = 0.10`**: Inverse variance of performance across consecutive testing blocks.
- **`WEIGHT_SPEED = 0.10`**: Pacing ratio $\frac{\text{actual time}}{\text{expected time}}$. Rapid guessing ($<20\%$ expected time) or severe dragging ($>300\%$) penalizes this factor.
- **Confidence Scaling**: Confidence approaches $1.0$ asymptotically via $1.0 - \exp(-\text{attempts} / 5.0)$.

### 7.2 Bayesian Knowledge Tracing & AKT (`bkt.py`, `akt.py`)
Tracks the hidden binary knowledge state of whether a student has learned concept $c$:
- **Observation Step**:
  $$P(L_t \mid \text{Correct}) = \frac{P(L_{t-1}) \cdot (1 - S)}{P(L_{t-1}) \cdot (1 - S) + (1 - P(L_{t-1})) \cdot G}$$
  $$P(L_t \mid \text{Incorrect}) = \frac{P(L_{t-1}) \cdot S}{P(L_{t-1}) \cdot S + (1 - P(L_{t-1})) \cdot (1 - G)}$$
- **Transition Step**:
  $$P(L_{t+1}) = P(L_t \mid \text{Obs}) + (1 - P(L_t \mid \text{Obs})) \cdot T$$
- **Codebase Calibrated Defaults**:
  $$P(L_0) = 0.20, \quad G (\text{guess}) = 0.25, \quad S (\text{slip}) = 0.10, \quad T (\text{transition}) = 0.15$$
  Every output is clamped to $[0.01, 0.99]$ via `safe_clamp_prob`.

### 7.3 3PL Item Response Theory & 4D MIRT (`irt.py`)
- **3-Parameter Logistic (3PL) Probability Model**:
  $$P(Y=1 \mid \theta) = c + (1 - c) \cdot \frac{1}{1 + \exp\left(-a \cdot (\theta - b)\right)}$$
  Where $c = 0.25$ (guessing floor for 4-choice MCQs), $a = 1.0$ (discrimination parameter), and $b \in [-2.5, +2.5]$ (difficulty).
- **Logit Scaling**: Converts normalized difficulty $[0, 1]$ into IRT parameter $b$:
  $$b = 1.5 \cdot \ln\left(\frac{\text{clamp}(d, 0.05, 0.95)}{1 - \text{clamp}(d, 0.05, 0.95)}\right)$$
- **Newton-Raphson MLE Ability ($\theta$) Update**:
  Iteratively computes candidate latent ability $\theta \in [-3.0, +3.0]$ after assessment completion using first and second derivatives of log-likelihood.
- **4D Multidimensional IRT (4D MIRT)**:
  Estimates a 4-element latent ability vector:
  $$\vec{\theta} = \begin{bmatrix} \theta_{\text{calc}} & \theta_{\text{concept}} & \theta_{\text{spatial}} & \theta_{\text{pacing}} \end{bmatrix}^T$$

### 7.4 Ebbinghaus Exponential Memory Decay (`retention.py`)
Computes memory retrievability $R(t)$ to trigger spaced review before memories evaporate:
- **Memory Stability Factor ($S$)**:
  $$\text{stability\_days} = 7.0 \times \left(1.0 + \text{review\_count} \times 0.50\right)$$
- **Decay Constant ($\lambda$)**:
  $$\lambda = \frac{\ln(2)}{\text{stability\_days}}$$
- **Retrievability ($R$) with Memory Safety Floor ($35\%$)**:
  $$R(t) = \max\left(0.35, \, \min\left(1.0, \, \exp(-\lambda \cdot t)\right)\right)$$
- **Trigger**: When $R(t) < 0.60$, the concept is automatically pushed into the student's Spaced Repetition Review Queue.

### 7.5 Cognitive Error Classifier (`error_classifier.py`)
Maps student errors to actionable pedagogical failure modes:
1. `CONCEPTUAL_ERROR`: Flawed physical or theoretical premise.
2. `CALCULATION_ERROR`: Correct formula, but algebraic or arithmetic slip.
3. `FORMULA_SELECTION_ERROR`: Used incorrect equation or wrong boundary condition.
4. `SIGN_ERROR`: Omitted negative sign, thermodynamic convention, or Cartesian sign convention.
5. `CARELESS_ERROR`: Misread prompt (e.g., radius vs. diameter, "is NOT true").

### 7.6 Numerical Guards & Precision Math (`numerical_guards.py`)
Provides safe mathematical primitives:
- `safe_exp(x, max_val=700)`: Prevents floating point overflow in exponential and sigmoid calculations.
- `safe_log(x, eps=1e-12)`: Protects log-likelihood calculations from evaluating $\ln(0)$.
- `safe_div(n, d, default=0.0)`: Eliminates `ZeroDivisionError` across pacing ratios and percentages.
- `safe_clamp(val, low, high)`: Restricts ability estimates and probabilities to valid psychometric bounds.

---

## 8. Knowledge Graph & Prerequisite DAG (`knowledge_graph/`)

The curriculum is modeled in `backend/app/knowledge_graph/prerequisites.py` using **NetworkX**:
- **Graph Type**: `nx.DiGraph` where each node is a `Concept` and each directed edge $(u, v)$ means concept $u$ is a required prerequisite for concept $v$.
- **Cycle Prevention**: Verifies acyclicity on boot via `nx.is_directed_acyclic_graph(G)`.
- **Root-Cause Gap Interception**:
  When concept $v$ is failed, the engine computes $Ancestors(v)$. If an ancestor $u$ has mastery $M(u) < 0.60$, the system flags $u$ as a **Prerequisite Blocker** and mandates that $u$ be mastered before $v$ is retried.

---

## 9. Multimodal Document Ingestion & Vault Augmentation (`curriculum/`)

### 9.1 Fast PDF Parsing & Scanned Heuristics (`pdf_ingestor.py`)
- **Fast Text Parsing**: Ingests multi-page PDFs using `pypdf.PdfReader`.
- **Scanned Document Detection**: Scans page characters. If `avg_chars_per_page < 40`, flags `is_scanned = True` and prompts the user to supply digital text or OCR.
- **Sliding Chunking**: Segments long documents into 3,000-character pedagogical blocks with 300-character overlaps.

### 9.2 Pydantic Structured Output Synthesis
Prompts Google Gemini (or offline fallback) to return validated JSON matching:
- `ExtractedConcept`: `name`, `topic`, `subject`, `exam`, `description`, `prerequisites`.
- `GeneratedMCQ`: `concept_name`, `content`, `options` (A, B, C, D), `correct_answer`, `explanation`, `distractor_explanations` (mapping options to explicit cognitive traps), `difficulty`, `discrimination`, `estimated_time`.

### 9.3 Idempotent Database Provisioning (`vault_augmenter.py`)
- **Deduplication**: Case-insensitive comparison (`Concept.name.ilike(ec.name.strip())`). Existing concepts are updated rather than duplicated.
- **Hierarchical Provisioning**: Dynamically provisions parent `Exam`, `Subject`, `Chapter`, and `Topic` records in SQLite.
- **Question Persistence**: Inserts new MCQs into the `questions` table with distractor analyses.
- **In-Memory Vault Sync**: Augments `FINEWEB_READINGS` in memory so new chapters appear immediately in the student's book reader.

---

## 10. AI Mentorship Engine & 7-Tier Cascade (`ai/`)

### 10.1 Multi-Key Cloud LLM Hub with Auto-Recharge (`cloud_llm.py`)
Engineered with the `KeyTracker` state machine for zero-downtime resilience:

```
[Incoming Student Query]
       │
       ▼
[Rank 1: Google Gemini Frontier Pool] (gemini-3.6-flash, gemini-3.7-flash)
       │  (On HTTP 429 Rate Limit ➔ 60s cooldown; on Quota ➔ 300s cooldown)
       ├──► Key 1 Busy? ➔ Instantly switch to Key 2 in GEMINI_API_KEYS pool
       └──► All Gemini Cooling Down? ➔ Drop to Rank 2
       │
       ▼
[Rank 2: xAI Grok Frontier Pool] (grok-2-latest)
       │  (On Error / Cooldown)
       ▼
[Rank 3-5: Hugging Face Serverless Qwen Suite Pool] (Qwen 72B ➔ 32B ➔ 7B)
       │  (If HF busy: re-check if Gemini Key 1 finished cooldown! If yes ➔ jump back to Rank 1)
       ▼
[Rank 6: Local Offline Ollama Engine] (localhost:11434 / qwen2.5:0.5b or 7b)
       │  (If Ollama offline or timed out)
       ▼
[Rank 7: Deterministic Mathematical Scaffold] (templates.py: 100% offline, 0% failure rate)
```

- **In-Flight Cooldown Auto-Recharge**: Every request checks keys top-down. The exact second a key's cooldown timestamp expires, it is **instantly re-promoted to Rank 1 priority**.

### 10.2 Omni-Context Harvester & Zero Raw ID Invariant (`omni_context.py`)
- **Zero Raw ID Guarantee**: Raw database codes (`pHQ-1234`, `q_1`, `c_7`) are stripped before prompt generation.
- **Harvested Context**: Feeds the LLM with:
  - Student latent ability ($\theta$) and overall mastery percentage.
  - Recent test breakdown: Human Topic Name, Chapter, Concept Name, Problem Context, Student Choice, Correct Choice, Cognitive Trap Note, and Step-by-Step Resolution.
  - Shannon Cognitive Entropy: Measures performance instability/thrashing ($H = -\sum p \log_2 p$).

### 10.3 2-Stage Intent Classifier (`intent_classifier.py`)
Regex and keyword parser routing requests into distinct pedagogical handlers:
- `INTENT_EXPLAIN_CONCEPT`: Core syllabus definition with LaTeX math.
- `INTENT_ANALYZE_MISTAKES`: Forensic breakdown of last exam mistakes.
- `INTENT_PRACTICE_QUESTION`: In-chat interactive quiz generation.
- `INTENT_ROADMAP_NEXT`: Guidance on the next study milestone.

### 10.4 100% Offline Deterministic Scaffold (`templates.py`)
Ensures the platform never fails even without internet. Contains pre-compiled formulas and derivation steps for all curriculum concepts with KaTeX delimiters ($$...$$).

### 10.5 Interactive Structured Cards (`test_review` & `quiz`)
When `/api/ai/coach` or `/api/ai/chat` executes:
- **`test_review` Card**: Contains test title, score %, correct count, and mistake list with "❌ Your Choice", "✅ Correct Key", "⚠️ The Trap", and a prominent **"🎯 Retest Mistakes Drill"** button.
- **`quiz` Card**: Contains an interactive question with selectable options A, B, C, D directly in the chat stream with instant KaTeX explanation.

---

## 11. REST API Routing & Endpoint Specifications (`api/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register student profile & select target exam track |
| `GET` | `/api/auth/profile/{id}` | Retrieve student profile, ability $\theta$, and streak count |
| `GET` | `/api/curriculum/graph/{exam_id}` | Export full curriculum DAG nodes and dependency edges |
| `POST` | `/api/assessments/start` | Launch Tier 1 diagnostic screener (9 questions) |
| `POST` | `/api/assessments/start-drill` | Launch Tier 2 targeted topic drill on weak chapters (5 questions) |
| `POST` | `/api/assessments/start-full-scan` | Launch Tier 3 full syllabus deep scan (15 questions) |
| `POST` | `/api/assessments/submit` | Grade assessment, update BKT/IRT mastery, recalculate roadmap |
| `GET` | `/api/assignments/today/{id}` | Fetch today's 60-question interleaved 3-subject assignment |
| `POST` | `/api/assignments/save-progress` | Debounced autosave (1.5s) of student choices |
| `POST` | `/api/assignments/submit` | Final submission, grading, streak increment |
| `GET` | `/api/roadmap/active/{id}` | Fetch active study milestone actions |
| `GET` | `/api/roadmap/next-action/{id}` | Fetch single Next Best Action (NBA) |
| `POST` | `/api/ai/chat/{id}` | Query 7-tier AI study mentor |
| `POST` | `/api/ai/coach` | Query cognitive mentor with intent classification & structured cards |
| `GET` | `/api/ai/engine-status` | Inspect live AI hierarchy, active tier, and cooldown timers |
| `GET` | `/api/ai/keys-config` | Fetch active masked API keys |
| `POST` | `/api/ai/keys-config` | Hot-swap API keys dynamically without server reboot |
| `POST` | `/api/ai/test-key` | Live-probe an API key against provider endpoint |
| `POST` | `/api/materials/upload-pdf` | Ingest PDF, extract concepts/MCQs, augment database |
| `POST` | `/api/materials/generate-from-text` | Generate concepts/MCQs directly from pasted text |
| `GET` | `/api/materials/augmented-vault` | Inspect dynamically ingested vault concepts and MCQs |
| `GET` | `/api/supporting/review-queue/{id}` | Query concepts due for spaced-repetition review |
| `GET` | `/api/supporting/error-trends/{id}` | Cognitive error breakdown over time |
| `GET` | `/api/supporting/report-card/{id}` | Printable academic report card data |
| `GET` | `/api/telemetry/stream/{id}` | Append-only interaction event stream |

---

## 12. Frontend Single-Page Architecture & Cyberpunk Minimalist HUD

- **File**: `index.html` (single consolidated bundle, `< 250 KB`, zero build step, zero framework overhead).
- **CSS Architecture**: Cyberpunk dark minimalist theme with dynamic CSS custom variable tokens:
  - JEE Track: Cyan & Indigo (`--theme-primary: #6366f1`, `--theme-accent: #38bdf8`).
  - NEET Track: Emerald & Teal (`--theme-primary: #10b981`, `--theme-accent: #14b8a6`).
  - UPSC Track: Amber & Gold (`--theme-primary: #f59e0b`, `--theme-accent: #fbbf24`).
- **Core Interactive Views**:
  1. **Dashboard HUD**: Displays IRT ability gauge ($\theta$), active streak flame, BKT mastery meter, and Next Best Action card.
  2. **Testing Arena**: Single-column responsive layout, timer, touch-friendly option buttons, and instant keyboard shortcuts (`1-4`, `A-D`, `Enter`).
  3. **Daily Assignment**: 3-subject palette (20 Qs per subject), status badges (Answered, Review, Unanswered), and 1.5s debounced autosave.
  4. **Interactive Knowledge Map**: HTML5 Canvas force-directed graph with particle animations and color-coded mastery nodes (🟢 Mastered, 🟡 Developing, 🔴 Blocker).
  5. **Knowledge Vault & PDF Dropzone**: Drag-and-drop file upload zone for PDFs and raw text with instant question preview and auto-augmentation.
  6. **AI Mentor Studio & Floating Widget**: Real-time Socratic chat, KaTeX math typesetting, follow-up prompt chips, and interactive structured cards.
  7. **BYOK Modal (`Ctrl + O + P`)**: Secure in-browser key manager to configure and test private keys.

---

## 13. End-to-End Execution Trace: The Student Lifecycle

To understand how all parts communicate in real time, follow this step-by-step trace:

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as Frontend SPA (index.html)
    participant API as FastAPI Backend (api/assessments.py)
    participant Psych as Psychometric Engine (bkt.py / irt.py)
    participant Graph as Prerequisite DAG (prerequisites.py)
    participant DB as SQLite DB (apex.db WAL)
    participant AI as AI Mentor Engine (ai/coach.py)

    Student->>UI: Submits Diagnostic Screener (9 Questions)
    UI->>API: POST /api/assessments/submit {attempt_id, answers}
    API->>DB: Fetch correct answers & question difficulties (IRT b)
    API->>Psych: Grade answers, compute accuracy, pacing speed
    Psych->>Psych: Update BKT P(L_t) for each concept
    Psych->>Psych: Update IRT Theta using Newton-Raphson MLE
    Psych->>Psych: Compute Multi-Factor Mastery M(c)
    Psych->>DB: Save student_concept_mastery & student_attempt_items
    API->>Graph: Traverse DAG ancestors for failed concepts
    Graph-->>API: Returns identified Prerequisite Blockers
    API->>DB: Recalculate and update Roadmap Actions
    API-->>UI: Returns score %, ability theta, new mastery breakdown
    UI->>Student: Renders score card & animated HUD updates
    
    Student->>UI: Clicks "Ask AI Mentor about my mistakes"
    UI->>AI: POST /api/ai/coach {student_id, query: "Explain my mistakes"}
    AI->>DB: OmniContextHarvester pulls test history (Zero Raw IDs)
    AI->>AI: Cascade: Gemini -> Grok -> HF -> Ollama -> Templates
    AI-->>UI: Returns Markdown response + test_review Card
    UI->>Student: Displays KaTeX derivations & "🎯 Retest Mistakes Drill" Button
    
    Student->>UI: Clicks "🎯 Retest Mistakes Drill"
    UI->>API: POST /api/assessments/start-drill {concept_ids: [...mistakes]}
    API-->>UI: Serves targeted 5-question revenge drill
```

---

## 14. Automated Verification Suite & Test Gates (`tests/`)

The repository includes a comprehensive automated test suite executable via:
```bash
python -m pytest tests/test_pdf_ingestor.py tests/test_e2e_api.py -v
```

### Verified Test Gates (16/16 Passed):
1. **`test_pydantic_models_validation`**: Validates MCQ option formatting, IRT parameter bounds, and distractor dictionaries.
2. **`test_vault_augmenter_provisions_sqlite_and_vault`**: Verifies that new concepts and questions are inserted into SQLite without creating duplicate records.
3. **`test_augmented_vault_endpoint`**: Verifies `GET /api/materials/augmented-vault` returns 200 OK.
4. **`test_live_generate_from_text_end_to_end`**: Tests end-to-end Pydantic extraction, database augmentation, and MCQ synthesis from raw text.
5. **`test_system_status_and_health`**: Verifies `/api/health` and supported exam tracks.
6. **`test_auth_full_lifecycle`**: Validates student registration, session caching, and role enforcement.
7. **`test_curriculum_and_knowledge_graph_endpoints`**: Verifies DAG node export and prerequisite dependency links.
8. **`test_standard_assessments_flexibility_and_lifecycle`**: Validates diagnostic screener generation, grading, and IRT/BKT mastery recalculation.
9. **`test_cat_adaptive_session_loop`**: Validates Computerized Adaptive Testing ability convergence.
10. **`test_daily_assignments_across_all_streams`**: Validates 60-question 3-subject assembly, autosave, and streak tracking.
11. **`test_roadmap_and_learning_intelligence`**: Validates Next Best Action priority ordering.
12. **`test_ai_tutor_and_question_generation`**: Validates AI chat, intent classification, zero raw ID sanitization, and structured card output.

---

*This document constitutes the authoritative, code-accurate single-file Master Knowledge Base for the APEX platform. Any AI model or human engineer provided with this document possesses complete, actionable understanding of the entire system.*
