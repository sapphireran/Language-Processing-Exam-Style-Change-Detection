"""Binary segmentation on a stylometric walk.

A pairwise hinge asks: are these two neighbouring paragraphs different?
A split score asks: if I saw the document here, how cleanly do the two
sides pull apart? That is the kerf — the gap the blade leaves.

The size weight ``sqrt(k * (n-k) / n)`` is the usual two-sample / CUSUM
factor. It punishes a cut that isolates a single odd paragraph unless the
oddness is large, and it prefers a cut that balances two real houses.

Recursion handles more than one author. An ABA return still shows a
first cut (A vs mixed B+A), then a second cut on the right piece.
"""

from __future__ import annotations

from dataclasses import dataclass

from .distance import euclidean
from .features import FeatureVector, mean_vector

# Frozen on the toy bank after looking at same-house vs cross-house
# split scores. Not a trained model. See docs/14-live-results.md.
DEFAULT_PENALTY = 0.42
DEFAULT_ADJ_Z = 1.35


@dataclass(frozen=True)
class SplitView:
    scores: list[float]
    adjacent: list[float]
    best_index: int | None
    best_score: float


def split_scores(vectors: list[FeatureVector]) -> list[float]:
    n = len(vectors)
    if n < 2:
        return []
    values = [v.values() for v in vectors]
    out: list[float] = []
    for k in range(1, n):
        left = _col_mean(values[:k])
        right = _col_mean(values[k:])
        sep = euclidean(left, right)
        weight = (k * (n - k) / n) ** 0.5
        out.append(sep * weight)
    return out


def adjacent_scores(vectors: list[FeatureVector]) -> list[float]:
    values = [v.values() for v in vectors]
    return [euclidean(a, b) for a, b in zip(values, values[1:])]


def inspect_splits(vectors: list[FeatureVector]) -> SplitView:
    scores = split_scores(vectors)
    adjacent = adjacent_scores(vectors)
    if not scores:
        return SplitView(scores=[], adjacent=[], best_index=None, best_score=0.0)
    best_i = max(range(len(scores)), key=lambda i: scores[i])
    return SplitView(
        scores=scores,
        adjacent=adjacent,
        best_index=best_i,
        best_score=scores[best_i],
    )


def binary_segment(
    vectors: list[FeatureVector],
    penalty: float = DEFAULT_PENALTY,
    min_span: int = 1,
) -> list[int]:
    """Return 0-based hinge indices (between paragraph i and i+1)."""
    n = len(vectors)
    if n < 2:
        return []
    return sorted(_segment(vectors, penalty, min_span, offset=0))


def _segment(
    vectors: list[FeatureVector],
    penalty: float,
    min_span: int,
    offset: int,
) -> set[int]:
    n = len(vectors)
    if n < 2 * min_span:
        return set()
    scores = split_scores(vectors)
    if not scores:
        return set()
    # Disallow cuts that would leave a side shorter than min_span.
    legal = [
        (i, s)
        for i, s in enumerate(scores)
        if (i + 1) >= min_span and (n - (i + 1)) >= min_span
    ]
    if not legal:
        return set()
    best_i, best = max(legal, key=lambda t: t[1])
    if best < penalty:
        return set()
    cuts = {offset + best_i}
    left = vectors[: best_i + 1]
    right = vectors[best_i + 1 :]
    cuts |= _segment(left, penalty, min_span, offset)
    cuts |= _segment(right, penalty, min_span, offset + best_i + 1)
    return cuts


def adjacent_peaks(vectors: list[FeatureVector], z_thresh: float = DEFAULT_ADJ_Z) -> list[int]:
    """Local peaks on the adjacent walk. Secondary to the split score.

    Used when a return pattern (ABA) leaves a modest global split but a
    loud local step. Quiet documents stay quiet: a flat walk has no peak
    above the threshold once the sample standard deviation is tiny.
    """
    adj = adjacent_scores(vectors)
    if len(adj) < 1:
        return []
    mu = sum(adj) / len(adj)
    if len(adj) == 1:
        return [0] if adj[0] >= z_thresh * 0.55 else []
    var = sum((x - mu) ** 2 for x in adj) / (len(adj) - 1)
    sd = var**0.5
    if sd < 1e-9:
        return []
    peaks: list[int] = []
    for i, value in enumerate(adj):
        left = adj[i - 1] if i > 0 else value
        right = adj[i + 1] if i + 1 < len(adj) else value
        if value + 1e-12 >= left and value + 1e-12 >= right and (value - mu) / sd >= z_thresh:
            peaks.append(i)
    return peaks


def _col_mean(rows: list[list[float]]) -> list[float]:
    if not rows:
        return []
    return mean_vector_values(rows)


def mean_vector_values(rows: list[list[float]]) -> list[float]:
    cols = list(zip(*rows))
    return [sum(col) / len(col) for col in cols]
