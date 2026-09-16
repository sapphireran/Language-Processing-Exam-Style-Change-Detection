"""Hinge-level scores. Accuracy is the liar; macro-F1 is the adult."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .detect import Detection, detect_path
from .io import paired_files, read_truth


@dataclass(frozen=True)
class HingeScores:
    tp: int
    fp: int
    tn: int
    fn: int
    accuracy: float
    precision: float
    recall: float
    f1_change: float
    f1_same: float
    macro_f1: float
    n_hinges: int
    n_docs: int = 1


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _f1(prec: float, rec: float) -> float:
    return _safe_div(2 * prec * rec, prec + rec)


def hinge_confusion(pred: list[int], gold: list[int]) -> tuple[int, int, int, int]:
    if len(pred) != len(gold):
        raise ValueError(f"hinge length mismatch: {len(pred)} vs {len(gold)}")
    tp = fp = tn = fn = 0
    for p, g in zip(pred, gold):
        if p and g:
            tp += 1
        elif p and not g:
            fp += 1
        elif (not p) and (not g):
            tn += 1
        else:
            fn += 1
    return tp, fp, tn, fn


def hinge_macro_f1(pred: list[int], gold: list[int]) -> HingeScores:
    tp, fp, tn, fn = hinge_confusion(pred, gold)
    n = len(pred)
    acc = _safe_div(tp + tn, n)
    prec_c = _safe_div(tp, tp + fp)
    rec_c = _safe_div(tp, tp + fn)
    prec_s = _safe_div(tn, tn + fn)
    rec_s = _safe_div(tn, tn + fp)
    f1_c = _f1(prec_c, rec_c)
    f1_s = _f1(prec_s, rec_s)
    return HingeScores(
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        accuracy=acc,
        precision=prec_c,
        recall=rec_c,
        f1_change=f1_c,
        f1_same=f1_s,
        macro_f1=0.5 * (f1_c + f1_s),
        n_hinges=n,
    )


def score_detection(det: Detection, gold: list[int]) -> HingeScores:
    return hinge_macro_f1(det.changes, gold)


def score_directory(
    directory: str | Path,
    penalty: float | None = None,
    adj_abs: float | None = None,
) -> dict[str, object]:
    kwargs = {}
    if penalty is not None:
        kwargs["penalty"] = penalty
    if adj_abs is not None:
        kwargs["adj_abs"] = adj_abs
    rows: list[dict[str, object]] = []
    pred_all: list[int] = []
    gold_all: list[int] = []
    for problem_path, truth_path in paired_files(directory):
        det = detect_path(problem_path, **kwargs)
        truth = read_truth(truth_path)
        gold = truth.changes
        if len(gold) != len(det.changes):
            raise ValueError(
                f"{problem_path.name}: predicted {len(det.changes)} hinges, truth has {len(gold)}"
            )
        scores = hinge_macro_f1(det.changes, gold)
        rows.append(
            {
                "id": problem_path.stem,
                "n_para": len(det.paragraphs),
                "pred": det.changes,
                "gold": gold,
                "reasons": det.cut_reason,
                "split": [round(s, 4) for s in det.split_scores],
                "adjacent": [round(s, 4) for s in det.adjacent],
                "macro_f1": scores.macro_f1,
                "accuracy": scores.accuracy,
                "tp": scores.tp,
                "fp": scores.fp,
                "fn": scores.fn,
                "tn": scores.tn,
            }
        )
        pred_all.extend(det.changes)
        gold_all.extend(gold)
    overall = hinge_macro_f1(pred_all, gold_all) if pred_all else hinge_macro_f1([], [])
    # Baselines on the same stacked hinges.
    never = hinge_macro_f1([0] * len(gold_all), gold_all) if gold_all else overall
    always = hinge_macro_f1([1] * len(gold_all), gold_all) if gold_all else overall
    mean_acc = sum(r["accuracy"] for r in rows) / len(rows) if rows else 0.0
    mean_f1 = sum(r["macro_f1"] for r in rows) / len(rows) if rows else 0.0
    return {
        "n_docs": len(rows),
        "n_hinges": overall.n_hinges,
        "overall": overall,
        "never": never,
        "always": always,
        "mean_doc_accuracy": mean_acc,
        "mean_doc_macro_f1": mean_f1,
        "rows": rows,
    }
