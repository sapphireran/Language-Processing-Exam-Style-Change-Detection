"""Metrics for the three style-change subtasks.

Task 1 uses accuracy / precision / recall / F1 on the multi-author bit.
Task 2 treats each inter-paragraph boundary as a binary item.
Task 3 is a clustering problem, so we report ARI and BCubed F1 rather
than raw label accuracy (label ids are arbitrary).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter, defaultdict
from collections.abc import Sequence
from itertools import combinations

from style_change.detectors import DetectionResult


@dataclass(frozen=True)
class BinaryScores:
    accuracy: float
    precision: float
    recall: float
    f1: float
    tp: int
    fp: int
    tn: int
    fn: int


@dataclass
class EvaluationReport:
    task1: BinaryScores
    task2: BinaryScores
    ari: float
    bcubed_f1: float
    bcubed_precision: float
    bcubed_recall: float
    n_paragraphs: int
    notes: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"Task 1 multi-author  acc={self.task1.accuracy:.3f}  P={self.task1.precision:.3f}  "
            f"R={self.task1.recall:.3f}  F1={self.task1.f1:.3f}",
            f"Task 2 boundaries    acc={self.task2.accuracy:.3f}  P={self.task2.precision:.3f}  "
            f"R={self.task2.recall:.3f}  F1={self.task2.f1:.3f}  "
            f"(tp={self.task2.tp} fp={self.task2.fp} fn={self.task2.fn})",
            f"Task 3 authors       ARI={self.ari:.3f}  BCubed P={self.bcubed_precision:.3f}  "
            f"R={self.bcubed_recall:.3f}  F1={self.bcubed_f1:.3f}",
            f"Paragraphs scored: {self.n_paragraphs}",
        ]
        if self.notes:
            lines.extend(f"Note: {note}" for note in self.notes)
        return "\n".join(lines)


def _binary_scores(pred: Sequence[bool], gold: Sequence[bool]) -> BinaryScores:
    if len(pred) != len(gold):
        raise ValueError(f"length mismatch: pred={len(pred)} gold={len(gold)}")
    tp = fp = tn = fn = 0
    for p, g in zip(pred, gold, strict=True):
        if p and g:
            tp += 1
        elif p and not g:
            fp += 1
        elif not p and not g:
            tn += 1
        else:
            fn += 1
    total = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total else 1.0
    if tp + fp + fn == 0:
        precision = recall = f1 = 1.0
    else:
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return BinaryScores(accuracy, precision, recall, f1, tp, fp, tn, fn)


def _comb2(n: int) -> int:
    return n * (n - 1) // 2 if n >= 2 else 0


def adjusted_rand_index(pred: Sequence[int], gold: Sequence[int]) -> float:
    """ARI on two labelings of the same items."""
    if len(pred) != len(gold):
        raise ValueError("label length mismatch")
    n = len(pred)
    if n < 2:
        return 1.0
    pred_counts = Counter(pred)
    gold_counts = Counter(gold)
    pair_counts: dict[tuple[int, int], int] = defaultdict(int)
    for p, g in zip(pred, gold, strict=True):
        pair_counts[(p, g)] += 1

    sum_comb_c = sum(_comb2(c) for c in pair_counts.values())
    sum_comb_pred = sum(_comb2(c) for c in pred_counts.values())
    sum_comb_gold = sum(_comb2(c) for c in gold_counts.values())
    total_pairs = _comb2(n)
    if total_pairs == 0:
        return 1.0
    expected = (sum_comb_pred * sum_comb_gold) / total_pairs
    max_index = 0.5 * (sum_comb_pred + sum_comb_gold)
    denom = max_index - expected
    if abs(denom) < 1e-12:
        return 1.0
    return (sum_comb_c - expected) / denom


def bcubed(pred: Sequence[int], gold: Sequence[int]) -> tuple[float, float, float]:
    """BCubed precision, recall, and F1."""
    if len(pred) != len(gold):
        raise ValueError("label length mismatch")
    n = len(pred)
    if n == 0:
        return 1.0, 1.0, 1.0

    pred_groups: dict[int, list[int]] = defaultdict(list)
    gold_groups: dict[int, list[int]] = defaultdict(list)
    for i, (p, g) in enumerate(zip(pred, gold, strict=True)):
        pred_groups[p].append(i)
        gold_groups[g].append(i)

    precision = 0.0
    recall = 0.0
    for i, (p, g) in enumerate(zip(pred, gold, strict=True)):
        cluster = pred_groups[p]
        truth = gold_groups[g]
        shared = sum(1 for j in cluster if gold[j] == g)
        precision += shared / len(cluster)
        shared_r = sum(1 for j in truth if pred[j] == p)
        recall += shared_r / len(truth)
    precision /= n
    recall /= n
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return precision, recall, f1


def authors_to_changes(authors: Sequence[int]) -> list[bool]:
    return [authors[i] != authors[i + 1] for i in range(len(authors) - 1)]


def evaluate_document(
    result: DetectionResult,
    gold_authors: Sequence[int],
    gold_multi: bool | None = None,
    gold_changes: Sequence[bool] | None = None,
) -> EvaluationReport:
    """Score one document. Gold author ids may use any integers."""
    notes: list[str] = []
    gold_authors = list(gold_authors)
    pred_authors = list(result.authors)

    if len(pred_authors) != len(gold_authors):
        raise ValueError(
            f"author length mismatch: pred={len(pred_authors)} gold={len(gold_authors)}"
        )

    if gold_multi is None:
        gold_multi = len(set(gold_authors)) > 1
    if gold_changes is None:
        gold_changes = authors_to_changes(gold_authors)

    pred_changes = list(result.changes)
    if len(pred_changes) != len(gold_changes):
        notes.append("falling back to author-derived change vector for Task 2")
        pred_changes = authors_to_changes(pred_authors)

    task1 = _binary_scores([result.multi_author], [gold_multi])
    task2 = _binary_scores(pred_changes, list(gold_changes))
    precision, recall, f1 = bcubed(pred_authors, gold_authors)
    ari = adjusted_rand_index(pred_authors, gold_authors)
    return EvaluationReport(
        task1=task1,
        task2=task2,
        ari=ari,
        bcubed_f1=f1,
        bcubed_precision=precision,
        bcubed_recall=recall,
        n_paragraphs=len(gold_authors),
        notes=notes + list(result.notes),
    )


def pairwise_agreement(labels: Sequence[int]) -> float:
    """Fraction of item pairs that share a label. Useful in notes."""
    n = len(labels)
    if n < 2:
        return 1.0
    same = sum(1 for i, j in combinations(range(n), 2) if labels[i] == labels[j])
    return same / _comb2(n)
