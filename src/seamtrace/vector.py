"""Small linear-algebra helpers. No NumPy."""

from __future__ import annotations

import math
from typing import Iterable, Mapping


def dot(a: Iterable[float], b: Iterable[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def l2(a: Iterable[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def cosine_distance(a: Iterable[float], b: Iterable[float]) -> float:
    va = list(a)
    vb = list(b)
    na = l2(va)
    nb = l2(vb)
    if na == 0.0 or nb == 0.0:
        return 1.0
    sim = max(-1.0, min(1.0, dot(va, vb) / (na * nb)))
    return 1.0 - sim


def manhattan(a: Iterable[float], b: Iterable[float]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


def mean(xs: Iterable[float]) -> float:
    vals = list(xs)
    if not vals:
        return 0.0
    return sum(vals) / len(vals)


def pop_std(xs: Iterable[float]) -> float:
    vals = list(xs)
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    var = sum((x - m) ** 2 for x in vals) / len(vals)
    return math.sqrt(var)


def zscores(xs: Iterable[float]) -> list[float]:
    vals = list(xs)
    s = pop_std(vals)
    if s == 0.0:
        return [0.0] * len(vals)
    m = mean(vals)
    return [(x - m) / s for x in vals]


def sparse_cosine_distance(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    if not a or not b:
        return 1.0
    keys = set(a) | set(b)
    return cosine_distance((a.get(k, 0.0) for k in keys), (b.get(k, 0.0) for k in keys))
