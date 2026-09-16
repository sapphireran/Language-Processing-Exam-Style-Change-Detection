"""CUSUM traces over a hinge-score series.

A style change often appears as a slope change in the cumulative sum of
(score - mean). The exam use is visual and diagnostic, not a standalone
detector: short teaching documents have too few hinges for a reliable
changepoint test.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CusumTrace:
    mean: float
    values: tuple[float, ...]
    peak_index: int
    peak_value: float


def cusum_trace(scores: Sequence[float]) -> CusumTrace:
    if not scores:
        return CusumTrace(mean=0.0, values=(), peak_index=0, peak_value=0.0)
    mu = sum(scores) / len(scores)
    running = 0.0
    values: list[float] = []
    peak_index = 0
    peak_value = 0.0
    for i, score in enumerate(scores):
        running += score - mu
        values.append(running)
        if abs(running) > abs(peak_value):
            peak_value = running
            peak_index = i
    return CusumTrace(
        mean=mu,
        values=tuple(values),
        peak_index=peak_index,
        peak_value=peak_value,
    )
