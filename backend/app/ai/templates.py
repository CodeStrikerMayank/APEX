"""
Humanized Pedagogical Templates for AI Study Mentor
Platform Upgrade v3.1 — Warm, Encouraging, Student-First, Zero-Hallucination
Supports: JEE Main/Advanced, NEET-UG Medical, and UPSC Civil Services
"""
from typing import Dict, Any, Optional

def format_mistake_analysis(ctx: Dict[str, Any]) -> str:
    exam = ctx.get("exam", "JEE")
    student_name = ctx.get("student_name", "Aspirant")
    attempt_info = ctx.get("latest_attempt")
    
    if not attempt_info:
        return (
            f"### 👋 Welcome, {student_name}!\n"
            f"I'm your personal academic mentor for **{exam}**. Your **Standby Diagnostic Profile** is active and ready on standby for you.\n\n"
            f"- **No Compulsory Quiz Required:** You don't have to complete a mandatory screening test before exploring. Jump straight into daily practice missions, study paths, or topic drills whenever you feel ready.\n"
            f"- **Smart Cognitive Calibration:** The moment you solve questions, I'll diagnose whether errors are from calculation slips, conceptual gaps, or time pressure, and calibrate your review schedule accordingly.\n"
            f"- **Comprehensive Concept Mentoring:** Ask me anytime to unpack complex derivations, clarify tricky syllabus concepts, or advise on exam pacing.\n\n"
            f"💡 *Ready to test your baseline? Take a quick 5-question drill or ask me to explain any tricky chapter!*"
        )

    items = attempt_info.get("items", [])
    wrong_items = [it for it in items if not it.get("is_correct")]
    score = attempt_info.get("score_percentage", 0)

    lines = [
        f"### 🤝 Hello {student_name}! Here is your {exam} Post-Test Breakdown",
        f"You scored **{score}%** ({len(items) - len(wrong_items)} out of {len(items)} correct). Every mistake is simply a clue pointing toward your next rank breakthrough!",
        ""
    ]

    if not wrong_items:
        lines.append("🎉 **Outstanding Execution! 100% Correct!**")
        lines.append(f"You demonstrated razor-sharp conceptual clarity across every question. Your latent ability $\\theta$ has leveled up. "
                     "I recommend taking on a **Tier 4 Advanced Challenge** or a timed full-syllabus revision scan to maintain your momentum!")
        return "\n".join(lines)

    lines.append(f"**Let's review the {len(wrong_items)} question(s) that tripped you up:**\n")
    for i, w in enumerate(wrong_items, 1):
        err = w.get("error_type", "CONCEPTUAL_GAP").replace("_", " ")
        q_id = w.get("question_id", "Q")
        ans = w.get("student_answer", "Skipped")
        correct = w.get("correct_answer", "-")
        time_spent = w.get("time_taken_seconds", 0)
        distractor = w.get("distractor_note")

        lines.append(f"**{i}. Question `{q_id}` — {err}**")
        lines.append(f"- Your choice: `{ans}` | Correct key: `{correct}` | Time taken: `{time_spent}s`")
        if distractor:
            lines.append(f"- 💡 *What caught you out:* {distractor}")
        lines.append("")

    lines.append("### 🌟 Your Actionable 3-Step Recovery Plan")
    lines.append("1. **Isolate the Concept:** Before moving to mixed questions, spend 5 minutes reviewing the core formula or NCERT diagram for the missed concepts above.")
    lines.append("2. **5-Question Recovery Drill:** Click the **Targeted Drill** button on your dashboard to solve 5 similar questions immediately while the fix is fresh in your mind.")
    lines.append("3. **Formula & Trap Notebook:** Note down the trap you fell for so you recognize it instantly on exam day.")
    return "\n".join(lines)


