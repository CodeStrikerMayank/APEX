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
