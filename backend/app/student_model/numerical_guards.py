"""
Numerical Safeguards & Floating-Point Stability Module
======================================================
Strict Programmatic Guards for Zero-Bug Production Stability:
  - Probability clamping: P in [10^-7, 1.0 - 10^-7]
  - Denominator safety: max(denominator, 10^-7)
  - Logarithm safety: ln(max(x, 10^-7))
  - Exp overflow/underflow clamping
"""
import math
from typing import Sequence, Union
import numpy as np

EPSILON: float = 1e-7
MIN_PROBABILITY: float = 1e-7
MAX_PROBABILITY: float = 1.0 - 1e-7

def safe_clamp_prob(p: float, min_p: float = MIN_PROBABILITY, max_p: float = MAX_PROBABILITY) -> float:
    """Clamps probability value strictly within [10^-7, 1.0 - 10^-7]."""
    try:
        val = float(p)
        if math.isnan(val):
            return 0.5
        return min(max(val, min_p), max_p)
    except (TypeError, ValueError):
        return 0.5

def safe_div(numerator: float, denominator: float, eps: float = EPSILON) -> float:
    """Guarantees safe division avoiding ZeroDivisionError or floating overflow."""
    try:
        num = float(numerator)
        denom = float(denominator)
        if math.isnan(num):
            return 0.0
        if math.isnan(denom) or abs(denom) < eps:
            sign = 1.0 if denom >= 0 else -1.0
            denom = sign * eps
        return num / denom
    except (TypeError, ValueError, OverflowError):
        return 0.0

def safe_log(x: float, eps: float = EPSILON) -> float:
    """Guarantees safe natural logarithm calculation: ln(max(x, 10^-7))."""
    try:
        val = float(x)
        if math.isnan(val) or val <= 0.0:
            return math.log(eps)
        return math.log(max(val, eps))
    except (TypeError, ValueError):
        return math.log(eps)

def safe_exp(z: float, min_z: float = -25.0, max_z: float = 25.0) -> float:
    """Guarantees safe exponential calculation avoiding overflow/underflow."""
    try:
        val = float(z)
        if math.isnan(val):
            return 1.0
        clamped_z = min(max(val, min_z), max_z)
        return math.exp(clamped_z)
    except (TypeError, ValueError):
        return 1.0

def safe_softmax(logits: Union[Sequence[float], np.ndarray], temperature: float = 1.0) -> np.ndarray:
    """Numerically stable softmax with safe denominator and temperature scaling."""
    arr = np.asarray(logits, dtype=np.float64)
    if arr.size == 0:
        return np.array([], dtype=np.float64)
    temp = max(float(temperature), EPSILON)
    scaled = arr / temp
    # Subtract max for numerical stability
    shifted = scaled - np.max(scaled)
    exp_vals = np.exp(np.clip(shifted, -25.0, 25.0))
    sum_exp = np.sum(exp_vals)
    denom = max(float(sum_exp), EPSILON)
    probs = exp_vals / denom
    return np.clip(probs, MIN_PROBABILITY, MAX_PROBABILITY)


class OutputNumericalGuard:
    """
    Deterministic Verification Gate:
    Enforces validation checks on LLM-generated explanations and technical outputs
    to ensure strict numerical, dimensional, and logical consistency.
    """
    import re
    ARITHMETIC_PATTERN = re.compile(
        r'(?<![A-Za-z0-9_])(\-?\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\-?\d+(?:\.\d+)?)\s*=\s*(\-?\d+(?:\.\d+)?)(?![A-Za-z0-9_])'
    )
    INVERTED_UNITS_PATTERNS = [
        (re.compile(r'\b(?:m/s\^2|m/s2)\s*(?:for\s+velocity|is\s+the\s+speed)', re.I), "Velocity cannot have units of acceleration (m/s^2)."),
        (re.compile(r'\b(?:m/s)\s*(?:for\s+acceleration|is\s+the\s+acceleration)', re.I), "Acceleration cannot have units of speed (m/s)."),
        (re.compile(r'\bN\s*\*\s*s\s*(?:for\s+force|is\s+the\s+force)', re.I), "Force cannot have units of impulse (N*s)."),
        (re.compile(r'\bJ\s*/\s*s\s*(?:for\s+energy|is\s+the\s+energy|is\s+the\s+work)', re.I), "Work/Energy cannot have units of power (J/s).")
    ]
    ANSWER_LEAK_REGEX = re.compile(
        r'\b(?:(?:the\s+)?correct\s+(?:option|answer|choice)\s+is|correct\s+is\s+option|choose\s+option|answer\s+is)\s*(?:option\s+)?[:=]?\s*([A-D])\b',
        re.I
    )


    @classmethod
    def verify_arithmetic_expressions(cls, text: str, tolerance: float = 1e-3) -> Tuple[bool, List[str]]:
        """
        Extracts explicit arithmetic statements like '15 / 3 = 5' or '4 * 12 = 48'
        and verifies their numerical correctness.
        """
        import re
        inconsistencies = []
        for match in cls.ARITHMETIC_PATTERN.finditer(text):
            try:
                n1 = float(match.group(1))
                op = match.group(2)
                n2 = float(match.group(3))
                stated = float(match.group(4))

                expected = None
                if op == '+':
                    expected = n1 + n2
                elif op == '-':
                    expected = n1 - n2
                elif op == '*':
                    expected = n1 * n2
                elif op == '/':
                    if abs(n2) < 1e-9:
                        inconsistencies.append(f"Division by zero in statement: {match.group(0)}")
                        continue
                    expected = n1 / n2

                if expected is not None and abs(expected - stated) > tolerance:
                    inconsistencies.append(
                        f"Numerical mismatch: '{match.group(0)}' (Calculated expected: {expected:.4g}, stated: {stated:.4g})"
                    )
            except (ValueError, OverflowError):
                continue

        return (len(inconsistencies) == 0, inconsistencies)

    @classmethod
    def verify_unit_consistency(cls, text: str) -> Tuple[bool, List[str]]:
        """
        Detects obvious inverted SI units and dimensional contradictions in physics explanations.
        """
        violations = []
        for pattern, note in cls.INVERTED_UNITS_PATTERNS:
            if pattern.search(text):
                violations.append(note)
        return (len(violations) == 0, violations)

    @classmethod
    def validate_explanation_invariants(
        cls,
        text: str,
        mode: str = "socratic"
    ) -> Tuple[bool, List[str]]:
        """
        Guarantees that in Socratic and Scaffolding modes, correct option letters
        are never prematurely leaked to the student.
        """
        flags = []
        if mode.lower() in ["socratic", "scaffolding"]:
            match = cls.ANSWER_LEAK_REGEX.search(text)
            if match:
                flags.append(f"Answer leakage detected in {mode} mode: Option {match.group(1)}")
        return (len(flags) == 0, flags)

    @classmethod
    def guard_llm_output(cls, text: str, mode: str = "socratic") -> Dict[str, Any]:
        """
        Runs comprehensive deterministic verification over LLM response text.
        Returns a verification report with boolean pass status and detected issues.
        """
        math_ok, math_issues = cls.verify_arithmetic_expressions(text)
        units_ok, unit_issues = cls.verify_unit_consistency(text)
        leak_ok, leak_issues = cls.validate_explanation_invariants(text, mode=mode)

        all_issues = math_issues + unit_issues + leak_issues
        return {
            "passed": len(all_issues) == 0,
            "math_consistent": math_ok,
            "units_consistent": units_ok,
            "leakage_free": leak_ok,
            "issues": all_issues
        }

