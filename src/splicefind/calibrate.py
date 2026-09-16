"""Threshold sweeps on a labelled collection.

A detector that always reports "no change" can look accurate on easy
documents. Sweeping the ensemble threshold and plotting F1 is the exam
way to show that you actually tuned the positive class.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .detect import detect_text
from .evaluate import DocumentScore, collection_report, score_document
from .io import Collection


@dataclass(frozen=True)
class ThresholdPoint:
    threshold: float
    macro_f1: float
    micro_f1: float
    mean_precision: float
    mean_recall: float
    mean_accuracy: float
    scores: tuple[DocumentScore, ...]


def sweep_thresholds(
    collection: Collection,
    thresholds: Sequence[float] | None = None,
    method: str = "ensemble",
) -> list[ThresholdPoint]:
    if thresholds is None:
        thresholds = [round(0.20 + i * 0.05, 2) for i in range(15)]
    labelled = [(problem, truth) for problem, truth in collection.pairs() if truth]
    if not labelled:
        raise ValueError("collection has no truth files; cannot calibrate")
    points = []
    for threshold in thresholds:
        scores = []
        for problem, truth in labelled:
            detection = detect_text(problem.text, threshold=threshold, method=method)
            scores.append(
                score_document(truth.changes, detection.changes, problem.problem_id)
            )
        summary = collection_report(scores)
        points.append(
            ThresholdPoint(
                threshold=threshold,
                macro_f1=summary["macro_f1"],
                micro_f1=summary["micro_f1"],
                mean_precision=summary["mean_precision"],
                mean_recall=summary["mean_recall"],
                mean_accuracy=summary["mean_accuracy"],
                scores=tuple(scores),
            )
        )
    return points


def best_threshold(points: Iterable[ThresholdPoint]) -> ThresholdPoint:
    ranked = sorted(points, key=lambda point: (point.macro_f1, point.micro_f1), reverse=True)
    if not ranked:
        raise ValueError("no calibration points")
    return ranked[0]


def format_sweep(points: Sequence[ThresholdPoint]) -> str:
    lines = [
        "threshold  macroF1  microF1  precision  recall  accuracy",
        "---------  -------  -------  ---------  ------  --------",
    ]
    winner = best_threshold(points)
    for point in points:
        mark = " *" if point.threshold == winner.threshold else "  "
        lines.append(
            f"{point.threshold:9.2f}  {point.macro_f1:7.3f}  {point.micro_f1:7.3f}  "
            f"{point.mean_precision:9.3f}  {point.mean_recall:6.3f}  "
            f"{point.mean_accuracy:8.3f}{mark}"
        )
    lines.append("")
    lines.append(f"best threshold by macro F1: {winner.threshold:.2f}")
    return "\n".join(lines)
