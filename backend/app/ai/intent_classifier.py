"""
Deterministic Intent Classifier
Platform Upgrade v3.0 — Hardened Offline AI Assistant
Keyword + Regex + Fuzzy Distance Matching with Zero Guessing
"""
import re
from difflib import SequenceMatcher
from typing import Tuple, Optional

INTENT_ANALYZE_MISTAKES = "ANALYZE_MISTAKES"
INTENT_EXPLAIN_ROADMAP = "EXPLAIN_ROADMAP"
INTENT_STRATEGY_TIPS = "STRATEGY_TIPS"
INTENT_EXPLAIN_CONCEPT = "EXPLAIN_CONCEPT"
INTENT_GREETING = "GREETING"
INTENT_OFF_TOPIC = "OFF_TOPIC"
INTENT_UNKNOWN = "UNKNOWN"

INTENT_KEYWORDS = {
    INTENT_GREETING: [
        "hi", "hello", "hey", "namaste", "good morning", "good evening", "good afternoon",
        "sup", "howdy", "greetings", "yo"
    ],
    INTENT_ANALYZE_MISTAKES: [
        "mistake", "error", "wrong", "failed", "incorrect", "postmortem",
        "analyze my mistakes", "why did i get wrong", "what did i miss", "weakness",
        "calculation error", "conceptual gap", "distractor", "past test", "last test",
        "test review", "retest", "review my test", "performance correction", "my score"
    ],
    INTENT_EXPLAIN_ROADMAP: [
        "roadmap", "plan", "milestone", "what next", "why this topic", "prerequisite",
        "explain my roadmap", "study schedule", "learning path", "next action",
        "why study", "curriculum sequence"
    ],
    INTENT_STRATEGY_TIPS: [
        "exam speed", "exam strategy", "time management", "exam tip", "exam tips",
        "how to improve score", "negative marking", "jee strategy", "neet strategy", "upsc strategy",
        "speed and accuracy", "score 99 percentile", "score 680", "pacing strategy"
    ],
    INTENT_EXPLAIN_CONCEPT: [
        "explain", "what is", "how does", "formula", "definition", "concept",
        "deriv", "law of", "theorem", "difference between", "why does", "solve"
    ]
}

INTENT_PATTERNS = {
    INTENT_GREETING: re.compile(r"^(hi|hello|hey|namaste|yo|good\s+(morning|afternoon|evening)|howdy)\b", re.IGNORECASE),
    INTENT_ANALYZE_MISTAKES: re.compile(r"\b(mistake|error|wrong|incorrect|fail|analysis|postmortem|past test|last test|test review|retest|performance correction)\b", re.IGNORECASE),
    INTENT_EXPLAIN_ROADMAP: re.compile(r"\b(roadmap|milestone|schedule|path|next step|prerequisite|why should i)\b", re.IGNORECASE),
    INTENT_STRATEGY_TIPS: re.compile(r"\b(speed|accuracy|tip|strategy|time|pace|negative mark|score)\b", re.IGNORECASE),
    INTENT_EXPLAIN_CONCEPT: re.compile(r"\b(explain|what is|how do|formula|define|definition|concept)\b", re.IGNORECASE)
}

