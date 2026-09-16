"""Metrics I can compute on paper: pairwise macro-F1 and a from-scratch ARI.

PAN-style scoring for the current sentence-level task is macro-F1 over
adjacent pairs. Author-assignment (the old Task 2) needs a clustering
metric; I implement adjusted Rand index without sklearn so the formula
stays visible.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


def _f1_one_class(gold: list[int], pred: list[int], label: int) -> tuple[float, float, float]:
    tp = sum(g == label and p == label for g, p in zip(gold, pred, strict=True))
    fp = sum(g != label and p == label for g, p in zip(gold, pred, strict=True))
    fn = sum(g == label and p != label for g, p in zip(gold, pred, strict=True))
    # Empty-class convention: if the class never occurs in gold or pred,
    # treat precision and recall as perfect. That makes an all-zero single
    # author document score 1.0 / 1.0 instead of 0.0 because "class 1
    # never fired".
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    if precision + recall == 0.0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def macro_f1(gold: list[int], pred: list[int]) -> float:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    if not gold:
        return 1.0
    scores = [_f1_one_class(gold, pred, label)[2] for label in (0, 1)]
    return sum(scores) / 2.0


@dataclass(frozen=True)
class BoundaryReport:
    gold: list[int]
    pred: list[int]
    precision_0: float
    recall_0: float
    f1_0: float
    precision_1: float
    recall_1: float
    f1_1: float
    macro_f1: float
    accuracy: float
    multi_author_gold: bool
    multi_author_pred: bool

    def as_dict(self) -> dict[str, float | bool | list[int]]:
        return {
            "gold": self.gold,
            "pred": self.pred,
            "precision_0": self.precision_0,
            "recall_0": self.recall_0,
            "f1_0": self.f1_0,
            "precision_1": self.precision_1,
            "recall_1": self.recall_1,
            "f1_1": self.f1_1,
            "macro_f1": self.macro_f1,
            "accuracy": self.accuracy,
            "multi_author_gold": self.multi_author_gold,
            "multi_author_pred": self.multi_author_pred,
        }


def boundary_report(gold: list[int], pred: list[int]) -> BoundaryReport:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    p0, r0, f0 = _f1_one_class(gold, pred, 0)
    p1, r1, f1 = _f1_one_class(gold, pred, 1)
    acc = (sum(g == p for g, p in zip(gold, pred, strict=True)) / len(gold)) if gold else 1.0
    return BoundaryReport(
        gold=list(gold),
        pred=list(pred),
        precision_0=p0,
        recall_0=r0,
        f1_0=f0,
        precision_1=p1,
        recall_1=r1,
        f1_1=f1,
        macro_f1=(f0 + f1) / 2.0,
        accuracy=acc,
        multi_author_gold=any(gold),
        multi_author_pred=any(pred),
    )


def _comb2(n: int) -> int:
    return n * (n - 1) // 2 if n >= 2 else 0


def adjusted_rand_index(gold: list[int], pred: list[int]) -> float:
    """ARI on author-id sequences. Permuting the labels does not change the score."""
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    n = len(gold)
    if n < 2:
        return 1.0
    pairs = Counter(zip(gold, pred, strict=True))
    gold_n = Counter(gold)
    pred_n = Counter(pred)
    sum_comb = sum(_comb2(c) for c in pairs.values())
    sum_gold = sum(_comb2(c) for c in gold_n.values())
    sum_pred = sum(_comb2(c) for c in pred_n.values())
    total_comb = _comb2(n)
    expected = (sum_gold * sum_pred / total_comb) if total_comb else 0.0
    max_index = 0.5 * (sum_gold + sum_pred)
    denom = max_index - expected
    if abs(denom) < 1e-12:
        return 1.0
    return (sum_comb - expected) / denom
