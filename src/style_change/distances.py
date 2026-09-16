"""Vector distances used by the detectors."""

from __future__ import annotations

import math


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same length")
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    norm_left = math.sqrt(sum(a * a for a in left))
    norm_right = math.sqrt(sum(b * b for b in right))
    if norm_left == 0.0 or norm_right == 0.0:
        return 0.0
    return max(-1.0, min(1.0, dot / (norm_left * norm_right)))


def cosine_distance(left: list[float], right: list[float]) -> float:
    return 1.0 - cosine_similarity(left, right)


def _kl(p: list[float], q: list[float]) -> float:
    total = 0.0
    for pi, qi in zip(p, q, strict=True):
        if pi <= 0.0:
            continue
        total += pi * math.log(pi / qi)
    return total


def jensen_shannon(left: list[float], right: list[float]) -> float:
    """JS divergence in nats, then square-rooted into a metric-like score."""
    if len(left) != len(right):
        raise ValueError("vectors must have the same length")
    if not left:
        return 0.0
    sum_left = sum(left)
    sum_right = sum(right)
    if sum_left == 0.0 and sum_right == 0.0:
        return 0.0
    if sum_left == 0.0 or sum_right == 0.0:
        return 1.0
    p = [x / sum_left for x in left]
    q = [x / sum_right for x in right]
    mid = [(a + b) / 2.0 for a, b in zip(p, q, strict=True)]
    js = 0.5 * _kl(p, mid) + 0.5 * _kl(q, mid)
    return math.sqrt(max(0.0, js))


def zscore_columns(rows: list[list[float]]) -> list[list[float]]:
    if not rows:
        return []
    width = len(rows[0])
    means = []
    scales = []
    for col in range(width):
        values = [row[col] for row in rows]
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(var)
        means.append(mean)
        scales.append(1.0 if std < 1e-12 else std)
    return [
        [(value - means[i]) / scales[i] for i, value in enumerate(row)]
        for row in rows
    ]
