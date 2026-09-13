"""
Formal Academic Protocol Sets & Domain Boundary Engine for APEX AI Cognitive Mentor.
Defines domain-specific epistemological guardrails, LaTeX formatting invariants,
and canonical problem-solving scaffolds for JEE, NEET, UPSC, and GENERAL_STEM.
"""
from typing import Dict, Any, List, Optional
import re


class BaseDomainProtocol:
    """Base academic protocol defining tone, mathematical standards, and pedagogical rules."""
    name: str = "BASE"
    display_title: str = "Academic Mentor"
    allowed_subjects: List[str] = []
    latex_required: bool = True

    def get_system_instructions(self, is_solve: bool = False) -> str:
        raise NotImplementedError

    def get_solve_structure(self) -> str:
        return (
            "PROBLEM SOLVING PROTOCOL (Strictly follow this 5-part structure):\n"
            "1. 🎯 **Given Data & Target Objective**: Explicitly list all given numerical/algebraic parameters with standard SI units, and define the exact target variable to find.\n"
            "2. 📐 **Governing Principles & Canonical Formulas**: State the fundamental law or theorem being applied, rendered in clear LaTeX ($$...$$).\n"
            "3. ⚡ **Step-by-Step Analytical Derivation**: Perform clean algebraic manipulations before plugging in numbers. Show intermediate cancellation steps clearly.\n"
            "4. 💡 **Final Value & Sanity Check**: Present the final simplified answer (boxed or bolded) with correct units. Provide a 1-line physical sense check (e.g. dimensional verification or limiting behavior).\n"
            "5. ⚠️ **Competitive Exam Trap Radar**: Highlight the exact trap, sign mistake, or unit confusion that students frequently fall into for this specific question type."
        )


class JEEProtocol(BaseDomainProtocol):
    """Protocol for Joint Entrance Examination (Main & Advanced) — Physics, Chemistry, Mathematics."""
    name = "JEE"
    display_title = "IIT-JEE Engineering Mentor"
    allowed_subjects = ["Physics", "Chemistry", "Mathematics", "Mechanics", "Calculus", "Electrodynamics", "Thermodynamics", "Optics", "Modern Physics", "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Algebra", "Coordinate Geometry", "Vectors"]
    latex_required = True

    def get_system_instructions(self, is_solve: bool = False) -> str:
        base = (
            "DOMAIN PROTOCOL: IIT-JEE (Physics, Chemistry, Mathematics).\n"
            "- Mathematical Rigor: High analytical depth. Never use hand-waving arguments when a calculus or vector derivation exists.\n"
            "- Formatting Invariant: All equations, formulas, coordinates, and algebraic steps MUST be formatted in LaTeX ($...$ inline, $$...$$ block).\n"
            "- Vector & Sign Conventions: Strictly specify reference frames and coordinate directions for mechanics and electrodynamics.\n"
            "- Physical Chemistry: State equilibrium constants, gas laws, and thermodynamic state functions explicitly with units.\n"
            "- Organic Chemistry: Emphasize reaction mechanisms, carbocation/carbanion stability, steric effects, and stereochemistry.\n"
            "- Mathematics: Prioritize symmetry arguments, King's rule for integrals, matrix/determinant properties, and coordinate transformations."
        )
        if is_solve:
            base += "\n\n" + self.get_solve_structure()
        return base


class NEETProtocol(BaseDomainProtocol):
    """Protocol for NEET-UG Medical Entrance — Physics, Chemistry, Biology (Botany & Zoology)."""
    name = "NEET"
    display_title = "NEET Medical Sciences Mentor"
    allowed_subjects = ["Physics", "Chemistry", "Biology", "Botany", "Zoology", "Genetics", "Physiology", "Ecology", "Biochemistry", "Organic Chemistry", "Physical Chemistry", "Mechanics", "Optics"]
    latex_required = True

    def get_system_instructions(self, is_solve: bool = False) -> str:
        base = (
            "DOMAIN PROTOCOL: NEET-UG (Biology, Physics, Chemistry).\n"
            "- NCERT Alignment: Align strictly with canonical NCERT terminology, physiological pathways, and anatomical classifications.\n"
            "- Biology First Principles: Explain biochemical energetics (ATP, Krebs cycle, Calvin cycle) and genetic inheritance (Mendelian ratios, DNA replication) with utmost precision.\n"
            "- Physics & Chemistry in Medicine: Relate physical principles (Poiseuille's law, osmotic pressure, radioactive half-life, optics of the eye) directly to biological systems when helpful.\n"
            "- Numerical Pacing: Emphasize rapid calculation shortcuts, mental arithmetic approximations, and formula memory aids for timed 45-second questions."
        )
        if is_solve:
            base += "\n\n" + self.get_solve_structure()
        return base


