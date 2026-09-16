"""Boundary-level precision, recall, and F1.

PAN 2023 scores a binary ``changes`` vector with F1. Accuracy is a poor
exam answer on its own: most adjacent paragraphs in a typical document
share an author, so a "never change" predictor looks strong until you
report the positive-class F1.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class DocumentScore:
    problem_id: str
    precision: float
    recall: float
    f1: float
    accuracy: float
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int
    n_boundaries: int
    gold_changes: int
    pred_changes: int

    def as_dict(self) -> dict[str, float | int | str]:
        return {
            "problem_id": self.problem_id,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "accuracy": self.accuracy,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "true_negatives": self.true_negatives,
            "n_boundaries": self.n_boundaries,
            "gold_changes": self.gold_changes,
            "pred_changes": self.pred_changes,
        }


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def confusion(gold: Sequence[int], pred: Sequence[int]) -> tuple[int, int, int, int]:
    if len(gold) != len(pred):
        raise ValueError(
            f"length mismatch: gold has {len(gold)} boundaries, pred has {len(pred)}"
        )
    tp = fp = fn = tn = 0
    for g, p in zip(gold, pred):
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 1 and p == 0:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def f1_from_counts(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)
    return precision, recall, f1


def score_document(
    gold: Sequence[int],
    pred: Sequence[int],
    problem_id: str = "",
) -> DocumentScore:
    tp, fp, fn, tn = confusion(gold, pred)
    precision, recall, f1 = f1_from_counts(tp, fp, fn)
    total = tp + fp + fn + tn
    return DocumentScore(
        problem_id=problem_id,
        precision=precision,
        recall=recall,
        f1=f1,
        accuracy=_safe_div(tp + tn, total),
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=tn,
        n_boundaries=total,
        gold_changes=sum(int(flag) for flag in gold),
        pred_changes=sum(int(flag) for flag in pred),
    )


def macro_f1(scores: Iterable[DocumentScore]) -> float:
    items = list(scores)
    if not items:
        return 0.0
    return sum(score.f1 for score in items) / len(items)


def micro_f1(scores: Iterable[DocumentScore]) -> float:
    tp = fp = fn = 0
    for score in scores:
        tp += score.true_positives
        fp += score.false_positives
        fn += score.false_negatives
    _, _, f1 = f1_from_counts(tp, fp, fn)
    return f1


def collection_report(scores: Sequence[DocumentScore]) -> dict[str, float]:
    if not scores:
        return {"macro_f1": 0.0, "micro_f1": 0.0, "mean_accuracy": 0.0, "n_docs": 0}
    return {
        "macro_f1": macro_f1(scores),
        "micro_f1": micro_f1(scores),
        "mean_accuracy": sum(score.accuracy for score in scores) / len(scores),
        "mean_precision": sum(score.precision for score in scores) / len(scores),
        "mean_recall": sum(score.recall for score in scores) / len(scores),
        "n_docs": float(len(scores)),
        "n_boundaries": float(sum(score.n_boundaries for score in scores)),
        "gold_changes": float(sum(score.gold_changes for score in scores)),
    }


def format_score(score: DocumentScore) -> str:
    return (
        f"{score.problem_id or 'document':<28}  "
        f"P={score.precision:5.3f}  R={score.recall:5.3f}  "
        f"F1={score.f1:5.3f}  Acc={score.accuracy:5.3f}  "
        f"gold={score.gold_changes}/{score.n_boundaries}"
    )
