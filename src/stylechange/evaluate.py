"""Macro-F1 evaluation used by PAN-style style-change tasks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .io import iter_problems, iter_solutions


@dataclass(frozen=True)
class EvaluationResult:
    accuracy: float
    precision: float
    recall: float
    f1_positive: float
    f1_negative: float
    macro_f1: float
    pairs: int
    documents: int
    skipped: int = 0

    def as_dict(self) -> dict[str, float | int]:
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_positive": self.f1_positive,
            "f1_negative": self.f1_negative,
            "macro_f1": self.macro_f1,
            "pairs": self.pairs,
            "documents": self.documents,
            "skipped": self.skipped,
        }


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _prf(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return precision, recall, _f1(precision, recall)


def evaluate_changes(
    gold: Sequence[Sequence[int]],
    predicted: Sequence[Sequence[int]],
) -> EvaluationResult:
    """Macro-F1 over every consecutive-unit pair in the collection."""
    if len(gold) != len(predicted):
        raise ValueError("gold and predicted document counts differ")

    tp = fp = tn = fn = 0
    skipped = 0
    documents = 0
    for truth, guess in zip(gold, predicted):
        if len(truth) != len(guess):
            skipped += 1
            continue
        documents += 1
        for y, y_hat in zip(truth, guess):
            if y == 1 and y_hat == 1:
                tp += 1
            elif y == 0 and y_hat == 1:
                fp += 1
            elif y == 0 and y_hat == 0:
                tn += 1
            else:
                fn += 1

    pairs = tp + fp + tn + fn
    accuracy = (tp + tn) / pairs if pairs else 0.0
    precision, recall, f1_pos = _prf(tp, fp, fn)
    # Negative class: "no change"
    precision_neg, recall_neg, f1_neg = _prf(tn, fn, fp)
    return EvaluationResult(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_positive=f1_pos,
        f1_negative=f1_neg,
        macro_f1=0.5 * (f1_pos + f1_neg),
        pairs=pairs,
        documents=documents,
        skipped=skipped,
    )


def evaluate_dataset(gold_dir: str | Path, pred_dir: str | Path) -> EvaluationResult:
    """Compare ``truth-problem-*.json`` (or gold solutions) with predictions."""
    gold_map = {}
    for problem in iter_problems(gold_dir):
        if problem.truth is None:
            continue
        gold_map[problem.problem_id] = problem.truth.changes
    # Also accept a directory that only contains truth/solution files.
    if not gold_map:
        gold_map = {pid: sol.changes for pid, sol in iter_solutions(gold_dir).items()}

    pred_map = {pid: sol.changes for pid, sol in iter_solutions(pred_dir).items()}
    ids = sorted(set(gold_map) & set(pred_map))
    if not ids:
        raise ValueError(f"no overlapping problem ids between {gold_dir} and {pred_dir}")
    return evaluate_changes([gold_map[i] for i in ids], [pred_map[i] for i in ids])
