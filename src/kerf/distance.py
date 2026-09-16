"""Distances on the closed-class vector. No topic space."""

from __future__ import annotations

import math


def euclidean(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vector length mismatch")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def manhattan(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vector length mismatch")
    return sum(abs(x - y) for x, y in zip(a, b))


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vector length mismatch")
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def hellinger(p: list[float], q: list[float]) -> float:
    """Hellinger on two non-negative vectors after L1 normalisation.

    Useful as a *rate* distance. Shape features that are not rates should
    not be fed here unless they have already been scaled into [0, 1].
    """
    if len(p) != len(q):
        raise ValueError("vector length mismatch")
    sp = sum(max(x, 0.0) for x in p)
    sq = sum(max(y, 0.0) for y in q)
    if sp == 0.0 and sq == 0.0:
        return 0.0
    if sp == 0.0 or sq == 0.0:
        return 1.0
    acc = 0.0
    for x, y in zip(p, q):
        acc += (math.sqrt(max(x, 0.0) / sp) - math.sqrt(max(y, 0.0) / sq)) ** 2
    return math.sqrt(acc / 2.0)


def js_divergence(p: list[float], q: list[float]) -> float:
    """Jensen–Shannon on L1-normalised non-negative vectors."""
    if len(p) != len(q):
        raise ValueError("vector length mismatch")

    def _norm(v: list[float]) -> list[float]:
        s = sum(max(x, 0.0) for x in v)
        if s == 0.0:
            return [0.0] * len(v)
        return [max(x, 0.0) / s for x in v]

    pn, qn = _norm(p), _norm(q)
    m = [(a + b) / 2.0 for a, b in zip(pn, qn)]
    return 0.5 * _kl(pn, m) + 0.5 * _kl(qn, m)


def _kl(p: list[float], q: list[float]) -> float:
    acc = 0.0
    for x, y in zip(p, q):
        if x <= 0.0:
            continue
        if y <= 0.0:
            return float("inf")
        acc += x * math.log(x / y)
    return acc
