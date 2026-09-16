"""Pair-level metrics, including the accuracy trap the exam likes to set."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class PairScores:
    precision: float
    recall: float
    f1: float
    support: int


@dataclass(frozen=True)
class BinaryReport:
    gold: tuple[int, ...]
    pred: tuple[int, ...]
    accuracy: float
    macro_f1: float
    change: PairScores
    hold: PairScores
    tp: int
    fp: int
    fn: int
    tn: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "accuracy": self.accuracy,
            "macro_f1": self.macro_f1,
            "change_p": self.change.precision,
            "change_r": self.change.recall,
            "change_f1": self.change.f1,
            "hold_f1": self.hold.f1,
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
            "tn": self.tn,
        }


@dataclass(frozen=True)
class CorpusScores:
    documents: int
    hinges: int
    micro: BinaryReport
    mean_macro_f1: float
    mean_accuracy: float
    per_document: tuple[tuple[str, BinaryReport], ...]


@dataclass(frozen=True)
class AccuracyTrap:
    gold: tuple[int, ...]
    pred: tuple[int, ...]
    accuracy: float
    macro_f1: float
    note: str


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _f1(p: float, r: float) -> float:
    return _safe_div(2 * p * r, p + r)


def score_pairs(gold: Sequence[int], pred: Sequence[int]) -> BinaryReport:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
    tp = fp = fn = tn = 0
    for g, p in zip(gold, pred):
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 1 and p == 0:
            fn += 1
        else:
            tn += 1
    change = PairScores(
        precision=_safe_div(tp, tp + fp),
        recall=_safe_div(tp, tp + fn),
        f1=_f1(_safe_div(tp, tp + fp), _safe_div(tp, tp + fn)),
        support=tp + fn,
    )
    hold = PairScores(
        precision=_safe_div(tn, tn + fn),
        recall=_safe_div(tn, tn + fp),
        f1=_f1(_safe_div(tn, tn + fn), _safe_div(tn, tn + fp)),
        support=tn + fp,
    )
    acc = _safe_div(tp + tn, len(gold))
    return BinaryReport(
        gold=tuple(gold),
        pred=tuple(pred),
        accuracy=acc,
        macro_f1=0.5 * (change.f1 + hold.f1),
        change=change,
        hold=hold,
        tp=tp,
        fp=fp,
        fn=fn,
        tn=tn,
    )


def score_corpus(
    items: Iterable[tuple[str, Sequence[int], Sequence[int]]],
) -> CorpusScores:
    rows: list[tuple[str, BinaryReport]] = []
    all_gold: list[int] = []
    all_pred: list[int] = []
    for name, gold, pred in items:
        report = score_pairs(gold, pred)
        rows.append((name, report))
        all_gold.extend(gold)
        all_pred.extend(pred)
    micro = score_pairs(all_gold, all_pred) if all_gold else score_pairs([], [])
    macros = [r.macro_f1 for _, r in rows]
    accs = [r.accuracy for _, r in rows]
    return CorpusScores(
        documents=len(rows),
        hinges=len(all_gold),
        micro=micro,
        mean_macro_f1=sum(macros) / len(macros) if macros else 0.0,
        mean_accuracy=sum(accs) / len(accs) if accs else 0.0,
        per_document=tuple(rows),
    )


def accuracy_trap() -> AccuracyTrap:
    """16 true holds + 4 missed changes: accuracy 0.80, macro-F1 0.444.

    This is the hand calculation the written paper likes. A never-fire
    detector looks competent on accuracy because holds dominate.
    """
    gold = (0,) * 16 + (1,) * 4
    pred = (0,) * 20
    report = score_pairs(gold, pred)
    return AccuracyTrap(
        gold=gold,
        pred=pred,
        accuracy=report.accuracy,
        macro_f1=report.macro_f1,
        note=(
            "TN=16 FP=0 FN=4 TP=0. Hold F1 = 2*0.8*1 / 1.8 = 0.889. "
            "Change F1 = 0. Macro-F1 = 0.444. Accuracy = 0.800."
        ),
    )
