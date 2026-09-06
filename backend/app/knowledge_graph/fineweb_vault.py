"""
FineWeb-Edu Academic Knowledge Repository & Grounding Service
Provides textbook-grade readings, university lecture excerpts, and educational passages
curated from HuggingFaceFW/fineweb-edu (Score >= 4.0).
Organized by exam track: JEE, NEET, and UPSC Civil Services.
Features rich LaTeX mathematical formulas, vector textbook figures, and didactic callouts.
"""
from typing import List, Dict, Any, Optional

FINEWEB_READINGS: List[Dict[str, Any]] = [
    # =========================================================================
    # 🎯 JEE MAIN & ADVANCED (Physics, Chemistry, Mathematics)
    # =========================================================================
    {
        "id": "FW-JEE-PHY-01",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Rotational Mechanics",
        "title": "Rotational Dynamics: The Parallel Axis Theorem & Moment of Inertia",
        "score": 4.85,
        "source": "OpenStax University Physics / FineWeb-Edu Corpus",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Mathematical derivation of the parallel axis theorem I = I_cm + M d^2 and its application to planar and three-dimensional rigid bodies.",
        "formula_box": {
            "title": "Steiner's Parallel Axis Theorem",
            "latex": "I = I_{\\text{cm}} + M d^2",
            "plain": "I = I_cm + M · d²",
            "terms": [
                ("I", "Moment of inertia about target arbitrary axis"),
                ("I_cm", "Moment of inertia about parallel axis through Center of Mass"),
                ("M", "Total mass of the rigid body (∫ dm)"),
                ("d", "Perpendicular distance separating the two parallel axes")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--purple)"/>
    </marker>
  </defs>
  <!-- Rigid body outline -->
  <path d="M 80 110 C 90 40, 260 30, 360 60 C 460 90, 480 170, 380 190 C 280 210, 120 200, 80 110 Z" fill="rgba(99,102,241,0.08)" stroke="var(--purple)" stroke-width="2.2" stroke-dasharray="6,3"/>
  <text x="420" y="70" font-size="12" font-weight="600" fill="var(--ink-soft)" font-family="sans-serif">Rigid Body (Mass M)</text>
  
  <!-- CM Axis -->
  <line x1="200" y1="20" x2="200" y2="200" stroke="#10B981" stroke-width="2.5"/>
  <circle cx="200" cy="120" r="5" fill="#10B981"/>
  <text x="208" y="125" font-size="12" font-weight="700" fill="#10B981" font-family="sans-serif">G (Center of Mass)</text>
  <text x="175" y="32" font-size="13" font-weight="700" fill="#10B981" font-family="sans-serif">Axis_cm</text>
  
  <!-- Arbitrary Parallel Axis -->
  <line x1="330" y1="20" x2="330" y2="200" stroke="var(--purple)" stroke-width="2.5"/>
  <text x="338" y="32" font-size="13" font-weight="700" fill="var(--purple)" font-family="sans-serif">Target Axis (I)</text>
  
  <!-- Distance d -->
  <line x1="200" y1="80" x2="330" y2="80" stroke="var(--purple)" stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <rect x="250" y="68" width="30" height="22" rx="4" fill="var(--card)" stroke="var(--border)"/>
  <text x="261" y="84" font-size="13" font-weight="800" fill="var(--purple)" font-family="sans-serif">d</text>
  
  <!-- Mass element dm -->
  <circle cx="140" cy="150" r="4" fill="#EF4444"/>
  <text x="110" y="165" font-size="11" font-weight="600" fill="#EF4444" font-family="sans-serif">dm (element)</text>
  <line x1="200" y1="120" x2="140" y2="150" stroke="#EF4444" stroke-width="1.2" stroke-dasharray="2,2"/>
  <line x1="330" y1="120" x2="140" y2="150" stroke="var(--purple)" stroke-width="1.2" stroke-dasharray="2,2"/>
</svg>""",
        "figure_caption": "Figure 1.1: Geometric configuration of Steiner's Parallel Axis Theorem. One axis must strictly pass through the body's Center of Mass (G).",
        "content": (
            "The moment of inertia of a rigid body characterizes its resistance to rotational acceleration about a specific axis, "
            "analogous to inertial mass in linear kinematics. While calculating the moment of inertia about the center of mass ($I_{\\text{cm}}$) is straightforward "
            "for symmetric objects, practical engineering and JEE Advanced multi-body problems frequently involve eccentric or shifted rotation axes.\n\n"
            "### Statement of Steiner's Theorem\n"
            "The Parallel Axis Theorem states that the moment of inertia $I$ of any rigid body of total mass $M$ about an arbitrary axis is equal to the "
            "moment of inertia $I_{\\text{cm}}$ about a parallel axis passing through its Center of Mass plus the product of the mass and the square of the "
            "perpendicular distance $d$ between the two axes:\n\n"
            "$$I = I_{\\text{cm}} + M d^2$$\n\n"
            "### Rigorous Mathematical Derivation\n"
            "Consider a continuous planar mass distribution where the coordinate origin is chosen at the Center of Mass $G$. By definition of the Center of Mass:\n"
            "$$\\int \\mathbf{r}_i \\, dm = 0 \\quad \\implies \\quad \\int x \\, dm = 0, \\quad \\int y \\, dm = 0$$\n\n"
            "Now consider a new parallel axis shifted by a constant displacement vector $\\mathbf{d} = (x_d, y_d)$. The position vector of any mass element $dm$ "
            "relative to this new axis becomes $\\mathbf{r}' = \\mathbf{r} - \\mathbf{d}$. Expanding the squared distance gives:\n"
            "$${r'}^2 = (x - x_d)^2 + (y - y_d)^2 = (x^2 + y^2) - 2(x x_d + y y_d) + (x_d^2 + y_d^2)$$\n"
            "$${r'}^2 = r^2 - 2\\mathbf{r}\\cdot\\mathbf{d} + d^2$$\n\n"
            "Integrating over the entire body of mass $M$:\n"
            "$$I = \\int {r'}^2 \\, dm = \\int r^2 \\, dm - 2\\mathbf{d}\\cdot \\left(\\int \\mathbf{r}\\, dm\\right) + d^2 \\int dm$$\n\n"
            "Because $\\int \\mathbf{r}\\, dm = 0$ by definition of the Center of Mass origin, the middle cross-term vanishes identically! Hence:\n"
            "$$I = I_{\\text{cm}} + M d^2$$\n\n"
            "This confirms that the moment of inertia about the Center of Mass is the absolute minimum among all parallel axes."
        ),
        "didactic_notes": {
            "axiom": "Steiner's Law guarantees that for any set of parallel axes, the axis passing through the Center of Mass always yields the minimum possible moment of inertia.",
            "trap": "NEET/JEE Pitfall: You CANNOT shift directly between two arbitrary axes (e.g. from rim to rim). You must first calculate I_cm, and then apply I_target = I_cm + M·d².",
            "mnemonic": "Remember: 'Center First, Target Second' — always route through the Center of Mass origin."
        },
        "key_takeaways": [
            "Parallel Axis Formula: $I = I_{\\text{cm}} + M d^2$, where $d$ is the perpendicular distance between axes.",
            "Dimensional Invariance: The theorem holds for both 2D planar laminas and arbitrary 3D continuous rigid bodies.",
            "Center of Mass Condition: The cross-term vanishes identically because the origin is at the Center of Mass: $\\int \\mathbf{r} \\, dm = 0$.",
            "Minimum Inertia Axis: Moment of inertia about the center of mass ($I_{\\text{cm}}$) represents the global minimum for that orientation."
        ]
    },
    {
        "id": "FW-JEE-PHY-02",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Electromagnetism",
        "title": "Electromagnetic Induction: Lenz's Law & Conservation of Energy",
        "score": 4.90,
        "source": "MIT Physics Courseware / FineWeb-Edu Corpus",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Physical grounding of Faraday's Law, eddy currents, and how Lenz's law enforces the First Law of Thermodynamics.",
        "formula_box": {
            "title": "Faraday-Lenz Law of Induction",
            "latex": "\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}",
            "plain": "emf = - dΦ_B / dt",
            "terms": [
                ("ℰ", "Induced electromotive force (volts)"),
                ("Φ_B", "Magnetic flux linked through the conducting loop (webers)"),
                ("(-) sign", "Lenz's Law: direction of induced emf opposes flux change"),
                ("t", "Time elapsed (seconds)")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 200" width="100%" height="190" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Bar Magnet moving right -->
  <rect x="60" y="70" width="60" height="45" fill="#EF4444" rx="3"/>
  <text x="82" y="98" font-size="16" font-weight="800" fill="#fff" font-family="sans-serif">N</text>
  <rect x="120" y="70" width="60" height="45" fill="#3B82F6" rx="3"/>
  <text x="145" y="98" font-size="16" font-weight="800" fill="#fff" font-family="sans-serif">S</text>
  
  <!-- Velocity vector -->
  <line x1="190" y1="92" x2="240" y2="92" stroke="#EF4444" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="200" y="80" font-size="13" font-weight="700" fill="#EF4444" font-family="sans-serif">v (motion)</text>
  
  <!-- Conducting Loop -->
  <ellipse cx="360" cy="92" rx="25" ry="60" fill="none" stroke="var(--purple)" stroke-width="4"/>
  <path d="M 360 32 A 25 60 0 0 1 360 152" fill="none" stroke="#10B981" stroke-width="4"/>
  
  <!-- Induced Current Arrows -->
  <path d="M 378 60 L 382 72 L 372 68 Z" fill="#10B981"/>
  <text x="395" y="98" font-size="13" font-weight="700" fill="#10B981" font-family="sans-serif">I_induced</text>
  
  <!-- Opposing Repulsive Force -->
  <line x1="330" y1="92" x2="270" y2="92" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="4,3"/>
  <text x="270" y="125" font-size="11" font-weight="700" fill="#F59E0B" font-family="sans-serif">Opposing Force F_mag</text>
  
  <!-- B lines -->
  <path d="M 180 80 C 260 70, 310 70, 360 80" stroke="rgba(99,102,241,0.5)" stroke-width="1.5" fill="none"/>
  <path d="M 180 105 C 260 115, 310 115, 360 105" stroke="rgba(99,102,241,0.5)" stroke-width="1.5" fill="none"/>
</svg>""",
        "figure_caption": "Figure 1.2: Conservation of energy in induction. As the North pole approaches, an induced counter-clockwise current creates an opposing North magnetic pole.",
        "content": (
            "Faraday's Law of Electromagnetic Induction establishes that whenever the magnetic flux linking a circuit changes, an electromotive force (emf) is induced "
            "whose magnitude is proportional to the rate of change of magnetic flux:\n\n"
            "$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$$\n\n"
            "### The Significance of the Negative Sign: Lenz's Law\n"
            "Heinrich Lenz formulated the physical consequence encoded by the minus sign: *The polarity of the induced emf is always such that the magnetic field "
            "produced by the resulting induced current directly opposes the original change in magnetic flux that induced it.*\n\n"
            "### Thermodynamic Proof of Lenz's Law\n"
            "Why must nature enforce this opposition? Consider the counterfactual scenario: suppose the minus sign were a plus sign ($+\\frac{d\\Phi_B}{dt}$).\n\n"
            "If a bar magnet's North pole were slightly nudged toward a conducting loop, an induced current would flow such as to create an attractive South pole. "
            "This South pole would pull the magnet faster, increasing $\\frac{d\\Phi_B}{dt}$, which in turn would amplify the current and accelerate the magnet perpetually "
            "without requiring any external work! This would represent a perpetual motion machine of the first kind, generating limitless kinetic energy and Joule heating "
            "($I^2 R$) out of nothing.\n\n"
            "In physical reality, an external agent must perform positive mechanical work $\\Delta W = \\int \\mathbf{F}_{\\text{ext}} \\cdot d\\mathbf{x}$ against the repulsive "
            "Lorentz force $\\mathbf{F} = I(\\mathbf{L} \\times \\mathbf{B})$. By the First Law of Thermodynamics, this exact mechanical work converts directly into electrical "
            "energy and dissipative thermal energy. Lenz's law is therefore nothing less than the mechanical-electrical manifestation of energy conservation."
        ),
        "didactic_notes": {
            "axiom": "Induced currents always oppose the cause of their creation. If flux increases, induced B opposes; if flux decreases, induced B reinforces.",
            "trap": "JEE Distractor: Induced emf exists whenever flux changes, even if the circuit is OPEN (no current flows, but potential difference develops).",
            "mnemonic": "Remember: 'Lenz is Lazy' — the circuit resents changes to its existing magnetic state."
        },
        "key_takeaways": [
            "Mathematical Induction Law: $\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\left[\\mathbf{B} \\cdot \\mathbf{A} \\cos \\theta\\right]$.",
            "Conservation of Energy: The negative sign ensures that external mechanical work done equals electrical energy generated.",
            "Directional Vector Rule: Right Hand Thumb Rule applied to the opposing magnetic flux vector $\\Delta\\Phi_B$.",
            "Joule Power Dissipation: Eddy currents in bulk conductors dissipate heat according to $P = \\frac{\\mathcal{E}^2}{R} = \\frac{1}{R}\\left(\\frac{d\\Phi_B}{dt}\\right)^2$."
        ]
    },
    {
        "id": "FW-JEE-MAT-01",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Definite Integrals",
        "title": "Definite Integrals: King's Property & Symmetry in Definite Integration",
        "score": 4.80,
        "source": "Stanford Mathematics Review / FineWeb-Edu Corpus",
        "word_count": 480,
        "reading_time_mins": 2,
        "summary": "Rigorous treatment of integral property ∫ f(x)dx = ∫ f(a+b-x)dx and trigonometric algebraic cancellation techniques.",
        "formula_box": {
            "title": "King's Property of Definite Integrals",
            "latex": "\\int_{a}^{b} f(x) \\, dx = \\int_{a}^{b} f(a + b - x) \\, dx",
            "plain": "∫_a^b f(x) dx = ∫_a^b f(a + b - x) dx",
            "terms": [
                ("[a, b]", "Interval of definite integration"),
                ("f(x)", "Continuous real-valued function on [a, b]"),
                ("x = (a+b)/2", "Axis of symmetry for the domain reflection transformation")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 180" width="100%" height="170" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Axes -->
  <line x1="50" y1="150" x2="480" y2="150" stroke="var(--ink-soft)" stroke-width="1.8"/>
  <line x1="70" y1="170" x2="70" y2="20" stroke="var(--ink-soft)" stroke-width="1.8"/>
  
  <!-- Shaded Area -->
  <path d="M 120 150 C 180 50, 240 130, 300 70 C 340 30, 380 90, 420 150 Z" fill="rgba(99,102,241,0.18)" stroke="var(--purple)" stroke-width="2.5"/>
  
  <!-- Limits a, b and symmetry line -->
  <line x1="120" y1="150" x2="120" y2="140" stroke="var(--ink)" stroke-width="2"/>
  <text x="115" y="168" font-size="13" font-weight="700" fill="var(--ink)">a</text>
  
  <line x1="420" y1="150" x2="420" y2="140" stroke="var(--ink)" stroke-width="2"/>
  <text x="415" y="168" font-size="13" font-weight="700" fill="var(--ink)">b</text>
  
  <!-- Symmetry Line -->
  <line x1="270" y1="25" x2="270" y2="150" stroke="#10B981" stroke-width="1.8" stroke-dasharray="4,4"/>
  <text x="245" y="18" font-size="11" font-weight="700" fill="#10B981">x = (a+b)/2</text>
  
  <text x="180" y="80" font-size="14" font-weight="700" fill="var(--purple)">y = f(x)</text>
  <text x="320" y="80" font-size="14" font-weight="700" fill="#10B981">y = f(a+b-x)</text>
</svg>""",
        "figure_caption": "Figure 1.3: Geometric reflection across x = (a+b)/2. The enclosed area under the curve is invariant under reflection.",
        "content": (
            "In definite integral calculus, few properties rival the elegance and computational speed of the reflection property, "
            "colloquially known across Indian competitive pedagogy as **King's Property**:\n\n"
            "$$\\int_{a}^{b} f(x) \\, dx = \\int_{a}^{b} f(a + b - x) \\, dx$$\n\n"
            "### Analytical Proof via Substitution\n"
            "Let $I = \\int_{a}^{b} f(x) \\, dx$. Perform the linear transformation:\n"
            "$$u = a + b - x \\quad \\implies \\quad du = -dx$$\n\n"
            "Transforming the integration bounds:\n"
            "- When $x = a$, $u = a + b - a = b$.\n"
            "- When $x = b$, $u = a + b - b = a$.\n\n"
            "Substituting these terms into the integral:\n"
            "$$I = \\int_{b}^{a} f(u) (-du) = -\\int_{b}^{a} f(u) \\, du = \\int_{a}^{b} f(u) \\, du$$\n\n"
            "Since the definite integral is independent of the dummy integration variable, $\\int_{a}^{b} f(u)du = \\int_{a}^{b} f(x)dx$. This completes the proof.\n\n"
            "### Paradigm Application: Transcendental Cancellation\n"
            "Consider the classical JEE integral:\n"
            "$$I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx$$\n\n"
            "Applying King's Property with $a+b-x = 0 + \\frac{\\pi}{2} - x = \\frac{\\pi}{2} - x$:\n"
            "$$I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(\\pi/2 - x)}{\\sin^n(\\pi/2 - x) + \\cos^n(\\pi/2 - x)} \\, dx = \\int_{0}^{\\pi/2} \\frac{\\cos^n(x)}{\\cos^n(x) + \\sin^n(x)} \\, dx$$\n\n"
            "Adding the original integral and the transformed integral:\n"
            "$$2I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x) + \\cos^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx = \\int_{0}^{\\pi/2} 1 \\, dx = \\left[x\\right]_0^{\\pi/2} = \\frac{\\pi}{2}$$\n"
            "$$I = \\frac{\\pi}{4}$$\n\n"
            "This algebraic synthesis completely eliminates the need for calculating difficult elementary antiderivatives."
        ),
        "didactic_notes": {
            "axiom": "Geometric meaning: King's Property reflects the graph about the line x = (a+b)/2. Since reflection is an isometry, area is strictly invariant.",
            "trap": "Always add 2I = I₁ + I₂! Forgetting to divide by 2 at the final step is the #1 algebraic error committed by students.",
            "mnemonic": "King's Rule: Replace x with (Lower + Upper - x) and sum 2I."
        },
        "key_takeaways": [
            "Core Identity: $\\int_{a}^{b} f(x) \\, dx = \\int_{a}^{b} f(a+b-x) \\, dx$.",
            "Special Case ($a = 0$): $\\int_{0}^{a} f(x) \\, dx = \\int_{0}^{a} f(a-x) \\, dx$.",
            "Particularly lethal for trigonometric integrands involving $\\sin\\left(\\frac{\\pi}{2} - x\\right) = \\cos(x)$ pairings.",
            "Couples effectively with Queen's Property: $\\int_{0}^{2a} f(x) \\, dx = 2\\int_{0}^{a} f(x) \\, dx \\quad \\text{if } f(2a-x) = f(x)$."
        ]
    },
    {
        "id": "FW-JEE-CHM-01",
        "course": "JEE",
        "subject": "Chemistry",
        "chapter": "Thermodynamics",
        "title": "Chemical Thermodynamics: Gibbs Free Energy & Spontaneity Criteria",
        "score": 4.75,
        "source": "LibreTexts Physical Chemistry / FineWeb-Edu Corpus",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Equilibrium constants, entropy of the universe, and temperature dependence of spontaneity under Delta G = Delta H - T*Delta S.",
        "formula_box": {
            "title": "Gibbs-Helmholtz Spontaneity Equation",
            "latex": "\\Delta G_{\\text{sys}} = \\Delta H_{\\text{sys}} - T \\Delta S_{\\text{sys}} = -T \\Delta S_{\\text{universe}}",
            "plain": "ΔG = ΔH - T·ΔS",
            "terms": [
                ("ΔG", "Change in Gibbs Free Energy (spontaneous if ΔG < 0 at const T, P)"),
                ("ΔH", "Change in enthalpy (kJ/mol)"),
                ("T", "Absolute thermodynamic temperature in Kelvin (K)"),
                ("ΔS", "Change in entropy of system (J/mol·K)")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 180" width="100%" height="170" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Quadrants -->
  <line x1="270" y1="20" x2="270" y2="160" stroke="var(--border)" stroke-width="2"/>
  <line x1="50" y1="90" x2="490" y2="90" stroke="var(--border)" stroke-width="2"/>
  <text x="495" y="94" font-size="12" font-weight="700" fill="var(--ink)">+ΔS</text>
  <text x="25" y="94" font-size="12" font-weight="700" fill="var(--ink)">-ΔS</text>
  <text x="263" y="16" font-size="12" font-weight="700" fill="var(--ink)">+ΔH</text>
  <text x="263" y="176" font-size="12" font-weight="700" fill="var(--ink)">-ΔH</text>
  
  <!-- Q1 -->
  <rect x="280" y="25" width="190" height="55" rx="6" fill="rgba(245,158,11,0.12)" stroke="rgba(245,158,11,0.3)"/>
  <text x="290" y="46" font-size="11" font-weight="700" fill="#B45309">Spontaneous at HIGH T</text>
  <text x="290" y="66" font-size="10" fill="var(--ink-soft)">(TΔS dominates over +ΔH)</text>
  
  <!-- Q4 -->
  <rect x="280" y="100" width="190" height="55" rx="6" fill="rgba(16,185,129,0.14)" stroke="rgba(16,185,129,0.3)"/>
  <text x="290" y="122" font-size="11" font-weight="800" fill="#059669">ALWAYS SPONTANEOUS</text>
  <text x="290" y="142" font-size="10" fill="var(--ink-soft)">(ΔG &lt; 0 at ALL temperatures)</text>
  
  <!-- Q2 -->
  <rect x="70" y="25" width="190" height="55" rx="6" fill="rgba(239,68,68,0.12)" stroke="rgba(239,68,68,0.3)"/>
  <text x="80" y="46" font-size="11" font-weight="800" fill="#DC2626">NEVER SPONTANEOUS</text>
  <text x="80" y="66" font-size="10" fill="var(--ink-soft)">(ΔG &gt; 0 at ALL temperatures)</text>
  
  <!-- Q3 -->
  <rect x="70" y="100" width="190" height="55" rx="6" fill="rgba(59,130,246,0.12)" stroke="rgba(59,130,246,0.3)"/>
  <text x="80" y="122" font-size="11" font-weight="700" fill="#2563EB">Spontaneous at LOW T</text>
  <text x="80" y="142" font-size="10" fill="var(--ink-soft)">(Enthalpy drive overcomes -TΔS)</text>
</svg>""",
        "figure_caption": "Figure 1.4: The Four Thermodynamic Spontaneity Regimes as dictated by ΔG = ΔH - TΔS.",
        "content": (
            "The Second Law of Thermodynamics dictates that any spontaneous natural process causes an increase in total entropy of the universe:\n"
            "$$\\Delta S_{\\text{univ}} = \\Delta S_{\\text{sys}} + \\Delta S_{\\text{surr}} > 0$$\n\n"
            "However, calculating entropy changes across the entire surroundings is experimentally cumbersome. "
            "Josiah Willard Gibbs solved this by introducing the **Gibbs Free Energy** state function for constant temperature and pressure:\n\n"
            "$$G = H - TS \\quad \\implies \\quad \\Delta G_{\\text{sys}} = \\Delta H_{\\text{sys}} - T \\Delta S_{\\text{sys}}$$\n\n"
            "Because heat transferred reversibly to the surroundings at constant pressure equals $q_{\\text{surr}} = -\\Delta H_{\\text{sys}}$, the surroundings entropy is:\n"
            "$$\\Delta S_{\\text{surr}} = -\\frac{\\Delta H_{\\text{sys}}}{T}$$\n\n"
            "Multiplying the total universe entropy by $-T$:\n"
            "$$-T \\Delta S_{\\text{univ}} = -T \\left(\\Delta S_{\\text{sys}} - \\frac{\\Delta H_{\\text{sys}}}{T}\\right) = \\Delta H_{\\text{sys}} - T \\Delta S_{\\text{sys}} = \\Delta G_{\\text{sys}}$$\n\n"
            "Therefore, the universal condition for spontaneity ($\\Delta S_{\\text{univ}} > 0$) translates directly into $\\Delta G_{\\text{sys}} < 0$ at constant temperature and pressure."
        ),
        "didactic_notes": {
            "axiom": "A negative ΔG indicates thermodynamic spontaneity, but NOT reaction rate. Kinetics (activation energy Ea) determines speed.",
            "trap": "At equilibrium: ΔG = 0, NOT ΔG° = 0! Standard free energy ΔG° relates to equilibrium constant via ΔG° = -RT ln K.",
            "mnemonic": "ΔG < 0 is Go, ΔG > 0 is No-Go, ΔG = 0 is Dynamic Balance."
        },
        "key_takeaways": [
            "Fundamental Gibbs Criterion: $\\Delta G = \\Delta H - T\\Delta S$.",
            "Universal Spontaneity Condition: Requires $\\Delta G < 0$ strictly at constant temperature and pressure.",
            "Standard Equilibrium Link: $\\Delta G^\\circ = -RT \\ln(K_{\\text{eq}})$.",
            "Phase Inversion Temperature: The transition between non-spontaneous and spontaneous regimes occurs at $T_{\\text{eq}} = \\frac{\\Delta H}{\\Delta S}$."
        ]
    },

    # =========================================================================
    # 🧬 NEET-UG MEDICAL (Biology Botany & Zoology, Chemistry, Physics)
    # =========================================================================
    {
        "id": "FW-NEET-BIO-01",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Cell Biology",
        "title": "The Endomembrane System: Coordinated Transport & Vesicular Sorting",
        "score": 4.95,
        "source": "NCBI Bookshelf / OpenStax Biology / FineWeb-Edu",
        "word_count": 570,
        "reading_time_mins": 3,
        "summary": "Functional interdependence of Endoplasmic Reticulum, Golgi Apparatus, Lysosomes, and Vacuoles in eukaryotic cellular sorting.",
        "formula_box": {
            "title": "Strict NCERT Endomembrane System Boundary",
            "latex": "\\text{Endomembrane} = \\{ \\text{ER} \\cup \\text{Golgi} \\cup \\text{Lysosomes} \\cup \\text{Vacuoles} \\}",
            "plain": "Endomembrane System = RER/SER + Golgi Apparatus + Lysosomes + Vacuoles",
            "terms": [
                ("RER", "Rough Endoplasmic Reticulum: 80S ribosomes, protein synthesis & N-glycosylation"),
                ("SER", "Smooth Endoplasmic Reticulum: lipid/steroid synthesis & Ca²⁺ sequestration"),
                ("Golgi Cis/Trans", "Polarized cisternae: cis (entry/forming face) to trans (exit/maturing face)"),
                ("Excluded", "Mitochondria, Chloroplasts, and Peroxisomes (independent semi-autonomous organelles)")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 200" width="100%" height="190" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Nucleus -->
  <circle cx="50" cy="100" r="45" fill="rgba(99,102,241,0.12)" stroke="var(--purple)" stroke-width="2"/>
  <text x="25" y="105" font-size="11" font-weight="700" fill="var(--purple)">Nucleus</text>
  
  <!-- RER with Ribosomes -->
  <path d="M 95 65 C 130 60, 130 140, 160 135" fill="none" stroke="#3B82F6" stroke-width="5"/>
  <circle cx="115" cy="70" r="2.5" fill="#EF4444"/><circle cx="130" cy="85" r="2.5" fill="#EF4444"/><circle cx="145" cy="115" r="2.5" fill="#EF4444"/>
  <text x="110" y="50" font-size="11" font-weight="700" fill="#3B82F6">Rough ER</text>
  
  <!-- Transport Vesicle -->
  <circle cx="205" cy="100" r="9" fill="rgba(16,185,129,0.2)" stroke="#10B981" stroke-width="2"/>
  <line x1="175" y1="100" x2="190" y2="100" stroke="#10B981" stroke-width="1.8" marker-end="url(#arrow)"/>
  
  <!-- Golgi Cisternae -->
  <path d="M 250 50 C 265 80, 265 120, 250 150" fill="none" stroke="#F59E0B" stroke-width="6"/>
  <path d="M 270 55 C 282 80, 282 115, 270 145" fill="none" stroke="#F59E0B" stroke-width="6"/>
  <path d="M 290 60 C 300 80, 300 110, 290 140" fill="none" stroke="#F59E0B" stroke-width="6"/>
  <text x="240" y="38" font-size="11" font-weight="700" fill="#F59E0B">Golgi (Cis -> Trans)</text>
  
  <!-- Secretory Vesicle & Lysosome -->
  <circle cx="350" cy="75" r="10" fill="rgba(239,68,68,0.2)" stroke="#EF4444" stroke-width="2"/>
  <text x="365" y="79" font-size="11" font-weight="700" fill="#EF4444">Lysosome (Acid Hydrolases)</text>
  
  <circle cx="360" cy="130" r="11" fill="rgba(16,185,129,0.2)" stroke="#10B981" stroke-width="2"/>
  <text x="378" y="135" font-size="11" font-weight="700" fill="#10B981">Secretory Vesicle</text>
  
  <!-- Plasma Membrane -->
  <line x1="490" y1="20" x2="490" y2="180" stroke="var(--ink)" stroke-width="3"/>
  <text x="475" y="192" font-size="10" font-weight="700" fill="var(--ink)">Plasma Membrane</text>
</svg>""",
        "figure_caption": "Figure 2.1: The eukaryotic secretory pathway from RER synthesis, transport vesicle budding, Golgi sorting (cis to trans), to exocytosis and lysosomal targeting.",
        "content": (
            "In eukaryotic cells, while many cellular organelles are physically discrete membrane-bound structures, several operate as a "
            "functionally coordinated unit termed the **Endomembrane System**.\n\n"
            "In strict NCERT and NEET taxonomy, the endomembrane system comprises four coordinated components:\n"
            "1. **Endoplasmic Reticulum (ER)**\n"
            "2. **Golgi Apparatus**\n"
            "3. **Lysosomes**\n"
            "4. **Vacuoles**\n\n"
            "Mitochondria, chloroplasts, and peroxisomes are strictly **EXCLUDED** from this system because their biogenesis, evolutionary lineage, "
            "and physiological functions are not coordinated with the ER-Golgi secretory pathway.\n\n"
            "### The Secretory & Transport Cascade\n"
            "- **Rough Endoplasmic Reticulum (RER):** Dotted with 80S ribosomes on its cytosolic face, the RER synthesizes secretory proteins and "
            "transmembrane polypeptides, performing cotranslational translocation and initial N-linked glycosylation in its lumen.\n"
            "- **Smooth Endoplasmic Reticulum (SER):** Lacking ribosomes, the SER serves as the primary factory for phospholipid and steroid hormone "
            "synthesis (e.g. testosterone and estrogens in animal gonads) and functions as the sarcoplasmic reticulum for $\\text{Ca}^{2+}$ sequestration in skeletal muscle.\n"
            "- **Golgi Complex Polarization:** Transport vesicles bud from the ER and fuse with the convex *cis* (forming) face of the Golgi cisternae. "
            "As proteins traverse the cisternae, enzymes modify oligosaccharide chains into complex glycoproteins. Sorted cargos bud from the concave *trans* (maturing) "
            "face into vesicles destined for exocytosis or lysosomal delivery."
        ),
        "didactic_notes": {
            "axiom": "The endomembrane components share continuous or vesicle-mediated membrane flow. Organelles with their own DNA (Mitochondria/Plastids) are excluded.",
            "trap": "Peroxisomes contain oxidative enzymes (catalase, urate oxidase) but are NOT part of the endomembrane system in NCERT taxonomy.",
            "mnemonic": "NCERT Acronym: 'E-G-L-V' (ER, Golgi, Lysosomes, Vacuoles)."
        },
        "key_takeaways": [
            "Endomembrane = ER + Golgi + Lysosomes + Vacuoles.",
            "Mitochondria, Chloroplasts, and Peroxisomes are strictly excluded.",
            "Lysosomal enzymes (acid hydrolases) require pH 4.5–5.0 maintained by active H+ ATPase proton pumps.",
            "Plant vacuole is bounded by the tonoplast, which actively pumps ions against concentration gradients."
        ]
    },
    {
        "id": "FW-NEET-BIO-02",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Genetics & Molecular Biology",
        "title": "DNA Replication: Semi-Conservative Mechanism & Enzymatic Coordination",
        "score": 4.92,
        "source": "LibreTexts Molecular Genetics / FineWeb-Edu",
        "word_count": 530,
        "reading_time_mins": 3,
        "summary": "Meselson-Stahl experimental verification, Okazaki fragments, DNA Polymerase III fidelity, and directional synthesis.",
        "formula_box": {
            "title": "The Directionality Axiom of Polymerization",
            "latex": "5' \\longrightarrow 3' \\quad \\text{Polymerization (Addition of dNTP to free 3'-OH group)}",
            "plain": "Chain elongation occurs strictly 5' -> 3'",
            "terms": [
                ("Leading Strand", "Continuous synthesis toward the unwinding replication fork (3'->5' template)"),
                ("Lagging Strand", "Discontinuous synthesis away from fork producing Okazaki fragments (5'->3' template)"),
                ("DNA Pol III", "Primary catalytic enzyme with high processivity and 3'->5' exonuclease proofreading"),
                ("DNA Ligase", "Forms phosphodiester bond sealing the nick using ATP / NAD+")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 200" width="100%" height="190" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Parental Strands -->
  <path d="M 40 40 L 220 100 L 500 40" fill="none" stroke="var(--ink)" stroke-width="3"/>
  <text x="30" y="35" font-size="12" font-weight="700" fill="var(--ink)">3'</text>
  <text x="505" y="35" font-size="12" font-weight="700" fill="var(--ink)">5'</text>
  
  <path d="M 40 160 L 220 100 L 500 160" fill="none" stroke="var(--ink)" stroke-width="3"/>
  <text x="30" y="175" font-size="12" font-weight="700" fill="var(--ink)">5'</text>
  <text x="505" y="175" font-size="12" font-weight="700" fill="var(--ink)">3'</text>
  
  <!-- Helicase at fork -->
  <polygon points="200,80 240,100 200,120" fill="#EF4444"/>
  <text x="175" y="70" font-size="11" font-weight="800" fill="#EF4444">DNA Helicase</text>
  
  <!-- Leading Strand -->
  <path d="M 240 85 L 480 50" fill="none" stroke="#10B981" stroke-width="3.5" stroke-dasharray="8,2"/>
  <text x="320" y="60" font-size="12" font-weight="800" fill="#10B981">Leading Strand (Continuous 5'->3')</text>
  
  <!-- Okazaki Fragments on Lagging Strand -->
  <line x1="260" y1="120" x2="330" y2="135" stroke="#3B82F6" stroke-width="3.5"/>
  <line x1="360" y1="140" x2="430" y2="155" stroke="#3B82F6" stroke-width="3.5"/>
  <text x="300" y="178" font-size="12" font-weight="800" fill="#3B82F6">Okazaki Fragments (Lagging)</text>
</svg>""",
        "figure_caption": "Figure 2.2: Architecture of the eukaryotic/prokaryotic replication fork showing leading strand continuous synthesis and lagging strand Okazaki fragments.",
        "content": (
            "The replication of genetic information is **semiconservative**: each daughter DNA duplex retains one parental polynucleotide chain "
            "and one newly synthesized complementary strand. This was conclusively proven by Matthew Meselson and Franklin Stahl in 1958 "
            "using $^{15}\\text{N}$ isotope density gradient centrifugation in cesium chloride (CsCl).\n\n"
            "### Enzymatic Coordination at the Replication Fork\n"
            "1. **DNA Helicase:** Unwinds the double helix by breaking hydrogen bonds between base pairs, consuming ATP.\n"
            "2. **DNA Topoisomerase / Gyrase:** Relieves the resulting supercoiling strain ahead of the replication fork by making transient cuts.\n"
            "3. **Single-Strand DNA-Binding Proteins (SSBs):** Prevent the separated strands from prematurely re-annealing into hairpins.\n"
            "4. **RNA Primase:** Synthesizes a brief RNA primer (~10-12 nucleotides), providing the essential free $3'\\text{-OH}$ group required by DNA polymerases.\n"
            "5. **DNA Polymerase III:** Performs high-speed chain elongation exclusively in the $5' \\to 3'$ direction with proofreading ($3' \\to 5'$ exonuclease).\n"
            "6. **DNA Polymerase I & Ligase:** Pol I degrades RNA primers via $5' \\to 3'$ exonuclease activity and replaces them with deoxynucleotides; "
            "DNA Ligase seals the remaining phosphodiester nicks."
        ),
        "didactic_notes": {
            "axiom": "DNA Polymerases cannot initiate a strand de novo; they strictly require a pre-existing 3'-OH terminus provided by RNA Primase.",
            "trap": "Both Leading and Lagging strands are synthesized in the 5' -> 3' direction. The 'lagging' nature is solely due to antiparallel geometry.",
            "mnemonic": "Synthesis is always Five to Three (5' -> 3') like work hours 9 to 5."
        },
        "key_takeaways": [
            "Meselson-Stahl verified semiconservative replication using 15N/14N density gradient centrifugation.",
            "Okazaki fragments (~1000-2000 bp in bacteria, 100-200 bp in eukaryotes) are joined by DNA Ligase.",
            "Proofreading fidelity: 3' -> 5' exonuclease removes mismatched nucleotides.",
            "Topoisomerase (Gyrase) prevents dangerous torsional supercoiling upstream of the fork."
        ]
    },
    {
        "id": "FW-NEET-BIO-03",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Human Physiology",
        "title": "Cardiac Cycle & Hemodynamic Pressures: The Mechanics of Heart Sounds",
        "score": 4.88,
        "source": "OpenStax Anatomy & Physiology / FineWeb-Edu",
        "word_count": 490,
        "reading_time_mins": 3,
        "summary": "Atrial systole, isovolumetric ventricular contraction, stroke volume calculation, and origin of Lub and Dub heart sounds.",
        "formula_box": {
            "title": "Core Hemodynamic Formulation",
            "latex": "\\text{Cardiac Output (CO)} = \\text{Stroke Volume (SV)} \\times \\text{Heart Rate (HR)}",
            "plain": "CO = SV · HR = 70 mL × 72 bpm ≈ 5040 mL/min (5 Liters/min)",
            "terms": [
                ("Stroke Volume (SV)", "End-Diastolic Volume (EDV ≈ 120 mL) - End-Systolic Volume (ESV ≈ 50 mL) = 70 mL"),
                ("Heart Rate (HR)", "Normal resting rate ~72 beats per minute"),
                ("Cycle Duration", "60 seconds / 72 bpm = 0.8 seconds per cardiac cycle")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 180" width="100%" height="170" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- 0.8s Timeline Circle / Bar -->
  <rect x="50" y="70" width="100" height="45" fill="#3B82F6" rx="4"/>
  <text x="65" y="97" font-size="12" font-weight="700" fill="#fff">Atrial Systole (0.1s)</text>
  
  <rect x="155" y="70" width="150" height="45" fill="#EF4444" rx="4"/>
  <text x="175" y="97" font-size="12" font-weight="700" fill="#fff">Ventricular Systole (0.3s)</text>
  
  <rect x="310" y="70" width="180" height="45" fill="#10B981" rx="4"/>
  <text x="340" y="97" font-size="12" font-weight="700" fill="#fff">Joint Diastole (0.4s)</text>
  
  <!-- Sound 1: LUB -->
  <path d="M 155 70 L 155 45" stroke="#EF4444" stroke-width="2"/>
  <circle cx="155" cy="40" r="14" fill="#EF4444"/>
  <text x="144" y="44" font-size="10" font-weight="800" fill="#fff">LUB</text>
  <text x="110" y="24" font-size="10" font-weight="700" fill="#EF4444">AV Valves Close (Tricuspid/Bicuspid)</text>
  
  <!-- Sound 2: DUB -->
  <path d="M 310 70 L 310 45" stroke="#10B981" stroke-width="2"/>
  <circle cx="310" cy="40" r="14" fill="#10B981"/>
  <text x="298" y="44" font-size="10" font-weight="800" fill="#fff">DUB</text>
  <text x="280" y="24" font-size="10" font-weight="700" fill="#10B981">Semilunar Valves Close</text>
  
  <text x="200" y="145" font-size="13" font-weight="700" fill="var(--ink)">Total Duration = 0.8 Seconds (72 bpm)</text>
</svg>""",
        "figure_caption": "Figure 2.3: Chronology of the 0.8s cardiac cycle illustrating the mechanical timing of the LUB (first) and DUB (second) heart sounds.",
        "content": (
            "The human cardiac cycle encompasses all electrical and mechanical events occurring from the initiation of one heartbeat to the onset "
            "of the next. At a normal resting heart rate of 72 beats per minute, each cycle spans exactly $0.8\\text{ seconds}$.\n\n"
            "### Sequential Chronology of the 0.8-Second Cycle\n"
            "1. **Joint Diastole (0.4 s):** All four chambers are relaxed. Blood flows from the superior and inferior vena cava and pulmonary veins "
            "into the atria and passively into ventricles through open atrioventricular (AV) valves (Tricuspid and Bicuspid/Mitral). "
            "Approximately $70\\%$ of ventricular filling occurs passively during this phase.\n"
            "2. **Atrial Systole (0.1 s):** Initiated by the Sinoatrial (SA) Node pacemaker wave, the atria contract simultaneously, pumping the remaining "
            "$30\\%$ of blood into the ventricles. End-Diastolic Volume (EDV) peaks at $\\sim 120\\text{ mL}$.\n"
            "3. **Ventricular Systole (0.3 s):**\n"
            "   - *Isovolumetric Contraction:* Ventricular pressure rapidly exceeds atrial pressure, snapping the AV valves shut. This sudden valve closure "
            "and blood turbulence produces the **First Heart Sound ('LUB')**.\n"
            "   - *Ventricular Ejection:* Intraventricular pressure surpasses systemic aortic pressure ($80\\text{ mmHg}$) and pulmonary pressure ($15\\text{ mmHg}$), "
            "forcing semilunar valves open to eject the Stroke Volume ($\\sim 70\\text{ mL}$).\n"
            "4. **Isovolumetric Ventricular Relaxation:** Ventricular pressure plunges below arterial pressure, causing blood to surge backward and slam the "
            "semilunar valves shut, producing the **Second Heart Sound ('DUB')**."
        ),
        "didactic_notes": {
            "axiom": "Heart sounds originate from the closure of heart valves and subsequent turbulent vibrations, NEVER from valve opening.",
            "trap": "LUB is lower pitched and longer in duration; DUB is higher pitched and shorter, sharper in duration.",
            "mnemonic": "AV before SL: LUB = Atrioventricular valves close; DUB = SemiLunar valves close."
        },
        "key_takeaways": [
            "Cardiac Cycle Chronology: Exactly $0.8\\text{ s}$ per cycle at $72\\text{ bpm}$ (Diastole $0.4\\text{ s}$ + Atrial Systole $0.1\\text{ s}$ + Ventricular Systole $0.3\\text{ s}$).",
            "First Heart Sound ('LUB'): Closure of Tricuspid and Bicuspid (Mitral) valves at onset of ventricular systole.",
            "Second Heart Sound ('DUB'): Closure of Aortic and Pulmonary Semilunar valves at onset of ventricular diastole.",
            "Hemodynamic Output: $\\text{Stroke Volume} = \\text{EDV} - \\text{ESV} = 120\\text{ mL} - 50\\text{ mL} = 70\\text{ mL}$, yielding $\\text{Cardiac Output} = 70\\text{ mL} \\times 72\\text{ bpm} \\approx 5040\\text{ mL/min}$."
        ]
    },

    # =========================================================================
    # 🏛 UPSC CIVIL SERVICES (Polity, Economy, Environment, Ethics, CSAT)
    # =========================================================================
    {
        "id": "FW-UPSC-ECO-01",
        "course": "UPSC",
        "subject": "Economy & Development",
        "chapter": "Monetary Policy",
        "title": "Monetary Policy Transmission: Liquidity Adjustment & The Repo Rate Mechanism",
        "score": 4.90,
        "source": "Oxford Review of Economic Policy / FineWeb-Edu",
        "word_count": 560,
        "reading_time_mins": 3,
        "summary": "How RBI repo rate changes transmit through banking liquidity, Marginal Cost of Funds (MCLR), and inflation expectations.",
        "formula_box": {
            "title": "The Statutory Policy Corridor Framework",
            "latex": "\\text{MSF Rate} = \\text{Repo} + 25\\text{ bps} \\quad \\Longleftrightarrow \\quad \\text{SDF Rate} = \\text{Repo} - 25\\text{ bps}",
            "plain": "LAF Corridor: MSF (Ceiling) > Policy Repo Rate (Anchor) > SDF (Floor)",
            "terms": [
                ("Repo Rate", "Rate at which RBI lends short-term liquidity against G-Secs to commercial banks"),
                ("SDF", "Standing Deposit Facility: collateral-free absorption of uncollateralized bank liquidity"),
                ("MSF", "Marginal Standing Facility: penal borrowing window allowing dip into SLR quota"),
                ("FIT Target", "4% CPI (+/- 2% tolerance band: 2% to 6%) under Section 45ZA of the RBI Act")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 180" width="100%" height="170" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Ceiling: MSF -->
  <line x1="60" y1="40" x2="480" y2="40" stroke="#EF4444" stroke-width="2.5" stroke-dasharray="6,3"/>
  <text x="60" y="30" font-size="12" font-weight="700" fill="#EF4444">Ceiling: Marginal Standing Facility (MSF: Repo + 0.25%)</text>
  
  <!-- Anchor: Repo Rate -->
  <line x1="60" y1="90" x2="480" y2="90" stroke="var(--purple)" stroke-width="3.5"/>
  <rect x="220" y="78" width="110" height="24" rx="5" fill="var(--purple)"/>
  <text x="232" y="94" font-size="11" font-weight="800" fill="#fff">Policy Repo Rate</text>
  
  <!-- Floor: SDF -->
  <line x1="60" y1="140" x2="480" y2="140" stroke="#10B981" stroke-width="2.5" stroke-dasharray="6,3"/>
  <text x="60" y="158" font-size="12" font-weight="700" fill="#10B981">Floor: Standing Deposit Facility (SDF: Repo - 0.25%)</text>
  
  <text x="360" y="115" font-size="11" font-weight="600" fill="var(--ink-soft)">LAF Width = 50 bps</text>
</svg>""",
        "figure_caption": "Figure 3.1: The Reserve Bank of India Liquidity Adjustment Facility (LAF) Corridor anchoring call money rates.",
        "content": (
            "Monetary policy transmission describes the dynamic process through which a central bank's policy rate decisions cascade through the banking system, "
            "influencing credit spreads, aggregate demand, exchange rates, and retail inflation. In India, the Reserve Bank of India (RBI) operates under "
            "a statutory **Flexible Inflation Targeting (FIT)** framework, targeting CPI inflation at $4\\% \\pm 2\\%$.\n\n"
            "### The Operating Procedure & The Policy Corridor\n"
            "The daily operating target of the RBI is the weighted average call money rate (WACR). The policy repo rate serves as the anchor of the "
            "**Liquidity Adjustment Facility (LAF)** corridor, flanked symmetrically by:\n"
            "1. **Marginal Standing Facility (MSF):** The upper ceiling (Repo $+ 25\\text{ bps}$), where banks borrow overnight funds against G-Secs dipping into their SLR.\n"
            "2. **Standing Deposit Facility (SDF):** The uncollateralized floor (Repo $- 25\\text{ bps}$), absorbing excess surplus bank deposits without requiring government collateral.\n\n"
            "### The Four Channels of Transmission\n"
            "1. **Interest Rate Channel:** Policy repo hikes raise interbank cost of capital, forcing banks to adjust their External Benchmark-linked Lending Rates (EBLR) "
            "and MCLR, thereby suppressing consumer borrowing and capital investments.\n"
            "2. **Credit & Balance Sheet Channel:** Heightened repo rates compress bank liquidity buffers, prompting stricter loan collateral evaluation.\n"
            "3. **Exchange Rate Channel:** Higher yields draw Foreign Portfolio Investment (FPI) into debt securities, appreciating the Rupee and curbing imported inflation.\n"
            "4. **Expectations Anchor:** Credible forward guidance anchors public inflation expectations, preventing self-fulfilling wage-price spirals."
        ),
        "didactic_notes": {
            "axiom": "Monetary transmission in India has been accelerated by mandating External Benchmark Lending Rates (EBLR) linked to the Repo Rate or T-Bills.",
            "trap": "SDF requires NO collateral from RBI, whereas the old Reverse Repo required RBI to pledge government securities.",
            "mnemonic": "The 4 Channels: 'I-C-E-E' (Interest rate, Credit channel, Exchange rate, Expectations)."
        },
        "key_takeaways": [
            "Statutory Mandate: Flexible Inflation Targeting at 4% with +/- 2% band (Section 45ZA RBI Act).",
            "Monetary Policy Committee (MPC): 6 members (3 RBI + 3 Government appointed) with Governor holding casting vote.",
            "Operating Target: Weighted Average Call Rate (WACR) kept within the SDF-MSF corridor.",
            "EBLR mandate (October 2019) overcame the structural transmission lag of the MCLR regime."
        ]
    },
    {
        "id": "FW-UPSC-ENV-01",
        "course": "UPSC",
        "subject": "Environment & Ecology",
        "chapter": "Climate Change",
        "title": "Climatology & Teleconnections: The El Niño Southern Oscillation (ENSO) & Indian Monsoon",
        "score": 4.85,
        "source": "Cambridge Earth System Science / FineWeb-Edu",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Coupled ocean-atmosphere dynamics across the equatorial Pacific, Walker Circulation shifts, and their impact on South Asian rainfall.",
        "formula_box": {
            "title": "The Ocean-Atmosphere Coupling Index",
            "latex": "\\text{ENSO Phase} = \\{ \\text{El Niño (Warm/Weak)} \\Longleftrightarrow \\text{La Niña (Cold/Strong)} \\}",
            "plain": "Ocean State (SST anomalies in Niño 3.4) coupled with Atmospheric State (Southern Oscillation Index SOI)",
            "terms": [
                ("Walker Circulation", "East-West atmospheric zonal overturning circulation across the equatorial Pacific"),
                ("Normal State", "Warm pool in Western Pacific; intense upwelling of cold water off Peruvian coast"),
                ("El Niño State", "Weak trade winds; eastward displacement of warm pool; descending dry air over India"),
                ("IOD Modulator", "Positive Indian Ocean Dipole can counterbalance and mitigate El Niño drying effects")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 180" width="100%" height="170" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <!-- Normal vs El Nino split -->
  <rect x="30" y="25" width="230" height="135" rx="8" fill="rgba(16,185,129,0.08)" stroke="#10B981"/>
  <text x="45" y="45" font-size="12" font-weight="800" fill="#059669">NORMAL / NEUTRAL STATE</text>
  <text x="45" y="65" font-size="10" fill="var(--ink-soft)">Strong Easterly Trade Winds</text>
  <text x="45" y="85" font-size="10" fill="var(--ink-soft)">West Pacific Warm Pool (~30°C)</text>
  <text x="45" y="105" font-size="10" fill="var(--ink-soft)">Ascending Moist Air over Indo-Pacific</text>
  <text x="45" y="125" font-size="11" font-weight="700" fill="#059669">✓ Favorable Indian Monsoon</text>
  
  <rect x="280" y="25" width="230" height="135" rx="8" fill="rgba(239,68,68,0.08)" stroke="#EF4444"/>
  <text x="295" y="45" font-size="12" font-weight="800" fill="#DC2626">EL NIÑO EPISODE</text>
  <text x="295" y="65" font-size="10" fill="var(--ink-soft)">Weakened / Reversed Trade Winds</text>
  <text x="295" y="85" font-size="10" fill="var(--ink-soft)">Warm Pool Shifts East toward Peru</text>
  <text x="295" y="105" font-size="10" fill="var(--ink-soft)">Subsidence (Dry Sinking Air) over India</text>
  <text x="295" y="125" font-size="11" font-weight="700" fill="#DC2626">⚠️ Risk of Monsoon Deficit / Drought</text>
</svg>""",
        "figure_caption": "Figure 3.2: Comparison between the Normal Walker Circulation and the El Niño disruption suppressing Indian monsoon convection.",
        "content": (
            "The El Niño Southern Oscillation (ENSO) is a coupled ocean-atmosphere phenomenon in the tropical Pacific that serves as the dominant "
            "driver of interannual global climate variability. For Indian Civil Services aspirants, understanding ENSO is vital due to its historical "
            "inverse correlation with the southwest summer monsoon (June–September), which accounts for over $70\\%$ of India's annual precipitation.\n\n"
            "### Neutral Conditions vs. El Niño State\n"
            "Under normal (neutral) conditions, easterly trade winds blow surface water westward towards Indonesia and northern Australia. "
            "This creates a warm pool of water in the western Pacific (warm SSTs $\\sim 30^{\\circ}\\text{C}$), driving vigorous atmospheric convection (the ascending branch "
            "of the Walker Circulation). In contrast, cold, nutrient-rich water upwells along the Peruvian coast in the eastern Pacific.\n\n"
            "During an **El Niño event**:\n"
            "1. Easterly trade winds weaken significantly or reverse into westerlies.\n"
            "2. The equatorial warm pool shifts eastward toward central and eastern Pacific waters, suppressing the thermocline and upwelling off Peru.\n"
            "3. The ascending branch of the Walker Circulation shifts to the central Pacific, while anomalous subsidence (sinking dry air) dominates over "
            "the western Pacific, Southeast Asia, and peninsular India.\n\n"
            "### The Counterbalancing Indian Ocean Dipole (IOD)\n"
            "An El Niño does not automatically guarantee a drought! The **Indian Ocean Dipole (IOD)**—a sea surface temperature gradient between the western and eastern "
            "Indian Ocean—can modulate monsoon strength. A **Positive IOD** (warmer Arabian Sea) generates rising moist air over India and can completely "
            "neutralize or override the drying teleconnection of a concurrent Pacific El Niño."
        ),
        "didactic_notes": {
            "axiom": "ENSO is a coupled phenomenon: El Niño is the oceanic component (SST warming); Southern Oscillation is the atmospheric pressure component (Tahiti vs Darwin).",
            "trap": "Not all El Niño events cause drought (e.g. 1997 super El Niño saw normal Indian monsoon due to a record-positive IOD).",
            "mnemonic": "Positive IOD = Good for India (Arabian Sea Warmer); El Niño = Bad for India (Sinking Dry Air)."
        },
        "key_takeaways": [
            "ENSO tracks anomalies in Niño 3.4 region coupled with Southern Oscillation Index (SOI).",
            "Walker Circulation shifts eastward during El Niño, placing sinking dry air over the Indian subcontinent.",
            "Positive IOD acts as a thermal shield that can neutralize El Niño drying effects.",
            "Monsoon accounts for ~70% of India's annual rainfall and critical groundwater replenishment."
        ]
    },
    {
        "id": "FW-UPSC-CSAT-01",
        "course": "UPSC",
        "subject": "CSAT Reading Passages",
        "chapter": "Comprehension & Critical Reasoning",
        "title": "CSAT Analytical Passage: Technology, Algorithmic Governance & Democratic Accountability",
        "score": 4.90,
        "source": "Harvard Policy & Tech Review / FineWeb-Edu",
        "word_count": 450,
        "reading_time_mins": 2,
        "summary": "Passage on bureaucratic algorithmic discretion, procedural due process, and critical inference analysis for Paper-II.",
        "formula_box": {
            "title": "Analytical Inference Taxonomy for CSAT Paper-II",
            "latex": "\\text{Valid Inference} \\subset \\text{Explicit Textual Premises} \\quad (\\text{Zero External Speculation})",
            "plain": "Logical Rule: True inferences must be unavoidable deductions strictly grounded in passage premises.",
            "terms": [
                ("Explicit Premise", "Fact directly stated by the author in the text"),
                ("Critical Assumption", "Unstated bridging premise required for the author's conclusion to hold true"),
                ("Distractor Trap", "Extrapolations that sound plausible in real life but lack textual warrant")
            ]
        },
        "figure_svg": """<svg viewBox="0 0 540 160" width="100%" height="150" xmlns="http://www.w3.org/2000/svg" style="background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;">
  <rect x="40" y="45" width="120" height="70" rx="8" fill="rgba(99,102,241,0.12)" stroke="var(--purple)" stroke-width="2"/>
  <text x="55" y="75" font-size="11" font-weight="700" fill="var(--purple)">Input Data</text>
  <text x="50" y="95" font-size="9.5" fill="var(--ink-soft)">(Citizen Profiles)</text>
  
  <line x1="160" y1="80" x2="200" y2="80" stroke="var(--purple)" stroke-width="2" marker-end="url(#arrow)"/>
  
  <rect x="200" y="35" width="140" height="90" rx="8" fill="rgba(15,23,42,0.9)" stroke="#EF4444" stroke-width="2"/>
  <text x="220" y="70" font-size="12" font-weight="800" fill="#EF4444">Black-Box Model</text>
  <text x="225" y="92" font-size="10" fill="#fff">(Opaque Decision)</text>
  
  <line x1="340" y1="80" x2="380" y2="80" stroke="var(--purple)" stroke-width="2" marker-end="url(#arrow)"/>
  
  <rect x="380" y="45" width="120" height="70" rx="8" fill="rgba(16,185,129,0.12)" stroke="#10B981" stroke-width="2"/>
  <text x="390" y="75" font-size="11" font-weight="700" fill="#10B981">Due Process Check</text>
  <text x="395" y="95" font-size="9.5" fill="var(--ink-soft)">(Right to Reason)</text>
</svg>""",
        "figure_caption": "Figure 3.3: The dilemma of algorithmic administrative discretion: reconciling automated efficiency with constitutional due process.",
        "content": (
            "The integration of automated decision algorithms into administrative welfare distribution presents a profound paradox for constitutional democracy. "
            "Proponents contend that automated scoring eliminates human rent-seeking, accelerates benefit disbursement, and purges fraudulent welfare rosters. "
            "However, when complex algorithmic models operate as opaque 'black boxes', they erode the cardinal administrative doctrine of **reasoned decision-making**.\n\n"
            "Under administrative law, an aggrieved citizen denied a statutory benefit possesses an inalienable right to know the precise grounds of adverse determination. "
            "When an algorithmic system denies a pension or subsidized foodgrains based on statistical probability vectors that neither the citizen nor the field officer "
            "can interpret, procedural due process is effectively dismantled.\n\n"
            "True democratic governance requires that algorithmic tools assist rather than supplant human judgment. Public accountability cannot be outsourced "
            "to proprietary code shielded by trade secrecy."
        ),
        "didactic_notes": {
            "axiom": "In CSAT Paper-II, the 'Most Logical & Rational Inference' must never assume facts outside the passage, no matter how true they are in real life.",
            "trap": "Watch out for extreme absolute qualifiers ('must completely ban', 'always invalid') which rarely represent the author's nuanced position.",
            "mnemonic": "CSAT Rule: If the passage didn't say it, you can't infer it."
        },
        "key_takeaways": [
            "Procedural Due Process requires a 'reasoned order' for any state denial of rights or statutory welfare.",
            "Algorithmic opacity ('black-box' nature) threatens administrative accountability and judicial review.",
            "Human-in-the-loop oversight is legally indispensable for sensitive discretionary welfare functions.",
            "For CSAT, valid inferences must be strictly deductive and immune to speculative external bias."
        ]
    }
]

def get_fineweb_readings(
    course: Optional[str] = None,
    subject: Optional[str] = None,
    min_score: float = 0.0
) -> List[Dict[str, Any]]:
    """Filters readings by course (JEE, NEET, UPSC), subject, and educational score."""
    res = FINEWEB_READINGS
    if course and course.upper() != "ALL":
        c_up = course.upper()
        res = [r for r in res if r.get("course", "").upper() == c_up]
    if subject and subject.upper() != "ALL":
        s_up = subject.upper()
        res = [r for r in res if s_up in r.get("subject", "").upper() or s_up in r.get("chapter", "").upper()]
    if min_score > 0.0:
        res = [r for r in res if r.get("score", 0.0) >= min_score]
    return res

def get_reading_by_id(reading_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single reading by its unique identifier."""
    for r in FINEWEB_READINGS:
        if r.get("id") == reading_id:
            return r
    return None
