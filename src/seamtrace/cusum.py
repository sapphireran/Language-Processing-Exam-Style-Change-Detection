"""CUSUM-style traces over a running style distance.

The exam version is a teaching CUSUM, not a production change-point
library. For each unit we take the mean pairwise score against a short
left context. Then we accumulate (score - mean). Peaks after a long
rise are candidate seams.

This is useful as an *explanation* device: a plot of the running sum
shows whether the detector saw one late jump or many small wobbles.
"""

from __future__ import annotations

from .features import FeatureTable
from .pairwise import pair_score
from .vector import mean


def window_scores(table: FeatureTable, window: int = 2) -> list[float]:
    if len(table) < 2:
        return []
    scores: list[float] = []
    for i in range(1, len(table)):
        left_ids = range(max(0, i - window), i)
        chunk = [pair_score(table.units[j], table.units[i], table) for j in left_ids]
        scores.append(mean(chunk))
    return scores


def cusum_scores(table: FeatureTable, window: int = 2) -> list[float]:
    raw = window_scores(table, window=window)
    if not raw:
        return []
    centre = mean(raw)
    running = 0.0
    out: list[float] = []
    for value in raw:
        running += value - centre
        out.append(running)
    return out


def cusum_peaks(values: list[float], *, min_rise: float = 0.15) -> list[int]:
    """Return pair indices where the CUSUM jumps up by at least min_rise."""
    if len(values) < 2:
        return []
    peaks: list[int] = []
    for i in range(1, len(values)):
        if values[i] - values[i - 1] >= min_rise:
            peaks.append(i)
    return peaks