def format_roadmap_explanation(ctx: Dict[str, Any]) -> str:
    exam = ctx.get("exam", "JEE")
    student_name = ctx.get("student_name", "Aspirant")
    milestones = ctx.get("roadmap_milestones", [])

    lines = [
        f"### 🗺️ Hello {student_name}! Here is the Logic Behind Your {exam} Roadmap (Dynamic DAG Priority Engine)",
        ""
    ]

    if not milestones:
        lines.append(f"Your dynamic roadmap is generated directly from the {exam} curriculum Directed Acyclic Graph (DAG).\n"
                     "All modules are unlocked. You can jump directly into foundational or high-weightage chapters at your own pace!")
        return "\n".join(lines)

    lines.append("Instead of a generic schedule, your roadmap is tailored using our **4-Pillar Learning Engine**:\n"
                 "1. **Prerequisite Foundation First:** Concepts that unlock downstream chapters are prioritized first so you never get stuck.\n"
                 "2. **High Exam Weightage:** Topics with the highest historical question frequency are prioritized for fast score gains.\n"
                 "3. **Knowledge Tracing (BKT):** Topics where your recent practice shows hesitation are scheduled for rapid reinforcement.\n"
                 "4. **Ebbinghaus Spaced Repetition:** Timed reviews are slotted right before memory decay sets in.\n")

    lines.append("**Your Immediate Recommended Focus:**")
    for m in milestones[:4]:
        step = m.get("order", 1)
        title = m.get("title", "Action")
        atype = m.get("action_type", "").replace("_", " ")
        reason_val = m.get("reasons") or m.get("reason") or "Foundational curriculum mastery"
        reason = "; ".join(reason_val) if isinstance(reason_val, list) else str(reason_val)
        mins = m.get("estimated_minutes", 45)
        lines.append(f"- **Step {step}: {title}** (~{mins} mins)")
        lines.append(f"  *Focus:* `{atype}` | *Why:* {reason}")

    lines.append("\n✨ *Every time you complete a drill or assignment, your roadmap recalculates in real-time to match your progress.*")
    return "\n".join(lines)


def format_strategy_tips(exam: str, ctx: Dict[str, Any]) -> str:
    student_name = ctx.get("student_name", "Aspirant")
    
    if exam == "NEET":
        return (
            f"### 🧬 Hello {student_name}! Master NEET-UG 2025 Strategy (Target: 680+ / 720)\n\n"
            "As your mentor, here is the battle-tested roadmap used by top medical rankers:\n\n"
            "1. **Biology NCERT Speed Run (360 / 360 Target):**\n"
            "   - Target: Complete all 90 Biology questions in **40–45 minutes**.\n"
            "   - Focus on direct NCERT lines, floral formulas, cell cycle stages, and ecological pyramids.\n\n"
            "2. **Chemistry Two-Pass Technique:**\n"
            "   - **Pass 1 (20 mins):** Inorganic NCERT facts + Organic named reactions & reagents.\n"
            "   - **Pass 2 (25 mins):** Physical chemistry numericals with structured unit cancellation.\n\n"
            "3. **Physics Problem Selection (140+ Target):**\n"
            "   - Reserve 50–55 minutes for Physics.\n"
            "   - Do direct formula questions first (Modern Physics, Current Electricity, Thermal Physics).\n"
            "   - Save long multi-step kinematics/rotational calculations for the second pass.\n\n"
            "4. **Defending Against Negative Marking (+4 / -1):**\n"
            "   - A wrong answer costs you **5 marks** compared to a correct answer! Never blind-guess when down to 3 options."
        )
    elif exam == "UPSC":
        return (
            f"### 🏛 Hello {student_name}! Master UPSC Civil Services Strategy (Prelims & Mains)\n\n"
            "Here is your high-yield blueprint for the Civil Services Examination:\n\n"
            "1. **Prelims GS Paper I (Cutoff Target: 100+ Marks):**\n"
            "   - **Static Foundation is King:** Polity, Modern History, Economy, and Geography must have 85%+ accuracy.\n"
            "   - **Elimination Discipline:** In multi-statement questions, first locate absolute words ('strictly', 'only', 'all') to eliminate improbable choices.\n"
            "   - **Negative Marking (1/3rd = -0.66):** Aim to attempt 82–88 questions. Stop guessing when completely ungrounded.\n\n"
            "2. **CSAT Paper II (Qualifying 33% = 66.7 Marks):**\n"
            "   - Do not take CSAT lightly! Secure 30 high-accuracy quant/reasoning questions before attempting dense reading passages.\n\n"
            "3. **Mains Answer Writing Structure:**\n"
            "   - **Introduction (25-30 words):** Constitutional Article, definition, or contemporary context.\n"
            "   - **Body (150-180 words):** Sub-headings with multi-dimensional viewpoints (Social, Economic, Legal, Environmental, International).\n"
            "   - **Conclusion / Way Forward (30 words):** Balanced, optimistic, committee recommendations (e.g. Sarkaria, Punchhi, NITI Aayog)."
        )
    else:  # JEE
        return (
            f"### ⚡ Hello {student_name}! Master JEE Main & Advanced Tactics (Target: 99+ Percentile)\n\n"
            "Here is the systematic pacing blueprint for top percentile ranks:\n\n"
            "1. **The 3-Pass Exam Method:**\n"
            "   - **Pass 1 (0–50 mins):** Scan and solve all 1-minute direct questions across Chemistry and Physics.\n"
            "   - **Pass 2 (50–120 mins):** Standard calculus, mechanics, coordinate geometry, and physical chemistry numericals.\n"
            "   - **Pass 3 (120–180 mins):** High-difficulty multi-concept problems and verification of numerical values.\n\n"
            "2. **Section B Numerical Value Selection:**\n"
            "   - You only need to solve 5 out of 10! Choose the ones with clean integer solutions and direct formula applications.\n\n"
            "3. **Mathematics Time Management:**\n"
            "   - Allocate 65–70 minutes for Math. It is deliberately lengthier, so prioritize Vectors, 3D Geometry, Matrices, and Differential Equations first."
        )


