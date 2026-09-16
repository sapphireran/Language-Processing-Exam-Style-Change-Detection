"""Tiny closed-form examples used in the exam notes.

These functions exist so a worked answer can be re-run instead of
trusted. They are not a second detector.
"""

from __future__ import annotations

import math


def type_token_ratio(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def cosine_from_counts(a: dict[str, int], b: dict[str, int]) -> float:
    keys = set(a) | set(b)
    va = [float(a.get(k, 0)) for k in keys]
    vb = [float(b.get(k, 0)) for k in keys]
    na = math.sqrt(sum(x * x for x in va))
    nb = math.sqrt(sum(x * x for x in vb))
    if na == 0 or nb == 0:
        return 0.0
    return sum(x * y for x, y in zip(va, vb)) / (na * nb)


def f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def macro_f1_from_cells(tp: int, fp: int, tn: int, fn: int) -> float:
    prec1 = tp / (tp + fp) if tp + fp else 0.0
    rec1 = tp / (tp + fn) if tp + fn else 0.0
    prec0 = tn / (tn + fn) if tn + fn else 0.0
    rec0 = tn / (tn + fp) if tn + fp else 0.0
    return (f1(prec1, rec1) + f1(prec0, rec0)) / 2.0
