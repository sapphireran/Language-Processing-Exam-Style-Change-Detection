"""Distances between two spans: register L1, function-word cosine, char-3, Delta."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

from .features import RegisterVector, SpanFeatures, extract_span


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / math.sqrt(na * nb)


def cosine_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return 1.0 - cosine(a, b)


def sparse_cosine(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    if not a or not b:
        return 0.0
    keys = set(a) | set(b)
    va = [a.get(k, 0.0) for k in keys]
    vb = [b.get(k, 0.0) for k in keys]
    return cosine(va, vb)


def sparse_cosine_distance(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    return 1.0 - sparse_cosine(a, b)


def burrows_delta(a: Sequence[float], b: Sequence[float], sigma: Sequence[float] | None = None) -> float:
    """Manhattan distance of z-scored function-word counts.

    Intra-document: if ``sigma`` is omitted we use a floor so a zero-variance
    word does not explode. This is the exam-card Delta, not a corpus Delta.
    """
    if sigma is None:
        sigma = [1.0] * len(a)
    total = 0.0
    n = 0
    for x, y, s in zip(a, b, sigma):
        width = s if s > 1e-6 else 1.0
        total += abs((x - y) / width)
        n += 1
    return total / n if n else 0.0


def register_l1(a: RegisterVector, b: RegisterVector) -> float:
    return a.l1(b)


def span_channels(left: SpanFeatures, right: SpanFeatures) -> dict[str, float]:
    """Four named distances used by the ensemble and the explain table."""
    reg = register_l1(left.register, right.register)
    fw = cosine_distance(left.function_counts, right.function_counts)
    c3 = sparse_cosine_distance(left.char3, right.char3)
    # Intra-doc Delta: treat raw smoothed counts as already comparable.
    delta = burrows_delta(left.function_counts, right.function_counts)
    return {
        "register_l1": reg,
        "function_cosine_distance": fw,
        "char3_distance": c3,
        "delta": delta,
    }


def blend(channels: Mapping[str, float], weights: Mapping[str, float] | None = None) -> float:
    """Exam blend: register L1 dominates. Char-3 is a content leak; keep it out.

    Function-word cosine is a 20% helper so two notices with different
    shall-rates still have a closed-class channel. Delta is recorded but
    not blended — on six-line documents it mostly tracks the same counts.
    """
    w = weights or {
        "register_l1": 0.80,
        "function_cosine_distance": 0.20,
        "char3_distance": 0.0,
        "delta": 0.0,
    }
    # Six rates in [0, 1] make raw L1 sit around 0.1 (same voice) to 0.6
    # (stall vs notice). Squash with a small scale so 0.25 → ~0.56.
    scaled = {
        "register_l1": _squash(channels.get("register_l1", 0.0), 0.20),
        "function_cosine_distance": channels.get("function_cosine_distance", 0.0),
        "char3_distance": channels.get("char3_distance", 0.0),
        "delta": _squash(channels.get("delta", 0.0), 0.8),
    }
    return sum(scaled[k] * w.get(k, 0.0) for k in scaled if k in w)


def _squash(x: float, scale: float) -> float:
    """x / (x + scale) so an L1 of 1.2 sits near 0.5, 2.4 near 0.67."""
    if x <= 0:
        return 0.0
    return x / (x + scale)


def score_cut(left_units: Sequence[str], right_units: Sequence[str]) -> tuple[float, dict[str, float]]:
    left = extract_span(left_units)
    right = extract_span(right_units)
    channels = span_channels(left, right)
    return blend(channels), channels