class UPSCProtocol(BaseDomainProtocol):
    """Protocol for UPSC Civil Services Examination (IAS/IPS) — General Studies & Aptitude."""
    name = "UPSC"
    display_title = "UPSC Civil Services Academic Mentor"
    allowed_subjects = ["Polity", "Governance", "Economy", "History", "Geography", "Environment", "Ecology", "Science & Tech", "International Relations", "Ethics", "Current Affairs", "CSAT"]
    latex_required = False

    def get_system_instructions(self, is_solve: bool = False) -> str:
        base = (
            "DOMAIN PROTOCOL: UPSC Civil Services Examination (General Studies I, II, III, IV & CSAT).\n"
            "- Multi-Dimensional Analysis: Always analyze issues through 360-degree lenses: Constitutional/Legal, Socio-Economic, Environmental, Administrative, and Geopolitical.\n"
            "- Constitutional Grounding: Cite specific Articles, Amendments, Landmark Supreme Court Judgments, or Committee Recommendations where applicable.\n"
            "- Balanced Perspectives: Present objective pros and cons (the 'Way Forward' approach) rather than subjective partisan opinions.\n"
            "- GS-3 Science & Tech: Explain emerging tech (AI, quantum computing, space exploration, CRISPR, renewables) in accessible, policy-impact terms."
        )
        if is_solve:
            base += (
                "\n\nCSAT / QUANTITATIVE SOLVING PROTOCOL:\n"
                "1. 🎯 **Given Conditions**: Clearly state all premises and constraints.\n"
                "2. 📐 **Logical / Mathematical Framework**: Formulate the underlying logic, ratio, or probability relation.\n"
                "3. ⚡ **Step-by-Step Resolution**: Walk through deductions or calculations concisely.\n"
                "4. 💡 **Conclusion & Verification**: State the unambiguous answer.\n"
                "5. ⚠️ **Comprehension / Logical Traps**: Point out edge conditions (e.g. leap years, double counting, ambiguous wording)."
            )
        return base


class GeneralSTEMProtocol(BaseDomainProtocol):
    """Protocol for General STEM disciplines (Computer Science, Advanced Physics, Higher Math, Engineering)."""
    name = "GENERAL_STEM"
    display_title = "General STEM & Scientific Research Mentor"
    allowed_subjects = ["Computer Science", "Algorithms", "Linear Algebra", "Calculus", "Quantum Mechanics", "Machine Learning", "Data Structures", "Astrophysics", "Engineering", "General Physics", "Chemistry"]
    latex_required = True

    def get_system_instructions(self, is_solve: bool = False) -> str:
        base = (
            "DOMAIN PROTOCOL: GENERAL STEM & ADVANCED COMPUTING.\n"
            "- First Principles: Ground all explanations in axiomatic definitions, mathematical theorems, or algorithmic invariants.\n"
            "- Mathematical Clarity: Use standard LaTeX ($...$, $$...$$) for matrices, operators, asymptotic notations ($O, \\Omega, \\Theta$), and proofs.\n"
            "- Engineering Pragmatism: Connect theoretical results (e.g. Fourier transforms, gradient descent, thermodynamic cycles) to real-world software or hardware implementations."
        )
        if is_solve:
            base += "\n\n" + self.get_solve_structure()
        return base


