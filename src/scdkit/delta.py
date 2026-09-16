"""Burrows's Delta and related pairwise style distances.

Classic Delta (Burrows 2002) z-scores function-word frequencies against
a comparison corpus, then takes the mean absolute difference of those
z-scores. In this intrinsic kit the 'corpus' is the other paragraphs of
the same document — that is a legitimate oral-exam answer, and you
should also mention the weakness (a document with one odd paragraph
contaminates the mean).
"""

from __future__ import annotations

import math
from typing import Sequence

from .features import ParagraphFeatures
from .ngrams import cosine_distance, jaccard


def _mean_std(columns: Sequence[Sequence[float]]) -> tuple[list[float], list[float]]:
    n = len(columns)
    width = len(columns[0]) if columns else 0
    means = [0.0] * width
    for row in columns:
        for i, value in enumerate(row):
            means[i] += value
    if n:
        means = [m / n for m in means]
    stds = [0.0] * width
    for row in columns:
        for i, value in enumerate(row):
            diff = value - means[i]
            stds[i] += diff * diff
    if n > 1:
        stds = [math.sqrt(s / (n - 1)) for s in stds]
    else:
        stds = [0.0] * width
    return means, stds


def zscore_rows(rows: Sequence[Sequence[float]]) -> list[list[float]]:
    if not rows:
        return []
    means, stds = _mean_std(rows)
    zrows: list[list[float]] = []
    for row in rows:
        zrows.append(
            [
                (value - mean) / std if std > 1e-9 else 0.0
                for value, mean, std in zip(row, means, stds, strict=True)
            ]
        )
    return zrows


def burrows_delta(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right:
        return 0.0
    return sum(abs(a - b) for a, b in zip(left, right, strict=True)) / len(left)


def document_deltas(features: Sequence[ParagraphFeatures]) -> list[float]:
    """Adjacent Burrows Delta using in-document function-word z-scores."""
    if len(features) < 2:
        return []
    rows = [feat.function_freqs for feat in features]
    zrows = zscore_rows(rows)
    return [burrows_delta(zrows[i], zrows[i + 1]) for i in range(len(zrows) - 1)]


def numeric_distances(features: Sequence[ParagraphFeatures]) -> list[float]:
    if len(features) < 2:
        return []
    rows = [feat.numeric_vector() for feat in features]
    zrows = zscore_rows(rows)
    out: list[float] = []
    for i in range(len(zrows) - 1):
        left, right = zrows[i], zrows[i + 1]
        # Cosine on the z-scored dense vector.
        dot = sum(a * b for a, b in zip(left, right, strict=True))
        n1 = math.sqrt(sum(a * a for a in left))
        n2 = math.sqrt(sum(b * b for b in right))
        if n1 < 1e-9 or n2 < 1e-9:
            out.append(0.0)
        else:
            out.append(1.0 - max(-1.0, min(1.0, dot / (n1 * n2))))
    return out


def char_ngram_distances(features: Sequence[ParagraphFeatures]) -> list[float]:
    return [
        cosine_distance(features[i].char_profile, features[i + 1].char_profile)
        for i in range(len(features) - 1)
    ]


def formality_jumps(features: Sequence[ParagraphFeatures]) -> list[float]:
    return [
        abs(features[i].formality - features[i + 1].formality)
        for i in range(len(features) - 1)
    ]


def sentence_length_jumps(features: Sequence[ParagraphFeatures]) -> list[float]:
    jumps = []
    for i in range(len(features) - 1):
        a, b = features[i].mean_sent_len, features[i + 1].mean_sent_len
        scale = max(8.0, 0.5 * (a + b))
        jumps.append(abs(a - b) / scale)
    return jumps


def contraction_jumps(features: Sequence[ParagraphFeatures]) -> list[float]:
    return [
        abs(features[i].contraction_rate - features[i + 1].contraction_rate)
        for i in range(len(features) - 1)
    ]


def topic_jaccard(features: Sequence[ParagraphFeatures]) -> list[float]:
    """Content-word Jaccard *distance* (1 - overlap). Topic confound channel."""
    return [
        1.0 - jaccard(features[i].content_types, features[i + 1].content_types)
        for i in range(len(features) - 1)
    ]