def format_concept_explanation(topic_hint: Optional[str], exam: str) -> str:
    if not topic_hint:
        if exam == "UPSC":
            return (
                "### 📖 Hello! Welcome to the UPSC Concept Mentor Center\n\n"
                "I can explain any topic across Indian Polity, Economy, Geography, Environment, and Ethics!\n\n"
                "Try asking me about:\n"
                "- *'Explain Basic Structure Doctrine and Kesavananda Bharati case'*\n"
                "- *'Explain Fiscal Deficit vs Primary Deficit & FRBM Act'*\n"
                "- *'Explain Article 21 and Due Process of Law'*\n"
                "- *'Explain Inflation Targeting framework of RBI'*"
            )
        elif exam == "NEET":
            return (
                "### 📖 Hello! Welcome to the NEET Concept Mentor Center\n\n"
                "I can explain any high-yield concept across Biology (Botany & Zoology), Chemistry, and Physics!\n\n"
                "Try asking me about:\n"
                "- *'Explain Cell Cycle and stages of Meiosis I'*\n"
                "- *'Explain Chemical Bonding and Hybridization tricks'*\n"
                "- *'Explain Optics and Lens Maker's Formula'*\n"
                "- *'Explain Genetics and Mendel's Dihybrid Cross'*"
            )
        else:
            return (
                "### 📖 Hello! Welcome to the JEE Concept Mentor Center\n\n"
                "I can explain any concept across Physics, Chemistry, and Mathematics!\n\n"
                "Try asking me about:\n"
                "- *'Explain SHM and damped oscillations'*\n"
                "- *'Explain Henderson-Hasselbalch buffer equation'*\n"
                "- *'Explain L'Hôpital's rule and indeterminate limits'*\n"
                "- *'Explain Rotational Dynamics and Moment of Inertia theorems'*"
            )

    th = topic_hint.lower()
    
    # UPSC Concepts
    if "basic structure" in th or "kesavananda" in th or "constitution" in th:
        return (
            "### ⚖️ Concept: The Basic Structure Doctrine (Indian Polity)\n\n"
            "Hello! Let's understand this foundational constitutional principle:\n\n"
            "- **Origin:** Propounded by a 13-judge bench of the Supreme Court in *Kesavananda Bharati v. State of Kerala (1973)*.\n"
            "- **Core Principle:** Parliament's amending power under **Article 368** is plenary but NOT unlimited; it cannot alter the fundamental identity or 'basic structure' of the Constitution.\n"
            "- **Core Elements:** Supremacy of the Constitution, Rule of Law, Separation of Powers, Judicial Review, Secularism, and Federalism.\n"
            "- **Exam Tip:** The term 'Basic Structure' is NOT explicitly mentioned anywhere in the text of the Constitution—it is an indigenous judicial safeguard!"
        )
    elif "fiscal" in th or "deficit" in th or "frbm" in th or "monetary" in th:
        return (
            "### 📈 Concept: Fiscal Deficit & Monetary Framework (Indian Economy)\n\n"
            "Hello! Here is the clear economic breakdown:\n\n"
            "- **Fiscal Deficit:** $\\text{Total Expenditure} - \\text{Total Receipts (excluding borrowings)}$. Represents the total borrowing requirement of the government.\n"
            "- **Primary Deficit:** $\\text{Fiscal Deficit} - \\text{Interest Payments}$. Indicates current fiscal stance minus past debt burdens.\n"
            "- **FRBM Act Framework:** Targets fiscal deficit around 3% of GDP and debt-to-GDP ratio around 60% (combined Centre + States).\n"
            "- **Exam Trap:** Fiscal deficit is financed by internal borrowing (g-sec issuance), external borrowing, and drawdown of cash balances—NOT by direct currency printing since 1997."
        )
    # Physics & JEE
    elif "shm" in th or "oscillation" in th:
        return (
            "### 🔬 Concept: Simple Harmonic Motion (SHM)\n\n"
            "Hello! Let's break down SHM cleanly:\n\n"
            "- **Governing Equation:** $F = -kx \\implies \\frac{d^2x}{dt^2} + \\omega^2 x = 0$\n"
            "- **Angular Frequency:** $\\omega = \\sqrt{\\frac{k}{m}} = \\frac{2\\pi}{T}$\n"
            "- **Energy Conservation:** $E_{\\text{total}} = \\frac{1}{2}kA^2 = K(t) + U(t)$\n"
            "- **High-Yield Trap:** At equilibrium ($x=0$), velocity and kinetic energy are maximal, but acceleration is precisely ZERO!"
        )
    elif "buffer" in th or "ionic" in th:
        return (
            "### 🧪 Concept: Acidic & Basic Buffers (Chemistry)\n\n"
            "Hello! Here is the essential buffer summary:\n\n"
            "- **Acidic Buffer:** Weak Acid (HA) + Conjugate Base Salt (NaA)\n"
            "- **Henderson-Hasselbalch Equation:** $\\text{pH} = \\text{pK}_a + \\log\\frac{[\\text{Conjugate Base}]}{[\\text{Weak Acid}]}$\n"
            "- **Buffer Capacity:** Maximized when $[\text{Salt}] = [\text{Acid}] \\implies \\text{pH} = \\text{pK}_a$.\n"
            "- **Exam Trap:** Moderate dilution changes concentrations but DOES NOT change the ratio $\\frac{[\\text{Salt}]}{[\\text{Acid}]}$, so pH remains constant!"
        )
    elif "limit" in th or "calculus" in th:
        return (
            "### 📐 Concept: Calculus Limits & L'Hôpital's Rule\n\n"
            "Hello! Let's master limit evaluations:\n\n"
            "- **Applicability:** Applies strictly to indeterminate forms $\\frac{0}{0}$ or $\\frac{\\infty}{\\infty}$.\n"
            "- **Method:** $\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)}$\n"
            "- **Core Standard Limits:** $\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$, $\\lim_{x \\to 0} \\frac{e^x - 1}{x} = 1$, $\\lim_{x \\to 0} \\frac{\\ln(1+x)}{x} = 1$.\n"
            "- **Crucial Reminder:** Differentiate the numerator and denominator separately—never use the quotient rule $(\\frac{u}{v})'$ for L'Hôpital!"
        )
    elif "cell" in th or "genetic" in th:
        return (
            "### 🧬 Concept: Cell Biology & Chromosomal Division (Biology)\n\n"
            "Hello! Let's review this core NEET chapter:\n\n"
            "- **Meiosis I vs II:** Homologous chromosomes segregate during Anaphase I (reductional division). Sister chromatids segregate during Anaphase II (equational division).\n"
            "- **Crossing Over:** Occurs during the **Pachytene** stage of Prophase I, mediated by enzyme recombinase.\n"
            "- **Synaptonemal Complex:** Formed during **Zygotene** and dissolves during **Diplotene**.\n"
            "- **NEET Trap:** In Anaphase I, centromeres DO NOT split; splitting occurs strictly in Anaphase II."
        )
    else:
        return (
            f"### 🔬 Concept: {topic_hint.title()}\n\n"
            f"Hello! For {exam}, here is the key takeaway for **{topic_hint.title()}**:\n\n"
            f"- Focus on the core foundational definition and governing formula/statute.\n"
            "- Check how this concept connects to prerequisite topics in your curriculum DAG.\n"
            "- Practice 3 to 5 targeted questions to test edge cases and distractor options!"
        )


def format_unknown_fallback(exam: str) -> str:
    return (
        f"### 👋 Hello Aspirant! I'm Your Personal {exam} Study Mentor\n\n"
        f"All our adaptive learning systems are live and standing by to help you succeed in {exam}. "
        "Here are a few quick ways we can work together right now:\n\n"
        "- 📊 **'What mistakes am I making most often?'** — Instant error diagnosis across your recent quizzes.\n"
        "- 🗺️ **'Why is my study plan ordered this way?'** — Learn which prerequisite gaps your roadmap is fixing.\n"
        "- ⚡ **'{exam} speed & accuracy strategy'** — Proven pacing and negative marking tactics.\n"
        "- 🔬 **'Explain [Concept Name]'** — Step-by-step conceptual breakdowns and formula recaps.\n\n"
        "*Feel free to ask any question or click a prompt chip above to get started!*"
    )

