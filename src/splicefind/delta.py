"""Burrows' Delta on closed-class word rates.

Delta is a nearest-neighbour authorship measure. For style *change*
detection we do not have candidate authors; we only compare adjacent
paragraphs. The exam-friendly reading is: z-score each function-word
rate across the document, then take the mean absolute difference.
"""

from __future__ import annotations

from typing import Sequence

from .features import FeatureVector, zscore_columns
from .function_words import FUNCTION_WORDS


def burrows_delta(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("Delta vectors must be non-empty and aligned")
    return sum(abs(a - b) for a, b in zip(left, right)) / len(left)


def pairwise_delta(
    vectors: Sequence[FeatureVector],
    names: Sequence[str] = FUNCTION_WORDS,
) -> list[float]:
    if len(vectors) < 2:
        return []
    rows = zscore_columns([vector.function_row(names) for vector in vectors])
    return [burrows_delta(rows[i], rows[i + 1]) for i in range(len(rows) - 1)]


def most_shifted_words(
    left: FeatureVector,
    right: FeatureVector,
    k: int = 8,
) -> list[tuple[str, float, float, float]]:
    """Return words with the largest absolute rate gap between two paragraphs."""
    rows = []
    for word in FUNCTION_WORDS:
        a = left.function_words.get(word, 0.0)
        b = right.function_words.get(word, 0.0)
        rows.append((word, a, b, abs(a - b)))
    rows.sort(key=lambda item: item[3], reverse=True)
    return rows[:k]
