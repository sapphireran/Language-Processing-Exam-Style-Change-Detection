"""Pair-level metrics. Macro-F1 is the teaching default.

Accuracy is the wrong headline number: teaching corpora, like PAN
sets, are change-sparse. A detector that never fires can look 'good'
on accuracy and fail the exam question.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PairMetrics:
    precision_0: float
    recall_0: float
    f1_0: float
    precision_1: float
    recall_1: float
    f1_1: float
    macro_f1: float
    accuracy: float
    support_0: int
    support_1: int
    tp: int
    fp: int
    tn: int
    fn: int

    def as_dict(self) -> dict[str, float | int]:
        return self.__dict__.copy()


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def score_pairs(gold: list[int], pred: list[int]) -> PairMetrics:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    tp = fp = tn = fn = 0
    for g, p in zip(gold, pred):
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 0 and p == 0:
            tn += 1
        else:
            fn += 1
    prec1 = _safe_div(tp, tp + fp)
    rec1 = _safe_div(tp, tp + fn)
    prec0 = _safe_div(tn, tn + fn)
    rec0 = _safe_div(tn, tn + fp)
    f1_1 = _f1(prec1, rec1)
    f1_0 = _f1(prec0, rec0)
    correct = tp + tn
    total = len(gold)
    return PairMetrics(
        precision_0=prec0,
        recall_0=rec0,
        f1_0=f1_0,
        precision_1=prec1,
        recall_1=rec1,
        f1_1=f1_1,
        macro_f1=(f1_0 + f1_1) / 2.0,
        accuracy=_safe_div(correct, total),
        support_0=tn + fp,
        support_1=tp + fn,
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
    )


def macro_f1(gold: list[int], pred: list[int]) -> float:
    return score_pairs(gold, pred).macro_f1


def confusion_rows(gold: list[int], pred: list[int]) -> list[str]:
    labels = []
    for i, (g, p) in enumerate(zip(gold, pred)):
        if g == 1 and p == 1:
            labels.append(f"pair {i}: hit")
        elif g == 1 and p == 0:
            labels.append(f"pair {i}: miss")
        elif g == 0 and p == 1:
            labels.append(f"pair {i}: false alarm")
        else:
            labels.append(f"pair {i}: correct stay")
    return labels
