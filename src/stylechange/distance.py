"""Pairwise distances between style profiles.

Scalars use a relative difference so a long paragraph can be compared to a
short one without a shared corpus z-score. Function-word and character
n-gram views use cosine *distance* (1 - cosine similarity).
"""

from __future__ import annotations

import math
from typing import Mapping

from stylechange.features import CORE_SCALAR_NAMES, StyleProfile

EPS = 1e-9


def cosine_similarity(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    keys = set(left) | set(right)
    if not keys:
        return 1.0
    dot = 0.0
    left_norm_sq = 0.0
    right_norm_sq = 0.0
    for key in keys:
        a = left.get(key, 0.0)
        b = right.get(key, 0.0)
        dot += a * b
        left_norm_sq += a * a
        right_norm_sq += b * b
    if left_norm_sq <= EPS or right_norm_sq <= EPS:
        return 0.0
    return dot / math.sqrt(left_norm_sq * right_norm_sq)


def cosine_distance(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    return 1.0 - cosine_similarity(left, right)


def relative_difference(a: float, b: float) -> float:
    return abs(a - b) / (abs(a) + abs(b) + EPS)


def scalar_distance(left: StyleProfile, right: StyleProfile) -> float:
    diffs = [
        relative_difference(left.scalars[name], right.scalars[name])
        for name in CORE_SCALAR_NAMES
    ]
    return sum(diffs) / len(diffs)


def pair_distance(
    left: StyleProfile,
    right: StyleProfile,
    *,
    w_scalar: float = 0.55,
    w_function: float = 0.25,
    w_trigram: float = 0.10,
    w_punct: float = 0.10,
) -> dict[str, float]:
    """Weighted blend of complementary style views.

    Weights sum to 1.0 in the default. They can be retuned on the
    validation split without touching the feature extractors.
    """
    parts = {
        "scalar": scalar_distance(left, right),
        "function_words": cosine_distance(left.function_words, right.function_words),
        "trigram": cosine_distance(left.char_trigrams, right.char_trigrams),
        "punct": cosine_distance(left.punct, right.punct),
    }
    parts["combined"] = (
        w_scalar * parts["scalar"]
        + w_function * parts["function_words"]
        + w_trigram * parts["trigram"]
        + w_punct * parts["punct"]
    )
    return parts