# Recognized academic syllabus concepts/topics for JEE, NEET, UPSC & Full STEM Curriculum
SYLLABUS_TOPIC_KEYWORDS = {
    # Physics & Mechanics
    "mechanics", "kinematics", "dynamics", "shm", "oscillations", "harmonic", "optics", "wave",
    "thermodynamics", "electrostatics", "magnetism", "electromagnetism", "induction", "gravitation",
    "work energy", "rotation", "rotational", "inertia", "torque", "lens", "refraction", "reflection",
    "doppler", "fluid", "bernoulli", "viscosity", "semiconductor", "quantum", "photoelectric",
    "nuclear", "atomic", "relativity", "sound", "friction", "circular", "projectile", "newton",
    # Chemistry
    "buffer", "ionic", "equilibrium", "organic", "inorganic", "goc", "reaction", "acid", "base",
    "polymer", "biomolecule", "periodic", "bonding", "hybridization", "coordination", "electrochemistry",
    "kinetics", "redox", "hydrocarbon", "aldehyde", "ketone", "thermo", "stoichiometry",
    # Mathematics & CS
    "calculus", "limits", "integrals", "integration", "derivative", "differentiation", "matrices",
    "determinants", "vectors", "probability", "algebra", "trigonometry", "complex number", "geometry",
    "conic", "ellipse", "parabola", "hyperbola", "sequence", "series", "binomial", "differential",
    "statistics", "algorithm", "programming", "code", "python", "data structure", "logic", "binary",
    # Biology & Medicine (NEET)
    "genetics", "cardiac", "heart", "cell", "meiosis", "mitosis", "photosynthesis", "respiration",
    "botany", "zoology", "circulation", "endocrine", "ecology", "evolution", "morphology", "anatomy",
    "dna", "rna", "protein", "enzyme", "immunity", "nervous", "reproduction", "plant", "animal",
    # UPSC & General Knowledge / Humanities
    "basic structure", "constitution", "polity", "economy", "fiscal", "inflation", "judiciary",
    "fundamental rights", "dpsp", "preamble", "geography", "monsoon", "ethics", "history", "ancient",
    "medieval", "modern history", "freedom struggle", "parliament", "president", "supreme court",
    "gdp", "monetary policy", "rbi", "budget", "taxation", "biodiversity", "environment", "climate",
    "international relations", "treaty", "governance", "agriculture", "trade", "culture", "heritage"
}

# Known purely casual/non-academic chit-chat that isn't academic
CASUAL_OFF_TOPIC_ENTITIES = {
    "apple", "banana", "mango", "fruit", "batman", "superman", "ironman", "movie", "song",
    "joke", "pizza", "burger", "messi", "ronaldo", "shoes", "clothes", "girlfriend", "boyfriend"
}


