"""Binary boundary scores and collection-level macro-F1.

PAN 2023 scores each document with F1 over the binary ``changes``
vector, then macro-averages those document F1s. That is *not* the same
as pooling every boundary and computing one micro-F1 — a short
single-author document counts as much as a long collage.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

from .detect import detect_changes
from .io import Truth, iter_collection


@dataclass(frozen=True)
class BinaryScore:
    precision: float
    recall: float
    f1: float
    accuracy: float
    tp: int
    fp: int
    tn: int
    fn: int
    n: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1": round(self.f1, 4),
            "accuracy": round(self.accuracy, 4),
            "tp": self.tp,
            "fp": self.fp,
            "tn": self.tn,
            "fn": self.fn,
            "n": self.n,
        }


@dataclass(frozen=True)
class DocumentScore:
    name: str
    gold: tuple[int, ...]
    pred: tuple[int, ...]
    score: BinaryScore
    difficulty: str | None = None


@dataclass(frozen=True)
class CollectionScore:
    documents: tuple[DocumentScore, ...]
    macro: BinaryScore
    micro: BinaryScore
    macro_f1: float

    def as_dict(self) -> dict:
        return {
            "macro_f1": round(self.macro_f1, 4),
            "macro": self.macro.as_dict(),
            "micro": self.micro.as_dict(),
            "documents": [
                {
                    "name": doc.name,
                    "difficulty": doc.difficulty,
                    "gold": list(doc.gold),
                    "pred": list(doc.pred),
                    **doc.score.as_dict(),
                }
                for doc in self.documents
            ],
        }


def _prf(tp: int, fp: int, tn: int, fn: int) -> BinaryScore:
    n = tp + fp + tn + fn
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    # PAN-style convention used in several student write-ups: an all-zero
    # gold *and* all-zero prediction is a perfect document (F1 = 1).
    if tp == 0 and fp == 0 and fn == 0:
        precision = recall = f1 = 1.0
    accuracy = (tp + tn) / n if n else 1.0
    return BinaryScore(precision, recall, f1, accuracy, tp, fp, tn, fn, n)


def confusion(gold: Sequence[int], pred: Sequence[int]) -> tuple[int, int, int, int]:
    if len(gold) != len(pred):
        raise ValueError("gold/pred length mismatch")
    tp = fp = tn = fn = 0
    for g, p in zip(gold, pred, strict=True):
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 0 and p == 0:
            tn += 1
        else:
            fn += 1
    return tp, fp, tn, fn


def binary_scores(gold: Sequence[int], pred: Sequence[int]) -> BinaryScore:
    tp, fp, tn, fn = confusion(gold, pred)
    return _prf(tp, fp, tn, fn)


def macro_f1(pairs: Iterable[tuple[Sequence[int], Sequence[int]]]) -> float:
    scores = [binary_scores(gold, pred).f1 for gold, pred in pairs]
    return sum(scores) / len(scores) if scores else 0.0


def evaluate_predictions(
    items: Iterable[tuple[str, Sequence[int], Sequence[int], str | None]],
) -> CollectionScore:
    docs: list[DocumentScore] = []
    tp = fp = tn = fn = 0
    f1s: list[float] = []
    precs: list[float] = []
    recs: list[float] = []
    accs: list[float] = []
    for name, gold, pred, difficulty in items:
        score = binary_scores(gold, pred)
        docs.append(
            DocumentScore(
                name=name,
                gold=tuple(gold),
                pred=tuple(pred),
                score=score,
                difficulty=difficulty,
            )
        )
        tp += score.tp
        fp += score.fp
        tn += score.tn
        fn += score.fn
        f1s.append(score.f1)
        precs.append(score.precision)
        recs.append(score.recall)
        accs.append(score.accuracy)
    micro = _prf(tp, fp, tn, fn)
    n = len(docs)
    macro = BinaryScore(
        precision=sum(precs) / n if n else 0.0,
        recall=sum(recs) / n if n else 0.0,
        f1=sum(f1s) / n if n else 0.0,
        accuracy=sum(accs) / n if n else 0.0,
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        n=n,
    )
    return CollectionScore(
        documents=tuple(docs),
        macro=macro,
        micro=micro,
        macro_f1=macro.f1,
    )


def evaluate_collection(
    document_dir: str | Path,
    truth_dir: str | Path | None = None,
    method: str = "ensemble",
    detector: Callable[[str], list[int]] | None = None,
) -> CollectionScore:
    predict = detector or (lambda text: detect_changes(text, method=method))
    items: list[tuple[str, list[int], list[int], str | None]] = []
    for path, text, truth in iter_collection(document_dir, truth_dir):
        pred = predict(text)
        items.append((path.name, list(truth.changes), pred, truth.difficulty))
    return evaluate_predictions(items)


def format_table(score: CollectionScore) -> str:
    headers = ("document", "gold", "pred", "P", "R", "F1")
    rows = [
        (
            doc.name,
            "".join(str(x) for x in doc.gold),
            "".join(str(x) for x in doc.pred),
            f"{doc.score.precision:.2f}",
            f"{doc.score.recall:.2f}",
            f"{doc.score.f1:.2f}",
        )
        for doc in score.documents
    ]
    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(w, len(cell)) for w, cell in zip(widths, row, strict=True)]
    def fmt(row: Sequence[str]) -> str:
        return "  ".join(cell.ljust(w) for cell, w in zip(row, widths, strict=True))
    lines = [fmt(headers), "  ".join("-" * w for w in widths)]
    lines.extend(fmt(row) for row in rows)
    lines.append("")
    lines.append(
        f"macro-F1 {score.macro_f1:.3f}   "
        f"macro-P {score.macro.precision:.3f}   "
        f"macro-R {score.macro.recall:.3f}   "
        f"micro-F1 {score.micro.f1:.3f}"
    )
    return "\n".join(lines)


def gold_from_authors(paragraph_authors: Sequence[int]) -> list[int]:
    return [
        0 if paragraph_authors[i] == paragraph_authors[i + 1] else 1
        for i in range(len(paragraph_authors) - 1)
    ]


def authors_from_changes(changes: Sequence[int], start: int = 1) -> list[int]:
    """Greedy new-author assignment (A B C …); cannot recover returning authors."""
    labels = [start]
    nxt = start + 1
    for flag in changes:
        if flag:
            labels.append(nxt)
            nxt += 1
        else:
            labels.append(labels[-1])
    return labels
