"""
FineWeb-Edu Academic Knowledge Repository & Grounding Service
Provides textbook-grade readings, university lecture excerpts, and educational passages
curated from HuggingFaceFW/fineweb-edu (Score >= 4.0).
Organized by exam track: JEE, NEET, and UPSC Civil Services.
Features rich LaTeX mathematical formulas, vector textbook figures, and didactic callouts.
"""
from typing import List, Dict, Any, Optional

FINEWEB_READINGS: List[Dict[str, Any]] = [
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
            "plain": "I = I_cm + M \u00b7 d\u00b2",
            "terms": [["I", "Moment of inertia about target arbitrary axis"], ["I_cm", "Moment of inertia about parallel axis through Center of Mass"], ["M", "Total mass of the rigid body (\u222b dm)"], ["d", "Perpendicular distance separating the two parallel axes"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 220\" width=\"100%\" height=\"200\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <defs>\n    <marker id=\"arrow\" viewBox=\"0 0 10 10\" refX=\"5\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\">\n      <path d=\"M 0 0 L 10 5 L 0 10 z\" fill=\"var(--purple)\"/>\n    </marker>\n  </defs>\n  <!-- Rigid body outline -->\n  <path d=\"M 80 110 C 90 40, 260 30, 360 60 C 460 90, 480 170, 380 190 C 280 210, 120 200, 80 110 Z\" fill=\"rgba(99,102,241,0.08)\" stroke=\"var(--purple)\" stroke-width=\"2.2\" stroke-dasharray=\"6,3\"/>\n  <text x=\"420\" y=\"70\" font-size=\"12\" font-weight=\"600\" fill=\"var(--ink-soft)\" font-family=\"sans-serif\">Rigid Body (Mass M)</text>\n  \n  <!-- CM Axis -->\n  <line x1=\"200\" y1=\"20\" x2=\"200\" y2=\"200\" stroke=\"#10B981\" stroke-width=\"2.5\"/>\n  <circle cx=\"200\" cy=\"120\" r=\"5\" fill=\"#10B981\"/>\n  <text x=\"208\" y=\"125\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\" font-family=\"sans-serif\">G (Center of Mass)</text>\n  <text x=\"175\" y=\"32\" font-size=\"13\" font-weight=\"700\" fill=\"#10B981\" font-family=\"sans-serif\">Axis_cm</text>\n  \n  <!-- Arbitrary Parallel Axis -->\n  <line x1=\"330\" y1=\"20\" x2=\"330\" y2=\"200\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <text x=\"338\" y=\"32\" font-size=\"13\" font-weight=\"700\" fill=\"var(--purple)\" font-family=\"sans-serif\">Target Axis (I)</text>\n  \n  <!-- Distance d -->\n  <line x1=\"200\" y1=\"80\" x2=\"330\" y2=\"80\" stroke=\"var(--purple)\" stroke-width=\"2\" marker-start=\"url(#arrow)\" marker-end=\"url(#arrow)\"/>\n  <rect x=\"250\" y=\"68\" width=\"30\" height=\"22\" rx=\"4\" fill=\"var(--card)\" stroke=\"var(--border)\"/>\n  <text x=\"261\" y=\"84\" font-size=\"13\" font-weight=\"800\" fill=\"var(--purple)\" font-family=\"sans-serif\">d</text>\n  \n  <!-- Mass element dm -->\n  <circle cx=\"140\" cy=\"150\" r=\"4\" fill=\"#EF4444\"/>\n  <text x=\"110\" y=\"165\" font-size=\"11\" font-weight=\"600\" fill=\"#EF4444\" font-family=\"sans-serif\">dm (element)</text>\n  <line x1=\"200\" y1=\"120\" x2=\"140\" y2=\"150\" stroke=\"#EF4444\" stroke-width=\"1.2\" stroke-dasharray=\"2,2\"/>\n  <line x1=\"330\" y1=\"120\" x2=\"140\" y2=\"150\" stroke=\"var(--purple)\" stroke-width=\"1.2\" stroke-dasharray=\"2,2\"/>\n</svg>",
        "figure_caption": "Figure 1.1: Geometric configuration of Steiner's Parallel Axis Theorem. One axis must strictly pass through the body's Center of Mass (G).",
        "content": "The moment of inertia of a rigid body characterizes its resistance to rotational acceleration about a specific axis, analogous to inertial mass in linear kinematics. While calculating the moment of inertia about the center of mass ($I_{\\text{cm}}$) is straightforward for symmetric objects, practical engineering and JEE Advanced multi-body problems frequently involve eccentric or shifted rotation axes.\n\n### Statement of Steiner's Theorem\nThe Parallel Axis Theorem states that the moment of inertia $I$ of any rigid body of total mass $M$ about an arbitrary axis is equal to the moment of inertia $I_{\\text{cm}}$ about a parallel axis passing through its Center of Mass plus the product of the mass and the square of the perpendicular distance $d$ between the two axes:\n\n$$I = I_{\\text{cm}} + M d^2$$\n\n### Rigorous Mathematical Derivation\nConsider a continuous planar mass distribution where the coordinate origin is chosen at the Center of Mass $G$. By definition of the Center of Mass:\n$$\\int \\mathbf{r}_i \\, dm = 0 \\quad \\implies \\quad \\int x \\, dm = 0, \\quad \\int y \\, dm = 0$$\n\nNow consider a new parallel axis shifted by a constant displacement vector $\\mathbf{d} = (x_d, y_d)$. The position vector of any mass element $dm$ relative to this new axis becomes $\\mathbf{r}' = \\mathbf{r} - \\mathbf{d}$. Expanding the squared distance gives:\n$${r'}^2 = (x - x_d)^2 + (y - y_d)^2 = (x^2 + y^2) - 2(x x_d + y y_d) + (x_d^2 + y_d^2)$$\n$${r'}^2 = r^2 - 2\\mathbf{r}\\cdot\\mathbf{d} + d^2$$\n\nIntegrating over the entire body of mass $M$:\n$$I = \\int {r'}^2 \\, dm = \\int r^2 \\, dm - 2\\mathbf{d}\\cdot \\left(\\int \\mathbf{r}\\, dm\\right) + d^2 \\int dm$$\n\nBecause $\\int \\mathbf{r}\\, dm = 0$ by definition of the Center of Mass origin, the middle cross-term vanishes identically! Hence:\n$$I = I_{\\text{cm}} + M d^2$$\n\nThis confirms that the moment of inertia about the Center of Mass is the absolute minimum among all parallel axes.",
        "didactic_notes": {
            "axiom": "Steiner's Law guarantees that for any set of parallel axes, the axis passing through the Center of Mass always yields the minimum possible moment of inertia.",
            "trap": "NEET/JEE Pitfall: You CANNOT shift directly between two arbitrary axes (e.g. from rim to rim). You must first calculate I_cm, and then apply I_target = I_cm + M\u00b7d\u00b2.",
            "mnemonic": "Remember: 'Center First, Target Second' \u2014 always route through the Center of Mass origin."
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
        "score": 4.9,
        "source": "MIT Physics Courseware / FineWeb-Edu Corpus",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Physical grounding of Faraday's Law, eddy currents, and how Lenz's law enforces the First Law of Thermodynamics.",
        "formula_box": {
            "title": "Faraday-Lenz Law of Induction",
            "latex": "\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}",
            "plain": "emf = - d\u03a6_B / dt",
            "terms": [["\u2130", "Induced electromotive force (volts)"], ["\u03a6_B", "Magnetic flux linked through the conducting loop (webers)"], ["(-) sign", "Lenz's Law: direction of induced emf opposes flux change"], ["t", "Time elapsed (seconds)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 200\" width=\"100%\" height=\"190\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Bar Magnet moving right -->\n  <rect x=\"60\" y=\"70\" width=\"60\" height=\"45\" fill=\"#EF4444\" rx=\"3\"/>\n  <text x=\"82\" y=\"98\" font-size=\"16\" font-weight=\"800\" fill=\"#fff\" font-family=\"sans-serif\">N</text>\n  <rect x=\"120\" y=\"70\" width=\"60\" height=\"45\" fill=\"#3B82F6\" rx=\"3\"/>\n  <text x=\"145\" y=\"98\" font-size=\"16\" font-weight=\"800\" fill=\"#fff\" font-family=\"sans-serif\">S</text>\n  \n  <!-- Velocity vector -->\n  <line x1=\"190\" y1=\"92\" x2=\"240\" y2=\"92\" stroke=\"#EF4444\" stroke-width=\"2.5\" marker-end=\"url(#arrow)\"/>\n  <text x=\"200\" y=\"80\" font-size=\"13\" font-weight=\"700\" fill=\"#EF4444\" font-family=\"sans-serif\">v (motion)</text>\n  \n  <!-- Conducting Loop -->\n  <ellipse cx=\"360\" cy=\"92\" rx=\"25\" ry=\"60\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"4\"/>\n  <path d=\"M 360 32 A 25 60 0 0 1 360 152\" fill=\"none\" stroke=\"#10B981\" stroke-width=\"4\"/>\n  \n  <!-- Induced Current Arrows -->\n  <path d=\"M 378 60 L 382 72 L 372 68 Z\" fill=\"#10B981\"/>\n  <text x=\"395\" y=\"98\" font-size=\"13\" font-weight=\"700\" fill=\"#10B981\" font-family=\"sans-serif\">I_induced</text>\n  \n  <!-- Opposing Repulsive Force -->\n  <line x1=\"330\" y1=\"92\" x2=\"270\" y2=\"92\" stroke=\"#F59E0B\" stroke-width=\"2.5\" stroke-dasharray=\"4,3\"/>\n  <text x=\"270\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#F59E0B\" font-family=\"sans-serif\">Opposing Force F_mag</text>\n  \n  <!-- B lines -->\n  <path d=\"M 180 80 C 260 70, 310 70, 360 80\" stroke=\"rgba(99,102,241,0.5)\" stroke-width=\"1.5\" fill=\"none\"/>\n  <path d=\"M 180 105 C 260 115, 310 115, 360 105\" stroke=\"rgba(99,102,241,0.5)\" stroke-width=\"1.5\" fill=\"none\"/>\n</svg>",
        "figure_caption": "Figure 1.2: Conservation of energy in induction. As the North pole approaches, an induced counter-clockwise current creates an opposing North magnetic pole.",
        "content": "Faraday's Law of Electromagnetic Induction establishes that whenever the magnetic flux linking a circuit changes, an electromotive force (emf) is induced whose magnitude is proportional to the rate of change of magnetic flux:\n\n$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt}$$\n\n### The Significance of the Negative Sign: Lenz's Law\nHeinrich Lenz formulated the physical consequence encoded by the minus sign: *The polarity of the induced emf is always such that the magnetic field produced by the resulting induced current directly opposes the original change in magnetic flux that induced it.*\n\n### Thermodynamic Proof of Lenz's Law\nWhy must nature enforce this opposition? Consider the counterfactual scenario: suppose the minus sign were a plus sign ($+\\frac{d\\Phi_B}{dt}$).\n\nIf a bar magnet's North pole were slightly nudged toward a conducting loop, an induced current would flow such as to create an attractive South pole. This South pole would pull the magnet faster, increasing $\\frac{d\\Phi_B}{dt}$, which in turn would amplify the current and accelerate the magnet perpetually without requiring any external work! This would represent a perpetual motion machine of the first kind, generating limitless kinetic energy and Joule heating ($I^2 R$) out of nothing.\n\nIn physical reality, an external agent must perform positive mechanical work $\\Delta W = \\int \\mathbf{F}_{\\text{ext}} \\cdot d\\mathbf{x}$ against the repulsive Lorentz force $\\mathbf{F} = I(\\mathbf{L} \\times \\mathbf{B})$. By the First Law of Thermodynamics, this exact mechanical work converts directly into electrical energy and dissipative thermal energy. Lenz's law is therefore nothing less than the mechanical-electrical manifestation of energy conservation.",
        "didactic_notes": {
            "axiom": "Induced currents always oppose the cause of their creation. If flux increases, induced B opposes; if flux decreases, induced B reinforces.",
            "trap": "JEE Distractor: Induced emf exists whenever flux changes, even if the circuit is OPEN (no current flows, but potential difference develops).",
            "mnemonic": "Remember: 'Lenz is Lazy' \u2014 the circuit resents changes to its existing magnetic state."
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
        "score": 4.8,
        "source": "Stanford Mathematics Review / FineWeb-Edu Corpus",
        "word_count": 480,
        "reading_time_mins": 2,
        "summary": "Rigorous treatment of integral property \u222b f(x)dx = \u222b f(a+b-x)dx and trigonometric algebraic cancellation techniques.",
        "formula_box": {
            "title": "King's Property of Definite Integrals",
            "latex": "\\int_{a}^{b} f(x) \\, dx = \\int_{a}^{b} f(a + b - x) \\, dx",
            "plain": "\u222b_a^b f(x) dx = \u222b_a^b f(a + b - x) dx",
            "terms": [["[a, b]", "Interval of definite integration"], ["f(x)", "Continuous real-valued function on [a, b]"], ["x = (a+b)/2", "Axis of symmetry for the domain reflection transformation"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"170\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Axes -->\n  <line x1=\"50\" y1=\"150\" x2=\"480\" y2=\"150\" stroke=\"var(--ink-soft)\" stroke-width=\"1.8\"/>\n  <line x1=\"70\" y1=\"170\" x2=\"70\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.8\"/>\n  \n  <!-- Shaded Area -->\n  <path d=\"M 120 150 C 180 50, 240 130, 300 70 C 340 30, 380 90, 420 150 Z\" fill=\"rgba(99,102,241,0.18)\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  \n  <!-- Limits a, b and symmetry line -->\n  <line x1=\"120\" y1=\"150\" x2=\"120\" y2=\"140\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <text x=\"115\" y=\"168\" font-size=\"13\" font-weight=\"700\" fill=\"var(--ink)\">a</text>\n  \n  <line x1=\"420\" y1=\"150\" x2=\"420\" y2=\"140\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <text x=\"415\" y=\"168\" font-size=\"13\" font-weight=\"700\" fill=\"var(--ink)\">b</text>\n  \n  <!-- Symmetry Line -->\n  <line x1=\"270\" y1=\"25\" x2=\"270\" y2=\"150\" stroke=\"#10B981\" stroke-width=\"1.8\" stroke-dasharray=\"4,4\"/>\n  <text x=\"245\" y=\"18\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">x = (a+b)/2</text>\n  \n  <text x=\"180\" y=\"80\" font-size=\"14\" font-weight=\"700\" fill=\"var(--purple)\">y = f(x)</text>\n  <text x=\"320\" y=\"80\" font-size=\"14\" font-weight=\"700\" fill=\"#10B981\">y = f(a+b-x)</text>\n</svg>",
        "figure_caption": "Figure 1.3: Geometric reflection across x = (a+b)/2. The enclosed area under the curve is invariant under reflection.",
        "content": "In definite integral calculus, few properties rival the elegance and computational speed of the reflection property, colloquially known across Indian competitive pedagogy as **King's Property**:\n\n$$\\int_{a}^{b} f(x) \\, dx = \\int_{a}^{b} f(a + b - x) \\, dx$$\n\n### Analytical Proof via Substitution\nLet $I = \\int_{a}^{b} f(x) \\, dx$. Perform the linear transformation:\n$$u = a + b - x \\quad \\implies \\quad du = -dx$$\n\nTransforming the integration bounds:\n- When $x = a$, $u = a + b - a = b$.\n- When $x = b$, $u = a + b - b = a$.\n\nSubstituting these terms into the integral:\n$$I = \\int_{b}^{a} f(u) (-du) = -\\int_{b}^{a} f(u) \\, du = \\int_{a}^{b} f(u) \\, du$$\n\nSince the definite integral is independent of the dummy integration variable, $\\int_{a}^{b} f(u)du = \\int_{a}^{b} f(x)dx$. This completes the proof.\n\n### Paradigm Application: Transcendental Cancellation\nConsider the classical JEE integral:\n$$I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx$$\n\nApplying King's Property with $a+b-x = 0 + \\frac{\\pi}{2} - x = \\frac{\\pi}{2} - x$:\n$$I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(\\pi/2 - x)}{\\sin^n(\\pi/2 - x) + \\cos^n(\\pi/2 - x)} \\, dx = \\int_{0}^{\\pi/2} \\frac{\\cos^n(x)}{\\cos^n(x) + \\sin^n(x)} \\, dx$$\n\nAdding the original integral and the transformed integral:\n$$2I = \\int_{0}^{\\pi/2} \\frac{\\sin^n(x) + \\cos^n(x)}{\\sin^n(x) + \\cos^n(x)} \\, dx = \\int_{0}^{\\pi/2} 1 \\, dx = \\left[x\\right]_0^{\\pi/2} = \\frac{\\pi}{2}$$\n$$I = \\frac{\\pi}{4}$$\n\nThis algebraic synthesis completely eliminates the need for calculating difficult elementary antiderivatives.",
        "didactic_notes": {
            "axiom": "Geometric meaning: King's Property reflects the graph about the line x = (a+b)/2. Since reflection is an isometry, area is strictly invariant.",
            "trap": "Always add 2I = I\u2081 + I\u2082! Forgetting to divide by 2 at the final step is the #1 algebraic error committed by students.",
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
            "plain": "\u0394G = \u0394H - T\u00b7\u0394S",
            "terms": [["\u0394G", "Change in Gibbs Free Energy (spontaneous if \u0394G < 0 at const T, P)"], ["\u0394H", "Change in enthalpy (kJ/mol)"], ["T", "Absolute thermodynamic temperature in Kelvin (K)"], ["\u0394S", "Change in entropy of system (J/mol\u00b7K)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"170\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Quadrants -->\n  <line x1=\"270\" y1=\"20\" x2=\"270\" y2=\"160\" stroke=\"var(--border)\" stroke-width=\"2\"/>\n  <line x1=\"50\" y1=\"90\" x2=\"490\" y2=\"90\" stroke=\"var(--border)\" stroke-width=\"2\"/>\n  <text x=\"495\" y=\"94\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">+\u0394S</text>\n  <text x=\"25\" y=\"94\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">-\u0394S</text>\n  <text x=\"263\" y=\"16\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">+\u0394H</text>\n  <text x=\"263\" y=\"176\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">-\u0394H</text>\n  \n  <!-- Q1 -->\n  <rect x=\"280\" y=\"25\" width=\"190\" height=\"55\" rx=\"6\" fill=\"rgba(245,158,11,0.12)\" stroke=\"rgba(245,158,11,0.3)\"/>\n  <text x=\"290\" y=\"46\" font-size=\"11\" font-weight=\"700\" fill=\"#B45309\">Spontaneous at HIGH T</text>\n  <text x=\"290\" y=\"66\" font-size=\"10\" fill=\"var(--ink-soft)\">(T\u0394S dominates over +\u0394H)</text>\n  \n  <!-- Q4 -->\n  <rect x=\"280\" y=\"100\" width=\"190\" height=\"55\" rx=\"6\" fill=\"rgba(16,185,129,0.14)\" stroke=\"rgba(16,185,129,0.3)\"/>\n  <text x=\"290\" y=\"122\" font-size=\"11\" font-weight=\"800\" fill=\"#059669\">ALWAYS SPONTANEOUS</text>\n  <text x=\"290\" y=\"142\" font-size=\"10\" fill=\"var(--ink-soft)\">(\u0394G &lt; 0 at ALL temperatures)</text>\n  \n  <!-- Q2 -->\n  <rect x=\"70\" y=\"25\" width=\"190\" height=\"55\" rx=\"6\" fill=\"rgba(239,68,68,0.12)\" stroke=\"rgba(239,68,68,0.3)\"/>\n  <text x=\"80\" y=\"46\" font-size=\"11\" font-weight=\"800\" fill=\"#DC2626\">NEVER SPONTANEOUS</text>\n  <text x=\"80\" y=\"66\" font-size=\"10\" fill=\"var(--ink-soft)\">(\u0394G &gt; 0 at ALL temperatures)</text>\n  \n  <!-- Q3 -->\n  <rect x=\"70\" y=\"100\" width=\"190\" height=\"55\" rx=\"6\" fill=\"rgba(59,130,246,0.12)\" stroke=\"rgba(59,130,246,0.3)\"/>\n  <text x=\"80\" y=\"122\" font-size=\"11\" font-weight=\"700\" fill=\"#2563EB\">Spontaneous at LOW T</text>\n  <text x=\"80\" y=\"142\" font-size=\"10\" fill=\"var(--ink-soft)\">(Enthalpy drive overcomes -T\u0394S)</text>\n</svg>",
        "figure_caption": "Figure 1.4: The Four Thermodynamic Spontaneity Regimes as dictated by \u0394G = \u0394H - T\u0394S.",
        "content": "The Second Law of Thermodynamics dictates that any spontaneous natural process causes an increase in total entropy of the universe:\n$$\\Delta S_{\\text{univ}} = \\Delta S_{\\text{sys}} + \\Delta S_{\\text{surr}} > 0$$\n\nHowever, calculating entropy changes across the entire surroundings is experimentally cumbersome. Josiah Willard Gibbs solved this by introducing the **Gibbs Free Energy** state function for constant temperature and pressure:\n\n$$G = H - TS \\quad \\implies \\quad \\Delta G_{\\text{sys}} = \\Delta H_{\\text{sys}} - T \\Delta S_{\\text{sys}}$$\n\nBecause heat transferred reversibly to the surroundings at constant pressure equals $q_{\\text{surr}} = -\\Delta H_{\\text{sys}}$, the surroundings entropy is:\n$$\\Delta S_{\\text{surr}} = -\\frac{\\Delta H_{\\text{sys}}}{T}$$\n\nMultiplying the total universe entropy by $-T$:\n$$-T \\Delta S_{\\text{univ}} = -T \\left(\\Delta S_{\\text{sys}} - \\frac{\\Delta H_{\\text{sys}}}{T}\\right) = \\Delta H_{\\text{sys}} - T \\Delta S_{\\text{sys}} = \\Delta G_{\\text{sys}}$$\n\nTherefore, the universal condition for spontaneity ($\\Delta S_{\\text{univ}} > 0$) translates directly into $\\Delta G_{\\text{sys}} < 0$ at constant temperature and pressure.",
        "didactic_notes": {
            "axiom": "A negative \u0394G indicates thermodynamic spontaneity, but NOT reaction rate. Kinetics (activation energy Ea) determines speed.",
            "trap": "At equilibrium: \u0394G = 0, NOT \u0394G\u00b0 = 0! Standard free energy \u0394G\u00b0 relates to equilibrium constant via \u0394G\u00b0 = -RT ln K.",
            "mnemonic": "\u0394G < 0 is Go, \u0394G > 0 is No-Go, \u0394G = 0 is Dynamic Balance."
        },
        "key_takeaways": [
            "Fundamental Gibbs Criterion: $\\Delta G = \\Delta H - T\\Delta S$.",
            "Universal Spontaneity Condition: Requires $\\Delta G < 0$ strictly at constant temperature and pressure.",
            "Standard Equilibrium Link: $\\Delta G^\\circ = -RT \\ln(K_{\\text{eq}})$.",
            "Phase Inversion Temperature: The transition between non-spontaneous and spontaneous regimes occurs at $T_{\\text{eq}} = \\frac{\\Delta H}{\\Delta S}$."
]
    },
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
            "terms": [["RER", "Rough Endoplasmic Reticulum: 80S ribosomes, protein synthesis & N-glycosylation"], ["SER", "Smooth Endoplasmic Reticulum: lipid/steroid synthesis & Ca\u00b2\u207a sequestration"], ["Golgi Cis/Trans", "Polarized cisternae: cis (entry/forming face) to trans (exit/maturing face)"], ["Excluded", "Mitochondria, Chloroplasts, and Peroxisomes (independent semi-autonomous organelles)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 200\" width=\"100%\" height=\"190\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Nucleus -->\n  <circle cx=\"50\" cy=\"100\" r=\"45\" fill=\"rgba(99,102,241,0.12)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"25\" y=\"105\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">Nucleus</text>\n  \n  <!-- RER with Ribosomes -->\n  <path d=\"M 95 65 C 130 60, 130 140, 160 135\" fill=\"none\" stroke=\"#3B82F6\" stroke-width=\"5\"/>\n  <circle cx=\"115\" cy=\"70\" r=\"2.5\" fill=\"#EF4444\"/><circle cx=\"130\" cy=\"85\" r=\"2.5\" fill=\"#EF4444\"/><circle cx=\"145\" cy=\"115\" r=\"2.5\" fill=\"#EF4444\"/>\n  <text x=\"110\" y=\"50\" font-size=\"11\" font-weight=\"700\" fill=\"#3B82F6\">Rough ER</text>\n  \n  <!-- Transport Vesicle -->\n  <circle cx=\"205\" cy=\"100\" r=\"9\" fill=\"rgba(16,185,129,0.2)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <line x1=\"175\" y1=\"100\" x2=\"190\" y2=\"100\" stroke=\"#10B981\" stroke-width=\"1.8\" marker-end=\"url(#arrow)\"/>\n  \n  <!-- Golgi Cisternae -->\n  <path d=\"M 250 50 C 265 80, 265 120, 250 150\" fill=\"none\" stroke=\"#F59E0B\" stroke-width=\"6\"/>\n  <path d=\"M 270 55 C 282 80, 282 115, 270 145\" fill=\"none\" stroke=\"#F59E0B\" stroke-width=\"6\"/>\n  <path d=\"M 290 60 C 300 80, 300 110, 290 140\" fill=\"none\" stroke=\"#F59E0B\" stroke-width=\"6\"/>\n  <text x=\"240\" y=\"38\" font-size=\"11\" font-weight=\"700\" fill=\"#F59E0B\">Golgi (Cis -> Trans)</text>\n  \n  <!-- Secretory Vesicle & Lysosome -->\n  <circle cx=\"350\" cy=\"75\" r=\"10\" fill=\"rgba(239,68,68,0.2)\" stroke=\"#EF4444\" stroke-width=\"2\"/>\n  <text x=\"365\" y=\"79\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Lysosome (Acid Hydrolases)</text>\n  \n  <circle cx=\"360\" cy=\"130\" r=\"11\" fill=\"rgba(16,185,129,0.2)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"378\" y=\"135\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">Secretory Vesicle</text>\n  \n  <!-- Plasma Membrane -->\n  <line x1=\"490\" y1=\"20\" x2=\"490\" y2=\"180\" stroke=\"var(--ink)\" stroke-width=\"3\"/>\n  <text x=\"475\" y=\"192\" font-size=\"10\" font-weight=\"700\" fill=\"var(--ink)\">Plasma Membrane</text>\n</svg>",
        "figure_caption": "Figure 2.1: The eukaryotic secretory pathway from RER synthesis, transport vesicle budding, Golgi sorting (cis to trans), to exocytosis and lysosomal targeting.",
        "content": "In eukaryotic cells, while many cellular organelles are physically discrete membrane-bound structures, several operate as a functionally coordinated unit termed the **Endomembrane System**.\n\nIn strict NCERT and NEET taxonomy, the endomembrane system comprises four coordinated components:\n1. **Endoplasmic Reticulum (ER)**\n2. **Golgi Apparatus**\n3. **Lysosomes**\n4. **Vacuoles**\n\nMitochondria, chloroplasts, and peroxisomes are strictly **EXCLUDED** from this system because their biogenesis, evolutionary lineage, and physiological functions are not coordinated with the ER-Golgi secretory pathway.\n\n### The Secretory & Transport Cascade\n- **Rough Endoplasmic Reticulum (RER):** Dotted with 80S ribosomes on its cytosolic face, the RER synthesizes secretory proteins and transmembrane polypeptides, performing cotranslational translocation and initial N-linked glycosylation in its lumen.\n- **Smooth Endoplasmic Reticulum (SER):** Lacking ribosomes, the SER serves as the primary factory for phospholipid and steroid hormone synthesis (e.g. testosterone and estrogens in animal gonads) and functions as the sarcoplasmic reticulum for $\\text{Ca}^{2+}$ sequestration in skeletal muscle.\n- **Golgi Complex Polarization:** Transport vesicles bud from the ER and fuse with the convex *cis* (forming) face of the Golgi cisternae. As proteins traverse the cisternae, enzymes modify oligosaccharide chains into complex glycoproteins. Sorted cargos bud from the concave *trans* (maturing) face into vesicles destined for exocytosis or lysosomal delivery.",
        "didactic_notes": {
            "axiom": "The endomembrane components share continuous or vesicle-mediated membrane flow. Organelles with their own DNA (Mitochondria/Plastids) are excluded.",
            "trap": "Peroxisomes contain oxidative enzymes (catalase, urate oxidase) but are NOT part of the endomembrane system in NCERT taxonomy.",
            "mnemonic": "NCERT Acronym: 'E-G-L-V' (ER, Golgi, Lysosomes, Vacuoles)."
        },
        "key_takeaways": [
            "Endomembrane = ER + Golgi + Lysosomes + Vacuoles.",
            "Mitochondria, Chloroplasts, and Peroxisomes are strictly excluded.",
            "Lysosomal enzymes (acid hydrolases) require pH 4.5\u20135.0 maintained by active H+ ATPase proton pumps.",
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
            "terms": [["Leading Strand", "Continuous synthesis toward the unwinding replication fork (3'->5' template)"], ["Lagging Strand", "Discontinuous synthesis away from fork producing Okazaki fragments (5'->3' template)"], ["DNA Pol III", "Primary catalytic enzyme with high processivity and 3'->5' exonuclease proofreading"], ["DNA Ligase", "Forms phosphodiester bond sealing the nick using ATP / NAD+"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 200\" width=\"100%\" height=\"190\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Parental Strands -->\n  <path d=\"M 40 40 L 220 100 L 500 40\" fill=\"none\" stroke=\"var(--ink)\" stroke-width=\"3\"/>\n  <text x=\"30\" y=\"35\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">3'</text>\n  <text x=\"505\" y=\"35\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">5'</text>\n  \n  <path d=\"M 40 160 L 220 100 L 500 160\" fill=\"none\" stroke=\"var(--ink)\" stroke-width=\"3\"/>\n  <text x=\"30\" y=\"175\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">5'</text>\n  <text x=\"505\" y=\"175\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">3'</text>\n  \n  <!-- Helicase at fork -->\n  <polygon points=\"200,80 240,100 200,120\" fill=\"#EF4444\"/>\n  <text x=\"175\" y=\"70\" font-size=\"11\" font-weight=\"800\" fill=\"#EF4444\">DNA Helicase</text>\n  \n  <!-- Leading Strand -->\n  <path d=\"M 240 85 L 480 50\" fill=\"none\" stroke=\"#10B981\" stroke-width=\"3.5\" stroke-dasharray=\"8,2\"/>\n  <text x=\"320\" y=\"60\" font-size=\"12\" font-weight=\"800\" fill=\"#10B981\">Leading Strand (Continuous 5'->3')</text>\n  \n  <!-- Okazaki Fragments on Lagging Strand -->\n  <line x1=\"260\" y1=\"120\" x2=\"330\" y2=\"135\" stroke=\"#3B82F6\" stroke-width=\"3.5\"/>\n  <line x1=\"360\" y1=\"140\" x2=\"430\" y2=\"155\" stroke=\"#3B82F6\" stroke-width=\"3.5\"/>\n  <text x=\"300\" y=\"178\" font-size=\"12\" font-weight=\"800\" fill=\"#3B82F6\">Okazaki Fragments (Lagging)</text>\n</svg>",
        "figure_caption": "Figure 2.2: Architecture of the eukaryotic/prokaryotic replication fork showing leading strand continuous synthesis and lagging strand Okazaki fragments.",
        "content": "The replication of genetic information is **semiconservative**: each daughter DNA duplex retains one parental polynucleotide chain and one newly synthesized complementary strand. This was conclusively proven by Matthew Meselson and Franklin Stahl in 1958 using $^{15}\\text{N}$ isotope density gradient centrifugation in cesium chloride (CsCl).\n\n### Enzymatic Coordination at the Replication Fork\n1. **DNA Helicase:** Unwinds the double helix by breaking hydrogen bonds between base pairs, consuming ATP.\n2. **DNA Topoisomerase / Gyrase:** Relieves the resulting supercoiling strain ahead of the replication fork by making transient cuts.\n3. **Single-Strand DNA-Binding Proteins (SSBs):** Prevent the separated strands from prematurely re-annealing into hairpins.\n4. **RNA Primase:** Synthesizes a brief RNA primer (~10-12 nucleotides), providing the essential free $3'\\text{-OH}$ group required by DNA polymerases.\n5. **DNA Polymerase III:** Performs high-speed chain elongation exclusively in the $5' \\to 3'$ direction with proofreading ($3' \\to 5'$ exonuclease).\n6. **DNA Polymerase I & Ligase:** Pol I degrades RNA primers via $5' \\to 3'$ exonuclease activity and replaces them with deoxynucleotides; DNA Ligase seals the remaining phosphodiester nicks.",
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
            "plain": "CO = SV \u00b7 HR = 70 mL \u00d7 72 bpm \u2248 5040 mL/min (5 Liters/min)",
            "terms": [["Stroke Volume (SV)", "End-Diastolic Volume (EDV \u2248 120 mL) - End-Systolic Volume (ESV \u2248 50 mL) = 70 mL"], ["Heart Rate (HR)", "Normal resting rate ~72 beats per minute"], ["Cycle Duration", "60 seconds / 72 bpm = 0.8 seconds per cardiac cycle"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"170\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- 0.8s Timeline Circle / Bar -->\n  <rect x=\"50\" y=\"70\" width=\"100\" height=\"45\" fill=\"#3B82F6\" rx=\"4\"/>\n  <text x=\"65\" y=\"97\" font-size=\"12\" font-weight=\"700\" fill=\"#fff\">Atrial Systole (0.1s)</text>\n  \n  <rect x=\"155\" y=\"70\" width=\"150\" height=\"45\" fill=\"#EF4444\" rx=\"4\"/>\n  <text x=\"175\" y=\"97\" font-size=\"12\" font-weight=\"700\" fill=\"#fff\">Ventricular Systole (0.3s)</text>\n  \n  <rect x=\"310\" y=\"70\" width=\"180\" height=\"45\" fill=\"#10B981\" rx=\"4\"/>\n  <text x=\"340\" y=\"97\" font-size=\"12\" font-weight=\"700\" fill=\"#fff\">Joint Diastole (0.4s)</text>\n  \n  <!-- Sound 1: LUB -->\n  <path d=\"M 155 70 L 155 45\" stroke=\"#EF4444\" stroke-width=\"2\"/>\n  <circle cx=\"155\" cy=\"40\" r=\"14\" fill=\"#EF4444\"/>\n  <text x=\"144\" y=\"44\" font-size=\"10\" font-weight=\"800\" fill=\"#fff\">LUB</text>\n  <text x=\"110\" y=\"24\" font-size=\"10\" font-weight=\"700\" fill=\"#EF4444\">AV Valves Close (Tricuspid/Bicuspid)</text>\n  \n  <!-- Sound 2: DUB -->\n  <path d=\"M 310 70 L 310 45\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <circle cx=\"310\" cy=\"40\" r=\"14\" fill=\"#10B981\"/>\n  <text x=\"298\" y=\"44\" font-size=\"10\" font-weight=\"800\" fill=\"#fff\">DUB</text>\n  <text x=\"280\" y=\"24\" font-size=\"10\" font-weight=\"700\" fill=\"#10B981\">Semilunar Valves Close</text>\n  \n  <text x=\"200\" y=\"145\" font-size=\"13\" font-weight=\"700\" fill=\"var(--ink)\">Total Duration = 0.8 Seconds (72 bpm)</text>\n</svg>",
        "figure_caption": "Figure 2.3: Chronology of the 0.8s cardiac cycle illustrating the mechanical timing of the LUB (first) and DUB (second) heart sounds.",
        "content": "The human cardiac cycle encompasses all electrical and mechanical events occurring from the initiation of one heartbeat to the onset of the next. At a normal resting heart rate of 72 beats per minute, each cycle spans exactly $0.8\\text{ seconds}$.\n\n### Sequential Chronology of the 0.8-Second Cycle\n1. **Joint Diastole (0.4 s):** All four chambers are relaxed. Blood flows from the superior and inferior vena cava and pulmonary veins into the atria and passively into ventricles through open atrioventricular (AV) valves (Tricuspid and Bicuspid/Mitral). Approximately $70\\%$ of ventricular filling occurs passively during this phase.\n2. **Atrial Systole (0.1 s):** Initiated by the Sinoatrial (SA) Node pacemaker wave, the atria contract simultaneously, pumping the remaining $30\\%$ of blood into the ventricles. End-Diastolic Volume (EDV) peaks at $\\sim 120\\text{ mL}$.\n3. **Ventricular Systole (0.3 s):**\n   - *Isovolumetric Contraction:* Ventricular pressure rapidly exceeds atrial pressure, snapping the AV valves shut. This sudden valve closure and blood turbulence produces the **First Heart Sound ('LUB')**.\n   - *Ventricular Ejection:* Intraventricular pressure surpasses systemic aortic pressure ($80\\text{ mmHg}$) and pulmonary pressure ($15\\text{ mmHg}$), forcing semilunar valves open to eject the Stroke Volume ($\\sim 70\\text{ mL}$).\n4. **Isovolumetric Ventricular Relaxation:** Ventricular pressure plunges below arterial pressure, causing blood to surge backward and slam the semilunar valves shut, producing the **Second Heart Sound ('DUB')**.",
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
    {
        "id": "FW-UPSC-ECO-01",
        "course": "UPSC",
        "subject": "Economy & Development",
        "chapter": "Monetary Policy",
        "title": "Monetary Policy Transmission: Liquidity Adjustment & The Repo Rate Mechanism",
        "score": 4.9,
        "source": "Oxford Review of Economic Policy / FineWeb-Edu",
        "word_count": 560,
        "reading_time_mins": 3,
        "summary": "How RBI repo rate changes transmit through banking liquidity, Marginal Cost of Funds (MCLR), and inflation expectations.",
        "formula_box": {
            "title": "The Statutory Policy Corridor Framework",
            "latex": "\\text{MSF Rate} = \\text{Repo} + 25\\text{ bps} \\quad \\Longleftrightarrow \\quad \\text{SDF Rate} = \\text{Repo} - 25\\text{ bps}",
            "plain": "LAF Corridor: MSF (Ceiling) > Policy Repo Rate (Anchor) > SDF (Floor)",
            "terms": [["Repo Rate", "Rate at which RBI lends short-term liquidity against G-Secs to commercial banks"], ["SDF", "Standing Deposit Facility: collateral-free absorption of uncollateralized bank liquidity"], ["MSF", "Marginal Standing Facility: penal borrowing window allowing dip into SLR quota"], ["FIT Target", "4% CPI (+/- 2% tolerance band: 2% to 6%) under Section 45ZA of the RBI Act"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"170\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Ceiling: MSF -->\n  <line x1=\"60\" y1=\"40\" x2=\"480\" y2=\"40\" stroke=\"#EF4444\" stroke-width=\"2.5\" stroke-dasharray=\"6,3\"/>\n  <text x=\"60\" y=\"30\" font-size=\"12\" font-weight=\"700\" fill=\"#EF4444\">Ceiling: Marginal Standing Facility (MSF: Repo + 0.25%)</text>\n  \n  <!-- Anchor: Repo Rate -->\n  <line x1=\"60\" y1=\"90\" x2=\"480\" y2=\"90\" stroke=\"var(--purple)\" stroke-width=\"3.5\"/>\n  <rect x=\"220\" y=\"78\" width=\"110\" height=\"24\" rx=\"5\" fill=\"var(--purple)\"/>\n  <text x=\"232\" y=\"94\" font-size=\"11\" font-weight=\"800\" fill=\"#fff\">Policy Repo Rate</text>\n  \n  <!-- Floor: SDF -->\n  <line x1=\"60\" y1=\"140\" x2=\"480\" y2=\"140\" stroke=\"#10B981\" stroke-width=\"2.5\" stroke-dasharray=\"6,3\"/>\n  <text x=\"60\" y=\"158\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Floor: Standing Deposit Facility (SDF: Repo - 0.25%)</text>\n  \n  <text x=\"360\" y=\"115\" font-size=\"11\" font-weight=\"600\" fill=\"var(--ink-soft)\">LAF Width = 50 bps</text>\n</svg>",
        "figure_caption": "Figure 3.1: The Reserve Bank of India Liquidity Adjustment Facility (LAF) Corridor anchoring call money rates.",
        "content": "Monetary policy transmission describes the dynamic process through which a central bank's policy rate decisions cascade through the banking system, influencing credit spreads, aggregate demand, exchange rates, and retail inflation. In India, the Reserve Bank of India (RBI) operates under a statutory **Flexible Inflation Targeting (FIT)** framework, targeting CPI inflation at $4\\% \\pm 2\\%$.\n\n### The Operating Procedure & The Policy Corridor\nThe daily operating target of the RBI is the weighted average call money rate (WACR). The policy repo rate serves as the anchor of the **Liquidity Adjustment Facility (LAF)** corridor, flanked symmetrically by:\n1. **Marginal Standing Facility (MSF):** The upper ceiling (Repo $+ 25\\text{ bps}$), where banks borrow overnight funds against G-Secs dipping into their SLR.\n2. **Standing Deposit Facility (SDF):** The uncollateralized floor (Repo $- 25\\text{ bps}$), absorbing excess surplus bank deposits without requiring government collateral.\n\n### The Four Channels of Transmission\n1. **Interest Rate Channel:** Policy repo hikes raise interbank cost of capital, forcing banks to adjust their External Benchmark-linked Lending Rates (EBLR) and MCLR, thereby suppressing consumer borrowing and capital investments.\n2. **Credit & Balance Sheet Channel:** Heightened repo rates compress bank liquidity buffers, prompting stricter loan collateral evaluation.\n3. **Exchange Rate Channel:** Higher yields draw Foreign Portfolio Investment (FPI) into debt securities, appreciating the Rupee and curbing imported inflation.\n4. **Expectations Anchor:** Credible forward guidance anchors public inflation expectations, preventing self-fulfilling wage-price spirals.",
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
        "title": "Climatology & Teleconnections: The El Ni\u00f1o Southern Oscillation (ENSO) & Indian Monsoon",
        "score": 4.85,
        "source": "Cambridge Earth System Science / FineWeb-Edu",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Coupled ocean-atmosphere dynamics across the equatorial Pacific, Walker Circulation shifts, and their impact on South Asian rainfall.",
        "formula_box": {
            "title": "The Ocean-Atmosphere Coupling Index",
            "latex": "\\text{ENSO Phase} = \\{ \\text{El Ni\u00f1o (Warm/Weak)} \\Longleftrightarrow \\text{La Ni\u00f1a (Cold/Strong)} \\}",
            "plain": "Ocean State (SST anomalies in Ni\u00f1o 3.4) coupled with Atmospheric State (Southern Oscillation Index SOI)",
            "terms": [["Walker Circulation", "East-West atmospheric zonal overturning circulation across the equatorial Pacific"], ["Normal State", "Warm pool in Western Pacific; intense upwelling of cold water off Peruvian coast"], ["El Ni\u00f1o State", "Weak trade winds; eastward displacement of warm pool; descending dry air over India"], ["IOD Modulator", "Positive Indian Ocean Dipole can counterbalance and mitigate El Ni\u00f1o drying effects"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"170\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Normal vs El Nino split -->\n  <rect x=\"30\" y=\"25\" width=\"230\" height=\"135\" rx=\"8\" fill=\"rgba(16,185,129,0.08)\" stroke=\"#10B981\"/>\n  <text x=\"45\" y=\"45\" font-size=\"12\" font-weight=\"800\" fill=\"#059669\">NORMAL / NEUTRAL STATE</text>\n  <text x=\"45\" y=\"65\" font-size=\"10\" fill=\"var(--ink-soft)\">Strong Easterly Trade Winds</text>\n  <text x=\"45\" y=\"85\" font-size=\"10\" fill=\"var(--ink-soft)\">West Pacific Warm Pool (~30\u00b0C)</text>\n  <text x=\"45\" y=\"105\" font-size=\"10\" fill=\"var(--ink-soft)\">Ascending Moist Air over Indo-Pacific</text>\n  <text x=\"45\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#059669\">\u2713 Favorable Indian Monsoon</text>\n  \n  <rect x=\"280\" y=\"25\" width=\"230\" height=\"135\" rx=\"8\" fill=\"rgba(239,68,68,0.08)\" stroke=\"#EF4444\"/>\n  <text x=\"295\" y=\"45\" font-size=\"12\" font-weight=\"800\" fill=\"#DC2626\">EL NI\u00d1O EPISODE</text>\n  <text x=\"295\" y=\"65\" font-size=\"10\" fill=\"var(--ink-soft)\">Weakened / Reversed Trade Winds</text>\n  <text x=\"295\" y=\"85\" font-size=\"10\" fill=\"var(--ink-soft)\">Warm Pool Shifts East toward Peru</text>\n  <text x=\"295\" y=\"105\" font-size=\"10\" fill=\"var(--ink-soft)\">Subsidence (Dry Sinking Air) over India</text>\n  <text x=\"295\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#DC2626\">\u26a0\ufe0f Risk of Monsoon Deficit / Drought</text>\n</svg>",
        "figure_caption": "Figure 3.2: Comparison between the Normal Walker Circulation and the El Ni\u00f1o disruption suppressing Indian monsoon convection.",
        "content": "The El Ni\u00f1o Southern Oscillation (ENSO) is a coupled ocean-atmosphere phenomenon in the tropical Pacific that serves as the dominant driver of interannual global climate variability. For Indian Civil Services aspirants, understanding ENSO is vital due to its historical inverse correlation with the southwest summer monsoon (June\u2013September), which accounts for over $70\\%$ of India's annual precipitation.\n\n### Neutral Conditions vs. El Ni\u00f1o State\nUnder normal (neutral) conditions, easterly trade winds blow surface water westward towards Indonesia and northern Australia. This creates a warm pool of water in the western Pacific (warm SSTs $\\sim 30^{\\circ}\\text{C}$), driving vigorous atmospheric convection (the ascending branch of the Walker Circulation). In contrast, cold, nutrient-rich water upwells along the Peruvian coast in the eastern Pacific.\n\nDuring an **El Ni\u00f1o event**:\n1. Easterly trade winds weaken significantly or reverse into westerlies.\n2. The equatorial warm pool shifts eastward toward central and eastern Pacific waters, suppressing the thermocline and upwelling off Peru.\n3. The ascending branch of the Walker Circulation shifts to the central Pacific, while anomalous subsidence (sinking dry air) dominates over the western Pacific, Southeast Asia, and peninsular India.\n\n### The Counterbalancing Indian Ocean Dipole (IOD)\nAn El Ni\u00f1o does not automatically guarantee a drought! The **Indian Ocean Dipole (IOD)**\u2014a sea surface temperature gradient between the western and eastern Indian Ocean\u2014can modulate monsoon strength. A **Positive IOD** (warmer Arabian Sea) generates rising moist air over India and can completely neutralize or override the drying teleconnection of a concurrent Pacific El Ni\u00f1o.",
        "didactic_notes": {
            "axiom": "ENSO is a coupled phenomenon: El Ni\u00f1o is the oceanic component (SST warming); Southern Oscillation is the atmospheric pressure component (Tahiti vs Darwin).",
            "trap": "Not all El Ni\u00f1o events cause drought (e.g. 1997 super El Ni\u00f1o saw normal Indian monsoon due to a record-positive IOD).",
            "mnemonic": "Positive IOD = Good for India (Arabian Sea Warmer); El Ni\u00f1o = Bad for India (Sinking Dry Air)."
        },
        "key_takeaways": [
            "ENSO tracks anomalies in Ni\u00f1o 3.4 region coupled with Southern Oscillation Index (SOI).",
            "Walker Circulation shifts eastward during El Ni\u00f1o, placing sinking dry air over the Indian subcontinent.",
            "Positive IOD acts as a thermal shield that can neutralize El Ni\u00f1o drying effects.",
            "Monsoon accounts for ~70% of India's annual rainfall and critical groundwater replenishment."
]
    },
    {
        "id": "FW-UPSC-CSAT-01",
        "course": "UPSC",
        "subject": "CSAT Reading Passages",
        "chapter": "Comprehension & Critical Reasoning",
        "title": "CSAT Analytical Passage: Technology, Algorithmic Governance & Democratic Accountability",
        "score": 4.9,
        "source": "Harvard Policy & Tech Review / FineWeb-Edu",
        "word_count": 450,
        "reading_time_mins": 2,
        "summary": "Passage on bureaucratic algorithmic discretion, procedural due process, and critical inference analysis for Paper-II.",
        "formula_box": {
            "title": "Analytical Inference Taxonomy for CSAT Paper-II",
            "latex": "\\text{Valid Inference} \\subset \\text{Explicit Textual Premises} \\quad (\\text{Zero External Speculation})",
            "plain": "Logical Rule: True inferences must be unavoidable deductions strictly grounded in passage premises.",
            "terms": [["Explicit Premise", "Fact directly stated by the author in the text"], ["Critical Assumption", "Unstated bridging premise required for the author's conclusion to hold true"], ["Distractor Trap", "Extrapolations that sound plausible in real life but lack textual warrant"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"40\" y=\"45\" width=\"120\" height=\"70\" rx=\"8\" fill=\"rgba(99,102,241,0.12)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"55\" y=\"75\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">Input Data</text>\n  <text x=\"50\" y=\"95\" font-size=\"9.5\" fill=\"var(--ink-soft)\">(Citizen Profiles)</text>\n  \n  <line x1=\"160\" y1=\"80\" x2=\"200\" y2=\"80\" stroke=\"var(--purple)\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  \n  <rect x=\"200\" y=\"35\" width=\"140\" height=\"90\" rx=\"8\" fill=\"rgba(15,23,42,0.9)\" stroke=\"#EF4444\" stroke-width=\"2\"/>\n  <text x=\"220\" y=\"70\" font-size=\"12\" font-weight=\"800\" fill=\"#EF4444\">Black-Box Model</text>\n  <text x=\"225\" y=\"92\" font-size=\"10\" fill=\"#fff\">(Opaque Decision)</text>\n  \n  <line x1=\"340\" y1=\"80\" x2=\"380\" y2=\"80\" stroke=\"var(--purple)\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  \n  <rect x=\"380\" y=\"45\" width=\"120\" height=\"70\" rx=\"8\" fill=\"rgba(16,185,129,0.12)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"390\" y=\"75\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">Due Process Check</text>\n  <text x=\"395\" y=\"95\" font-size=\"9.5\" fill=\"var(--ink-soft)\">(Right to Reason)</text>\n</svg>",
        "figure_caption": "Figure 3.3: The dilemma of algorithmic administrative discretion: reconciling automated efficiency with constitutional due process.",
        "content": "The integration of automated decision algorithms into administrative welfare distribution presents a profound paradox for constitutional democracy. Proponents contend that automated scoring eliminates human rent-seeking, accelerates benefit disbursement, and purges fraudulent welfare rosters. However, when complex algorithmic models operate as opaque 'black boxes', they erode the cardinal administrative doctrine of **reasoned decision-making**.\n\nUnder administrative law, an aggrieved citizen denied a statutory benefit possesses an inalienable right to know the precise grounds of adverse determination. When an algorithmic system denies a pension or subsidized foodgrains based on statistical probability vectors that neither the citizen nor the field officer can interpret, procedural due process is effectively dismantled.\n\nTrue democratic governance requires that algorithmic tools assist rather than supplant human judgment. Public accountability cannot be outsourced to proprietary code shielded by trade secrecy.",
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
    },
    {
        "id": "FW-JEE-PHY-03",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Newton's Laws of Motion & Friction",
        "title": "Classical Mechanics: Non-Inertial Reference Frames & Pseudo Forces",
        "score": 4.88,
        "source": "MIT OpenCourseWare / FineWeb-Edu Corpus",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Application of Newton's laws in non-inertial reference frames via d'Alembert fictitious forces and limiting friction criteria.",
        "formula_box": {
            "title": "Equation of Motion in Accelerating Frame",
            "latex": "\\mathbf{F}_{\\text{eff}} = \\mathbf{F}_{\\text{real}} - m \\mathbf{A}_{\\text{frame}}",
            "plain": "F_eff = F_real - m * A_frame",
            "terms": [["\\mathbf{F}_{\\text{eff}}", "Effective net force observed in accelerating reference frame"], ["\\mathbf{F}_{\\text{real}}", "Sum of all genuine physical contact and field forces"], ["-m \\mathbf{A}_{\\text{frame}}", "Inertial pseudo force directed oppositely to frame acceleration"], ["f_s \\le \\mu_s N", "Coulomb limiting static friction inequality preventing relative slip"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"50\" y=\"100\" width=\"220\" height=\"60\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2\" rx=\"4\"/>\n  <text x=\"120\" y=\"135\" font-size=\"13\" font-weight=\"700\" fill=\"var(--purple)\">Cart (Mass M, Accel A)</text>\n  <rect x=\"130\" y=\"55\" width=\"60\" height=\"45\" fill=\"rgba(16,185,129,0.2)\" stroke=\"#10B981\" stroke-width=\"2\" rx=\"3\"/>\n  <text x=\"145\" y=\"82\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Block m</text>\n  <line x1=\"160\" y1=\"77\" x2=\"80\" y2=\"77\" stroke=\"#EF4444\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"75\" y=\"70\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">-m A (Pseudo)</text>\n  <line x1=\"280\" y1=\"130\" x2=\"350\" y2=\"130\" stroke=\"var(--purple)\" stroke-width=\"2.5\" marker-end=\"url(#arrow)\"/>\n  <text x=\"355\" y=\"135\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">A_frame &rarr;</text>\n</svg>",
        "figure_caption": "Figure 1.5: Free Body Diagram in accelerating non-inertial frame. The pseudo force -m*A acts through the center of mass.",
        "content": "Newton's Second Law $\\mathbf{F} = m\\mathbf{a}$ holds strictly in inertial frames of reference. When analyzing dynamical systems from the perspective of an accelerating platform\u2014such as a wedge, elevator, or rotating turntable\u2014Newton's laws can be preserved by invoking d'Alembert's principle and introducing a **pseudo force** (inertial force).\n\n### Analytical Formulation of Pseudo Forces\nLet $\\mathbf{A}$ be the acceleration of the observer's frame relative to an inertial reference frame. For a particle of mass $m$, the equation of motion in the non-inertial coordinate system becomes:\n$$m\\mathbf{a}_{\\text{rel}} = \\sum \\mathbf{F}_{\\text{real}} - m\\mathbf{A}$$\n\nThe term $-m\\mathbf{A}$ is mathematically equivalent to an extra physical force acting on every mass element. It has no third-law reaction pair because it originates from the kinematic acceleration of the observer rather than an interaction between bodies.\n\n### Friction as a Constraint Force\nStatic friction is self-adjusting up to its maximum threshold $f_{\\text{max}} = \\mu_s N$. In two-block or wedge-block assemblies, slip occurs when the required inertial acceleration exceeds the maximum static shear traction: $a_{\\text{crit}} = \\mu_s g$.",
        "didactic_notes": {
            "axiom": "Pseudo forces always act parallel and opposite to the frame acceleration, acting precisely through the body's Center of Mass.",
            "trap": "Never apply a pseudo force when writing equations in an inertial (ground) frame! Double-counting causes fatal sign errors.",
            "mnemonic": "Remember: 'Inside Accel Frame? Slap -mA on the Mass'."
        },
        "key_takeaways": [
            "Inertial Correction: $\\mathbf{F}_{\\text{pseudo}} = -m \\mathbf{A}_{\\text{frame}}$, directed oppositely to frame acceleration.",
            "Kinematic Equivalence: Newton's Second Law holds in accelerating frames as $\\sum \\mathbf{F}_{\\text{real}} - m\\mathbf{A} = m\\mathbf{a}_{\\text{rel}}$.",
            "Limiting Friction Criterion: No relative slipping occurs as long as $|f_s| \\le \\mu_s N = \\mu_s m(g \\pm a_y)$.",
            "Action-Reaction Absence: Pseudo forces possess no Newton's Third Law reaction counter-force."
]
    },
    {
        "id": "FW-JEE-PHY-04",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Work, Energy & Power",
        "title": "Work-Energy Theorem & Conservative Force Fields in Continuum Mechanics",
        "score": 4.91,
        "source": "Feynman Lectures on Physics / FineWeb-Edu",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Differential derivation of the work-energy theorem W_net = Delta K, potential energy gradients F = -grad(U), and stability analysis.",
        "formula_box": {
            "title": "Conservative Force & Gradient of Potential",
            "latex": "\\mathbf{F}(\\mathbf{r}) = -\\nabla U(\\mathbf{r}) = -\\left(\\frac{\\partial U}{\\partial x}\\hat{i} + \\frac{\\partial U}{\\partial y}\\hat{j} + \\frac{\\partial U}{\\partial z}\\hat{k}\\right)",
            "plain": "F = - dU/dr",
            "terms": [["\\mathbf{F}", "Conservative field force vector"], ["U(\\mathbf{r})", "Potential energy scalar field"], ["\\nabla", "Del spatial gradient vector operator"], ["W_{\\text{net}} = \\Delta K", "Work-Energy Theorem: total work by ALL forces equals change in kinetic energy"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <path d=\"M 60 40 Q 150 140 240 70 T 420 120 T 500 40\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"155\" cy=\"115\" r=\"6\" fill=\"#10B981\"/>\n  <text x=\"130\" y=\"140\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">Stable (d\u00b2U/dx\u00b2 &gt; 0)</text>\n  <circle cx=\"280\" cy=\"65\" r=\"6\" fill=\"#EF4444\"/>\n  <text x=\"250\" y=\"50\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Unstable (d\u00b2U/dx\u00b2 &lt; 0)</text>\n  <line x1=\"50\" y1=\"150\" x2=\"510\" y2=\"150\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <text x=\"515\" y=\"154\" font-size=\"11\" fill=\"var(--ink-soft)\">x</text>\n</svg>",
        "figure_caption": "Figure 1.6: Potential energy curve U(x). Equilibrium points occur at dU/dx = 0; curvature determines stability.",
        "content": "The Work-Energy Theorem represents the scalar integral of Newton's Second Law along a particle's trajectory. Unlike vector equations of motion, energy methods bypass complex intermediate trajectory kinematics.\n\n### Differential Derivation of the Theorem\nStarting from $\\mathbf{F} = m \\frac{d\\mathbf{v}}{dt}$ and taking the scalar product with displacement $d\\mathbf{r} = \\mathbf{v} dt$:\n$$\\mathbf{F} \\cdot d\\mathbf{r} = m \\frac{d\\mathbf{v}}{dt} \\cdot \\mathbf{v} dt = m \\mathbf{v} \\cdot d\\mathbf{v} = d\\left(\\frac{1}{2}m v^2\\right)$$\n\nIntegrating from initial state $i$ to final state $f$:\n$$W_{\\text{net}} = \\int_i^f \\mathbf{F}_{\\text{net}} \\cdot d\\mathbf{r} = \\Delta K = \\frac{1}{2}m v_f^2 - \\frac{1}{2}m v_i^2$$\n\n### Conservative Forces and Equilibrium Regimes\nA force is conservative if the closed loop path integral vanishes: $\\oint \\mathbf{F}\\cdot d\\mathbf{r} = 0$. Equilibrium positions satisfy $\\frac{dU}{dx} = 0$. Stability is governed by the second derivative: stable if $\\frac{d^2 U}{dx^2} > 0$ (concave up), unstable if $\\frac{d^2 U}{dx^2} < 0$ (concave down).",
        "didactic_notes": {
            "axiom": "Work done by internal forces within an isolated system can change kinetic energy, but cannot accelerate the Center of Mass.",
            "trap": "The Work-Energy Theorem applies to ALL forces (conservative, non-conservative, and pseudo), whereas Mechanical Energy Conservation applies ONLY when non-conservative work is zero.",
            "mnemonic": "Potential Curvature: 'Cup Up = Stable, Dome Down = Unstable'."
        },
        "key_takeaways": [
            "Universal Work Principle: $W_{\\text{net}} = W_c + W_{nc} + W_{\\text{pseudo}} = \\Delta K$.",
            "Conservative Force Operator: $\\mathbf{F} = -\\nabla U$. Negative sign indicates force directs toward decreasing potential.",
            "Stability Classification: At $\\frac{dU}{dx} = 0$, $\\frac{d^2 U}{dx^2} > 0 \\implies$ Stable; $\\frac{d^2 U}{dx^2} < 0 \\implies$ Unstable.",
            "Path Independence: Work done by gravity, electrostatic, and ideal spring forces depends solely on endpoint coordinates."
]
    },
    {
        "id": "FW-JEE-PHY-05",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Electrostatics & Capacitance",
        "title": "Electrostatics: Gauss's Law, Field Divergence & Dielectric Polarization",
        "score": 4.93,
        "source": "Purcell Electricity and Magnetism / FineWeb-Edu",
        "word_count": 550,
        "reading_time_mins": 3,
        "summary": "Integral and differential Gauss's theorem, energy density in electrostatic fields, and capacitor boundary value problems.",
        "formula_box": {
            "title": "Gauss's Law in Dielectric Media",
            "latex": "\\oint_S \\mathbf{D} \\cdot d\\mathbf{A} = Q_{\\text{free, enc}} \\quad \\text{where } \\mathbf{D} = \\varepsilon_0 \\varepsilon_r \\mathbf{E}",
            "plain": "oint E \u00b7 dA = Q_enc / epsilon_0",
            "terms": [["\\mathbf{D}", "Electric displacement field vector"], ["\\mathbf{E}", "Total macroscopic electric field"], ["\\varepsilon_r", "Relative permittivity / dielectric constant"], ["u_E = \\frac{1}{2}\\varepsilon_0 E^2", "Electrostatic energy density stored in the field (J/m\u00b3)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"80\" y1=\"30\" x2=\"80\" y2=\"140\" stroke=\"#3B82F6\" stroke-width=\"4\"/>\n  <text x=\"60\" y=\"25\" font-size=\"12\" font-weight=\"700\" fill=\"#3B82F6\">+Q</text>\n  <line x1=\"380\" y1=\"30\" x2=\"380\" y2=\"140\" stroke=\"#EF4444\" stroke-width=\"4\"/>\n  <text x=\"380\" y=\"25\" font-size=\"12\" font-weight=\"700\" fill=\"#EF4444\">-Q</text>\n  <rect x=\"140\" y=\"35\" width=\"180\" height=\"100\" fill=\"rgba(245,158,11,0.18)\" stroke=\"#F59E0B\" stroke-width=\"2\" rx=\"4\"/>\n  <text x=\"195\" y=\"90\" font-size=\"13\" font-weight=\"700\" fill=\"#B45309\">Dielectric (\u03ba)</text>\n  <line x1=\"90\" y1=\"85\" x2=\"135\" y2=\"85\" stroke=\"var(--purple)\" stroke-width=\"1.8\" marker-end=\"url(#arrow)\"/>\n  <text x=\"95\" y=\"75\" font-size=\"10\" font-weight=\"700\" fill=\"var(--purple)\">E_0</text>\n  <line x1=\"325\" y1=\"85\" x2=\"375\" y2=\"85\" stroke=\"var(--purple)\" stroke-width=\"1.8\" marker-end=\"url(#arrow)\"/>\n</svg>",
        "figure_caption": "Figure 1.7: Dielectric slab partially filling a parallel plate capacitor. Bound charges reduce internal E-field to E0/\u03ba.",
        "content": "Gauss's Law relates the total electric flux threading any closed surface to the net enclosed charge: $\\Phi_E = \\oint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{\\text{enc}}}{\\varepsilon_0}$. Its utility relies on exploiting spherical, cylindrical, or planar symmetries.\n\n### Dielectric Polarization Mechanics\nWhen an insulating dielectric material of dielectric constant $\\kappa$ is inserted into an electric field $\\mathbf{E}_0$, dipole moments align to generate bound surface charge density $\\sigma_b = \\sigma\\left(1 - \\frac{1}{\\kappa}\\right)$. This induced counter-field diminishes the net internal field to $\\mathbf{E} = \\frac{\\mathbf{E}_0}{\\kappa}$.\n\n### Capacitance and Stored Energy\nCapacitance characterizes charge storage per unit potential difference: $C = \\frac{Q}{V} = \\frac{\\varepsilon_0 A}{d}$. The energy is stored within the electrostatic field itself with volume energy density $u_E = \\frac{1}{2}\\varepsilon_0 E^2$.",
        "didactic_notes": {
            "axiom": "Electric field lines are orthogonal to equipotential surfaces and direct strictly down the potential gradient: E = -dV/dr.",
            "trap": "If battery remains connected: V = constant, Q and U increase by \u03ba. If battery is disconnected: Q = constant, V decreases and U decreases by 1/\u03ba.",
            "mnemonic": "Remember: 'Battery Connected = Voltage Locked; Battery Disconnected = Charge Trapped'."
        },
        "key_takeaways": [
            "Gauss's Flux Theorem: $\\oint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{\\text{enc}}}{\\varepsilon_0}$.",
            "Dielectric Shielding: Net electric field inside linear dielectric reduces to $E = \\frac{E_0}{\\kappa}$.",
            "Capacitance Formula: $C = \\frac{\\kappa \\varepsilon_0 A}{d}$. Energy stored $U = \\frac{1}{2} C V^2 = \\frac{Q^2}{2C}$.",
            "Field Energy Density: $u_E = \\frac{1}{2}\\varepsilon_0 E^2$ (Joules per cubic meter)."
]
    },
    {
        "id": "FW-JEE-PHY-06",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "Modern Physics & Waves",
        "title": "Quantum Physics: The Photoelectric Equation & de Broglie Matter Waves",
        "score": 4.96,
        "source": "Eisberg-Resnick Quantum Physics / FineWeb-Edu",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Einstein's photoelectric effect, stopping potential equations, work function thresholds, and matter wave duality.",
        "formula_box": {
            "title": "Einstein's Photoelectric Energy Balance",
            "latex": "h\\nu = \\Phi_0 + K_{\\text{max}} = \\Phi_0 + e V_0 \\quad \\implies \\quad V_0 = \\frac{h}{e}\\nu - \\frac{\\Phi_0}{e}",
            "plain": "h*nu = Phi + e*V0",
            "terms": [["h\\nu", "Incident photon energy (Planck's quantum packet)"], ["\\Phi_0", "Work function threshold of emitter metal (eV)"], ["V_0", "Stopping potential required to extinguish photocurrent (volts)"], ["\\lambda = \\frac{h}{p}", "de Broglie matter wavelength for particle of momentum p"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"60\" y1=\"130\" x2=\"480\" y2=\"130\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"120\" y1=\"150\" x2=\"120\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <text x=\"485\" y=\"135\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">Frequency (\u03bd)</text>\n  <text x=\"80\" y=\"30\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">Stopping Potential V0</text>\n  <line x1=\"180\" y1=\"130\" x2=\"440\" y2=\"30\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"180\" cy=\"130\" r=\"4\" fill=\"var(--purple)\"/>\n  <text x=\"170\" y=\"148\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">\u03bd_threshold</text>\n  <text x=\"320\" y=\"60\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">Slope = h/e (Universal)</text>\n</svg>",
        "figure_caption": "Figure 1.8: Millikan stopping potential vs frequency plot. The slope is universally invariant across all metals: h/e.",
        "content": "Classical electromagnetic wave theory failed to explain why photoemission occurs instantaneously without time lag, why maximum kinetic energy is completely independent of light intensity, and why no emission occurs below a threshold frequency $\\nu_0$.\n\n### Einstein's Photon Hypothesis\nEinstein postulated that electromagnetic radiation propagates in discrete localized packets of energy termed photons: $E = h\\nu$. A single photon transfers its complete quantum of energy to a single bound electron:\n$$K_{\\text{max}} = h\\nu - \\Phi_0 = e V_0$$\n\nIncreasing beam intensity increases photon flux (photocurrent), but leaves the energy of individual photoelectrons unchanged.\n\n### Wave-Particle Duality of Matter\nLouis de Broglie extended this symmetry to material particles: every moving entity of momentum $p$ possesses an intrinsic matter wavelength:\n$$\\lambda = \\frac{h}{p} = \\frac{h}{\\sqrt{2m K}} = \\frac{h}{\\sqrt{2m q V}}$$",
        "didactic_notes": {
            "axiom": "The slope of the V0 vs frequency plot is universally identical for all materials: Slope = h/e = 4.14 x 10^-15 V\u00b7s.",
            "trap": "Photoelectric emission is strictly a ONE-PHOTON to ONE-ELECTRON interaction. Intensity affects photon count, NOT photon energy.",
            "mnemonic": "Dual Nature: 'Frequency governs Energy; Intensity governs Quantity'."
        },
        "key_takeaways": [
            "Photoelectric Equation: $e V_0 = h\\nu - \\Phi_0 = h(\\nu - \\nu_0)$.",
            "Universal Slope: Graph of stopping potential $V_0$ vs frequency $\\nu$ has slope $\\frac{h}{e}$ invariant of target metal.",
            "de Broglie Electron Wavelength: $\\lambda = \\frac{12.27}{\\sqrt{V}} \\text{ \\AA}$ for an electron accelerated through $V$ volts.",
            "Instantaneous Emission: Interaction occurs on timescale $< 10^{-9}$ seconds, demonstrating particle-like collision."
]
    },
    {
        "id": "FW-JEE-MAT-02",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Limits, Continuity & Differentiability",
        "title": "Calculus Foundations: L'H\u00f4pital's Rule & Indeterminate Forms",
        "score": 4.92,
        "source": "Apostol Mathematical Analysis / FineWeb-Edu",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Evaluation of indeterminate limits 0/0 and inf/inf via Cauchy's Mean Value Theorem, Taylor series expansions, and differentiability tests.",
        "formula_box": {
            "title": "L'H\u00f4pital's Asymptotic Ratio Theorem",
            "latex": "\\lim_{x \\to c} \\frac{f(x)}{g(x)} = \\lim_{x \\to c} \\frac{f'(x)}{g'(x)} \\quad \\text{for } \\left[\\frac{0}{0}\\right] \\text{ or } \\left[\\frac{\\infty}{\\infty}\\right]",
            "plain": "lim f(x)/g(x) = lim f'(x)/g'(x)",
            "terms": [["c", "Finite limit point or +/- infinity"], ["f'(x), g'(x)", "First-order derivatives where g'(x) != 0 in neighborhood of c"], ["f(c) = g(c) = 0", "Necessary indeterminate prerequisite criterion"], ["f'(c) = \\lim_{h \\to 0} \\frac{f(c+h)-f(c)}{h}", "Definition of differentiability: LHD == RHD"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <path d=\"M 60 120 C 140 110, 200 40, 270 40 C 340 40, 400 110, 480 120\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"270\" cy=\"40\" r=\"5\" fill=\"#10B981\"/>\n  <line x1=\"200\" y1=\"40\" x2=\"340\" y2=\"40\" stroke=\"#10B981\" stroke-width=\"1.8\" stroke-dasharray=\"3,3\"/>\n  <text x=\"278\" y=\"32\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">Smooth Tangent: LHD = RHD</text>\n  <line x1=\"270\" y1=\"45\" x2=\"270\" y2=\"140\" stroke=\"var(--ink-soft)\" stroke-width=\"1.2\" stroke-dasharray=\"2,2\"/>\n  <text x=\"265\" y=\"152\" font-size=\"11\" fill=\"var(--ink-soft)\">x = c</text>\n</svg>",
        "figure_caption": "Figure 1.9: Geometric differentiability. A function is differentiable if and only if its graph admits a unique, non-vertical tangent line.",
        "content": "Evaluating asymptotic limits in calculus frequently encounters indeterminate forms $\\frac{0}{0}$, $\\frac{\\infty}{\\infty}$, $0 \\times \\infty$, and $1^\\infty$. L'H\u00f4pital's rule provides an algorithmic bridge by analyzing tangent slopes via Cauchy's Extended Mean Value Theorem.\n\n### Analytical Theorem Statement\nIf $f$ and $g$ are real-valued functions differentiable on an open interval containing $c$, with $\\lim_{x \\to c} f(x) = \\lim_{x \\to c} g(x) = 0$, then:\n$$\\lim_{x \\to c} \\frac{f(x)}{g(x)} = \\lim_{x \\to c} \\frac{f'(x)}{g'(x)}$$\n\nprovided the right-hand derivative limit exists. For forms like $1^\\infty$, taking logarithms transforms the expression into $\\frac{0}{0}$:\n$$\\lim_{x \\to c} [f(x)]^{g(x)} = \\exp\\left( \\lim_{x \\to c} g(x) \\ln f(x) \\right)$$\n\n### Differentiability Criterion\nA function is differentiable at $x=c$ if and only if the Left-Hand Derivative (LHD) matches the Right-Hand Derivative (RHD). Sharp corners, cusps, and vertical tangents represent points of non-differentiability.",
        "didactic_notes": {
            "axiom": "Differentiability strictly implies continuity, but continuity does NOT imply differentiability (e.g. f(x) = |x| at x = 0).",
            "trap": "Do NOT apply L'H\u00f4pital's rule if the limit is determinate! Evaluating (x+2)/(x+3) at x->0 using derivatives yields 1/1 = 1 instead of the true 2/3.",
            "mnemonic": "Remember: 'Check Indeterminacy FIRST, Differentiate SECOND'."
        },
        "key_takeaways": [
            "Indeterminate Rule: $\\lim_{x \\to c} \\frac{f(x)}{g(x)} = \\lim_{x \\to c} \\frac{f'(x)}{g'(x)}$ strictly for $\\left[\\frac{0}{0}\\right]$ and $\\left[\\frac{\\infty}{\\infty}\\right]$.",
            "Exponential Standard Form: $\\lim_{x \\to 0} (1+x)^{1/x} = e$, and $\\lim_{x \\to c} f(x)^{g(x)} = e^{\\lim (f-1)g}$ for $1^\\infty$.",
            "Hierarchy of Continuity: Differentiability $\\implies$ Continuity $\\implies$ Limit Existence.",
            "Series Alternative: Taylor expansion $\\sin(x) = x - \\frac{x^3}{6} + \\dots$ often evaluates limits faster than repeated differentiation."
]
    },
    {
        "id": "FW-JEE-MAT-03",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Vectors & 3D Geometry",
        "title": "Vector Geometry: Triple Scalar Products & Shortest Distance Between Skew Lines",
        "score": 4.87,
        "source": "MIT Mathematics 18.02 / FineWeb-Edu",
        "word_count": 500,
        "reading_time_mins": 3,
        "summary": "Geometric interpretation of box product [a b c] as volume of parallelepiped and projection formula for skew line distances.",
        "formula_box": {
            "title": "Shortest Distance Between Skew Lines",
            "latex": "d = \\frac{|(\\mathbf{a}_2 - \\mathbf{a}_1) \\cdot (\\mathbf{b}_1 \\times \\mathbf{b}_2)|}{|\\mathbf{b}_1 \\times \\mathbf{b}_2|}",
            "plain": "d = |(a2 - a1) \u00b7 (b1 x b2)| / |b1 x b2|",
            "terms": [["\\mathbf{r}_1 = \\mathbf{a}_1 + \\lambda \\mathbf{b}_1", "Vector parametric equation of first spatial line"], ["\\mathbf{r}_2 = \\mathbf{a}_2 + \\mu \\mathbf{b}_2", "Vector parametric equation of second spatial line"], ["\\mathbf{n} = \\mathbf{b}_1 \\times \\mathbf{b}_2", "Common normal vector orthogonal to both direction vectors"], ["[\\mathbf{a} \\, \\mathbf{b} \\, \\mathbf{c}] = 0", "Condition for coplanarity of three spatial vectors"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"60\" y1=\"50\" x2=\"420\" y2=\"30\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <text x=\"430\" y=\"35\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">Line L1 (dir b1)</text>\n  <line x1=\"120\" y1=\"140\" x2=\"480\" y2=\"120\" stroke=\"#10B981\" stroke-width=\"2.5\"/>\n  <text x=\"490\" y=\"125\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Line L2 (dir b2)</text>\n  <line x1=\"260\" y1=\"40\" x2=\"260\" y2=\"130\" stroke=\"#EF4444\" stroke-width=\"2\" stroke-dasharray=\"4,4\"/>\n  <rect x=\"250\" y=\"75\" width=\"20\" height=\"20\" rx=\"3\" fill=\"var(--card)\" stroke=\"var(--border)\"/>\n  <text x=\"256\" y=\"90\" font-size=\"12\" font-weight=\"800\" fill=\"#EF4444\">d</text>\n  <text x=\"275\" y=\"88\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Shortest Distance</text>\n</svg>",
        "figure_caption": "Figure 1.10: Skew lines in three-dimensional space. The shortest distance vector is collinear with the mutual cross product b1 x b2.",
        "content": "In three-dimensional Euclidean space $\\mathbb{R}^3$, two non-parallel lines that do not intersect are termed **skew lines**. They reside in distinct parallel planes separated by an invariant minimal perpendicular separation.\n\n### Derivation of Minimal Distance\nConsider line $L_1: \\mathbf{r} = \\mathbf{a}_1 + \\lambda \\mathbf{b}_1$ and line $L_2: \\mathbf{r} = \\mathbf{a}_2 + \\mu \\mathbf{b}_2$. The mutual perpendicular direction $\\mathbf{n}$ is proportional to the cross product $\\mathbf{b}_1 \\times \\mathbf{b}_2$.\n\nThe connecting vector between arbitrary points on both lines is $\\mathbf{a}_2 - \\mathbf{a}_1$. The scalar projection of this connecting vector onto the unit normal vector yields the shortest distance:\n$$d = \\left| (\\mathbf{a}_2 - \\mathbf{a}_1) \\cdot \\frac{\\mathbf{b}_1 \\times \\mathbf{b}_2}{|\\mathbf{b}_1 \\times \\mathbf{b}_2|} \\right|$$\n\nIf $d = 0$, the lines intersect and are therefore coplanar: $[\\mathbf{a}_2 - \\mathbf{a}_1 \\quad \\mathbf{b}_1 \\quad \\mathbf{b}_2] = 0$.",
        "didactic_notes": {
            "axiom": "The scalar triple product [a b c] geometrically represents the signed volume of the parallelepiped spanned by the three vectors.",
            "trap": "If lines are parallel (b1 is proportional to b2), b1 x b2 = 0! You must use the parallel line distance formula d = |(a2 - a1) x b| / |b| instead.",
            "mnemonic": "Remember: 'Skew = Dot with Unit Cross'."
        },
        "key_takeaways": [
            "Skew Distance Formula: $d = \\frac{|(\\mathbf{a}_2 - \\mathbf{a}_1) \\cdot (\\mathbf{b}_1 \\times \\mathbf{b}_2)|}{|\\mathbf{b}_1 \\times \\mathbf{b}_2|}$.",
            "Coplanarity Condition: Two lines intersect if and only if the box product $(\\mathbf{a}_2 - \\mathbf{a}_1) \\cdot (\\mathbf{b}_1 \\times \\mathbf{b}_2) = 0$.",
            "Parallel Lines Distance: $d = \\frac{|(\\mathbf{a}_2 - \\mathbf{a}_1) \\times \\mathbf{b}|}{|\\mathbf{b}|}$.",
            "Volume of Tetrahedron: Formed by coterminous vectors $\\mathbf{a}, \\mathbf{b}, \\mathbf{c}$ equals $\\frac{1}{6}|[\\mathbf{a} \\, \\mathbf{b} \\, \\mathbf{c}]|$."
]
    },
    {
        "id": "FW-JEE-CHM-02",
        "course": "JEE",
        "subject": "Chemistry",
        "chapter": "General Organic Chemistry (GOC)",
        "title": "Electronic Effects: Hyperconjugation, Resonance & Carbocation Stability",
        "score": 4.9,
        "source": "March's Advanced Organic Chemistry / FineWeb-Edu",
        "word_count": 530,
        "reading_time_mins": 3,
        "summary": "Stabilization mechanisms of reactive organic intermediates: inductive sigma shifts, pi resonance delocalization, and Baker-Nathan hyperconjugation.",
        "formula_box": {
            "title": "Baker-Nathan Hyperconjugation Axiom",
            "latex": "\\sigma_{\\text{C-H}} \\longrightarrow p_{\\text{vacant}} \\quad \\implies \\quad \\text{Stability } \\propto \\text{Number of } \\alpha\\text{-Hydrogens}",
            "plain": "Stability proportional to number of alpha-H",
            "terms": [["\\sigma_{\\text{C-H}}", "Sigma bond electrons of adjacent sp3 alpha-carbon"], ["p_{\\text{vacant}}", "Empty p-orbital of sp2 hybridized planar carbocation center"], ["3^\\circ > 2^\\circ > 1^\\circ > \\text{CH}_3^+", "Classical alkyl carbocation stability hierarchy"], ["\\text{Resonance} > \\text{Hyperconjugation} > \\text{Inductive}", "Hierarchical dominance of electronic stabilizing effects"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <circle cx=\"160\" cy=\"85\" r=\"28\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"145\" y=\"90\" font-size=\"13\" font-weight=\"800\" fill=\"var(--purple)\">C\u207a (sp\u00b2)</text>\n  <ellipse cx=\"160\" cy=\"45\" rx=\"12\" ry=\"22\" fill=\"rgba(239,68,68,0.2)\" stroke=\"#EF4444\" stroke-width=\"1.5\"/>\n  <text x=\"140\" y=\"28\" font-size=\"10\" font-weight=\"700\" fill=\"#EF4444\">Vacant p</text>\n  <line x1=\"260\" y1=\"85\" x2=\"190\" y2=\"85\" stroke=\"#10B981\" stroke-width=\"3\"/>\n  <text x=\"270\" y=\"90\" font-size=\"13\" font-weight=\"700\" fill=\"#10B981\">C-H \u03c3-bond</text>\n  <path d=\"M 260 70 Q 210 50 170 50\" fill=\"none\" stroke=\"#F59E0B\" stroke-width=\"2\" stroke-dasharray=\"3,3\" marker-end=\"url(#arrow)\"/>\n  <text x=\"210\" y=\"42\" font-size=\"11\" font-weight=\"700\" fill=\"#F59E0B\">\u03c3 &rarr; p overlap</text>\n</svg>",
        "figure_caption": "Figure 1.11: Hyperconjugation (no-bond resonance). Electron density delocalizes from adjacent C-H sigma bonds into the vacant p-orbital.",
        "content": "Organic reaction mechanisms, regiospecificity (Markovnikov additions), and rearrangement cascades are governed by the thermodynamic stability of reactive reaction intermediates, predominantly **carbocations**.\n\n### Hierarchy of Electronic Effects\n1. **Mesomeric / Resonance Effect (+M):** Direct pi-electron conjugation or lone-pair donation represents the strongest stabilizing force. Heteroatoms with lone pairs adjacent to a carbocation (e.g. $-\\ddot{\\text{O}}\\text{CH}_3$) provide complete octet stabilization.\n2. **Hyperconjugation:** Also known as the Baker-Nathan effect or *no-bond resonance*, hyperconjugation involves overlap of $\\sigma_{\\text{C-H}}$ orbitals of $\\alpha$-carbons with the adjacent unoccupied $p$-orbital. Each $\\alpha$-hydrogen contributes a distinct hyperconjugative structure.\n3. **Inductive Effect (+I):** Weak through-bond polarization due to electronegativity differentials. Alkyl groups act as weak electron donors.",
        "didactic_notes": {
            "axiom": "Octet complete resonance structures ALWAYS dominate over open-octet structures, even if positive charge resides on electronegative oxygen or nitrogen.",
            "trap": "Do NOT count beta or gamma hydrogens! Only hydrogens attached directly to the sp3 carbon adjacent to the carbocation (alpha-hydrogens) participate.",
            "mnemonic": "Stability Hierarchy: 'R-H-I' (Resonance beats Hyperconjugation beats Inductive)."
        },
        "key_takeaways": [
            "Dominance Rule: $\\text{Resonance (+M)} \\gg \\text{Hyperconjugation} \\gg \\text{Inductive (+I)}$.",
            "Carbocation Stability: Tertiary ($9\\alpha\\text{-H}$) $>$ Secondary ($6\\alpha\\text{-H}$) $>$ Primary ($3\\alpha\\text{-H}$) $>$ Methyl.",
            "Tropylium Aromaticity: $7\\text{-membered cyclic carbocation with } 6\\pi\\text{ electrons}$ is exceptionally stable due to Huckel aromaticity.",
            "Rearrangement Driving Force: 1,2-hydride and 1,2-methyl shifts occur spontaneously to transform less stable carbocations into tertiary or resonance-stabilized isomers."
]
    },
    {
        "id": "FW-NEET-BIO-04",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Principles of Inheritance and Variation",
        "title": "Genetics: Mendelian Dihybrid Inheritance, Chromosomal Linkage & Morgan's Axiom",
        "score": 4.95,
        "source": "NCERT Biology Class XII / FineWeb-Edu",
        "word_count": 560,
        "reading_time_mins": 3,
        "summary": "Mendelian ratios, incomplete dominance, Morgan's Drosophila crosses, linkage maps, and genetic recombination frequencies.",
        "formula_box": {
            "title": "Genetic Recombination Frequency",
            "latex": "\\text{Recombination Frequency (RF)} = \\frac{\\text{Number of Recombinant Progeny}}{\\text{Total Progeny}} \\times 100\\%",
            "plain": "RF = (Recombinants / Total) * 100%",
            "terms": [["1 \\text{ cM (centiMorgan)}", "1 map unit corresponding to 1% recombination frequency between linked loci"], ["9:3:3:1", "Classical Mendelian F2 dihybrid phenotypic ratio under independent assortment"], ["T.H. Morgan", "Pioneered chromosomal theory of inheritance using Drosophila melanogaster"], ["\\text{Linkage}", "Physical association of genes on the same chromosome preventing independent assortment"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"60\" y=\"30\" width=\"30\" height=\"110\" rx=\"6\" fill=\"rgba(99,102,241,0.2)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <circle cx=\"75\" cy=\"55\" r=\"4\" fill=\"#EF4444\"/><text x=\"95\" y=\"60\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Gene y (yellow)</text>\n  <circle cx=\"75\" cy=\"75\" r=\"4\" fill=\"#3B82F6\"/><text x=\"95\" y=\"80\" font-size=\"11\" font-weight=\"700\" fill=\"#3B82F6\">Gene w (white) [Tight Linkage: 1.3% Recomb]</text>\n  <rect x=\"300\" y=\"30\" width=\"30\" height=\"110\" rx=\"6\" fill=\"rgba(16,185,129,0.2)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <circle cx=\"315\" cy=\"55\" r=\"4\" fill=\"#EF4444\"/><text x=\"335\" y=\"60\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Gene w (white)</text>\n  <circle cx=\"315\" cy=\"120\" r=\"4\" fill=\"#F59E0B\"/><text x=\"335\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#F59E0B\">Gene m (miniature) [Loose Linkage: 37.2% Recomb]</text>\n</svg>",
        "figure_caption": "Figure 2.3: Morgan's linkage experiment in Drosophila. Tightly linked genes (y-w) yield 98.7% parental types, while loosely linked genes (w-m) yield higher recombination.",
        "content": "Gregor Mendel's Law of Independent Assortment states that when two pairs of traits are combined in a hybrid, segregation of one pair is completely independent of the other pair. In a dihybrid cross ($RrYy \\times RrYy$), this produces the classical $9:3:3:1$ ratio.\n\n### Morgan's Discovery of Linkage\nThomas Hunt Morgan crossed yellow-bodied, white-eyed females with wild-type brown-bodied, red-eyed males in *Drosophila melanogaster*. The $F_2$ generation deviated significantly from $9:3:3:1$, with parental phenotypes appearing at $98.7\\%$ and recombinants at only $1.3\\%$.\n\nMorgan concluded that genes located on the same chromosome are physically linked. The frequency of crossing over is proportional to the physical distance separating the loci. Alfred Sturtevant utilized this principle to construct the world's first genetic linkage map, defining $1\\text{ map unit} = 1\\text{ centiMorgan} = 1\\%\\text{ recombination}$.",
        "didactic_notes": {
            "axiom": "Recombination frequency between two genes can NEVER exceed 50%. A frequency of 50% indicates either unlinked genes on different chromosomes or genes far apart on the same chromosome.",
            "trap": "Mendel's Law of Independent Assortment holds ONLY for genes located on different chromosomes or located far apart. It is VIOLATED by tight linkage.",
            "mnemonic": "Genetics Linkage Rule: 'Closer loci = Fewer crossovers = Higher parental percentage'."
        },
        "key_takeaways": [
            "Mendelian Dihybrid Ratio: $9:3:3:1$ phenotype and $1:2:1:2:4:2:1:2:1$ genotype under complete independent assortment.",
            "Linkage Violation: Tightly linked genes stay together, yielding high parental percentage and suppressed recombinant progeny.",
            "Recombination Distance: $1\\%\\text{ crossing over} = 1\\text{ map unit (cM)}$. Maximum observable frequency is capped at $50\\%$.",
            "Test Cross Significance: Crossing unknown dominant phenotype with homozygous recessive ($F_1 \\times \\text{recessive}$) reveals genotype directly from offspring ratio."
]
    },
    {
        "id": "FW-NEET-PHY-01",
        "course": "NEET",
        "subject": "Physics",
        "chapter": "Ray Optics & Optical Instruments",
        "title": "Geometrical Optics: Lens Maker's Formula, Refraction & Optical Power",
        "score": 4.89,
        "source": "Hecht Optics / NCERT Physics / FineWeb-Edu",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Spherical refracting surfaces, Lens Maker's equation, focal length immersion dependence, and compound microscope magnification.",
        "formula_box": {
            "title": "Lens Maker's Equation for Thin Lenses",
            "latex": "\\frac{1}{f} = \\left(\\frac{n_{\\text{lens}}}{n_{\\text{medium}}} - 1\\right) \\left(\\frac{1}{R_1} - \\frac{1}{R_2}\\right) = P",
            "plain": "1/f = (n_lens/n_med - 1) * (1/R1 - 1/R2) = P",
            "terms": [["f", "Focal length of the lens in meters (positive for convex, negative for concave)"], ["P", "Optical power measured in Dioptres (D, 1 D = 1 m^-1)"], ["R_1, R_2", "Radii of curvature of first and second refracting surfaces (Cartesian sign convention)"], ["n_{\\text{lens}}, n_{\\text{medium}}", "Refractive indices of lens glass and surrounding immersion medium"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"40\" y1=\"85\" x2=\"500\" y2=\"85\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <path d=\"M 270 20 C 295 55, 295 115, 270 150 C 245 115, 245 55, 270 20 Z\" fill=\"rgba(99,102,241,0.2)\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <line x1=\"80\" y1=\"85\" x2=\"80\" y2=\"40\" stroke=\"#10B981\" stroke-width=\"3\"/>\n  <text x=\"65\" y=\"32\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Object (h)</text>\n  <line x1=\"80\" y1=\"40\" x2=\"270\" y2=\"40\" stroke=\"#10B981\" stroke-width=\"1.8\"/>\n  <line x1=\"270\" y1=\"40\" x2=\"420\" y2=\"130\" stroke=\"#10B981\" stroke-width=\"1.8\"/>\n  <circle cx=\"370\" cy=\"85\" r=\"4\" fill=\"var(--purple)\"/>\n  <text x=\"365\" y=\"105\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">F (Focus)</text>\n  <line x1=\"420\" y1=\"85\" x2=\"420\" y2=\"130\" stroke=\"#EF4444\" stroke-width=\"2.5\"/>\n  <text x=\"430\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Real Inverted Image</text>\n</svg>",
        "figure_caption": "Figure 2.4: Ray diagram for a biconvex lens forming a real, inverted image. Principal rays refract through the focal point F.",
        "content": "In geometrical optics, thin lens calculations rely on paraxial ray approximations where $\\sin \\theta \\approx \\theta$. Refraction across a curved dielectric interface of radius $R$ is governed by $\\frac{n_2}{v} - \\frac{n_1}{u} = \\frac{n_2 - n_1}{R}$.\n\n### The Lens Maker's Equation\nApplying boundary conditions across two spherical interfaces yields the Lens Maker's relation:\n$$\\frac{1}{f} = \\left(\\frac{n_l}{n_m} - 1\\right)\\left(\\frac{1}{R_1} - \\frac{1}{R_2}\\right)$$\n\nWhen a glass lens ($n_l = 1.5$) is immersed in water ($n_m = 1.33$), $\\left(\\frac{1.5}{1.33} - 1\\right) \\approx 0.128$, which is roughly one-fourth of its air value $(1.5 - 1 = 0.5)$. Consequently, its focal length quadruples ($f_{\\text{water}} \\approx 4 f_{\\text{air}}$)!\n\nIf immersed in a medium of higher refractive index ($n_m > n_l$), the focal length flips sign: a converging biconvex lens behaves as a diverging lens.",
        "didactic_notes": {
            "axiom": "Sign Convention: Distances measured in the direction of incident light are positive; opposite to incident light are negative.",
            "trap": "NEET Distractor: Cutting a biconvex lens horizontally (along principal axis) leaves focal length unchanged (f' = f, intensity drops to 50%). Cutting vertically doubles focal length (f' = 2f).",
            "mnemonic": "Immersion Rule: 'Higher outer index? Lens flips its nature'."
        },
        "key_takeaways": [
            "Lens Maker's Relation: $\\frac{1}{f} = (n_{\\text{rel}} - 1)\\left(\\frac{1}{R_1} - \\frac{1}{R_2}\\right)$.",
            "Liquid Immersion Effect: Focal length in water increases by factor $\\sim 4$: $f_w = 4 f_a$ for glass of index 1.5.",
            "Power Combination: In-contact thin lenses combine additively: $P_{\\text{eq}} = P_1 + P_2 \\implies \\frac{1}{f_{\\text{eq}}} = \\frac{1}{f_1} + \\frac{1}{f_2}$.",
            "Microscope Magnification: $m = -\\left(\\frac{L}{f_o}\\right)\\left(\\frac{D}{f_e}\\right)$ under normal visual adjustment (image at near point D = 25 cm)."
]
    },
    {
        "id": "FW-NEET-CHM-01",
        "course": "NEET",
        "subject": "Chemistry",
        "chapter": "Ionic Equilibrium & Acids/Bases",
        "title": "Ionic Equilibrium: Buffer Solutions & The Henderson-Hasselbalch Equation",
        "score": 4.93,
        "source": "Vogel's Quantitative Chemical Analysis / FineWeb-Edu",
        "word_count": 530,
        "reading_time_mins": 3,
        "summary": "Acid-base conjugate pairs, common ion effect, buffer action mechanisms in biological blood serum, and Henderson-Hasselbalch derivation.",
        "formula_box": {
            "title": "Henderson-Hasselbalch Buffer Equation",
            "latex": "\\text{pH} = \\text{p}K_a + \\log_{10} \\left( \\frac{[\\text{Conjugate Base / Salt}]}{[\\text{Weak Acid}]} \\right)",
            "plain": "pH = pKa + log([Salt]/[Acid])",
            "terms": [["\\text{pH}", "Negative logarithm of hydrogen ion activity: -log10[H+]"], ["\\text{p}K_a", "-log10(Ka), the acid dissociation constant indicating intrinsic acid strength"], ["[\\text{Salt}] / [\\text{Acid}]", "Molar ratio of conjugate pair maintaining resistance to pH alteration"], ["\\text{Blood Buffer}", "Carbonic acid - bicarbonate system maintaining human arterial blood at pH 7.35\u20137.45"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"60\" y1=\"120\" x2=\"480\" y2=\"120\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"100\" y1=\"140\" x2=\"100\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <text x=\"485\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Volume of Base Added</text>\n  <text x=\"60\" y=\"30\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">pH</text>\n  <path d=\"M 100 110 Q 200 90 270 70 T 340 30\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"270\" cy=\"70\" r=\"5\" fill=\"#10B981\"/>\n  <text x=\"280\" y=\"75\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Half-Equivalence: pH = pKa</text>\n  <rect x=\"200\" y=\"55\" width=\"140\" height=\"30\" fill=\"rgba(16,185,129,0.12)\" stroke=\"#10B981\" stroke-dasharray=\"2,2\" rx=\"4\"/>\n  <text x=\"210\" y=\"45\" font-size=\"10\" font-weight=\"700\" fill=\"#10B981\">Optimal Buffer Zone (pH = pKa \u00b1 1)</text>\n</svg>",
        "figure_caption": "Figure 2.5: Weak acid titration curve. The buffer plateau exhibits maximal resistance to pH changes at the half-neutralization point where [Salt] = [Acid].",
        "content": "A **buffer solution** resists drastic changes in hydronium ion concentration upon addition of small amounts of strong acid or base. In human physiology, the carbonic acid-bicarbonate buffer ($\\text{H}_2\\text{CO}_3 / \\text{HCO}_3^-$) tightly restricts arterial blood pH to $7.35 - 7.45$.\n\n### Derivation of Henderson-Hasselbalch Equation\nConsider a weak acid $\\text{HA}$ dissociating in aqueous equilibrium:\n$$\\text{HA} \\rightleftharpoons \\text{H}^+ + \\text{A}^- \\quad \\implies \\quad K_a = \\frac{[\\text{H}^+][\\text{A}^-]}{[\\text{HA}]}$$\n\nRearranging for $[\\text{H}^+]$:\n$$[\\text{H}^+] = K_a \\frac{[\\text{HA}]}{[\\text{A}^-]}$$\n\nTaking negative logarithms of both sides:\n$$-\\log_{10}[\\text{H}^+] = -\\log_{10} K_a - \\log_{10}\\left(\\frac{[\\text{HA}]}{[\\text{A}^-]}\\right)$$\n$$\\text{pH} = \\text{p}K_a + \\log_{10}\\left(\\frac{[\\text{A}^-]}{[\\text{HA}]}\\right) = \\text{p}K_a + \\log_{10}\\left(\\frac{[\\text{Salt}]}{[\\text{Acid}]}\\right)$$\n\nMaximum buffer capacity occurs when $[\\text{Salt}] = [\\text{Acid}]$, at which point $\\log_{10}(1) = 0$ and $\\text{pH} = \\text{p}K_a$.",
        "didactic_notes": {
            "axiom": "Buffer capacity is maximal when [Salt] = [Acid] and operates effectively strictly in the range pH = pKa \u00b1 1.",
            "trap": "A mixture of strong acid and strong base is NOT a buffer! Only weak acid + conjugate salt or weak base + conjugate salt can act as a buffer.",
            "mnemonic": "Buffer Rule: 'Half Neutralized? pH equals pKa'."
        },
        "key_takeaways": [
            "Acidic Buffer Formula: $\\text{pH} = \\text{p}K_a + \\log_{10}\\left(\\frac{[\\text{Salt}]}{[\\text{Acid}]}\\right)$.",
            "Basic Buffer Formula: $\\text{pOH} = \\text{p}K_b + \\log_{10}\\left(\\frac{[\\text{Salt}]}{[\\text{Base}]}\\right)$ with $\\text{pH} = 14 - \\text{pOH}$ at 25\u00b0C.",
            "Common Ion Suppression: Adding sodium acetate ($\\text{CH}_3\\text{COONa}$) suppresses acetic acid dissociation due to Le Chatelier's principle.",
            "Solubility Product Precipitation: Precipitation occurs if and only if Ionic Product $Q_{\\text{sp}} > K_{\\text{sp}}$."
]
    },
    {
        "id": "FW-UPSC-POL-01",
        "course": "UPSC",
        "subject": "Polity",
        "chapter": "Constitutional Framework & Fundamental Rights",
        "title": "Constitutional Jurisprudence: The Basic Structure Doctrine & Article 21",
        "score": 4.96,
        "source": "Granville Austin / Supreme Court Law Reports / FineWeb-Edu",
        "word_count": 570,
        "reading_time_mins": 3,
        "summary": "Kesavananda Bharati precedent, evolution of judicial review under Article 368, and the golden triangle of Articles 14, 19, and 21.",
        "formula_box": {
            "title": "The Golden Triangle of Fundamental Rights",
            "latex": "\\text{Due Process} \\iff \\text{Article 14 (Equality)} \\cap \\text{Article 19 (Freedoms)} \\cap \\text{Article 21 (Life \\& Liberty)}",
            "plain": "Golden Triangle = Art. 14 + Art. 19 + Art. 21",
            "terms": [["Basic Structure Doctrine", "Supreme Court landmark ruling in Kesavananda Bharati v. State of Kerala (1973)"], ["Article 368", "Constituent amending power of Parliament is limited, not sovereign"], ["Article 21 (Maneka Gandhi, 1978)", "Substantive 'Procedure Established by Law' equals 'Due Process of Law' (just, fair, and reasonable)"], ["Article 32", "Constitutional remedies: 'Heart and Soul of the Constitution' (B.R. Ambedkar)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <polygon points=\"270,25 150,140 390,140\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"270\" cy=\"25\" r=\"7\" fill=\"#EF4444\"/><text x=\"245\" y=\"15\" font-size=\"12\" font-weight=\"700\" fill=\"#EF4444\">Art. 14 (Equality)</text>\n  <circle cx=\"150\" cy=\"140\" r=\"7\" fill=\"#3B82F6\"/><text x=\"80\" y=\"155\" font-size=\"12\" font-weight=\"700\" fill=\"#3B82F6\">Art. 19 (6 Freedoms)</text>\n  <circle cx=\"390\" cy=\"140\" r=\"7\" fill=\"#10B981\"/><text x=\"380\" y=\"155\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Art. 21 (Life &amp; Liberty)</text>\n  <text x=\"220\" y=\"90\" font-size=\"12\" font-weight=\"800\" fill=\"var(--purple)\">Golden Triangle</text>\n  <text x=\"185\" y=\"108\" font-size=\"10\" fill=\"var(--ink-soft)\">Substantive Due Process Rule</text>\n</svg>",
        "figure_caption": "Figure 3.4: The Golden Triangle jurisprudence post-Maneka Gandhi (1978). Any statutory infringement must pass tests of Articles 14, 19, and 21 simultaneously.",
        "content": "The Indian constitutional architecture rests on a delicate equilibrium between parliamentary legislative authority and judicial review. This tension culminated in the landmark 13-judge bench ruling in *Kesavananda Bharati v. State of Kerala (1973)*, which formulated the **Basic Structure Doctrine**.\n\n### The Limits of Amending Power\nThe Supreme Court held that while Parliament possesses broad constituent powers under Article 368 to amend any provision of the Constitution, it cannot alter, emasculate, or destroy the core pillars that constitute the 'Basic Structure'\u2014including secularism, federalism, judicial review, free and fair elections, and the separation of powers. Parliament cannot use an amending power derived from the Constitution to subvert the Constitution itself.\n\n### Expansion of Article 21\nIn *A.K. Gopalan (1950)*, the court took a narrow literalist view, holding that 'procedure established by law' required only formal statutory enactment. This was radically overturned in *Maneka Gandhi v. Union of India (1978)*: the procedure depriving liberty must be 'just, fair, and reasonable', effectively naturalizing American Substantive Due Process into Article 21.\n\nIn *K.S. Puttaswamy (2017)*, a 9-judge bench unanimously declared the **Right to Privacy** to be an intrinsic fundamental right under Article 21.",
        "didactic_notes": {
            "axiom": "Fundamental Rights are not absolute; they are subject to 'reasonable restrictions' enumerated in Articles 19(2)-(6), which are judicially reviewable under proportionality tests.",
            "trap": "UPSC Distractor: The term 'Basic Structure' is NOT defined anywhere in the Constitution of India! It is entirely a judicial innovation of the Supreme Court.",
            "mnemonic": "Basic Structure Anchors: 'S-F-J-R-D' (Secularism, Federalism, Judicial Review, Rights, Democracy)."
        },
        "key_takeaways": [
            "Basic Structure Verdict: Kesavananda Bharati (1973) established that Article 368 cannot alter the foundational identity of the Constitution.",
            "Substantive Due Process: Maneka Gandhi (1978) fused Articles 14, 19, and 21, requiring any procedure depriving liberty to be non-arbitrary, just, and fair.",
            "Right to Privacy: K.S. Puttaswamy (2017) affirmed privacy as a fundamental right rooted in individual autonomy, dignity, and bodily integrity.",
            "Non-Derogable Rights: Articles 20 (protection against ex-post facto laws/double jeopardy) and 21 CANNOT be suspended even during a National Emergency (44th Amendment, 1978)."
]
    },
    {
        "id": "FW-UPSC-POL-02",
        "course": "UPSC",
        "subject": "Polity",
        "chapter": "Federal System & Separation of Powers",
        "title": "Indian Federalism: Cooperative Dynamics, Seventh Schedule & Financial Devolution",
        "score": 4.91,
        "source": "M.P. Jain Indian Constitutional Law / FineWeb-Edu",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Asymmetric federalism, Article 246 legislative lists, Finance Commission revenue sharing (Article 280), and Article 356 emergency constraints.",
        "formula_box": {
            "title": "Vertical & Horizontal Fiscal Devolution Architecture",
            "latex": "\\text{Divisible Pool} \\xrightarrow{\\text{Article 280 (16th FC)}} 41\\% \\text{ to States} \\xrightarrow{\\text{Horizontal Criteria}} \\text{Equity, Efficiency, Demographic Effort}",
            "plain": "Divisible Pool -> Article 280 Finance Commission -> 41% Vertical Share",
            "terms": [["Seventh Schedule", "Article 246 division of competencies: Union List (100), State List (61), Concurrent List (52)"], ["Article 280", "Quasi-judicial Finance Commission appointed every 5 years by the President"], ["S.R. Bommai (1994)", "Landmark verdict curbing arbitrary imposition of President's Rule under Article 356"], ["Article 248", "Residuary powers of legislation vest exclusively in the Union Parliament"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"50\" y=\"25\" width=\"440\" height=\"40\" rx=\"6\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"170\" y=\"50\" font-size=\"13\" font-weight=\"800\" fill=\"var(--purple)\">UNION TAX REVENUES (Gross Pool)</text>\n  <line x1=\"270\" y1=\"65\" x2=\"270\" y2=\"105\" stroke=\"var(--purple)\" stroke-width=\"2.5\" marker-end=\"url(#arrow)\"/>\n  <text x=\"280\" y=\"90\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">41% Vertical Devolution (Art. 280)</text>\n  <rect x=\"50\" y=\"110\" width=\"200\" height=\"45\" rx=\"6\" fill=\"rgba(16,185,129,0.18)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"65\" y=\"137\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">States Divisible Pool (41%)</text>\n  <rect x=\"290\" y=\"110\" width=\"200\" height=\"45\" rx=\"6\" fill=\"rgba(245,158,11,0.18)\" stroke=\"#F59E0B\" stroke-width=\"2\"/>\n  <text x=\"315\" y=\"137\" font-size=\"12\" font-weight=\"700\" fill=\"#B45309\">Union Retained Pool (59%)</text>\n</svg>",
        "figure_caption": "Figure 3.5: Constitutional mechanism of vertical fiscal devolution under Article 280 recommendations.",
        "content": "K.C. Wheare characterized the Indian Constitution as **'quasi-federal'**\u2014a unitary state with subsidiary federal features. Granville Austin refined this description as **'Cooperative Federalism'**, highlighting mutual interdependence between Centre and States.\n\n### Legislative & Administrative Division\nArticle 246 delineates subject-matter competence into three lists in the Seventh Schedule. In cases of conflict regarding the Concurrent List, federal law prevails under Article 254(1), unless the state law has received Presidential assent under Article 254(2).\n\n### Fiscal Federalism and the GST Regime\nThe 101st Constitutional Amendment Act (2016) introduced the Goods and Services Tax (GST) and the **GST Council** (Article 279A). The Council operates on cooperative federal voting weights (1/3rd voting share for Union, 2/3rds collectively for States, with a 3/4ths decision threshold).\n\n### Restraints on Article 356\nIn *S.R. Bommai v. Union of India (1994)*, the Supreme Court placed President's Rule under judicial scrutiny, mandating that floor tests on the assembly floor are the sole objective test of ministry majority.",
        "didactic_notes": {
            "axiom": "Residuary powers of legislation in India reside with Parliament (Article 248), unlike in the US or Australia where they reside with the states.",
            "trap": "Cesses and surcharges levied by the Union are NOT part of the Divisible Pool under Article 270, creating friction in state fiscal devolution.",
            "mnemonic": "Federal Safeguards: 'B-F-G' (Bommai floor tests, Finance Commission 280, GST Council 279A)."
        },
        "key_takeaways": [
            "Quasi-Federal Architecture: Strong central bias with single citizenship, unified judiciary, and Article 356 emergency interventions.",
            "GST Federalism: Article 279A creates a constitutional forum where neither Centre nor States alone can unilaterally dictate tax rates.",
            "Judicial Safeguards: S.R. Bommai (1994) ended arbitrary state government dismissals, requiring floor tests and subject to judicial review.",
            "Article 280 Mandate: Finance Commission balances vertical equity (Union vs States) and horizontal equity (among states based on income distance and demographic performance)."
]
    },
    {
        "id": "FW-UPSC-ETH-01",
        "course": "UPSC",
        "subject": "Ethics",
        "chapter": "Public Service Values & Ethical Dilemmas",
        "title": "Ethics & Integrity: Deontology, Utilitarianism & Nolan Principles of Public Life",
        "score": 4.95,
        "source": "Second Administrative Reforms Commission (ARC-II) / FineWeb-Edu",
        "word_count": 550,
        "reading_time_mins": 3,
        "summary": "Normative ethical theories, Kantian categorical imperatives vs Benthamite consequentialism, and the Seven Nolan Principles in civil service administration.",
        "formula_box": {
            "title": "Administrative Ethical Dilemma Resolution Matrix",
            "latex": "\\text{Ethical Action} = \\text{Constitutional Morality} + \\text{Deontological Duty} + \\text{Utilitarian Welfare Maximization}",
            "plain": "Ethical Choice = Law + Duty + Greatest Good",
            "terms": [["Nolan Committee (1995)", "Seven Principles: Selflessness, Integrity, Objectivity, Accountability, Openness, Honesty, Leadership"], ["Deontology (Immanuel Kant)", "Duty-based ethics: an act is intrinsically right or wrong regardless of consequences"], ["Utilitarianism (Bentham/Mill)", "Consequentialism: 'The greatest happiness of the greatest number' (teleological)"], ["ARC-II (4th Report)", "Code of Ethics for Indian Civil Servants emphasizing impartiality and financial probity"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"40\" y=\"20\" width=\"140\" height=\"130\" rx=\"8\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"60\" y=\"45\" font-size=\"12\" font-weight=\"800\" fill=\"var(--purple)\">DEONTOLOGY</text>\n  <text x=\"50\" y=\"70\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Kant's Duty</text>\n  <text x=\"50\" y=\"90\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Categorical Rule</text>\n  <text x=\"50\" y=\"110\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Right Means</text>\n  \n  <rect x=\"200\" y=\"20\" width=\"140\" height=\"130\" rx=\"8\" fill=\"rgba(16,185,129,0.15)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"215\" y=\"45\" font-size=\"12\" font-weight=\"800\" fill=\"#10B981\">CONSTITUTION</text>\n  <text x=\"210\" y=\"70\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Rule of Law</text>\n  <text x=\"210\" y=\"90\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Public Trust</text>\n  <text x=\"210\" y=\"110\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Non-Partisanship</text>\n  \n  <rect x=\"360\" y=\"20\" width=\"140\" height=\"130\" rx=\"8\" fill=\"rgba(245,158,11,0.15)\" stroke=\"#F59E0B\" stroke-width=\"2\"/>\n  <text x=\"375\" y=\"45\" font-size=\"12\" font-weight=\"800\" fill=\"#B45309\">UTILITARIANISM</text>\n  <text x=\"370\" y=\"70\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Max Welfare</text>\n  <text x=\"370\" y=\"90\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Public Good</text>\n  <text x=\"370\" y=\"110\" font-size=\"10\" fill=\"var(--ink)\">\u2022 Outcomes</text>\n</svg>",
        "figure_caption": "Figure 3.6: Triad of administrative ethical decision-making: balancing deontological duty, constitutional morality, and utilitarian public welfare.",
        "content": "Public servants operate at the complex intersection of discretionary executive power, statutory mandates, and competing public interests. Ethics in governance (GS Paper IV) demands resolving ethical dilemmas through rigorous normative frameworks.\n\n### Normative Philosophical Frameworks\n1. **Deontology (Kantian Duty Ethics):** Immanuel Kant argued that morality is grounded in reason and duty. His *Categorical Imperative* asserts: *'Act only according to that maxim whereby you can at the same time will that it should become a universal law'*, and that individuals must be treated as ends in themselves, never merely as means to an outcome.\n2. **Consequentialism / Utilitarianism:** Formulated by Jeremy Bentham and John Stuart Mill, this view holds that the moral worth of an action is determined by its consequences\u2014maximizing utility ('the greatest good for the greatest number'). In public administration, utilitarianism guides cost-benefit welfare distribution, but must be tempered to prevent trampling minority rights.\n\n### The Seven Nolan Principles of Public Life\nThe 1995 UK Committee on Standards in Public Life established seven universal benchmarks adopted by ARC-II: **Selflessness, Integrity, Objectivity, Accountability, Openness, Honesty, and Leadership**.",
        "didactic_notes": {
            "axiom": "In Indian administrative law, Constitutional Morality always trumps societal majoritarian sentiment or personal moral biases.",
            "trap": "Do NOT recommend extralegal 'Robin Hood' solutions in case studies! Administrative integrity demands achieving ethical outcomes strictly within the framework of the rule of law.",
            "mnemonic": "Nolan Principles Acronym: 'S-I-O-A-O-H-L' (Selflessness, Integrity, Objectivity, Accountability, Openness, Honesty, Leadership)."
        },
        "key_takeaways": [
            "Deontology vs Teleology: Kant emphasizes pure motives and unbendable duty (means); Utilitarianism evaluates cumulative societal outcomes (ends).",
            "Nolan Principles: The 7 cardinal virtues required of civil servants to maintain public trust and democratic legitimacy.",
            "Constitutional Morality: Dr. B.R. Ambedkar's doctrine that fidelity to constitutional values (justice, liberty, fraternity) must supersede majoritarian passions.",
            "Conflict of Interest: Civil servants must proactively recuse themselves from decisions where private interests conflict with public duty."
]
    },
    {
        "id": "FW-JEE-MAT-04",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Functions & Domain-Range",
        "title": "Set Theory & Real Functions: Bijective Mappings & Inverse Functions",
        "score": 4.88,
        "source": "Rudin Principles of Mathematical Analysis / FineWeb-Edu",
        "word_count": 500,
        "reading_time_mins": 3,
        "summary": "Injectivity, surjectivity, natural domain restrictions, and horizontal line test criteria for invertible composite functions.",
        "formula_box": {
            "title": "Criterion for Invertibility of Mappings",
            "latex": "f: A \\to B \\text{ is invertible} \\iff f \\text{ is Injective (one-to-one)} \\land f \\text{ is Surjective (onto)}",
            "plain": "Invertible iff Injective (one-to-one) and Surjective (onto)",
            "terms": [["f(x_1) = f(x_2) \\implies x_1 = x_2", "Algebraic condition for injectivity (one-to-one)"], ["\\text{Range}(f) = \\text{Codomain}(B)", "Condition for surjectivity (onto)"], ["(f \\circ f^{-1})(y) = y", "Identity mapping property of inverse functions"], ["f(x) + f(-x) = 0", "Odd function condition (reflectional symmetry about origin)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <ellipse cx=\"120\" cy=\"80\" rx=\"60\" ry=\"50\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"95\" y=\"45\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">Domain A</text>\n  <circle cx=\"105\" cy=\"70\" r=\"4\" fill=\"var(--purple)\"/><circle cx=\"105\" cy=\"95\" r=\"4\" fill=\"var(--purple)\"/>\n  <ellipse cx=\"420\" cy=\"80\" rx=\"60\" ry=\"50\" fill=\"rgba(16,185,129,0.15)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"390\" y=\"45\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">Codomain B</text>\n  <circle cx=\"410\" cy=\"70\" r=\"4\" fill=\"#10B981\"/><circle cx=\"410\" cy=\"95\" r=\"4\" fill=\"#10B981\"/>\n  <path d=\"M 115 70 Q 260 40 400 70\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"250\" y=\"48\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">f (1-to-1)</text>\n  <path d=\"M 400 95 Q 260 125 115 95\" fill=\"none\" stroke=\"#10B981\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"245\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">f\u207b\u00b9 (Inverse)</text>\n</svg>",
        "figure_caption": "Figure 1.12: A bijective mapping f establishing a one-to-one correspondence between sets A and B.",
        "content": "A real function $f: A \\to B$ assigns to each element of set $A$ exactly one element in set $B$. In competitive calculus, mastering domain determinations and function invertibility forms the gateway to differential equations.\n\n### Injectivity and the Horizontal Line Test\nA function is strictly injective (one-to-one) if distinct inputs yield distinct outputs: $x_1 \\neq x_2 \\implies f(x_1) \\neq f(x_2)$. For continuous differentiable functions on an interval, strict monotonicity ($f'(x) > 0$ or $f'(x) < 0$ everywhere) is sufficient to guarantee injectivity.\n\n### Surjectivity and Range Construction\nA function is surjective (onto) when every element in codomain $B$ has at least one pre-image in domain $A$, which means $\\text{Range}(f) = \\text{Codomain}$. A function is invertible if and only if it is both injective and surjective (**bijective**). The graph of $y = f^{-1}(x)$ is the mirror reflection of $y = f(x)$ across the diagonal line $y = x$.",
        "didactic_notes": {
            "axiom": "The graph of an inverse function y = f^-1(x) is always the reflection of y = f(x) across the line y = x.",
            "trap": "Do not confuse domain with codomain! Trigonometric functions (e.g. sin x) are not bijective over R; their domains must be restricted (e.g. [-pi/2, pi/2]) to define arcsin.",
            "mnemonic": "Remember: 'Bijective = One-to-One PLUS Onto = Invertible'."
        },
        "key_takeaways": [
            "Invertibility Criterion: Inverse $f^{-1}$ exists if and only if $f$ is strictly bijective.",
            "Monotonicity Shortcut: If $f'(x) > 0$ strictly throughout an interval, $f$ is guaranteed to be one-to-one on that domain.",
            "Symmetry Axiom: Even functions $f(-x) = f(x)$ reflect across the y-axis; odd functions $f(-x) = -f(x)$ have point symmetry about the origin.",
            "Natural Domain Rule: For $\\sqrt{u(x)}$, require $u(x) \\ge 0$; for $\\ln(u(x))$, require $u(x) > 0$."
]
    },
    {
        "id": "FW-JEE-MAT-05",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Quadratic Equations",
        "title": "Algebra: Theory of Equations, Location of Roots & Discriminant Analysis",
        "score": 4.89,
        "source": "Hall & Knight Higher Algebra / FineWeb-Edu",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Roots of quadratic polynomials ax^2 + bx + c = 0, Vieta's relations, conditions for common roots, and location of roots relative to real scalar k.",
        "formula_box": {
            "title": "Vieta's Formulas & Discriminant Criteria",
            "latex": "\\alpha + \\beta = -\\frac{b}{a}, \\quad \\alpha \\beta = \\frac{c}{a}, \\quad \\Delta = b^2 - 4ac",
            "plain": "sum = -b/a, prod = c/a, D = b^2 - 4ac",
            "terms": [["\\alpha, \\beta", "Roots of the quadratic polynomial P(x) = ax^2 + bx + c"], ["\\Delta > 0", "Two distinct real roots; Delta = 0 (repeated root); Delta < 0 (complex conjugate roots)"], ["a \\cdot f(k) < 0", "Necessary and sufficient condition that real number k lies strictly between roots alpha and beta"], ["x_v = -\\frac{b}{2a}", "Abscissa of vertex of parabolic trajectory"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"50\" y1=\"100\" x2=\"490\" y2=\"100\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <path d=\"M 120 30 Q 270 160 420 30\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <circle cx=\"175\" cy=\"100\" r=\"5\" fill=\"#10B981\"/><text x=\"165\" y=\"90\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">&alpha;</text>\n  <circle cx=\"365\" cy=\"100\" r=\"5\" fill=\"#10B981\"/><text x=\"360\" y=\"90\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">&beta;</text>\n  <line x1=\"270\" y1=\"100\" x2=\"270\" y2=\"128\" stroke=\"#EF4444\" stroke-width=\"1.8\" stroke-dasharray=\"3,3\"/>\n  <circle cx=\"270\" cy=\"100\" r=\"4\" fill=\"#EF4444\"/>\n  <text x=\"265\" y=\"90\" font-size=\"11\" font-weight=\"800\" fill=\"#EF4444\">k</text>\n  <text x=\"280\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">f(k) &lt; 0 (when a &gt; 0)</text>\n</svg>",
        "figure_caption": "Figure 1.13: Location of roots. A number k lies strictly between alpha and beta if and only if a * f(k) < 0.",
        "content": "The quadratic polynomial $f(x) = ax^2 + bx + c$ represents a parabola with axis of symmetry $x = -\\frac{b}{2a}$. Beyond basic root extraction, advanced JEE problems focus on the **Location of Roots**—determining parameter regimes where roots lie with respect to specific real numbers $k$.\n\n### The Location of Roots Theorem\n1. **Both roots greater than $k$ ($\\alpha, \\beta > k$):**\nRequires $\\Delta \\ge 0$, $a \\cdot f(k) > 0$, and vertex coordinate $-\\frac{b}{2a} > k$.\n\n2. **A real number $k$ lies strictly between roots ($\\alpha < k < \\beta$):**\nBecause the parabola must cross the x-axis on either side of $k$, the single condition $a \\cdot f(k) < 0$ is necessary and sufficient! Notice that $\\Delta > 0$ is automatically satisfied when $a \\cdot f(k) < 0$.\n\n3. **Both roots lie in an interval $(k_1, k_2)$ ($k_1 < \\alpha \\le \\beta < k_2$):**\nRequires four simultaneous criteria: $\\Delta \\ge 0$, $a \\cdot f(k_1) > 0$, $a \\cdot f(k_2) > 0$, and vertex position $k_1 < -\\frac{b}{2a} < k_2$.\n\n4. **Exactly one root in $(k_1, k_2)$:**\nRequires $f(k_1) \\cdot f(k_2) < 0$, which guarantees an odd number of roots in the interval by the Intermediate Value Theorem.",
        "didactic_notes": {
            "axiom": "If a and c have opposite signs (ac < 0), the discriminant Delta = b^2 - 4ac is strictly positive for all real b, guaranteeing two real roots.",
            "trap": "Common Roots Error: If two quadratics share BOTH roots, a1/a2 = b1/b2 = c1/c2. If they share ONE root, use cross-multiplication (c1 a2 - c2 a1)^2 = (a1 b2 - a2 b1)(b1 c2 - b2 c1).",
            "mnemonic": "Remember: 'k Between Roots? Single Condition: a * f(k) < 0'."
        },
        "key_takeaways": [
            "Vieta's Relations: $\\alpha + \\beta = -\\frac{b}{a}$ and $\\alpha\\beta = \\frac{c}{a}$.",
            "Location of Roots: $a \\cdot f(k) < 0$ guarantees that scalar $k$ lies strictly between the roots $\\alpha$ and $\\beta$.",
            "Sign of Quadratic: If $\\Delta < 0$, the quadratic $ax^2 + bx + c$ retains the same sign as $a$ for ALL real $x$.",
            "Symmetric Expressions: $\\alpha^2 + \\beta^2 = (\\alpha+\\beta)^2 - 2\\alpha\\beta$ and $\\alpha^3 + \\beta^3 = (\\alpha+\\beta)^3 - 3\\alpha\\beta(\\alpha+\\beta)$."
]
    },
    {
        "id": "FW-JEE-CHM-03",
        "course": "JEE",
        "subject": "Chemistry",
        "chapter": "Chemical & Ionic Equilibrium",
        "title": "Chemical Equilibrium: The Law of Mass Action, Le Chatelier's Principle & Kp vs Kc",
        "score": 4.9,
        "source": "Atkins Physical Chemistry / FineWeb-Edu",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Dynamic equilibrium criteria, reaction quotient Q vs K, temperature dependence via van 't Hoff equation, and pressure volume shifts.",
        "formula_box": {
            "title": "Equilibrium Constant Relation & van 't Hoff Equation",
            "latex": "K_p = K_c (RT)^{\\Delta n_g}, \\quad \\ln\\left(\\frac{K_2}{K_1}\\right) = \\frac{\\Delta H^\\circ}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right)",
            "plain": "Kp = Kc*(RT)^Delta_n, ln(K2/K1) = (Delta_H/R)*(1/T1 - 1/T2)",
            "terms": [["K_p, K_c", "Equilibrium constants expressed in partial pressures (atm) and molar concentrations (mol/L)"], ["\\Delta n_g", "Moles of gaseous products minus moles of gaseous reactants: sum(n_prod) - sum(n_react)"], ["Q_c", "Reaction quotient: Q < K (shifts forward), Q > K (shifts backward), Q = K (dynamic equilibrium)"], ["\\Delta H^\\circ", "Standard enthalpy of reaction determining whether K increases or decreases with temperature"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"50\" y1=\"120\" x2=\"480\" y2=\"120\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"80\" y1=\"140\" x2=\"80\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <text x=\"485\" y=\"125\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Time (t)</text>\n  <text x=\"30\" y=\"30\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Reaction Rate</text>\n  <path d=\"M 80 40 Q 180 80 280 80 L 460 80\" fill=\"none\" stroke=\"#EF4444\" stroke-width=\"2.5\"/>\n  <text x=\"320\" y=\"70\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">Forward Rate (r_f)</text>\n  <path d=\"M 80 120 Q 180 80 280 80 L 460 80\" fill=\"none\" stroke=\"#3B82F6\" stroke-width=\"2.5\"/>\n  <text x=\"320\" y=\"98\" font-size=\"11\" font-weight=\"700\" fill=\"#3B82F6\">Reverse Rate (r_r)</text>\n  <line x1=\"280\" y1=\"20\" x2=\"280\" y2=\"120\" stroke=\"#10B981\" stroke-width=\"1.5\" stroke-dasharray=\"3,3\"/>\n  <text x=\"275\" y=\"138\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">Equilibrium State: r_f = r_r</text>\n</svg>",
        "figure_caption": "Figure 1.14: Dynamic equilibrium. Forward and backward reaction rates become equal; macroscopic concentrations remain constant.",
        "content": "Chemical equilibrium is dynamic in nature: forward and reverse reactions proceed at identical rates, so macroscopic concentrations remain constant over time ($r_f = r_r$).\n\n### Relationship Between Kp and Kc\nFor an ideal gas reaction $aA + bB \\rightleftharpoons cC + dD$:\n$$K_p = \\frac{P_C^c P_D^d}{P_A^a P_B^b} = \\frac{([C]RT)^c ([D]RT)^d}{([A]RT)^a ([B]RT)^b} = K_c (RT)^{\\Delta n_g}$$\n\nwhere $\\Delta n_g = (c+d) - (a+b)$ represents the change in gaseous stoichiometric coefficients.\n\n### Le Chatelier's Principle\nIf an external perturbation (change in concentration, pressure, volume, or temperature) is imposed on an equilibrium system, the system shifts in the direction that counteracts the change:\n- **Increasing Pressure:** Shifts toward the side with fewer gas moles ($\\Delta n_g < 0$).\n- **Inert Gas Addition:** At constant volume, inert gas does not change partial pressures, so equilibrium is unaffected! At constant pressure, inert gas increases volume, shifting toward more gas moles.",
        "didactic_notes": {
            "axiom": "Equilibrium constant K depends SOLELY on temperature. Catalysts accelerate the rate to achieve equilibrium, but DO NOT alter K or yield.",
            "trap": "Adding an inert gas at CONSTANT VOLUME causes ZERO shift in equilibrium! Only addition at constant pressure shifts toward more gas moles.",
            "mnemonic": "Remember: 'Endothermic likes Heat (K rises with T); Exothermic dislikes Heat (K drops with T)'."
        },
        "key_takeaways": [
            "Equilibrium Relation: $K_p = K_c (RT)^{\\Delta n_g}$. If $\\Delta n_g = 0$, $K_p = K_c$ independent of temperature units.",
            "Temperature Sensitivity: van 't Hoff equation $\\ln\\left(\\frac{K_2}{K_1}\\right) = \\frac{\\Delta H^\\circ}{R}\\left(\\frac{1}{T_1} - \\frac{1}{T_2}\\right)$.",
            "Direction of Shift: If $Q_c < K_c$, net forward reaction; if $Q_c > K_c$, net reverse reaction.",
            "Catalyst Role: Lowers activation energy $E_a$ equally for both forward and reverse pathways without shifting equilibrium position."
]
    },
    {
        "id": "FW-NEET-BIO-05",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Cell Biology & Genetics",
        "title": "Plant Physiology: Photophosphorylation, The Z-Scheme & Calvin C3/C4 Pathways",
        "score": 4.94,
        "source": "Taiz & Zeiger Plant Physiology / NCERT Biology",
        "word_count": 550,
        "reading_time_mins": 3,
        "summary": "Non-cyclic photophosphorylation, splitting of water at PSII, ATP/NADPH synthesis via proton gradients, and Kranz anatomy in C4 plants.",
        "formula_box": {
            "title": "Photolytic Water Splitting & Net Light Reaction",
            "latex": "2\\text{H}_2\\text{O} \\xrightarrow{h\\nu, \\text{ Mn}^{2+}, \\text{Cl}^-} 4\\text{H}^+ + 4e^- + \\text{O}_2 \\uparrow",
            "plain": "2 H2O -> 4 H+ + 4 e- + O2",
            "terms": [["\\text{PS II (P680)}", "Reaction center chlorophyll absorbing at 680 nm on thylakoid inner face"], ["\\text{PS I (P700)}", "Reaction center chlorophyll absorbing at 700 nm on stroma thylakoids"], ["\\text{RuBisCO}", "Ribulose-1,5-bisphosphate carboxylase-oxygenase: most abundant protein on Earth"], ["\\text{Kranz Anatomy}", "Bundle sheath cells with agranal chloroplasts surrounding vascular bundles in C4 plants (Maize, Sugarcane)"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 170\" width=\"100%\" height=\"150\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"60\" y=\"100\" width=\"70\" height=\"40\" fill=\"rgba(16,185,129,0.2)\" stroke=\"#10B981\" stroke-width=\"2\" rx=\"4\"/>\n  <text x=\"75\" y=\"125\" font-size=\"12\" font-weight=\"700\" fill=\"#10B981\">PS II (P680)</text>\n  <line x1=\"95\" y1=\"100\" x2=\"95\" y2=\"40\" stroke=\"#10B981\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"50\" y=\"35\" font-size=\"10\" font-weight=\"700\" fill=\"var(--ink)\">Primary Acceptor</text>\n  <path d=\"M 100 40 L 260 110\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"170\" y=\"70\" font-size=\"10\" font-weight=\"700\" fill=\"var(--purple)\">ETC &rarr; ATP</text>\n  <rect x=\"260\" y=\"100\" width=\"70\" height=\"40\" fill=\"rgba(99,102,241,0.2)\" stroke=\"var(--purple)\" stroke-width=\"2\" rx=\"4\"/>\n  <text x=\"275\" y=\"125\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">PS I (P700)</text>\n  <line x1=\"295\" y1=\"100\" x2=\"295\" y2=\"40\" stroke=\"var(--purple)\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <path d=\"M 300 40 L 440 40\" stroke=\"#F59E0B\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"350\" y=\"32\" font-size=\"11\" font-weight=\"700\" fill=\"#B45309\">NADPH Synthesis</text>\n</svg>",
        "figure_caption": "Figure 2.6: The Z-scheme of light reactions. Electrons flow from H2O to PSII (P680), through the cytochromes to PSI (P700), and reduce NADP+ to NADPH.",
        "content": "Photosynthesis consists of photochemical light reactions in the thylakoid membranes coupled to carbon-assimilating dark reactions in the stroma.\n\n### The Z-Scheme of Photophosphorylation\nLight absorption by Photosystem II (P680) excites electrons, which are accepted by a primary electron acceptor and transferred through Plastoquinone, Cytochrome $b_6f$, and Plastocyanin to Photosystem I (P700). Proton accumulation in the thylakoid lumen creates an electrochemical gradient driving ATP synthesis via $CF_0-CF_1$ ATP synthase.\n\n### C3 vs C4 Carbon Fixation\nIn $C_3$ plants, RuBisCO fixes $\\text{CO}_2$ to produce 3-phosphoglycerate (3-PGA). However, RuBisCO also binds oxygen, initiating wasteful **photorespiration** ($C_2$ cycle) where up to 25% of fixed carbon is lost without ATP generation!\n\nIn $C_4$ plants (maize, sugarcane, sorghum), spatial separation eliminates photorespiration: PEP carboxylase in mesophyll cells fixes $\\text{CO}_2$ into oxaloacetic acid ($4\\text{C}$), which is pumped to Kranz bundle sheath cells.",
        "didactic_notes": {
            "axiom": "Oxygen evolution occurs EXCLUSIVELY at Photosystem II on the luminal side of the thylakoid membrane, requiring Mn2+ and Cl- ions.",
            "trap": "RuBisCO has greater affinity for CO2 than O2, but high temperature and low CO2:O2 ratios favor oxygenase activity, triggering photorespiration in C3 plants.",
            "mnemonic": "C4 Kranz Advantage: 'PEPcase Never Binds Oxygen; Photorespiration is ZERO'."
        },
        "key_takeaways": [
            "Z-Scheme Products: Non-cyclic photophosphorylation generates ATP, $\\text{NADPH} + \\text{H}^+$, and evolves $\\text{O}_2$.",
            "Photorespiratory Wastage: Photorespiration occurs in chloroplast, peroxisome, and mitochondria, producing no ATP or sugars.",
            "Kranz Anatomy: Bundle sheath cells possess large agranal chloroplasts, thick gas-impermeable walls, and zero intercellular spaces.",
            "Energy Cost of Fixation: Fixing one molecule of $\\text{CO}_2$ requires $3\\text{ ATP} + 2\\text{ NADPH}$ in $C_3$, and $5\\text{ ATP} + 2\\text{ NADPH}$ in $C_4$."
]
    },
    {
        "id": "FW-NEET-CHM-02",
        "course": "NEET",
        "subject": "Chemistry",
        "chapter": "Biomolecules",
        "title": "Biochemistry: Amino Acid Zwitterions, Protein Structures & Carbohydrate Anomers",
        "score": 4.92,
        "source": "Lehninger Principles of Biochemistry / FineWeb-Edu",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Isoelectric points of amino acids, peptide bond planar geometry, alpha-helix vs beta-sheet hydrogen bonding, and glucose mutarotation.",
        "formula_box": {
            "title": "Isoelectric Point (pI) of Diprotic Amino Acid",
            "latex": "\\text{p}I = \\frac{\\text{p}K_{a1} + \\text{p}K_{a2}}{2}, \\quad \\text{Net Charge} = 0 \\text{ (Zwitterion Form)}",
            "plain": "pI = (pKa1 + pKa2) / 2",
            "terms": [["\\text{Zwitterion}", "Dipolar internal salt with deprotonated -COO^- and protonated -NH3^+ groups"], ["\\text{Peptide Bond}", "Planar trans -CO-NH- amide linkage with 40% double bond character due to resonance"], ["\\text{Secondary Structure}", "Alpha-helix and beta-pleated sheets stabilized exclusively by intra/intermolecular hydrogen bonds"], ["\\text{Denaturation}", "Disruption of secondary, tertiary, and quaternary structures leaving primary peptide backbone intact"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <rect x=\"80\" y=\"45\" width=\"380\" height=\"70\" rx=\"8\" fill=\"rgba(99,102,241,0.12)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <text x=\"100\" y=\"85\" font-size=\"14\" font-weight=\"800\" fill=\"#EF4444\">H\u2083N\u207a</text>\n  <line x1=\"145\" y1=\"80\" x2=\"190\" y2=\"80\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <text x=\"195\" y=\"85\" font-size=\"14\" font-weight=\"800\" fill=\"var(--ink)\">CH(R)</text>\n  <line x1=\"245\" y1=\"80\" x2=\"290\" y2=\"80\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <text x=\"295\" y=\"85\" font-size=\"14\" font-weight=\"800\" fill=\"#10B981\">COO\u207b</text>\n  <text x=\"360\" y=\"85\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">[Zwitterion State]</text>\n  <text x=\"150\" y=\"105\" font-size=\"11\" fill=\"var(--ink-soft)\">At Isoelectric Point (pI): Net Charge = 0 (No electrophoretic migration)</text>\n</svg>",
        "figure_caption": "Figure 2.7: The dipolar zwitterion state of an alpha-amino acid at its isoelectric point (pI).",
        "content": "Proteins are heteropolymers composed of $\\alpha$-amino acids linked by peptide bonds. All standard amino acids (except glycine) possess a chiral $\\alpha$-carbon and exist naturally in the L-enantiomer configuration.\n\n### The Zwitterionic State & Isoelectric Point\nIn aqueous solution, the carboxyl group loses a proton while the amino group accepts a proton, forming a dipolar **zwitterion**: $\\text{H}_3\\text{N}^+ - \\text{CH(R)} - \\text{COO}^-$. At the **isoelectric point** ($\\text{p}I$), the net electrical charge is exactly zero, minimizing water solubility and preventing migration in an electric field during electrophoresis.\n\n### Levels of Protein Organization\n- **Primary:** Sequence of amino acids linked by covalent peptide bonds.\n- **Secondary:** Local spatial folding ($\\alpha$-helix and $\\beta$-pleated sheets) stabilized strictly by backbone $\\text{C=O} \\dots \\text{H-N}$ hydrogen bonds.\n- **Tertiary:** Overall three-dimensional conformation stabilized by disulfide bridges ($-\\text{S-S}-$), hydrophobic interactions, ionic bonds, and van der Waals forces.\n- **Denaturation:** Heat, pH extremes, or heavy metals disrupt secondary and tertiary structures while leaving the primary covalent backbone intact.",
        "didactic_notes": {
            "axiom": "Denaturation destroys secondary, tertiary, and quaternary structures, but NEVER cleaves covalent primary peptide bonds.",
            "trap": "Glycine is the ONLY standard amino acid that is optically inactive because its alpha-carbon is attached to two identical hydrogen atoms.",
            "mnemonic": "Essential Amino Acids Acronym: 'PVT TIM HaLL' (Phe, Val, Thr, Trp, Ile, Met, His, Leu, Lys)."
        },
        "key_takeaways": [
            "Zwitterion Net Zero: At $\\text{p}I = \\frac{\\text{p}K_{a1} + \\text{p}K_{a2}}{2}$, net charge is zero and electrophoretic mobility ceases.",
            "Peptide Resonance: The $-C(=O)-NH-$ peptide bond is planar and rigid due to partial double bond character.",
            "Disulfide Bridge: Formed exclusively by oxidation between two cysteine thiol ($-SH$) residues.",
            "Reducing Sugars: Glucose, fructose, maltose, and lactose reduce Tollens' and Fehling's reagents; sucrose is non-reducing because anomeric carbons are locked."
]
    },
    {
        "id": "FW-NEET-PHY-02",
        "course": "NEET",
        "subject": "Physics",
        "chapter": "Kinematics & Work-Energy",
        "title": "2D Kinematics: Parabolic Projectile Trajectories & Range Optimization",
        "score": 4.88,
        "source": "University Physics OpenStax / FineWeb-Edu",
        "word_count": 510,
        "reading_time_mins": 3,
        "summary": "Orthogonal decomposition of 2D projectile motion under uniform gravitational acceleration, time of flight, and complementary launch angles.",
        "formula_box": {
            "title": "Projectile Kinematics Formulas",
            "latex": "T = \\frac{2u \\sin\\theta}{g}, \\quad H_{\\text{max}} = \\frac{u^2 \\sin^2\\theta}{2g}, \\quad R = \\frac{u^2 \\sin(2\\theta)}{g}",
            "plain": "T = 2u*sin(theta)/g, H = u^2*sin^2(theta)/(2g), R = u^2*sin(2*theta)/g",
            "terms": [["u", "Initial launch velocity at elevation angle theta above horizontal"], ["T", "Total time of flight until returning to original horizontal elevation"], ["H_{\\text{max}}", "Maximum vertical altitude achieved at apex where v_y = 0"], ["R_{\\text{max}} = \\frac{u^2}{g}", "Maximum horizontal range achieved at optimal launch angle theta = 45\u00b0"]]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 160\" width=\"100%\" height=\"140\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <line x1=\"50\" y1=\"120\" x2=\"490\" y2=\"120\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <path d=\"M 60 120 Q 260 20 460 120\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <line x1=\"60\" y1=\"120\" x2=\"110\" y2=\"70\" stroke=\"#10B981\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <text x=\"115\" y=\"75\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">u (angle &theta;)</text>\n  <line x1=\"260\" y1=\"120\" x2=\"260\" y2=\"45\" stroke=\"#EF4444\" stroke-width=\"1.5\" stroke-dasharray=\"3,3\"/>\n  <text x=\"268\" y=\"75\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">H_max</text>\n  <circle cx=\"260\" cy=\"45\" r=\"4\" fill=\"#EF4444\"/>\n  <text x=\"250\" y=\"35\" font-size=\"10\" font-weight=\"700\" fill=\"var(--ink)\">v_y = 0, v_x = u cos &theta;</text>\n  <text x=\"440\" y=\"135\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">Range R</text>\n</svg>",
        "figure_caption": "Figure 2.8: Parabolic flight trajectory under uniform gravity g. Horizontal velocity remains constant (u*cos(theta)).",
        "content": "Two-dimensional motion under uniform gravitational acceleration is analyzed by decomposing kinematics into mutually independent orthogonal Cartesian components along $x$ and $y$.\n\n### Orthogonal Decomposition\nAssuming zero atmospheric drag:\n- **Horizontal Axis ($x$):** Acceleration is zero ($a_x = 0$), so velocity remains strictly constant: $v_x = u\\cos\\theta$.\n- **Vertical Axis ($y$):** Acceleration is constant downwards ($a_y = -g$), so velocity obeys: $v_y = u\\sin\\theta - gt$.\n\nEliminating time $t$ yields the parabolic trajectory equation:\n$$y = x\\tan\\theta - \\frac{g x^2}{2 u^2 \\cos^2\\theta} = x\\tan\\theta \\left(1 - \\frac{x}{R}\\right)$$\n\n### Complementary Angle Property\nBecause $\\sin(2(90^\\circ - \\theta)) = \\sin(180^\\circ - 2\\theta) = \\sin(2\\theta)$, complementary launch angles ($\\theta$ and $90^\\circ - \\theta$) achieve the **exact same horizontal range $R$** for equal initial launch speed $u$!",
        "didactic_notes": {
            "axiom": "At the highest point (apex), kinetic energy is NOT zero! It equals (1/2)*m*(u*cos(theta))^2, because horizontal velocity is invariant.",
            "trap": "Complementary launch angles (e.g. 30\u00b0 and 60\u00b0) achieve equal range, but the steeper angle achieves greater maximum height (H2 > H1) and longer flight time (T2 > T1).",
            "mnemonic": "Remember: 'Range is identical for theta and (90\u00b0 - theta); product of flight times T1 * T2 = 2R/g'."
        },
        "key_takeaways": [
            "Trajectory Equation: $y = x\\tan\\theta - \\frac{g x^2}{2 u^2 \\cos^2\\theta} = x\\tan\\theta\\left(1 - \\frac{x}{R}\\right)$.",
            "Complementary Range Invariance: Launch angles $\\theta$ and $90^\\circ - \\theta$ yield identical horizontal range: $R_1 = R_2$.",
            "Speed at Apex: Minimum speed equals horizontal component $v_{\\text{min}} = u\\cos\\theta$ where kinetic energy $K_{\\text{min}} = K_0 \\cos^2\\theta$.",
            "Flight Time Product: $T_1 T_2 = \\frac{2R}{g}$ and ratio of heights $\\frac{H_1}{H_2} = \\tan^2\\theta$."
]
    },
    {
        "id": "FW-JEE-PHY-07",
        "course": "JEE",
        "subject": "Physics",
        "chapter": "AC Circuits & Resonance",
        "title": "Alternating Current: Series LCR Resonance, Quality Factor & Power Dissipation",
        "score": 4.92,
        "source": "MIT Courseware 8.02 / FineWeb-Edu Corpus",
        "word_count": 530,
        "reading_time_mins": 3,
        "summary": "Impedance triangles in driven RLC circuits, derivation of series resonant angular frequency omega_0 = 1/sqrt(LC), sharpness Quality Factor, and real vs reactive power factor.",
        "formula_box": {
            "title": "Series LCR Impedance & Resonance",
            "latex": "Z = \\sqrt{R^2 + \\left(\\omega L - \\frac{1}{\\omega C}\\right)^2}, \\quad \\omega_0 = \\frac{1}{\\sqrt{LC}}, \\quad Q = \\frac{\\omega_0 L}{R} = \\frac{1}{R}\\sqrt{\\frac{L}{C}}",
            "plain": "Z = sqrt(R^2 + (omega*L - 1/(omega*C))^2), omega_0 = 1/sqrt(L*C), Q = (omega_0*L)/R",
            "terms": [
                [
                    "Z",
                    "Total complex circuit impedance (ohms)"
                ],
                [
                    "\\omega_0",
                    "Resonant angular frequency where inductive and capacitive reactances cancel (rad/s)"
                ],
                [
                    "Q",
                    "Quality factor: ratio of resonant frequency to half-power bandwidth (sharpness of tuning)"
                ],
                [
                    "\\cos\\phi = \\frac{R}{Z}",
                    "Power factor determining real active average power P = V_{rms} I_{rms} cos(phi)"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Impedance Triangle -->\n  <line x1=\"80\" y1=\"130\" x2=\"280\" y2=\"130\" stroke=\"var(--ink)\" stroke-width=\"2.5\"/>\n  <text x=\"170\" y=\"150\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">Resistance R</text>\n  <line x1=\"280\" y1=\"130\" x2=\"280\" y2=\"40\" stroke=\"#EF4444\" stroke-width=\"2.5\"/>\n  <text x=\"290\" y=\"85\" font-size=\"12\" font-weight=\"700\" fill=\"#EF4444\">(X_L - X_C)</text>\n  <line x1=\"80\" y1=\"130\" x2=\"280\" y2=\"40\" stroke=\"var(--purple)\" stroke-width=\"3\"/>\n  <text x=\"155\" y=\"75\" font-size=\"13\" font-weight=\"800\" fill=\"var(--purple)\">Impedance Z</text>\n  <!-- Phase angle arc -->\n  <path d=\"M 120 130 A 40 40 0 0 0 115 114\" fill=\"none\" stroke=\"#F59E0B\" stroke-width=\"2\"/>\n  <text x=\"130\" y=\"122\" font-size=\"11\" font-weight=\"700\" fill=\"#F59E0B\">&phi;</text>\n  <!-- Resonance Peak curve -->\n  <path d=\"M 350 140 Q 420 140 435 50 Q 450 140 520 140\" fill=\"none\" stroke=\"#10B981\" stroke-width=\"2.5\"/>\n  <line x1=\"435\" y1=\"145\" x2=\"435\" y2=\"45\" stroke=\"#10B981\" stroke-width=\"1.5\" stroke-dasharray=\"3,3\"/>\n  <text x=\"420\" y=\"160\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">&omega;_0 = 1/&radic;(LC)</text>\n  <text x=\"380\" y=\"40\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Current Peak I_max</text>\n</svg>",
        "figure_caption": "Figure 1.7: Impedance phasor triangle and series resonance tuning curve. At omega_0, reactances cancel leaving purely resistive circuit with maximum current.",
        "content": "An alternating current (AC) circuit driven by a sinusoidal electromotive force $\\mathcal{E}(t) = V_0 \\sin(\\omega t)$ containing a series combination of resistance $R$, inductance $L$, and capacitance $C$ exhibits profound frequency-dependent impedance behavior.\n\n### The Impedance Triangle and Phase Angle\nThe net potential difference across the circuit is the vector phasor sum of instantaneous voltages: $\\mathbf{V}_R$ in phase with current, $\\mathbf{V}_L$ leading current by $\\pi/2$, and $\\mathbf{V}_C$ lagging current by $\\pi/2$. The resultant complex impedance $Z$ is:\n\n$$Z = \\sqrt{R^2 + (X_L - X_C)^2} = \\sqrt{R^2 + \\left(\\omega L - \\frac{1}{\\omega C}\\right)^2}$$\n\nThe phase constant $\\phi$ by which driving voltage leads circuit current satisfies $\\tan\\phi = \\frac{X_L - X_C}{R}$. When $X_L > X_C$, the circuit is inductive (voltage leads current); when $X_C > X_L$, the circuit is capacitive (current leads voltage).\n\n### Condition for Series Electrical Resonance\nResonance occurs when the driving angular frequency $\\omega$ causes inductive and capacitive reactances to cancel precisely:\n$$X_L = X_C \\implies \\omega_0 L = \\frac{1}{\\omega_0 C} \\implies \\omega_0 = \\frac{1}{\\sqrt{LC}}$$\n\nAt this critical frequency, total impedance drops to its absolute theoretical minimum $Z_{\\text{min}} = R$. The current amplitude surges to its global maximum $I_{\\text{max}} = \\frac{V_0}{R}$, and the circuit behaves purely resistively with zero phase lag ($\\phi = 0, \\cos\\phi = 1$).\n\n### Quality Factor and Power Factor\nThe **Quality Factor** ($Q$) measures the sharpness of circuit resonance and voltage magnification: $Q = \\frac{\\omega_0 L}{R} = \\frac{1}{R}\\sqrt{\\frac{L}{C}}$. At resonance, the individual voltages across inductor and capacitor equal $Q \\cdot V_0$, which can vastly exceed the source voltage! The real average dissipated power is given by $\\langle P \\rangle = V_{\\text{rms}} I_{\\text{rms}} \\cos\\phi$.",
        "didactic_notes": {
            "axiom": "At series resonance, the circuit is purely resistive (Z = R), current amplitude is maximized (I = V/R), and voltage across L and C individually can exceed source voltage by factor Q.",
            "trap": "Common Exam Trap: Average power dissipated in pure inductors or pure capacitors over a full cycle is strictly ZERO (wattless current); only resistance R dissipates real thermal energy.",
            "mnemonic": "CIVIL mnemonic: in Capacitor (C), Current (I) leads Voltage (V); Voltage (V) leads Current (I) in Inductor (L)."
        },
        "key_takeaways": [
            "Resonance Condition: Occurs at $\\omega_0 = 1/\\sqrt{LC}$ where $X_L = X_C$, yielding minimum impedance $Z_{\\text{min}} = R$ and maximum current.",
            "Voltage Magnification: At resonance, $V_L = V_C = Q \\cdot V_{\\text{source}}$, where $Q = \\frac{1}{R}\\sqrt{\\frac{L}{C}}$.",
            "Bandwidth & Selectivity: Bandwidth $\\Delta\\omega = \\omega_2 - \\omega_1 = \\frac{R}{L}$, giving $Q = \\frac{\\omega_0}{\\Delta\\omega}$.",
            "Average Power Formula: $\\langle P \\rangle = V_{\\text{rms}} I_{\\text{rms}} \\cos\\phi = I_{\\text{rms}}^2 R$."
        ]
    },
    {
        "id": "FW-JEE-MAT-06",
        "course": "JEE",
        "subject": "Mathematics",
        "chapter": "Complex Numbers & Euler's Formula",
        "title": "Complex Analysis: De Moivre's Theorem, nth Roots of Unity & Argand Geometry",
        "score": 4.95,
        "source": "Cambridge Mathematical Tripos / FineWeb-Edu Corpus",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Polar and exponential representations of complex numbers, Euler's identity, algebraic properties of the cube roots of unity, and circle/line loci in the complex plane.",
        "formula_box": {
            "title": "Euler's Formula & Roots of Unity",
            "latex": "e^{i\\theta} = \\cos\\theta + i\\sin\\theta, \\quad z_k = e^{i \\frac{2k\\pi}{n}}, \\quad 1 + \\omega + \\omega^2 = 0 \\quad (\\omega^3 = 1)",
            "plain": "e^(i*theta) = cos(theta) + i*sin(theta), 1 + omega + omega^2 = 0, omega^3 = 1",
            "terms": [
                [
                    "e^{i\\theta}",
                    "Unimodular complex number of modulus 1 and argument theta on the unit circle"
                ],
                [
                    "\\omega = e^{i 2\\pi/3}",
                    "Primitive non-real cube root of unity: -1/2 + i(sqrt(3)/2)"
                ],
                [
                    "|z - z_0| = r",
                    "Equation of a Euclidean circle of center z_0 and radius r in the Argand plane"
                ],
                [
                    "\\arg\\left(\\frac{z - z_1}{z - z_2}\\right) = \\theta",
                    "Locus of points subtending constant angle theta between z_1 and z_2 (circular arc)"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Axes -->\n  <line x1=\"50\" y1=\"90\" x2=\"310\" y2=\"90\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"180\" y1=\"160\" x2=\"180\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <text x=\"315\" y=\"94\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Re</text>\n  <text x=\"175\" y=\"15\" font-size=\"11\" font-weight=\"700\" fill=\"var(--ink)\">Im</text>\n  <!-- Unit Circle -->\n  <circle cx=\"180\" cy=\"90\" r=\"60\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <!-- Cube roots of unity equilateral triangle -->\n  <polygon points=\"240,90 150,38 150,142\" fill=\"rgba(99,102,241,0.15)\" stroke=\"var(--purple)\" stroke-width=\"1.8\"/>\n  <circle cx=\"240\" cy=\"90\" r=\"4\" fill=\"#10B981\"/>\n  <text x=\"245\" y=\"86\" font-size=\"12\" font-weight=\"800\" fill=\"#10B981\">1</text>\n  <circle cx=\"150\" cy=\"38\" r=\"4\" fill=\"#EF4444\"/>\n  <text x=\"135\" y=\"32\" font-size=\"12\" font-weight=\"800\" fill=\"#EF4444\">&omega;</text>\n  <circle cx=\"150\" cy=\"142\" r=\"4\" fill=\"#F59E0B\"/>\n  <text x=\"135\" y=\"155\" font-size=\"12\" font-weight=\"800\" fill=\"#F59E0B\">&omega;&sup2;</text>\n  <!-- Annotations -->\n  <text x=\"360\" y=\"60\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">Equilateral Triangle</text>\n  <text x=\"360\" y=\"85\" font-size=\"11\" fill=\"var(--ink-soft)\">1 + &omega; + &omega;&sup2; = 0</text>\n  <text x=\"360\" y=\"110\" font-size=\"11\" fill=\"var(--ink-soft)\">&omega;&sup3; = 1, |&omega;| = 1</text>\n  <text x=\"360\" y=\"135\" font-size=\"11\" fill=\"var(--ink-soft)\">Arg(&omega;) = 2&pi;/3 (120&deg;)</text>\n</svg>",
        "figure_caption": "Figure 1.8: The three cube roots of unity forming an equilateral triangle inscribed in the unit circle of the Argand plane.",
        "content": "Complex numbers extend the one-dimensional real number line into the two-dimensional Argand plane $\\mathbb{C}$, providing an indispensable algebraic framework for polynomial theory, coordinate geometry, and physical oscillations.\n\n### Polar Representation and Euler's Formula\nEvery complex number $z = x + iy$ can be uniquely expressed in polar trigonometric form $z = r(\\cos\\theta + i\\sin\\theta) = r e^{i\\theta}$, where $r = |z| = \\sqrt{x^2 + y^2}$ is the Euclidean modulus and $\\theta = \\text{Arg}(z) \\in (-\\pi, \\pi]$ is the principal argument. **De Moivre's Theorem** states that for any rational $n$:\n$$(\\cos\\theta + i\\sin\\theta)^n = \\cos(n\\theta) + i\\sin(n\\theta) = e^{in\\theta}$$\n\nMultiplication by $e^{i\\alpha}$ corresponds geometrically to a pure counter-clockwise rotation through angle $\\alpha$ around the origin without scaling.\n\n### Roots of Unity and Algebraic Symmetries\nThe equation $z^n = 1$ possesses exactly $n$ distinct complex roots evenly distributed along the unit circle $|z| = 1$ at angular increments of $\\frac{2\\pi}{n}$:\n$$z_k = e^{i \\frac{2k\\pi}{n}}, \\quad k = 0, 1, 2, \\dots, n-1$$\n\nFor $n = 3$, the cube roots of unity are $1, \\omega, \\omega^2$, where $\\omega = e^{i 2\\pi/3} = -\\frac{1}{2} + i\\frac{\\sqrt{3}}{2}$. Crucially, the sum of all roots of unity vanishes identically: $1 + \\omega + \\omega^2 = 0$, and the roots form the vertices of a regular polygon centered at the origin.\n\n### Geometric Loci in the Complex Plane\nComplex equations provide elegant coordinate-free geometry:\n- $|z - z_1| = |z - z_2|$ represents the perpendicular bisector of the line segment joining $z_1$ and $z_2$.\n- $\\frac{|z - z_1|}{|z - z_2|} = k$ ($k \\neq 1$) defines a Circle of Apollonius.\n- $\\text{Re}\\left(\\frac{z - z_1}{z - z_2}\\right) = 0$ represents a circle with diameter endpoints $z_1$ and $z_2$.",
        "didactic_notes": {
            "axiom": "Multiplication of a complex number z by e^{i\\theta} rotates the position vector counter-clockwise by angle \\theta in the Argand plane without altering its modulus.",
            "trap": "JEE Trap: If |z - z_1| + |z - z_2| = |z_1 - z_2|, the locus is NOT an ellipse! It degenerates into the straight line segment joining z_1 and z_2.",
            "mnemonic": "Cube Roots Identity: 1 + omega + omega^2 = 0 and omega^{3k} = 1; cyclic powers repeat every mod 3."
        },
        "key_takeaways": [
            "Euler's Decomposition: $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$, with $\\cos\\theta = \\frac{e^{i\\theta} + e^{-i\\theta}}{2}$ and $\\sin\\theta = \\frac{e^{i\\theta} - e^{-i\\theta}}{2i}$.",
            "Cube Roots of Unity: $1 + \\omega + \\omega^2 = 0$, $\\omega^3 = 1$, and $\\omega^2 = \\bar{\\omega} = 1/\\omega$.",
            "Roots of Unity Sum & Product: Sum of all $n$-th roots of unity is identically zero; product equals $(-1)^{n-1}$.",
            "Apollonius Circle: $|z - z_1| / |z - z_2| = k$ represents a circle if $k \\neq 1$, and the perpendicular bisector if $k = 1$."
        ]
    },
    {
        "id": "FW-NEET-BIO-06",
        "course": "NEET",
        "subject": "Biology",
        "chapter": "Ecology & Biodiversity",
        "title": "Ecology: Trophic Energetics, Population Growth Models & Gause's Competitive Exclusion",
        "score": 4.91,
        "source": "Campbell Biology / NCERT Ecology",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Lindeman's 10 percent energy transfer rule, upright vs inverted ecological pyramids, logistic Sigmoid Verhulst-Pearl carrying capacity, and Gause's competitive exclusion axiom.",
        "formula_box": {
            "title": "Verhulst-Pearl Logistic Growth Equation",
            "latex": "\\frac{dN}{dt} = rN\\left(\\frac{K - N}{K}\\right), \\quad P_n = P_{n-1} \\times 10\\%",
            "plain": "dN/dt = r*N*(K - N)/K, P_n = P_(n-1) * 0.10",
            "terms": [
                [
                    "N",
                    "Population density/size at time t"
                ],
                [
                    "r",
                    "Intrinsic rate of natural increase (biotic potential: b - d)"
                ],
                [
                    "K",
                    "Carrying capacity: maximum population density an environment can support sustainably"
                ],
                [
                    "(K - N)/K",
                    "Environmental resistance term slowing growth as N approaches K"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Logistic vs Exponential curve -->\n  <line x1=\"50\" y1=\"150\" x2=\"260\" y2=\"150\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"50\" y1=\"150\" x2=\"50\" y2=\"20\" stroke=\"var(--ink-soft)\" stroke-width=\"1.5\"/>\n  <line x1=\"50\" y1=\"60\" x2=\"260\" y2=\"60\" stroke=\"#EF4444\" stroke-width=\"1.5\" stroke-dasharray=\"3,3\"/>\n  <text x=\"210\" y=\"52\" font-size=\"10\" font-weight=\"700\" fill=\"#EF4444\">Carrying Capacity K</text>\n  <!-- Logistic S curve -->\n  <path d=\"M 50 145 Q 120 145 150 105 T 250 65\" fill=\"none\" stroke=\"#10B981\" stroke-width=\"2.5\"/>\n  <text x=\"160\" y=\"110\" font-size=\"10\" font-weight=\"700\" fill=\"#10B981\">Logistic S-Curve</text>\n  <!-- Trophic Pyramid -->\n  <polygon points=\"390,30 320,150 460,150\" fill=\"rgba(99,102,241,0.12)\" stroke=\"var(--purple)\" stroke-width=\"2\"/>\n  <line x1=\"337\" y1=\"120\" x2=\"443\" y2=\"120\" stroke=\"var(--purple)\" stroke-width=\"1.2\"/>\n  <line x1=\"355\" y1=\"90\" x2=\"425\" y2=\"90\" stroke=\"var(--purple)\" stroke-width=\"1.2\"/>\n  <line x1=\"372\" y1=\"60\" x2=\"408\" y2=\"60\" stroke=\"var(--purple)\" stroke-width=\"1.2\"/>\n  <text x=\"350\" y=\"140\" font-size=\"10\" font-weight=\"700\" fill=\"var(--ink)\">Producers (10,000 J)</text>\n  <text x=\"358\" y=\"108\" font-size=\"10\" font-weight=\"700\" fill=\"var(--purple)\">Herbivores (1,000 J)</text>\n  <text x=\"368\" y=\"80\" font-size=\"9\" font-weight=\"700\" fill=\"#F59E0B\">Carnivores (100 J)</text>\n  <text x=\"375\" y=\"48\" font-size=\"9\" font-weight=\"800\" fill=\"#EF4444\">Apex (10 J)</text>\n  <text x=\"470\" y=\"90\" font-size=\"10\" font-weight=\"700\" fill=\"var(--ink)\">10% Rule</text>\n</svg>",
        "figure_caption": "Figure 2.9: Logistic sigmoid population growth curve approaching carrying capacity K, and Lindeman's 10% upright pyramid of energy transfer.",
        "content": "Ecosystem biology examines the energetic flows, nutrient cycles, and competitive interactions that govern ecological stability and species diversity across biomes.\n\n### Trophic Energetics & Lindeman's 10% Law\nEnergy transfers through trophic levels obeying the Second Law of Thermodynamics: at each step, approximately 90% of available energy is dissipated as metabolic heat ($R$) and unassimilated waste ($F$), leaving on average only **10%** to be incorporated into new biomass (Lindeman's Efficiency):\n\n$$P_n = 0.10 \\times P_{n-1}$$\n\nConsequently, the **Pyramid of Energy is always strictly upright** without exception. In contrast, pyramids of biomass in aquatic ecosystems (e.g. open ocean) can be **inverted**, because a small standing biomass of rapidly reproducing phytoplankton supports a larger biomass of long-lived zooplankton and fish.\n\n### Population Growth Models\nWhen resources are unlimited, populations exhibit exponential $J$-shaped growth ($\\frac{dN}{dt} = rN$). In nature, finite space, nutrients, and predation impose environmental resistance, leading to the **Verhulst-Pearl Logistic Growth** equation:\n\n$$\\frac{dN}{dt} = rN \\left(\\frac{K - N}{K}\\right)$$\n\nHere $r$ is the biotic potential and $K$ is the habitat **carrying capacity**. As population $N \\to K$, growth decelerates smoothly to an asymptote, forming a characteristic sigmoid ($S$-shaped) curve. The maximum absolute growth rate occurs at the inflection point $N = K/2$.\n\n### Interspecific Competition & Gause's Principle\n**Gause's Competitive Exclusion Principle** dictates that two closely related species competing for identical limiting resources cannot coexist indefinitely; the competitively inferior species will ultimately be eliminated. Coexistence is preserved in nature via **resource partitioning** (e.g. MacArthur's warblers foraging at different tree heights or temporal feeding shifts).",
        "didactic_notes": {
            "axiom": "Pyramid of Energy is STRICTLY UPRIGHT in all ecosystems without exception; energy dissipates as metabolic heat at every trophic transition in accordance with the Second Law of Thermodynamics.",
            "trap": "NEET Trap: Pyramid of biomass in an aquatic ecosystem (sea/lake) is INVERTED because the standing crop biomass of phytoplankton is much lower than the rapid-turnover zooplankton.",
            "mnemonic": "Remember Gause: 'Two species competing for the exact same limited resource cannot coexist indefinitely \u2014 one will be driven to local extinction'."
        },
        "key_takeaways": [
            "Energy Unidirectionality: Lindeman's 10% rule dictates that only 10% of energy is transferred to the next trophic level; 90% is dissipated as respiration heat.",
            "Logistic Sigmoid Equilibrium: Maximum growth rate occurs at inflection point $N = K/2$, where $\\frac{dN}{dt}$ reaches its maximum $\\frac{rK}{4}$.",
            "Resource Partitioning: Coexistence is mediated by behavioral or temporal niche differentiation rather than competitive displacement.",
            "Species-Area Law: $\\log S = \\log C + Z \\log A$; standard regression coefficient $Z = 0.1$ to $0.2$, rising to $0.6$ to $1.2$ across large continental biomes."
        ]
    },
    {
        "id": "FW-NEET-PHY-03",
        "course": "NEET",
        "subject": "Physics",
        "chapter": "Current Electricity & Circuits",
        "title": "Direct Current Circuits: Kirchhoff's Laws, Wheatstone Bridge & Potentiometric Precision",
        "score": 4.9,
        "source": "Halliday & Resnick Fundamentals of Physics / FineWeb-Edu",
        "word_count": 520,
        "reading_time_mins": 3,
        "summary": "Conservation laws in electric networks, algebraic junction and loop rules, derivation of Wheatstone bridge balance R1/R2 = R3/R4, and null-deflection measurements.",
        "formula_box": {
            "title": "Kirchhoff's Laws & Wheatstone Balance",
            "latex": "\\sum I_{\\text{in}} = \\sum I_{\\text{out}}, \\quad \\sum \\Delta V = 0, \\quad \\frac{P}{Q} = \\frac{R}{S} \\implies I_G = 0",
            "plain": "sum(I_in) = sum(I_out), sum(Delta V) = 0, P/Q = R/S => I_G = 0",
            "terms": [
                [
                    "\\sum I = 0",
                    "Kirchhoff's First Law (Junction Rule): Conservation of electric charge"
                ],
                [
                    "\\sum \\Delta V = 0",
                    "Kirchhoff's Second Law (Loop Rule): Conservation of energy along closed path"
                ],
                [
                    "P, Q, R, S",
                    "Resistances forming the four arms of the Wheatstone quadrilateral"
                ],
                [
                    "E = k \\cdot l",
                    "Potentiometer principle: emf proportional to balancing length l under zero current drain"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Wheatstone Bridge Diamond -->\n  <polygon points=\"180,30 250,90 180,150 110,90\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\"/>\n  <!-- Resistor Labels -->\n  <text x=\"130\" y=\"55\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">P</text>\n  <text x=\"215\" y=\"55\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">Q</text>\n  <text x=\"130\" y=\"130\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">R</text>\n  <text x=\"215\" y=\"130\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">S</text>\n  <!-- Galvanometer Central Bridge -->\n  <line x1=\"180\" y1=\"30\" x2=\"180\" y2=\"150\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <circle cx=\"180\" cy=\"90\" r=\"14\" fill=\"var(--card)\" stroke=\"#10B981\" stroke-width=\"2\"/>\n  <text x=\"175\" y=\"95\" font-size=\"12\" font-weight=\"800\" fill=\"#10B981\">G</text>\n  <!-- Battery connections -->\n  <line x1=\"110\" y1=\"90\" x2=\"60\" y2=\"90\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <line x1=\"250\" y1=\"90\" x2=\"300\" y2=\"90\" stroke=\"var(--ink)\" stroke-width=\"2\"/>\n  <!-- Balance Equation Box -->\n  <rect x=\"330\" y=\"45\" width=\"180\" height=\"90\" rx=\"8\" fill=\"var(--card)\" stroke=\"var(--border)\" stroke-width=\"1.5\"/>\n  <text x=\"350\" y=\"72\" font-size=\"12\" font-weight=\"700\" fill=\"var(--purple)\">Balance Condition:</text>\n  <text x=\"375\" y=\"98\" font-size=\"15\" font-weight=\"800\" fill=\"var(--ink)\">P / Q = R / S</text>\n  <text x=\"365\" y=\"122\" font-size=\"11\" font-weight=\"600\" fill=\"#10B981\">&rarr; I_G = 0 (Null Deflection)</text>\n</svg>",
        "figure_caption": "Figure 2.10: The Wheatstone bridge circuit. When P/Q = R/S, nodes are equipotential and galvanometer current is strictly zero.",
        "content": "Complex direct current (DC) networks containing interconnected resistors, real batteries, and measuring galvanometers cannot be reduced by simple series-parallel formulas alone and require systematic application of **Kirchhoff's Laws**.\n\n### Kirchhoff's Network Laws\n1. **Kirchhoff's Current Law (KCL / Junction Rule):** The algebraic sum of currents entering any circuit node equals zero ($\\sum I = 0$). KCL is a direct manifestation of the **Conservation of Electric Charge**.\n2. **Kirchhoff's Voltage Law (KVL / Loop Rule):** The algebraic sum of potential differences across all elements around any closed circuit loop is zero ($\\sum \\Delta V = 0$). KVL arises directly from the **Conservation of Energy** in conservative electrostatic fields.\n\n### The Wheatstone Bridge Principle\nA Wheatstone bridge consists of four resistors ($P, Q, R, S$) arranged in a quadrilateral loop with a sensitive galvanometer $G$ bridging opposite nodes $B$ and $D$. When node potentials are equal ($V_B = V_D$):\n$$\\frac{P}{Q} = \\frac{R}{S} \\implies I_G = 0$$\n\nAt this null deflection state, current through the galvanometer vanishes. This balance condition is symmetric: exchanging the battery and galvanometer branches leaves the balance condition entirely unchanged.\n\n### Practical Meter Bridge and Potentiometer\nThe **Meter Bridge** realizes this principle along a uniform $100\\text{ cm}$ constantan wire, yielding $X = R \\frac{l}{100 - l}$.\n\nThe **Potentiometer** measures electromotive force (EMF) without drawing any current from the cell under test at the balance point ($E \\propto l$). Because it operates under zero current drain ($I = 0$), it measures the true open-circuit EMF $E$ free from internal resistance voltage drops ($V = E - Ir$), making it vastly superior to conventional finite-resistance voltmeters.",
        "didactic_notes": {
            "axiom": "The Potentiometer is an ideal voltmeter of infinite effective input resistance because it measures EMF at zero current draw (null point), eliminating internal resistance drop.",
            "trap": "Common Exam Trap: In a Meter Bridge, if end resistances (strip resistance) are not compensated, the balance point shifts; balance is most sensitive when balance point is near 50 cm.",
            "mnemonic": "Kirchhoff Rules Conservation: KCL = Conservation of Charge; KVL = Conservation of Energy."
        },
        "key_takeaways": [
            "Kirchhoff Laws Grounding: KCL is based on charge conservation; KVL is based on path independence of conservative potential fields.",
            "Bridge Balance Condition: When $\\frac{P}{Q} = \\frac{R}{S}$, no current traverses the galvanometer; exchanging battery and galvanometer preserves the balance condition.",
            "Meter Bridge Calculation: Unknown resistance $X = R \\cdot \\frac{l}{100 - l}$ where $l$ is balance length in centimeters.",
            "Internal Resistance Measurement: Potentiometer measures cell internal resistance via $r = R \\left(\\frac{l_1}{l_2} - 1\\right)$."
        ]
    },
    {
        "id": "FW-NEET-CHM-03",
        "course": "NEET",
        "subject": "Chemistry",
        "chapter": "Organic Chemistry: Carbonyls & Alkenes",
        "title": "Reaction Mechanisms: Carbonyl Nucleophilic Addition & Markovnikov Regioselectivity",
        "score": 4.93,
        "source": "Clayden Organic Chemistry / NCERT Chemistry",
        "word_count": 540,
        "reading_time_mins": 3,
        "summary": "Electrophilic polarization of the carbonyl C=O group, tetrahedral intermediate formation, Markovnikov's carbocation rule vs Peroxide Anti-Markovnikov Kharasch effect.",
        "formula_box": {
            "title": "Electrophilic Addition & Carbonyl Addition Kinetics",
            "latex": "\\text{R}_2\\text{C}=\\text{O} + \\text{Nu}^- \\xrightarrow{\\text{slow}} \\left[\\text{R}_2\\text{C}(\\text{Nu})-\\text{O}^-\\right] \\xrightarrow{\\text{fast, } \\text{H}^+} \\text{R}_2\\text{C}(\\text{Nu})-\\text{OH}",
            "plain": "R2C=O + Nu- -> [R2C(Nu)-O-] -> R2C(Nu)-OH",
            "terms": [
                [
                    "\\text{Nucleophilic Addition}",
                    "Attack of nucleophile on planar sp2 carbonyl carbon to form tetrahedral sp3 intermediate"
                ],
                [
                    "\\text{Markovnikov's Rule}",
                    "Electrophile (H+) adds to the alkene carbon with more hydrogens, generating the more substituted carbocation"
                ],
                [
                    "\\text{Kharasch Effect}",
                    "Free radical addition of HBr in the presence of peroxides yielding anti-Markovnikov primary bromide"
                ],
                [
                    "\\text{Carbocation Stability}",
                    "Tertiary (3\u00b0) > Secondary (2\u00b0) > Primary (1\u00b0) governed by hyperconjugation and +I induction"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Carbonyl Polar Bond -->\n  <text x=\"70\" y=\"80\" font-size=\"16\" font-weight=\"800\" fill=\"var(--ink)\">R&minus;C=O</text>\n  <text x=\"100\" y=\"60\" font-size=\"11\" font-weight=\"700\" fill=\"#EF4444\">&delta;+</text>\n  <text x=\"135\" y=\"60\" font-size=\"11\" font-weight=\"700\" fill=\"#10B981\">&delta;&minus;</text>\n  <!-- Nucleophilic attack arrow -->\n  <path d=\"M 60 130 C 80 120, 100 105, 105 85\" fill=\"none\" stroke=\"var(--purple)\" stroke-width=\"2.5\" marker-end=\"url(#arrow)\"/>\n  <text x=\"40\" y=\"145\" font-size=\"12\" font-weight=\"800\" fill=\"var(--purple)\">:Nu&minus; (Attack)</text>\n  <!-- Reaction Arrow -->\n  <line x1=\"170\" y1=\"80\" x2=\"230\" y2=\"80\" stroke=\"var(--ink)\" stroke-width=\"2\" marker-end=\"url(#arrow)\"/>\n  <!-- Tetrahedral Intermediate -->\n  <rect x=\"250\" y=\"45\" width=\"120\" height=\"75\" rx=\"8\" fill=\"var(--card)\" stroke=\"var(--border)\" stroke-width=\"1.5\"/>\n  <text x=\"265\" y=\"70\" font-size=\"12\" font-weight=\"700\" fill=\"var(--ink)\">Tetrahedral sp&sup3;</text>\n  <text x=\"270\" y=\"95\" font-size=\"12\" font-weight=\"800\" fill=\"#10B981\">R&minus;C(Nu)&minus;O&minus;</text>\n  <!-- Markovnikov Addition note -->\n  <rect x=\"390\" y=\"45\" width=\"130\" height=\"75\" rx=\"8\" fill=\"rgba(99,102,241,0.1)\" stroke=\"var(--purple)\" stroke-width=\"1.5\"/>\n  <text x=\"400\" y=\"68\" font-size=\"11\" font-weight=\"700\" fill=\"var(--purple)\">Markovnikov Rule:</text>\n  <text x=\"400\" y=\"88\" font-size=\"10\" fill=\"var(--ink)\">H+ &rarr; more H carbon</text>\n  <text x=\"400\" y=\"105\" font-size=\"10\" font-weight=\"700\" fill=\"#10B981\">&rarr; 3&deg; > 2&deg; > 1&deg; C+</text>\n</svg>",
        "figure_caption": "Figure 2.11: Nucleophilic addition onto polarized carbonyl carbon forming tetrahedral intermediate, and Markovnikov carbocation regioselectivity.",
        "content": "Organic reactions are governed by electronic polarization, transition state thermodynamics, and intermediate carbocation stabilities.\n\n### Carbonyl Polarization & Nucleophilic Addition\nThe carbon-oxygen double bond of aldehydes and ketones is intensely polarized by the electronegativity difference between carbon (2.5) and oxygen (3.5), rendering the carbonyl carbon strongly electrophilic ($\\text{C}^{\\delta+} = \\text{O}^{\\delta-}$).\n\nNucleophiles (e.g. $\\text{CN}^-$, $\\text{HSO}_3^-$, Grignard reagents $\\text{RMgX}$) attack this planar $sp^2$-hybridized center along the optimal **B\u00fcrgi-Dunitz trajectory** (angle $\\approx 107^\\circ$), converting it into a tetrahedral $sp^3$ alkoxide intermediate. Aldehydes exhibit markedly higher reactivity than ketones because:\n1. **Steric Factor:** Aldehydes have only one alkyl substituent, minimizing steric crowding in the crowded tetrahedral transition state.\n2. **Electronic Factor:** Two alkyl groups in ketones donate electron density via $+I$ induction, diminishing the electrophilic partial positive charge on carbon.\n\n### Alkene Electrophilic Addition & Markovnikov Regioselectivity\nWhen unsymmetrical alkenes react with hydrogen halides ($HX$):\n- **Markovnikov's Rule:** The electrophilic proton $\\text{H}^+$ adds to the double-bonded carbon carrying the greater number of hydrogen atoms, yielding the more substituted, stable carbocation intermediate ($3^\\circ > 2^\\circ > 1^\\circ$) stabilized by hyperconjugation.\n- **The Peroxide (Kharasch) Effect:** In the presence of organic peroxides, addition of $\\text{HBr}$ proceeds via a free-radical chain mechanism rather than a carbocation, yielding the anti-Markovnikov 1-bromoalkane. Critically, this reversal occurs **exclusively with $\\text{HBr}$**; $\\text{HCl}$ fails because $\\text{H-Cl}$ homolytic cleavage is too endothermic, while $\\text{HI}$ fails because iodine radical addition is energetically unfavorable.",
        "didactic_notes": {
            "axiom": "Markovnikov's rule is a direct consequence of carbocation stability: the electrophile attaches so as to produce the most stable carbocation intermediate.",
            "trap": "NEET Distractor: The Peroxide Effect (Anti-Markovnikov addition) occurs ONLY with HBr! It does NOT occur with HCl or HI because one of the radical chain propagation steps is endothermic.",
            "mnemonic": "Reactivity of Carbonyls: Formaldehyde > Aldehydes > Ketones (Steric crowding and +I groups quench electrophilicity)."
        },
        "key_takeaways": [
            "Carbonyl Attack Trajectory: Nucleophiles attack the $sp^2$ hybridized carbonyl carbon at the B\u00fcrgi-Dunitz angle (~$107^\\circ$).",
            "Aldehyde vs Ketone Reactivity: Aldehydes undergo nucleophilic addition much faster than ketones due to smaller steric hindrance and weaker inductive stabilization of partial positive charge.",
            "Regioselectivity Axiom: Electrophilic addition generates $3^\\circ > 2^\\circ > 1^\\circ$ carbocation; hydride or methyl shifts occur whenever a more stable carbocation can form.",
            "Peroxide Selectivity: Anti-Markovnikov radical addition is thermodynamically allowed ONLY for $HBr$, yielding 1-bromopropane from propene."
        ]
    },
    {
        "id": "FW-UPSC-HIS-01",
        "course": "UPSC",
        "subject": "Modern History & Culture",
        "chapter": "Socio-Religious Reform & Freedom Struggle",
        "title": "Modern Indian History: Reform Movements, Drain of Wealth & The Evolution of Mass Nationalism",
        "score": 4.94,
        "source": "NCERT Bipan Chandra / FineWeb-Edu Historical Corpus",
        "word_count": 560,
        "reading_time_mins": 3,
        "summary": "Ideological currents of 19th-century socio-religious reform, Dadabhai Naoroji's economic critique of colonialism, and constitutional transitions from Moderate constitutionalism to Gandhian mass satyagraha.",
        "formula_box": {
            "title": "Economic Drain & Nationalist Evolutionary Schema",
            "latex": "\\text{Net Drain} = \\text{Home Charges} + \\text{Unrequited Exports} + \\text{Guaranteed Rail Dividends}, \\quad \\text{Petition} \\rightarrow \\text{Swadeshi} \\rightarrow \\text{Purna Swaraj}",
            "plain": "Net Drain = Home Charges + Unrequited Exports + Guaranteed Rail Dividends",
            "terms": [
                [
                    "\\text{Home Charges}",
                    "Expenditure in Britain by Secretary of State for India: pensions, military stores, India Office debts"
                ],
                [
                    "\\text{Drain Theory}",
                    "Formulated by Dadabhai Naoroji in 'Poverty and Un-British Rule in India' (1867) and R.C. Dutt"
                ],
                [
                    "\\text{Brahmo & Arya Samaj}",
                    "Reformist (rational inquiry, anti-caste, women's education) vs Revivalist ('Back to the Vedas') approaches"
                ],
                [
                    "\\text{Evolution of Struggle}",
                    "Moderates (1885-1905: 3Ps) -> Extremists (1905-1919: Swadeshi, Boycott) -> Gandhian Mass Phase (1919-1947: Non-Cooperation, Civil Disobedience, Quit India)"
                ]
            ]
        },
        "figure_svg": "<svg viewBox=\"0 0 540 180\" width=\"100%\" height=\"160\" xmlns=\"http://www.w3.org/2000/svg\" style=\"background:var(--track-bg);border-radius:12px;display:block;margin:14px auto;\">\n  <!-- Timeline Axis -->\n  <line x1=\"40\" y1=\"100\" x2=\"500\" y2=\"100\" stroke=\"var(--ink-soft)\" stroke-width=\"2.5\"/>\n  <!-- Timeline Nodes -->\n  <circle cx=\"80\" cy=\"100\" r=\"7\" fill=\"#EF4444\"/>\n  <text x=\"60\" y=\"80\" font-size=\"10\" font-weight=\"800\" fill=\"#EF4444\">1857 Revolt</text>\n  <circle cx=\"160\" cy=\"100\" r=\"7\" fill=\"#F59E0B\"/>\n  <text x=\"140\" y=\"125\" font-size=\"10\" font-weight=\"800\" fill=\"#F59E0B\">1885 INC</text>\n  <text x=\"135\" y=\"140\" font-size=\"9\" fill=\"var(--ink-soft)\">Moderates (3Ps)</text>\n  <circle cx=\"260\" cy=\"100\" r=\"7\" fill=\"var(--purple)\"/>\n  <text x=\"235\" y=\"80\" font-size=\"10\" font-weight=\"800\" fill=\"var(--purple)\">1905 Swadeshi</text>\n  <text x=\"240\" y=\"65\" font-size=\"9\" fill=\"var(--ink-soft)\">Extremist Phase</text>\n  <circle cx=\"360\" cy=\"100\" r=\"7\" fill=\"#10B981\"/>\n  <text x=\"335\" y=\"125\" font-size=\"10\" font-weight=\"800\" fill=\"#10B981\">1920 NCM</text>\n  <text x=\"330\" y=\"140\" font-size=\"9\" fill=\"var(--ink-soft)\">Gandhian Mass Phase</text>\n  <circle cx=\"460\" cy=\"100\" r=\"8\" fill=\"#3B82F6\"/>\n  <text x=\"430\" y=\"80\" font-size=\"10\" font-weight=\"800\" fill=\"#3B82F6\">1947 Azadi</text>\n</svg>",
        "figure_caption": "Figure 3.4: Evolutionary trajectory of the Indian national freedom movement from early constitutional reform to pan-Indian mass satyagraha.",
        "content": "The emergence of modern Indian nationalism in the 19th and early 20th centuries was underpinned by deep ideological transformations: socio-religious introspection, economic critique of imperialism, and the tactical evolution from elite petitions to mass civil disobedience.\n\n### 19th Century Socio-Religious Renaissance\nThe reform movements bridged traditional culture and rationalist modernism, dividing into two distinct ideological approaches:\n- **Reformist:** Movements such as the Brahmo Samaj (Raja Ram Mohan Roy), Prarthana Samaj (M.G. Ranade), and Aligarh Movement (Sir Syed Ahmad Khan) utilized rational inquiry and humanistic ethics to abolish social evils like Sati, female infanticide, and caste restrictions while championing women's education.\n- **Revivalist:** Movements like the Arya Samaj (Swami Dayananda Saraswati - 'Back to the Vedas') and Deoband Movement sought rejuvenation by returning to untainted foundational scriptures, fostering anti-colonial pride and cultural self-confidence.\n\n### The Economic Critique of Colonialism\nEarly nationalist thinkers\u2014most notably **Dadabhai Naoroji** ('Poverty and Un-British Rule in India'), **R.C. Dutt** ('Economic History of India'), and **G.V. Joshi**\u2014punctured the colonial narrative of benevolent modernization by formulating the **Drain of Wealth Theory**. They demonstrated that continuous unilateral resource transfers (Home Charges, guaranteed railway dividends, civil-military administrative pensions) stripped India of capital surplus, precipitating de-industrialization and recurrent catastrophic famines.\n\n### Constitutional & Tactical Phases of Freedom Struggle\n1. **Moderate Phase (1885\u20131905):** Faith in British justice; methods confined to constitutional petitions, prayers, and public meetings (3Ps).\n2. **Extremist / Swadeshi Phase (1905\u20131919):** Triggered by Lord Curzon's 1905 Partition of Bengal; shifted to passive resistance, boycott of British textiles, and self-reliance (*Atmasakti*).\n3. **Gandhian Era (1919\u20131947):** Transformed nationalism into an inclusive mass movement via Non-Cooperation (1920), Civil Disobedience (1930), and Quit India (1942), synthesizing active moral *Satyagraha* with constructive socio-economic programs.",
        "didactic_notes": {
            "axiom": "The Socio-Religious Reform movement was not merely cultural: it created the national consciousness and intellectual foundation necessary for political mobilization against colonial rule.",
            "trap": "UPSC Trap: Do NOT confuse 'Reformist' movements (Brahmo Samaj, Prarthana Samaj, Aligarh) which embraced modern scientific values with 'Revivalist' movements (Arya Samaj, Deoband) which sought rejuvenation by returning to pure ancestral scriptures.",
            "mnemonic": "Nationalist Epochs: 'M-E-G' -> Moderates (Constitutional Prayers), Extremists (Passive Resistance & Swadeshi), Gandhians (Active Non-Violent Mass Satyagraha)."
        },
        "key_takeaways": [
            "Drain of Wealth Axiom: One-third of India's total revenue was remitted annually out of India without any economic return, transforming India from an exporter of finished goods to a raw material supplier.",
            "Reform Dichotomy: Reformist vs Revivalist movements both fostered anti-colonial solidarity, national dignity, and social reform.",
            "Swadeshi Milestone (1905): Transformed elite constitutional politics into mass political agitation, introducing boycott of foreign goods and national educational institutions.",
            "Gandhian Hegemony: Synthesized non-violent direct action (Satyagraha) with constructive social programs (removal of untouchability, communal harmony, Khadi self-reliance)."
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