class DomainProtocolEngine:
    """
    Central router for academic domain protocols and boundary checking.
    Distinguishes between:
    - IN_SYLLABUS: Exactly on target for the student's exam track.
    - IN_DOMAIN_ADVANCED: Advanced STEM topic within the broader subject domain (e.g. Quantum Tunneling for JEE).
    - CROSS_DISCIPLINARY: Legitimate academic topic from another exam track (e.g. JEE student asking about UPSC Polity or Biology).
    - CASUAL_OFF_TOPIC: Non-academic chit-chat (movies, sports gossip, celebrities, gaming).
    """
    _PROTOCOLS: Dict[str, BaseDomainProtocol] = {
        "JEE": JEEProtocol(),
        "NEET": NEETProtocol(),
        "UPSC": UPSCProtocol(),
        "GENERAL_STEM": GeneralSTEMProtocol(),
        "STEM": GeneralSTEMProtocol(),
    }

    # Subject Keywords for Domain Mapping
    _JEE_KEYWORDS = {
        "physics", "chemistry", "math", "mathematics", "calculus", "derivative", "integral",
        "mechanics", "rotational", "inertia", "torque", "kinematics", "projectile", "shm",
        "oscillation", "thermodynamics", "entropy", "carnot", "electromagnetism", "flux",
        "lenz", "faraday", "induction", "optics", "refraction", "interference", "diffraction",
        "quantum", "photoelectric", "bohr", "organic", "inorganic", "isomerism", "carbocation",
        "aromatic", "sn1", "sn2", "coordination", "matrix", "determinant", "probability",
        "vector", "complex numbers", "parabola", "hyperbola", "ellipse", "trigonometry",
        "gravity", "gravitation", "gravitational", "kepler", "orbit", "escape velocity", "planetary"
    }

    _NEET_KEYWORDS = {
        "biology", "botany", "zoology", "photosynthesis", "cell", "mitosis", "meiosis",
        "dna", "rna", "genetics", "mendel", "ecology", "ecosystem", "respiration", "krebs",
        "calvin", "circulatory", "nephron", "neuron", "hormone", "endocrine", "reproduction",
        "embryo", "plant kingdom", "animal kingdom", "taxonomy", "evolution", "hardy weinberg"
    }

    _UPSC_KEYWORDS = {
        "polity", "constitution", "article", "preamble", "fundamental rights", "dpsp",
        "parliament", "judiciary", "supreme court", "governance", "economy", "gdp", "fiscal",
        "monetary", "rbi", "inflation", "history", "mughal", "british raj", "freedom struggle",
        "geography", "monsoon", "tectonics", "environment", "biodiversity", "treaty",
        "ethics", "ias", "ips", "civil services", "federalism", "lok sabha", "rajya sabha"
    }

    _ADVANCED_STEM_KEYWORDS = {
        "quantum tunneling", "schrodinger", "dirac", "special relativity", "general relativity",
        "lorentz transformation", "eigenvalue", "eigenvector", "tensor", "fourier transform",
        "laplace", "neural network", "machine learning", "backpropagation", "gradient descent",
        "algorithm", "binary search", "graph theory", "dijkstra", "compiler", "operating system",
        "black hole", "string theory", "quantum electrodynamics", "topology", "manifold"
    }

    _CASUAL_OFF_TOPIC_KEYWORDS = {
        "apple", "banana", "mango", "fruit", "pizza", "burger", "batman", "superman", "ironman",
        "movie", "actor", "actress", "celebrity", "gossip", "netflix", "video game", "minecraft",
        "fortnite", "cricket match", "football match", "ipl", "fifa", "dating", "girlfriend",
        "boyfriend", "song lyrics", "taylor swift", "marvel", "dc comics"
    }

    _SOLVE_KEYWORDS = {
        "solve", "calculate", "find the value", "determine", "evaluate", "derive",
        "what is the value of", "find i", "find v", "find force", "find acceleration",
        "find momentum", "find energy", "find velocity", "find torque", "find probability"
    }

    @classmethod
    def get_protocol(cls, exam: str) -> BaseDomainProtocol:
        key = (exam or "JEE").upper().strip()
        return cls._PROTOCOLS.get(key, cls._PROTOCOLS["JEE"])

    @classmethod
    def detect_solve_intent(cls, prompt: str) -> bool:
        """Determines if the student prompt is asking to solve a concrete numerical/formulaic problem."""
        p_lower = prompt.lower()
        # Direct solve keywords
        if any(w in p_lower for w in cls._SOLVE_KEYWORDS):
            return True
        # Presence of numbers with standard units: e.g. 5 kg, 2 m/s, 10 N, 0.5 rad/s
        unit_pattern = re.search(r'\d+(\.\d+)?\s*(kg|g|m|cm|mm|s|ms|m/s|m/s\^2|n|j|w|v|a|ohm|hz|rad|deg|mol)', p_lower)
        if unit_pattern:
            return True
        # Mathematical equation with = sign and variable
        if re.search(r'[a-zA-Z]\s*=\s*\d+', prompt) or ("=" in prompt and any(c.isdigit() for c in prompt)):
            return True
        return False

    @classmethod
    def classify_query_domain(cls, prompt: str, target_exam: str = "JEE") -> Dict[str, Any]:
        """
        Classifies query against academic domains and syllabus boundaries.
        Returns dict with:
        - category: IN_SYLLABUS | IN_DOMAIN_ADVANCED | CROSS_DISCIPLINARY | CASUAL_OFF_TOPIC
        - domain: JEE | NEET | UPSC | GENERAL_STEM
        - is_solve: bool
        - detected_subject: str
        - advisory_note: Optional guidance note
        """
        p_lower = prompt.lower().strip()
        target_exam = (target_exam or "JEE").upper()
        is_solve = cls.detect_solve_intent(prompt)

        # 1. Pure Casual Off-Topic check
        is_casual = any(w in p_lower for w in cls._CASUAL_OFF_TOPIC_KEYWORDS)
        has_academic_term = any(w in p_lower for w in cls._JEE_KEYWORDS | cls._NEET_KEYWORDS | cls._UPSC_KEYWORDS | cls._ADVANCED_STEM_KEYWORDS)
        if is_casual and not has_academic_term:
            return {
                "category": "CASUAL_OFF_TOPIC",
                "domain": "OFF_TOPIC",
                "is_solve": False,
                "detected_subject": "General Entertainment",
                "advisory_note": "Intercepted non-academic chit-chat."
            }

        # 2. Check Advanced STEM (relativity, quantum mechanics, CS, machine learning)
        has_adv_stem = any(w in p_lower for w in cls._ADVANCED_STEM_KEYWORDS)
        if has_adv_stem:
            return {
                "category": "IN_DOMAIN_ADVANCED",
                "domain": "GENERAL_STEM",
                "is_solve": is_solve,
                "detected_subject": "Advanced STEM / Theoretical Science",
                "advisory_note": (
                    f"Advanced collegiate STEM topic. While this extends beyond the standard {target_exam} syllabus, "
                    "full mathematical derivation and first-principles reasoning are provided."
                )
            }

        # 3. Check Domain Keyword Overlaps
        jee_hits = sum(1 for w in cls._JEE_KEYWORDS if w in p_lower)
        neet_hits = sum(1 for w in cls._NEET_KEYWORDS if w in p_lower)
        upsc_hits = sum(1 for w in cls._UPSC_KEYWORDS if w in p_lower)

        # Map target exam
        if target_exam == "JEE":
            if jee_hits > 0 or (neet_hits == 0 and upsc_hits == 0):
                return {
                    "category": "IN_SYLLABUS",
                    "domain": "JEE",
                    "is_solve": is_solve,
                    "detected_subject": "Physics / Chemistry / Mathematics",
                    "advisory_note": None
                }
            elif neet_hits > 0:
                return {
                    "category": "CROSS_DISCIPLINARY",
                    "domain": "NEET",
                    "is_solve": is_solve,
                    "detected_subject": "Biology & Life Sciences",
                    "advisory_note": "Note: You are currently enrolled in IIT-JEE. Biology is a medical entrance topic, but here is the accurate scientific explanation:"
                }
            elif upsc_hits > 0:
                return {
                    "category": "CROSS_DISCIPLINARY",
                    "domain": "UPSC",
                    "is_solve": is_solve,
                    "detected_subject": "General Studies / Polity / Economy",
                    "advisory_note": "Note: You are currently enrolled in IIT-JEE. Here is the analytical explanation from General Studies:"
                }

        elif target_exam == "NEET":
            if neet_hits > 0 or jee_hits > 0:
                return {
                    "category": "IN_SYLLABUS",
                    "domain": "NEET",
                    "is_solve": is_solve,
                    "detected_subject": "Biology / Physics / Chemistry",
                    "advisory_note": None
                }
            elif upsc_hits > 0:
                return {
                    "category": "CROSS_DISCIPLINARY",
                    "domain": "UPSC",
                    "is_solve": is_solve,
                    "detected_subject": "General Studies / Polity / Economy",
                    "advisory_note": "Note: You are currently enrolled in NEET-UG Medical. Here is the analytical explanation from General Studies:"
                }

        elif target_exam == "UPSC":
            if upsc_hits > 0 or neet_hits > 0 or jee_hits > 0:
                return {
                    "category": "IN_SYLLABUS",
                    "domain": "UPSC",
                    "is_solve": is_solve,
                    "detected_subject": "General Studies / Science & Tech",
                    "advisory_note": None
                }

        # Default fallback: Treat as in-syllabus for the student's exam
        return {
            "category": "IN_SYLLABUS",
            "domain": target_exam,
            "is_solve": is_solve,
            "detected_subject": "Academic Curriculum",
            "advisory_note": None
        }
