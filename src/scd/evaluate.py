"""Macro-F1 evaluation over pairwise style-change labels."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score, precision_recall_fscore_support

from scd.io import (
    FormatError,
    check_alignment,
    list_problems,
    problem_id,
    read_problem,
    read_solution,
    read_truth,
)
from scd.sentences import split_units


def macro_f1(y_true: list[int] | np.ndarray, y_pred: list[int] | np.ndarray) -> float:
    if len(y_true) != len(y_pred):
        raise FormatError(
            f"label length mismatch: truth {len(y_true)} vs pred {len(y_pred)}"
        )
    if len(y_true) == 0:
        return 0.0
    return float(
        f1_score(y_true, y_pred, average="macro", zero_division=0, labels=[0, 1])
    )


def class_report(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=[0, 1], zero_division=0
    )
    return {
        "f1_0": float(f1[0]),
        "f1_1": float(f1[1]),
        "p_0": float(precision[0]),
        "p_1": float(precision[1]),
        "r_0": float(recall[0]),
        "r_1": float(recall[1]),
        "support_0": float(support[0]),
        "support_1": float(support[1]),
        "macro_f1": (float(f1[0]) + float(f1[1])) / 2.0,
    }


@dataclass(frozen=True)
class DocScore:
    problem_id: str
    n_units: int
    n_pairs: int
    positive_rate: float
    macro_f1: float
    y_true: list[int]
    y_pred: list[int]


@dataclass(frozen=True)
class DirectoryScores:
    n_docs: int
    n_pairs: int
    positive_rate: float
    macro_f1: float
    mean_doc_macro_f1: float
    per_document: list[DocScore]

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n_docs": self.n_docs,
            "n_pairs": self.n_pairs,
            "positive_rate": self.positive_rate,
            "macro_f1": self.macro_f1,
            "mean_doc_macro_f1": self.mean_doc_macro_f1,
        }


def evaluate_directory(
    pred_dir: str | Path,
    truth_dir: str | Path,
    *,
    mode: str = "line",
    id_min: int | None = None,
    id_max: int | None = None,
) -> DirectoryScores:
    truth_dir = Path(truth_dir)
    pred_dir = Path(pred_dir)
    problems = list_problems(truth_dir)
    if id_min is not None or id_max is not None:
        filtered = []
        for problem in problems:
            pid = problem_id(problem)
            numeric = int(pid) if pid.isdigit() else None
            if numeric is None:
                continue
            if id_min is not None and numeric < id_min:
                continue
            if id_max is not None and numeric > id_max:
                continue
            filtered.append(problem)
        problems = filtered
    if not problems:
        raise FormatError(f"no problem-*.txt files in {truth_dir}")

    all_true: list[int] = []
    all_pred: list[int] = []
    per_doc: list[DocScore] = []

    for problem in problems:
        pid = problem_id(problem)
        truth_path = truth_dir / f"truth-problem-{pid}.json"
        pred_path = pred_dir / f"solution-problem-{pid}.json"
        if not truth_path.exists():
            raise FormatError(f"missing truth for problem {pid}: {truth_path}")
        if not pred_path.exists():
            raise FormatError(f"missing solution for problem {pid}: {pred_path}")

        units = split_units(read_problem(problem), mode=mode)
        y_true = read_truth(truth_path).changes
        y_pred = read_solution(pred_path)
        check_alignment(len(units), y_true, path=truth_path)
        if len(y_pred) != len(y_true):
            raise FormatError(
                f"{pred_path}: expected {len(y_true)} labels, got {len(y_pred)}"
            )

        doc_f1 = macro_f1(y_true, y_pred) if y_true else 0.0
        positive = sum(y_true) / len(y_true) if y_true else 0.0
        per_doc.append(
            DocScore(
                problem_id=pid,
                n_units=len(units),
                n_pairs=len(y_true),
                positive_rate=positive,
                macro_f1=doc_f1,
                y_true=y_true,
                y_pred=y_pred,
            )
        )
        all_true.extend(y_true)
        all_pred.extend(y_pred)

    docs_with_pairs = [doc for doc in per_doc if doc.n_pairs]
    mean_doc = (
        float(np.mean([doc.macro_f1 for doc in docs_with_pairs]))
        if docs_with_pairs
        else 0.0
    )
    return DirectoryScores(
        n_docs=len(per_doc),
        n_pairs=len(all_true),
        positive_rate=(sum(all_true) / len(all_true)) if all_true else 0.0,
        macro_f1=macro_f1(all_true, all_pred),
        mean_doc_macro_f1=mean_doc,
        per_document=per_doc,
    )


def bootstrap_doc_f1(
    scores: DirectoryScores,
    *,
    n_boot: int = 200,
    seed: int = 0,
) -> tuple[float, float]:
    """Document-level bootstrap percentile interval for global macro F1."""
    docs = [doc for doc in scores.per_document if doc.n_pairs]
    if not docs:
        return (0.0, 0.0)
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_boot):
        draw = rng.integers(0, len(docs), size=len(docs))
        y_true: list[int] = []
        y_pred: list[int] = []
        for index in draw:
            y_true.extend(docs[int(index)].y_true)
            y_pred.extend(docs[int(index)].y_pred)
        values.append(macro_f1(y_true, y_pred))
    lo, hi = np.percentile(values, [2.5, 97.5])
    return (float(lo), float(hi))
