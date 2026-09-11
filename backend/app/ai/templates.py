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
    
    # Physics & JEE: Simple Harmonic Motion
    if "shm" in th or "oscillation" in th or "harmonic" in th:
        return (
            "### 🔬 Concept Masterclass: Simple Harmonic Motion (SHM)\n\n"
            "#### 💡 1. Intuitive Mental Model (Feynman Analogy)\n"
            "Imagine a ball rolling inside a frictionless curved bowl. The farther it climbs up the rim, the harder gravity pulls it back toward the bottom. "
            "In SHM, the **restoring force** acts like an elastic leash that gets strictly stronger in direct linear proportion to displacement.\n\n"
            "#### 📐 2. Canonical Analytical Formulation\n"
            "$$\\frac{d^2x}{dt^2} + \\omega^2 x = 0 \\quad \\text{where } \\omega = \\sqrt{\\frac{k}{m}} = \\frac{2\\pi}{T}$$\n"
            "- $x(t) = A \\sin(\\omega t + \\phi)$: Instantaneous displacement (meters)\n"
            "- $v(t) = \\omega \\sqrt{A^2 - x^2}$: Velocity at displacement $x$ (m/s)\n"
            "- $a(t) = -\\omega^2 x$: Acceleration (strictly opposes displacement)\n\n"
            "#### 🔬 3. Step-by-Step Derivation & Energy Invariants\n"
            "By integrating $F = m\\frac{dv}{dt} = -kx$ over displacement:\n"
            "$$\\int m v \\, dv = -\\int k x \\, dx \\implies \\frac{1}{2}m v^2 + \\frac{1}{2}k x^2 = E_{\\text{total}} = \\frac{1}{2}k A^2$$\n"
            "The system continuously trades kinetic energy ($K$) and elastic potential energy ($U$), but their sum remains constant at all times.\n\n"
            "#### ⚠️ 4. Exam Trap Radar (JEE / NEET Traps)\n"
            "- **The Equilibrium Zero Trap:** At mean position ($x=0$), velocity and kinetic energy are maximal, but acceleration is **precisely ZERO**.\n"
            "- **The Frequency Doubling Trap:** While displacement oscillates with frequency $f = \\frac{\\omega}{2\\pi}$, kinetic energy and potential energy oscillate with **double frequency ($2f$)**!\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*At what displacement from the mean position does the kinetic energy of an undamped particle equal its potential energy?* (Hint: $x = \\pm \\frac{A}{\\sqrt{2}}$)"
        )
    # Chemistry: Buffers
    elif "buffer" in th or "ionic" in th:
        return (
            "### 🧪 Concept Masterclass: Acidic & Basic Buffers\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "Think of a buffer as a chemical shock absorber. When hydronium ions ($H^+$) enter, the conjugate base sponge absorbs them; when hydroxide ($OH^-$) enters, the weak acid donates a proton. The system neutralizes disturbances without shifting pH dramatically.\n\n"
            "#### 📐 2. Canonical Analytical Formulation (Henderson-Hasselbalch)\n"
            "$$\\text{pH} = \\text{pK}_a + \\log_{10} \\left( \\frac{[\\text{Conjugate Base}]}{[\\text{Weak Acid}]} \\right)$$\n"
            "- Maximum Buffer Capacity occurs when $[\\text{Salt}] = [\\text{Acid}]$, meaning $\\text{pH} = \\text{pK}_a$.\n\n"
            "#### 🔬 3. Step-by-Step Derivation\n"
            "For weak acid $HA \\rightleftharpoons H^+ + A^-$ with acid dissociation constant $K_a = \\frac{[H^+][A^-]}{[HA]}$:\n"
            "1. Take negative logarithm of both sides: $-\\log K_a = -\\log [H^+] - \\log \\frac{[A^-]}{[HA]}$\n"
            "2. Rearranging gives: $\\text{pH} = \\text{pK}_a + \\log \\frac{[A^-]}{[HA]}$\n\n"
            "#### ⚠️ 4. Exam Trap Radar\n"
            "- **The Dilution Invariance Trap:** Moderate dilution with pure water reduces both $[A^-]$ and $[HA]$ by identical factors, so the ratio $\\frac{[A^-]}{[HA]}$ does not change—**pH remains unchanged** upon moderate dilution!\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*If a buffer contains $0.1\\text{ M } \\text{CH}_3\\text{COOH}$ and $0.01\\text{ M } \\text{CH}_3\\text{COONa}$ (with $\\text{pK}_a = 4.74$), is the pH greater than or less than 4.74?* (Answer: Less, specifically $\\text{pH} = 3.74$)."
        )
    # Mathematics: Calculus Limits & L'Hôpital
    elif "limit" in th or "calculus" in th:
        return (
            "### 📐 Concept Masterclass: Indeterminate Limits & L'Hôpital's Rule\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "When evaluating $\\frac{f(x)}{g(x)}$ as both tend to 0, you aren't dividing zero by zero—you are comparing the *relative rates of descent* of both functions toward zero.\n\n"
            "#### 📐 2. Canonical Analytical Formulation\n"
            "$$\\lim_{x \\to a} \\frac{f(x)}{g(x)} = \\lim_{x \\to a} \\frac{f'(x)}{g'(x)} \\quad \\text{iff form is } \\left[\\frac{0}{0}\\right] \\text{ or } \\left[\\frac{\\pm\\infty}{\\pm\\infty}\\right]$$\n\n"
            "#### 🔬 3. Step-by-Step Execution Protocol\n"
            "1. Verify indeterminate form before differentiating; never apply if the denominator has a non-zero finite limit.\n"
            "2. Differentiate numerator $f'(x)$ and denominator $g'(x)$ independently.\n"
            "3. Substitute $x \\to a$. If indeterminate persists, apply second derivative $\\frac{f''(x)}{g''(x)}$.\n\n"
            "#### ⚠️ 4. Exam Trap Radar\n"
            "- **The Quotient Rule Trap:** Never use the quotient formula $\\frac{f'g - fg'}{g^2}$! L'Hôpital requires differentiating the numerator and denominator separately.\n"
            "- **Standard Limit Supremacy:** In competitive exams, standard expansions (Taylor series) like $\\sin x = x - \\frac{x^3}{6} + \\dots$ are 3x faster than multiple L'Hôpital differentiations.\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*Evaluate $\\lim_{x \\to 0} \\frac{\\tan x - x}{x^3}$.* (Answer: $1/3$ via Taylor expansion or L'Hôpital)."
        )
    # Biology / NEET: Meiosis
    elif "cell" in th or "genetic" in th or "meiosis" in th:
        return (
            "### 🧬 Concept Masterclass: Meiosis & Chromosomal Recombination\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "Meiosis is nature's genetic shuffling deck. Unlike mitosis (which creates identical photocopies), Meiosis deliberately cuts chromosome count in half while exchanging pieces of maternal and paternal DNA to create infinite variety.\n\n"
            "#### 📐 2. Key Stages & Cytogenetic Landmarks\n"
            "- **Leptotene:** Chromatin condensation begins.\n"
            "- **Zygotene:** Synapsis and Synaptonemal Complex formation between homologous pairs.\n"
            "- **Pachytene:** Recombination nodules appear; crossing over mediated by enzyme **Recombinase**.\n"
            "- **Diplotene:** Dissolution of synaptonemal complex; **Chiasmata** (X-shaped structures) visible.\n"
            "- **Diakinesis:** Terminalization of chiasmata.\n\n"
            "#### 🔬 3. Division Mechanism Comparison\n"
            "- **Meiosis I (Reductional):** Homologous chromosomes separate ($2n \\to n$). Centromeres DO NOT split.\n"
            "- **Meiosis II (Equational):** Sister chromatids separate. Centromeres split during Anaphase II.\n\n"
            "#### ⚠️ 4. Exam Trap Radar (NEET)\n"
            "- **Centromere Splitting Trap:** NEET examiners love asking in which stage centromeres divide. Remember: Anaphase I separates homologous chromosomes; centromeres divide strictly in **Anaphase II**!\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*In which specific sub-stage of Prophase I do chiasmata first become visible due to synaptonemal complex dissolution?* (Answer: Diplotene)."
        )
    # UPSC: Basic Structure Doctrine
    elif "basic structure" in th or "kesavananda" in th or "constitution" in th:
        return (
            "### ⚖️ Concept Masterclass: The Basic Structure Doctrine\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "Think of the Constitution as a foundational building. Parliament can repaint the walls, add rooms, or update the plumbing under Article 368, but it cannot demolish the load-bearing pillars that hold up the edifice.\n\n"
            "#### 📐 2. Canonical Constitutional Jurisprudence\n"
            "- **Propounded in:** *Kesavananda Bharati v. State of Kerala (1973)* by a historic 13-judge constitutional bench (7:6 majority).\n"
            "- **Core Principle:** Parliament's constituent power under **Article 368** is broad but bounded; it does not extend to altering or destroying the essential framework of the Constitution.\n\n"
            "#### 🔬 3. Core Structural Pillars Recognized by Supreme Court\n"
            "1. Supremacy of the Constitution\n"
            "2. Republican and Democratic form of Government\n"
            "3. Secular character of the Constitution\n"
            "4. Separation of Powers between Legislature, Executive, and Judiciary\n"
            "5. Federal Character\n"
            "6. Power of Judicial Review (*Minerva Mills*, 1980)\n\n"
            "#### ⚠️ 4. Exam Trap Radar (UPSC Prelims)\n"
            "- **Textual Absence:** The term 'Basic Structure' is **NOT defined or mentioned anywhere** in the written text of the Constitution of India—it is an indigenous judicial safeguard developed via case law.\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*Which landmark case held that Judicial Review is an inviolable part of the Basic Structure?* (Answer: *Minerva Mills v. Union of India*, 1980)."
        )
    # Physics: Rotational Dynamics & Moment of Inertia
    elif "rotat" in th or "inertia" in th or "torque" in th or "angular" in th:
        return (
            "### 🔄 Concept Masterclass: Rotational Dynamics & Moment of Inertia\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "Moment of inertia is the rotational clone of linear mass. Just as linear inertia resists changes in straight-line speed ($F = ma$), rotational inertia ($I$) resists being spun up or slowed down ($\\tau = I\\alpha$). Crucially, mass distributed farther from the axis of rotation counts quadratically ($mr^2$)!\n\n"
            "#### 📐 2. Canonical Analytical Formulation\n"
            "$$\\tau_{\\text{net}} = I \\alpha = \\frac{dL}{dt}, \\quad K_{\\text{rot}} = \\frac{1}{2} I \\omega^2$$\n"
            "- Parallel Axis Theorem: $I = I_{\\text{cm}} + M d^2$ (Valid for any rigid body)\n"
            "- Perpendicular Axis Theorem: $I_z = I_x + I_y$ (Valid strictly for planar 2D laminae)\n\n"
            "#### 🔬 3. Step-by-Step Rolling Derivation\n"
            "For a body of radius $R$ rolling down an incline of angle $\\theta$ without slipping ($a = \\alpha R$):\n"
            "$$a = \\frac{g \\sin \\theta}{1 + \\frac{I_{\\text{cm}}}{M R^2}}$$\n"
            "Notice how the acceleration depends solely on the shape factor $\\beta = \\frac{I_{\\text{cm}}}{M R^2}$! A solid sphere ($\\beta = 2/5$) always beats a ring ($\\beta = 1$) down the incline.\n\n"
            "#### ⚠️ 4. Exam Trap Radar\n"
            "- **The Incline Shape Trap:** In pure rolling down an incline, the velocity at the bottom does NOT depend on mass or radius—it depends strictly on the geometric distribution parameter $\\frac{I}{MR^2}$!\n"
            "- **Perpendicular Axis Trap:** Never apply $I_z = I_x + I_y$ to solid 3D spheres or cylinders; it holds strictly for planar laminae.\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*Which reaches the bottom first in pure rolling down an incline: a hollow cylinder or a solid cylinder?* (Answer: Solid cylinder, because smaller $I/MR^2 = 1/2 < 1$ produces higher linear acceleration)."
        )
    # Physics: Optics & Lens Maker's Formula
    elif "optic" in th or "lens" in th or "refract" in th:
        return (
            "### 🔍 Concept Masterclass: Refraction & Lens Maker's Formula\n\n"
            "#### 💡 1. Intuitive Mental Model\n"
            "A lens alters light wavefronts because light travels slower in glass than in air. Curving the surfaces changes the optical path delay across the aperture, bending parallel rays to converge at a sharp focal point.\n\n"
            "#### 📐 2. Canonical Analytical Formulation\n"
            "$$\\frac{1}{f} = \\left( \\frac{\\mu_2}{\\mu_1} - 1 \\right) \\left( \\frac{1}{R_1} - \\frac{1}{R_2} \\right)$$\n"
            "- $\\mu_2$: Refractive index of lens material\n"
            "- $\\mu_1$: Refractive index of surrounding medium\n"
            "- $R_1, R_2$: Radii of curvature with strict Cartesian sign convention\n\n"
            "#### 🔬 3. Step-by-Step Derivation from Spherical Refraction\n"
            "Applying single-surface refraction $\\frac{\\mu_2}{v} - \\frac{\\mu_1}{u} = \\frac{\\mu_2 - \\mu_1}{R}$ across both front and rear curved interfaces and summing the equations yields the thin-lens focal equation.\n\n"
            "#### ⚠️ 4. Exam Trap Radar\n"
            "- **The Immersion Inversion Trap:** When a glass convex lens ($\\mu = 1.5$) is placed in a medium with higher refractive index (e.g. carbon disulfide $\\mu = 1.63$), the term $(\\frac{\\mu_2}{\\mu_1} - 1)$ becomes negative—the converging convex lens behaves as a **diverging concave lens**!\n\n"
            "#### 🎯 5. Quick Micro-Check\n"
            "*What happens to the focal length of a biconvex glass lens if immersed in water ($\\mu_w = 4/3$)?* (Answer: Focal length increases by approximately $4\\times$)."
        )
    else:
        return (
            f"### 🔬 Concept Masterclass: {topic_hint.title()}\n\n"
            f"#### 💡 1. Intuitive Mental Model\n"
            f"To master **{topic_hint.title()}** in {exam}, ground the concept in foundational physical and conceptual symmetries before diving into complex problems.\n\n"
            f"#### 📐 2. Governing Analytical Formulation\n"
            f"Isolate the canonical governing relations and dimensional units for **{topic_hint.title()}**.\n\n"
            f"#### 🔬 3. Step-by-Step Logical Derivation\n"
            f"Trace the derivation from first principles (conservation laws or fundamental definitions) to competitive exam shortcuts.\n\n"
            f"#### ⚠️ 4. Exam Trap Radar\n"
            f"- Verify boundary conditions and sign conventions to eliminate common distractor traps.\n\n"
            f"#### 🎯 5. Quick Micro-Check\n"
            f"*Ready to test your mastery of {topic_hint.title()}? Click '🎯 Test Me on This' below for an instant micro-drill!*"
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

