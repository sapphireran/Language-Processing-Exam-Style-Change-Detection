"""Boundary F1, the accuracy trap, and folder-level scoreboards."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .detectors import Detection, EnsembleDetector, never_fire
from .io import Problem


@dataclass
class BinaryScores:
    tp: int
    fp: int
    tn: int
    fn: int

    @property
    def support(self) -> int:
        return self.tp + self.fp + self.tn + self.fn

    @property
    def accuracy(self) -> float:
        return (self.tp + self.tn) / self.support if self.support else 0.0

    @property
    def precision_pos(self) -> float:
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) else 0.0

    @property
    def recall_pos(self) -> float:
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) else 0.0

    @property
    def f1_pos(self) -> float:
        p, r = self.precision_pos, self.recall_pos
        return 2 * p * r / (p + r) if (p + r) else 0.0

    @property
    def precision_neg(self) -> float:
        return self.tn / (self.tn + self.fn) if (self.tn + self.fn) else 0.0

    @property
    def recall_neg(self) -> float:
        return self.tn / (self.tn + self.fp) if (self.tn + self.fp) else 0.0

    @property
    def f1_neg(self) -> float:
        p, r = self.precision_neg, self.recall_neg
        return 2 * p * r / (p + r) if (p + r) else 0.0

    @property
    def macro_f1(self) -> float:
        return 0.5 * (self.f1_pos + self.f1_neg)


def confusion(gold: Sequence[int], pred: Sequence[int]) -> BinaryScores:
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
    return BinaryScores(tp=tp, fp=fp, tn=tn, fn=fn)


@dataclass
class DocumentScore:
    problem_id: str
    site: str
    gold_changes: list[int]
    pred_changes: list[int]
    gold_authors: int
    pred_authors: int
    scores: BinaryScores
    expected_error: str | None = None
    notes: str = ""

    @property
    def exact_boundaries(self) -> bool:
        return self.gold_changes == self.pred_changes

    @property
    def author_ok(self) -> bool:
        return self.gold_authors == self.pred_authors


def score_document(problem: Problem, detection: Detection) -> DocumentScore:
    gold = problem.truth.changes
    pred = detection.changes
    if len(pred) != len(gold):
        # Pad / trim so a broken detector still produces a row.
        if len(pred) < len(gold):
            pred = pred + [0] * (len(gold) - len(pred))
        else:
            pred = pred[: len(gold)]
    return DocumentScore(
        problem_id=problem.problem_id,
        site=problem.truth.site,
        gold_changes=list(gold),
        pred_changes=list(pred),
        gold_authors=problem.truth.authors,
        pred_authors=detection.authors,
        scores=confusion(gold, pred),
        expected_error=problem.truth.expected_error,
        notes=problem.truth.notes,
    )


def merge_scores(rows: Iterable[DocumentScore]) -> BinaryScores:
    tp = fp = tn = fn = 0
    for row in rows:
        tp += row.scores.tp
        fp += row.scores.fp
        tn += row.scores.tn
        fn += row.scores.fn
    return BinaryScores(tp=tp, fp=fp, tn=tn, fn=fn)


@dataclass
class FolderScore:
    rows: list[DocumentScore] = field(default_factory=list)

    def by_site(self) -> dict[str, BinaryScores]:
        buckets: dict[str, list[DocumentScore]] = {}
        for row in self.rows:
            buckets.setdefault(row.site, []).append(row)
        return {site: merge_scores(rs) for site, rs in sorted(buckets.items())}

    @property
    def overall(self) -> BinaryScores:
        return merge_scores(self.rows)

    def mean_macro_f1(self) -> float:
        if not self.rows:
            return 0.0
        return sum(r.scores.macro_f1 for r in self.rows) / len(self.rows)

    def never_baseline(self) -> BinaryScores:
        # Reconstruct gold and score a never-fire predictor.
        gold = [c for row in self.rows for c in row.gold_changes]
        pred = [0] * len(gold)
        return confusion(gold, pred)


def score_folder(problems: Sequence[Problem], detector: EnsembleDetector | None = None) -> FolderScore:
    det = detector or EnsembleDetector()
    rows = []
    for problem in problems:
        detection = det.detect(problem.units)
        rows.append(score_document(problem, detection))
    return FolderScore(rows=rows)


def accuracy_trap_demo(problems: Sequence[Problem]) -> dict[str, float]:
    """Show why accuracy is a bad exam answer on this corpus."""
    folder = FolderScore()
    for problem in problems:
        detection = never_fire(problem.units)
        folder.rows.append(score_document(problem, detection))
    never = folder.overall
    real = score_folder(problems).overall
    return {
        "n_boundaries": never.support,
        "n_changes": never.fn + never.tp,  # gold positives
        "never_accuracy": never.accuracy,
        "never_macro_f1": never.macro_f1,
        "detector_accuracy": real.accuracy,
        "detector_macro_f1": real.macro_f1,
    }
