"""Intra-document Burrows' Delta on function-word rates.

Classic Delta z-scores features against a reference corpus. Inside one
exam document we z-score each function word across the document's own
units, then take the mean absolute difference of those z-scores between
neighbours. Short documents make the z-score noisy; the pairwise blender
therefore treats Delta as a supporting channel, not the only cut.
"""

from __future__ import annotations

import math
from typing import Sequence

from .features import UnitFeatures


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: Sequence[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mu = _mean(xs)
    var = sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def zscore_matrix(feats: Sequence[UnitFeatures]) -> list[list[float]]:
    if not feats:
        return []
    dim = len(feats[0].function_counts)
    columns = []
    for j in range(dim):
        col = [f.function_vector()[j] for f in feats]
        mu = _mean(col)
        sd = _std(col)
        if sd == 0:
            columns.append([0.0] * len(feats))
        else:
            columns.append([(v - mu) / sd for v in col])
    return [[columns[j][i] for j in range(dim)] for i in range(len(feats))]


def adjacent_delta(feats: Sequence[UnitFeatures]) -> list[float]:
    """Mean absolute z-difference between consecutive units."""
    z = zscore_matrix(feats)
    if len(z) < 2:
        return []
    out: list[float] = []
    for left, right in zip(z, z[1:]):
        out.append(sum(abs(a - b) for a, b in zip(left, right)) / len(left))
    return out
