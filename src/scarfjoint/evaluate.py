"""Document-level scores used in the lab: binary F1, macro-F1, accuracy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricBundle:
    n_pairs: int
    n_true_change: int
    n_pred_change: int
    tp: int
    fp: int
    tn: int
    fn: int
    accuracy: float
    precision: float
    recall: float
    f1: float
    macro_f1: float
    exact: bool


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def binary_f1(gold: list[int], pred: list[int], positive: int = 1) -> float:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    tp = sum(g == positive and p == positive for g, p in zip(gold, pred))
    fp = sum(g != positive and p == positive for g, p in zip(gold, pred))
    fn = sum(g == positive and p != positive for g, p in zip(gold, pred))
    _, _, f1 = _prf(tp, fp, fn)
    return f1


def macro_f1(gold: list[int], pred: list[int]) -> float:
    return 0.5 * (binary_f1(gold, pred, 1) + binary_f1(gold, pred, 0))


def document_scores(gold: list[int], pred: list[int]) -> MetricBundle:
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
    n = len(gold)
    acc = (tp + tn) / n if n else 1.0
    p1, r1, f1 = _prf(tp, fp, fn)
    p0, r0, f0 = _prf(tn, fn, fp)
    return MetricBundle(
        n_pairs=n,
        n_true_change=sum(gold),
        n_pred_change=sum(pred),
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        accuracy=acc,
        precision=p1,
        recall=r1,
        f1=f1,
        macro_f1=0.5 * (f1 + f0),
        exact=gold == pred,
    )


def mean_bundle(bundles: list[MetricBundle]) -> dict[str, float]:
    if not bundles:
        return {}
    n = len(bundles)
    return {
        "documents": float(n),
        "accuracy": sum(b.accuracy for b in bundles) / n,
        "precision": sum(b.precision for b in bundles) / n,
        "recall": sum(b.recall for b in bundles) / n,
        "f1": sum(b.f1 for b in bundles) / n,
        "macro_f1": sum(b.macro_f1 for b in bundles) / n,
        "exact_match": sum(1.0 for b in bundles if b.exact) / n,
    }
