"""F1 helpers that do not lie on all-negative documents.

PAN-style scoring treats each document as a sequence of boundary bits.
A single-author document has a gold vector of zeros. Predicting all zeros
must be a perfect score, not an undefined F1. Predicting a stray 1 must
hurt. That special case is the whole point of `safe_f1`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


def _counts(gold: Sequence[int], pred: Sequence[int]) -> tuple[int, int, int]:
    if len(gold) != len(pred):
        raise ValueError("gold and pred must be the same length")
    tp = sum(1 for g, p in zip(gold, pred) if g == 1 and p == 1)
    fp = sum(1 for g, p in zip(gold, pred) if g == 0 and p == 1)
    fn = sum(1 for g, p in zip(gold, pred) if g == 1 and p == 0)
    return tp, fp, fn


def safe_f1(gold: Sequence[int], pred: Sequence[int]) -> float:
    tp, fp, fn = _counts(gold, pred)
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0.0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def precision_recall(gold: Sequence[int], pred: Sequence[int]) -> tuple[float, float]:
    tp, fp, fn = _counts(gold, pred)
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0, 1.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall


def accuracy(gold: Sequence[int], pred: Sequence[int]) -> float:
    if not gold:
        return 1.0
    if len(gold) != len(pred):
        raise ValueError("gold and pred must be the same length")
    return sum(1 for g, p in zip(gold, pred) if g == p) / len(gold)


def micro_f1(pairs: Iterable[tuple[Sequence[int], Sequence[int]]]) -> float:
    tp = fp = fn = 0
    for gold, pred in pairs:
        d_tp, d_fp, d_fn = _counts(gold, pred)
        tp += d_tp
        fp += d_fp
        fn += d_fn
    if tp == 0 and fp == 0 and fn == 0:
        return 1.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0.0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def macro_f1(pairs: Iterable[tuple[Sequence[int], Sequence[int]]]) -> float:
    scores = [safe_f1(gold, pred) for gold, pred in pairs]
    if not scores:
        return 1.0
    return sum(scores) / len(scores)


@dataclass(frozen=True)
class DocumentScore:
    name: str
    gold: list[int]
    pred: list[int]
    f1: float
    precision: float
    recall: float
    accuracy: float
    n_boundaries: int
    n_true_changes: int
    n_pred_changes: int

    @classmethod
    def from_pair(cls, name: str, gold: Sequence[int], pred: Sequence[int]) -> "DocumentScore":
        precision, recall = precision_recall(gold, pred)
        return cls(
            name=name,
            gold=list(gold),
            pred=list(pred),
            f1=safe_f1(gold, pred),
            precision=precision,
            recall=recall,
            accuracy=accuracy(gold, pred),
            n_boundaries=len(gold),
            n_true_changes=sum(gold),
            n_pred_changes=sum(pred),
        )


def corpus_report(rows: list[DocumentScore]) -> dict[str, float]:
    pairs = [(row.gold, row.pred) for row in rows]
    return {
        "n_docs": float(len(rows)),
        "macro_f1": macro_f1(pairs),
        "micro_f1": micro_f1(pairs),
        "mean_accuracy": (sum(row.accuracy for row in rows) / len(rows)) if rows else 1.0,
        "n_boundaries": float(sum(row.n_boundaries for row in rows)),
        "n_true_changes": float(sum(row.n_true_changes for row in rows)),
        "n_pred_changes": float(sum(row.n_pred_changes for row in rows)),
    }
