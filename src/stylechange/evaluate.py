"""Macro-F1 over consecutive-unit change / no-change labels.

PAN reports a macro-averaged F1 so the majority class (almost always
*no change*) cannot hide a detector that never fires. We compute that
document-wise and also pooled over a whole folder of problems.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .detector import detect
from .io import iter_problems, load_problem, load_truth, solution_path, write_solution
from .tokenize import Granularity


def _f1(true_pos: int, pred_pos: int, gold_pos: int) -> float:
    if pred_pos == 0 and gold_pos == 0:
        return 1.0
    precision = true_pos / pred_pos if pred_pos else 0.0
    recall = true_pos / gold_pos if gold_pos else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def macro_f1(gold: list[int], pred: list[int]) -> float:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    scores = []
    for label in (0, 1):
        true_pos = sum(g == label and p == label for g, p in zip(gold, pred))
        pred_pos = sum(p == label for p in pred)
        gold_pos = sum(g == label for g in gold)
        scores.append(_f1(true_pos, pred_pos, gold_pos))
    return sum(scores) / 2.0


def pair_accuracy(gold: list[int], pred: list[int]) -> float:
    if not gold:
        return 1.0
    if len(gold) != len(pred):
        raise ValueError("length mismatch")
    return sum(g == p for g, p in zip(gold, pred)) / len(gold)


@dataclass
class DocumentScore:
    problem_id: str
    gold: list[int]
    pred: list[int]
    f1: float
    accuracy: float

    @property
    def match(self) -> bool:
        return self.gold == self.pred


@dataclass
class CollectionScore:
    documents: list[DocumentScore]

    @property
    def macro_f1(self) -> float:
        gold = [label for doc in self.documents for label in doc.gold]
        pred = [label for doc in self.documents for label in doc.pred]
        return macro_f1(gold, pred) if gold else 1.0

    @property
    def accuracy(self) -> float:
        gold = [label for doc in self.documents for label in doc.gold]
        pred = [label for doc in self.documents for label in doc.pred]
        return pair_accuracy(gold, pred)

    @property
    def n_pairs(self) -> int:
        return sum(len(doc.gold) for doc in self.documents)

    @property
    def n_exact(self) -> int:
        return sum(1 for doc in self.documents if doc.match)


def evaluate_collection(
    directory: Path | str,
    *,
    output_dir: Path | str | None = None,
    granularity: Granularity = "auto",
    threshold: float = 1.00,
) -> CollectionScore:
    root = Path(directory)
    out = Path(output_dir) if output_dir is not None else None
    rows: list[DocumentScore] = []
    for problem in iter_problems(root):
        truth = load_truth(problem)
        if truth is None or "changes" not in truth:
            raise FileNotFoundError(f"missing truth for {problem.name}")
        gold = [int(x) for x in truth["changes"]]
        text = load_problem(problem)
        detection = detect(text, granularity=granularity, threshold=threshold)
        pred = detection.changes
        if out is not None:
            write_solution(solution_path(problem, out), pred)
        rows.append(
            DocumentScore(
                problem_id=problem.stem.removeprefix("problem-"),
                gold=gold,
                pred=pred,
                f1=macro_f1(gold, pred) if len(gold) == len(pred) else 0.0,
                accuracy=pair_accuracy(gold, pred) if len(gold) == len(pred) else 0.0,
            )
        )
    return CollectionScore(rows)


def format_collection(score: CollectionScore) -> str:
    header = f"{'id':<32} {'gold':<28} {'pred':<28} {'match':<5} {'F1'}"
    lines = [header, "-" * len(header)]
    for doc in score.documents:
        lines.append(
            f"{doc.problem_id:<32} {str(doc.gold):<28} {str(doc.pred):<28} "
            f"{'yes' if doc.match else 'no':<5} {doc.f1:.3f}"
        )
    lines.append("")
    lines.append(
        f"collection macro-F1={score.macro_f1:.3f}  "
        f"accuracy={score.accuracy:.3f}  "
        f"pairs={score.n_pairs}  "
        f"exact={score.n_exact}/{len(score.documents)}"
    )
    return "\n".join(lines)
