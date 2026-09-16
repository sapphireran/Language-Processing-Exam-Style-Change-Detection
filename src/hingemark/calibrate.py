"""Threshold search and leave-one-document-out checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .corpus import CorpusItem
from .detectors import threshold_detect
from .evaluate import score_corpus, score_pairs
from .pairwise import score_unit_hinges


@dataclass(frozen=True)
class ThresholdRow:
    threshold: float
    mean_macro_f1: float
    micro_macro_f1: float
    mean_accuracy: float


@dataclass(frozen=True)
class LooRow:
    held_out: str
    best_threshold: float
    held_out_macro_f1: float
    train_macro_f1: float


def _predict(item: CorpusItem, threshold: float) -> tuple[int, ...]:
    hinges = score_unit_hinges(item.problem.units)
    return threshold_detect(hinges, threshold=threshold).changes


def grid_thresholds(
    items: Sequence[CorpusItem],
    grid: Iterable[float] | None = None,
) -> list[ThresholdRow]:
    if grid is None:
        grid = [i / 100 for i in range(18, 72, 2)]
    rows: list[ThresholdRow] = []
    for tau in grid:
        scored = score_corpus((it.name, it.truth.changes, _predict(it, tau)) for it in items)
        rows.append(
            ThresholdRow(
                threshold=tau,
                mean_macro_f1=scored.mean_macro_f1,
                micro_macro_f1=scored.micro.macro_f1,
                mean_accuracy=scored.mean_accuracy,
            )
        )
    rows.sort(key=lambda r: (r.mean_macro_f1, r.micro_macro_f1), reverse=True)
    return rows


def leave_one_out(
    items: Sequence[CorpusItem],
    grid: Iterable[float] | None = None,
) -> list[LooRow]:
    """Pick a threshold on all-but-one documents, score the held-out one.

    This is the honest exam story: a cut that fits the study set can
    still miss a hard hinge it never saw.
    """
    if grid is None:
        grid = [i / 100 for i in range(18, 72, 2)]
    grid = list(grid)
    rows: list[LooRow] = []
    for i, held in enumerate(items):
        train = [it for j, it in enumerate(items) if j != i]
        if not train:
            continue
        best = grid_thresholds(train, grid=grid)[0]
        pred = _predict(held, best.threshold)
        held_report = score_pairs(held.truth.changes, pred)
        rows.append(
            LooRow(
                held_out=held.name,
                best_threshold=best.threshold,
                held_out_macro_f1=held_report.macro_f1,
                train_macro_f1=best.mean_macro_f1,
            )
        )
    return rows
