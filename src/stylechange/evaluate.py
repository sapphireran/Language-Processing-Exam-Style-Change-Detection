"""Binary evaluation for paragraph-boundary change labels.

PAN reports an F1 on the change array. Accuracy is a trap: most boundaries
in a typical document are *not* changes, so a constant-0 predictor looks
strong until you look at recall.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Score:
    precision: float
    recall: float
    f1: float
    accuracy: float
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int
    n: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "accuracy": self.accuracy,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "true_negatives": self.true_negatives,
            "n": self.n,
        }


def _safe_div(num: float, den: float, empty: float) -> float:
    return num / den if den else empty


def score_changes(y_true: Sequence[int], y_pred: Sequence[int]) -> Score:
    if len(y_true) != len(y_pred):
        raise ValueError(
            f"length mismatch: truth has {len(y_true)} boundaries, "
            f"prediction has {len(y_pred)}"
        )
    tp = fp = fn = tn = 0
    for truth, pred in zip(y_true, y_pred):
        if truth not in (0, 1) or pred not in (0, 1):
            raise ValueError("labels must be 0 or 1")
        if truth == 1 and pred == 1:
            tp += 1
        elif truth == 0 and pred == 1:
            fp += 1
        elif truth == 1 and pred == 0:
            fn += 1
        else:
            tn += 1
    precision = _safe_div(tp, tp + fp, 1.0)
    recall = _safe_div(tp, tp + fn, 1.0)
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    n = len(y_true)
    accuracy = _safe_div(tp + tn, n, 1.0)
    return Score(
        precision=precision,
        recall=recall,
        f1=f1,
        accuracy=accuracy,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=tn,
        n=n,
    )


def macro_f1(scores: Iterable[Score]) -> float:
    items = list(scores)
    if not items:
        return 0.0
    return sum(item.f1 for item in items) / len(items)


def micro_score(scores: Iterable[Score]) -> Score:
    items = list(scores)
    tp = sum(s.true_positives for s in items)
    fp = sum(s.false_positives for s in items)
    fn = sum(s.false_negatives for s in items)
    tn = sum(s.true_negatives for s in items)
    n = sum(s.n for s in items)
    precision = _safe_div(tp, tp + fp, 1.0)
    recall = _safe_div(tp, tp + fn, 1.0)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    accuracy = _safe_div(tp + tn, n, 1.0)
    return Score(
        precision=precision,
        recall=recall,
        f1=f1,
        accuracy=accuracy,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=tn,
        n=n,
    )


def score_corpus(
    pairs: Iterable[tuple[str, Sequence[int], Sequence[int]]],
) -> dict[str, object]:
    """``pairs`` is an iterable of ``(doc_id, y_true, y_pred)``."""
    per_doc: dict[str, Score] = {}
    for doc_id, y_true, y_pred in pairs:
        per_doc[doc_id] = score_changes(y_true, y_pred)
    return {
        "per_document": per_doc,
        "macro_f1": macro_f1(per_doc.values()),
        "micro": micro_score(per_doc.values()),
    }