class IntentClassifier:
    """
    Two-stage intent classifier:
    1. Fast regex & keyword inclusion.
    2. Fuzzy similarity matching via SequenceMatcher for typos.
    3. Strict UNKNOWN fallback when confidence < 0.60.
    """

    @classmethod
    def sanitize_input(cls, user_text: str) -> str:
        """Strip dangerous characters, prompt injection patterns, and limit length to 500 chars."""
        if not user_text:
            return ""
        # Remove prompt injection delimiters
        cleaned = re.sub(r"[<>{}\[\]\\]", " ", user_text)
        # Collapse whitespace
        cleaned = " ".join(cleaned.split())
        return cleaned[:500]

    @classmethod
    def is_syllabus_topic(cls, term: str) -> bool:
        """Returns True if term contains or matches any recognized competitive exam keyword."""
        if not term:
            return False
        clean_term = term.lower().strip()
        for kw in SYLLABUS_TOPIC_KEYWORDS:
            if kw in clean_term or clean_term in kw:
                return True
        return False

    @classmethod
    def classify(cls, user_text: str) -> Tuple[str, float, Optional[str]]:
        """
        Classifies user prompt into (intent, confidence, matched_topic_or_concept).
        Guarantees:
        1. Pure greetings ('hi', 'hello') return INTENT_GREETING.
        2. Casual/out-of-syllabus queries ('what is apple', 'who is batman') return INTENT_OFF_TOPIC.
        3. Real academic queries return INTENT_EXPLAIN_CONCEPT, INTENT_ANALYZE_MISTAKES, etc.
        """
        cleaned = cls.sanitize_input(user_text).lower()
        if not cleaned or len(cleaned) < 2:
            return INTENT_UNKNOWN, 0.0, None

        words = [w.strip("?,.!:;") for w in cleaned.split() if w.strip("?,.!:;")]

        # Stage 0: Pure greeting check
        greeting_tokens = {"hi", "hello", "hey", "namaste", "yo", "sup", "howdy", "heya"}
        if len(words) <= 3 and any(w in greeting_tokens for w in words):
            # Check if it has a substantive query beyond greeting
            substantive = [w for w in words if w not in greeting_tokens and w not in {"there", "sir", "mentor", "bro", "coach", "mr", "ji"}]
            if not substantive:
                return INTENT_GREETING, 0.99, None

        # Stage 0b: Check for explicit off-topic entities
        for off in CASUAL_OFF_TOPIC_ENTITIES:
            if re.search(rf"\b{re.escape(off)}\b", cleaned):
                # Verify if it's not actually an in-syllabus topic containing the word
                if not cls.is_syllabus_topic(cleaned):
                    return INTENT_OFF_TOPIC, 0.95, off

        # Stage 1: Exact keyword / substring match
        # Check mistake, roadmap, and strategy tips first
        for intent in [INTENT_ANALYZE_MISTAKES, INTENT_EXPLAIN_ROADMAP, INTENT_STRATEGY_TIPS]:
            for kw in INTENT_KEYWORDS[intent]:
                if kw in cleaned:
                    return intent, 0.95, cls._extract_topic_hint(cleaned)

        # Stage 2: Concept inquiry check
        for kw in INTENT_KEYWORDS[INTENT_EXPLAIN_CONCEPT]:
            if kw in cleaned:
                topic_hint = cls._extract_topic_hint(cleaned)
                # Only flag as off-topic if it matches an explicit non-academic casual entity
                if topic_hint and any(off in topic_hint for off in CASUAL_OFF_TOPIC_ENTITIES):
                    return INTENT_OFF_TOPIC, 0.95, topic_hint
                return INTENT_EXPLAIN_CONCEPT, 0.90, topic_hint

        # Stage 3: Regex pattern match
        for intent, pattern in INTENT_PATTERNS.items():
            if pattern.search(cleaned):
                hint = cls._extract_topic_hint(cleaned)
                if intent == INTENT_EXPLAIN_CONCEPT and hint:
                    if any(off in hint for off in CASUAL_OFF_TOPIC_ENTITIES):
                        return INTENT_OFF_TOPIC, 0.90, hint
                return intent, 0.85, hint

        # Stage 4: Fuzzy similarity matching for typos
        best_intent = INTENT_UNKNOWN
        best_score = 0.0

        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                kw_words = kw.split()
                # Check token-level similarity
                for w in words:
                    for kw_w in kw_words:
                        sim = SequenceMatcher(None, w, kw_w).ratio()
                        if sim > best_score:
                            best_score = sim
                            best_intent = intent

        # Threshold check: require >= 0.75 similarity for fuzzy match
        if best_score >= 0.75:
            hint = cls._extract_topic_hint(cleaned)
            if best_intent == INTENT_EXPLAIN_CONCEPT and hint and any(off in hint for off in CASUAL_OFF_TOPIC_ENTITIES):
                return INTENT_OFF_TOPIC, round(best_score, 2), hint
            return best_intent, round(best_score, 2), hint

        return INTENT_UNKNOWN, 0.0, None

    @classmethod
    def _extract_topic_hint(cls, text: str) -> Optional[str]:
        """Extracts potential concept or subject name from query text."""
        # 1. Check known syllabus topics first
        for t in sorted(SYLLABUS_TOPIC_KEYWORDS, key=len, reverse=True):
            if re.search(rf"\b{re.escape(t)}\b", text):
                return t

        # 2. Check casual off-topic entities
        for off in sorted(CASUAL_OFF_TOPIC_ENTITIES, key=len, reverse=True):
            if re.search(rf"\b{re.escape(off)}\b", text):
                return off

        # 3. Check prefixes
        for prefix in ["explain", "what is", "tell me about", "concept of", "teach me"]:
            if prefix in text:
                candidate = text.split(prefix, 1)[-1].strip(" ?:.,")
                if candidate:
                    return candidate
        return None
