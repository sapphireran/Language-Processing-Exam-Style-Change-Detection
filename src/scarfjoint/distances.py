"""Pairwise distances that can be derived, slowly, on paper."""

from __future__ import annotations

import math
from collections import Counter

from .features import ParagraphFeatures, content_types


def cosine(a: dict[str, float] | tuple[float, ...] | list[float], b) -> float:
    if isinstance(a, dict):
        keys = set(a) | set(b)
        num = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
    else:
        num = sum(x * y for x, y in zip(a, b, strict=True))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return num / (na * nb)


def cosine_distance(a, b) -> float:
    return 1.0 - cosine(a, b)


def euclidean(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b, strict=True)))


def manhattan(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b, strict=True))


def _kl(p: list[float], q: list[float]) -> float:
    total = 0.0
    for pi, qi in zip(p, q, strict=True):
        if pi <= 0.0:
            continue
        total += pi * math.log(pi / qi)
    return total


def jensen_shannon(p: tuple[float, ...], q: tuple[float, ...], floor: float = 1e-12) -> float:
    """JS divergence on two discrete distributions (not the sqrt distance)."""
    pn = [max(x, 0.0) for x in p]
    qn = [max(x, 0.0) for x in q]
    sp, sq = sum(pn), sum(qn)
    if sp == 0.0 or sq == 0.0:
        return 0.0
    pn = [x / sp for x in pn]
    qn = [x / sq for x in qn]
    m = [(a + b) / 2.0 for a, b in zip(pn, qn, strict=True)]
    m = [max(x, floor) for x in m]
    pn = [max(x, floor) for x in pn]
    qn = [max(x, floor) for x in qn]
    return 0.5 * _kl(pn, m) + 0.5 * _kl(qn, m)


def burrows_delta(a: tuple[float, ...], b: tuple[float, ...], scales: tuple[float, ...] | None = None) -> float:
    """Mean absolute difference. If ``scales`` is given, z-score first."""
    if not a:
        return 0.0
    if scales is None:
        return sum(abs(x - y) for x, y in zip(a, b, strict=True)) / len(a)
    total = 0.0
    n = 0
    for x, y, s in zip(a, b, scales, strict=True):
        if s <= 0.0:
            continue
        total += abs((x - y) / s)
        n += 1
    return total / n if n else 0.0


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 1.0
    return len(a & b) / len(union)


def topic_distance(left: ParagraphFeatures, right: ParagraphFeatures) -> float:
    return 1.0 - jaccard(
        content_types(left.tokens.words_lower),
        content_types(right.tokens.words_lower),
    )


def zscore_rows(rows: list[tuple[float, ...]]) -> list[tuple[float, ...]]:
    if not rows:
        return []
    dim = len(rows[0])
    means = []
    stds = []
    n = len(rows)
    for j in range(dim):
        col = [row[j] for row in rows]
        mean = sum(col) / n
        var = sum((x - mean) ** 2 for x in col) / n
        means.append(mean)
        stds.append(math.sqrt(var) if var > 1e-12 else 1.0)
    out = []
    for row in rows:
        out.append(tuple((row[j] - means[j]) / stds[j] for j in range(dim)))
    return out


def compression_ncd(a: str, b: str) -> float:
    """Normalised compression distance via zlib, a cheap intrinsic probe."""
    import zlib

    ca = len(zlib.compress(a.encode("utf-8"), level=9))
    cb = len(zlib.compress(b.encode("utf-8"), level=9))
    cab = len(zlib.compress((a + "\n" + b).encode("utf-8"), level=9))
    denom = max(ca, cb)
    if denom == 0:
        return 0.0
    return (cab - min(ca, cb)) / denom


def char_profile(text: str, n: int = 3) -> dict[str, float]:
    from .tokenize import char_ngrams

    counts: Counter[str] = Counter(char_ngrams(text, n))
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}
