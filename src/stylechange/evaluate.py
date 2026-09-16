"""Macro-F1 and related pair-label scores."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np


def _as_int_array(values: Sequence[int] | np.ndarray) -> np.ndarray:
    return np.asarray(list(values), dtype=int)


def confusion(gold: Sequence[int], pred: Sequence[int]) -> tuple[int, int, int, int]:
    """Return tn, fp, fn, tp with 1 as the positive (change) class."""
    y = _as_int_array(gold)
    p = _as_int_array(pred)
    if y.shape != p.shape:
        raise ValueError("gold and pred must have the same length")
    tn = int(np.sum((y == 0) & (p == 0)))
    fp = int(np.sum((y == 0) & (p == 1)))
    fn = int(np.sum((y == 1) & (p == 0)))
    tp = int(np.sum((y == 1) & (p == 1)))
    return tn, fp, fn, tp


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _pr(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall, _f1(precision, recall)


def score_pairs(gold: Sequence[int], pred: Sequence[int]) -> dict[str, float]:
    tn, fp, fn, tp = confusion(gold, pred)
    n = tn + fp + fn + tp
    acc = (tn + tp) / n if n else 0.0
    p0, r0, f0 = _pr(tn, fn, fp)  # class 0: treat 0 as "positive" for that class
    p1, r1, f1 = _pr(tp, fp, fn)
    return {
        "n_pairs": float(n),
        "accuracy": acc,
        "precision_0": p0,
        "recall_0": r0,
        "f1_0": f0,
        "precision_1": p1,
        "recall_1": r1,
        "f1_1": f1,
        "macro_f1": 0.5 * (f0 + f1),
        "tn": float(tn),
        "fp": float(fp),
        "fn": float(fn),
        "tp": float(tp),
    }


def macro_f1(gold: Sequence[int], pred: Sequence[int]) -> float:
    return score_pairs(gold, pred)["macro_f1"]


@dataclass
class EvaluationResult:
    pooled: dict[str, float]
    per_document: dict[str, dict[str, float]] = field(default_factory=dict)
    io_failures: list[str] = field(default_factory=list)

    @property
    def mean_document_macro_f1(self) -> float:
        if not self.per_document:
            return 0.0
        return float(np.mean([row["macro_f1"] for row in self.per_document.values()]))

    def summary_rows(self) -> list[str]:
        p = self.pooled
        lines = [
            f"pairs            {int(p['n_pairs'])}",
            f"io_failures      {len(self.io_failures)}",
            f"accuracy         {p['accuracy']:.4f}",
            f"f1_0             {p['f1_0']:.4f}",
            f"f1_1             {p['f1_1']:.4f}",
            f"macro_f1         {p['macro_f1']:.4f}",
            f"mean_doc_macro   {self.mean_document_macro_f1:.4f}",
            f"tn/fp/fn/tp      {int(p['tn'])}/{int(p['fp'])}/{int(p['fn'])}/{int(p['tp'])}",
        ]
        if self.io_failures:
            lines.append("failed_ids       " + ", ".join(self.io_failures))
        return lines

    def __str__(self) -> str:
        return "\n".join(self.summary_rows())


def evaluate_aligned(
    gold_by_id: dict[str, Sequence[int]],
    pred_by_id: dict[str, Sequence[int]],
) -> EvaluationResult:
    pooled_gold: list[int] = []
    pooled_pred: list[int] = []
    per_doc: dict[str, dict[str, float]] = {}
    failures: list[str] = []
    for pid, gold in sorted(gold_by_id.items()):
        if pid not in pred_by_id:
            failures.append(pid)
            continue
        pred = list(pred_by_id[pid])
        gold_list = list(gold)
        if len(pred) != len(gold_list):
            failures.append(pid)
            continue
        per_doc[pid] = score_pairs(gold_list, pred)
        pooled_gold.extend(gold_list)
        pooled_pred.extend(pred)
    pooled = score_pairs(pooled_gold, pooled_pred) if pooled_gold else score_pairs([], [])
    return EvaluationResult(pooled=pooled, per_document=per_doc, io_failures=failures)


def evaluate_dirs(gold_dir: str, pred_dir: str):
    from .io import load_changes, problem_id
    from pathlib import Path

    gold_map = {}
    for path in Path(gold_dir).rglob("truth-problem-*.json"):
        gold_map[problem_id(path)] = load_changes(path)
    pred_map = {}
    for path in Path(pred_dir).rglob("solution-problem-*.json"):
        pred_map[problem_id(path)] = load_changes(path)
    return evaluate_aligned(gold_map, pred_map)
