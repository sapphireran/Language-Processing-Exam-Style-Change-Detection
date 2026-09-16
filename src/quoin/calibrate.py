"""Threshold grid search on a list of (gold, score-vector) pairs.

I do not hide a learning library behind this. The lab prints a table of
thresholds, picks the one with the best macro-F1, and that is the number
baked into `QuoinDetector.threshold` until I change the bank.
"""

from __future__ import annotations

from dataclasses import dataclass

from .evaluate import macro_f1, micro_f1


@dataclass(frozen=True)
class ThresholdRow:
    threshold: float
    macro_f1: float
    micro_f1: float
    n_pred: int


def _predict(scores: list[float], threshold: float) -> list[int]:
    return [1 if score >= threshold else 0 for score in scores]


def grid_search_threshold(
    documents: list[tuple[list[int], list[float]]],
    start: float = 0.16,
    stop: float = 0.60,
    step: float = 0.02,
) -> list[ThresholdRow]:
    if start >= stop:
        raise ValueError("start must be < stop")
    if step <= 0:
        raise ValueError("step must be positive")
    rows: list[ThresholdRow] = []
    threshold = start
    # Guard against float drift so 0.60 is actually visited.
    while threshold <= stop + 1e-9:
        pairs = []
        n_pred = 0
        for gold, scores in documents:
            pred = _predict(scores, threshold)
            pairs.append((gold, pred))
            n_pred += sum(pred)
        rows.append(
            ThresholdRow(
                threshold=round(threshold, 4),
                macro_f1=macro_f1(pairs),
                micro_f1=micro_f1(pairs),
                n_pred=n_pred,
            )
        )
        threshold += step
    return rows


def best_threshold(rows: list[ThresholdRow]) -> ThresholdRow:
    if not rows:
        raise ValueError("empty grid")
    return max(rows, key=lambda row: (row.macro_f1, row.micro_f1, -abs(row.threshold - 0.34)))
