"""Macro-F1 over hinge labels, plus the two liars an oral needs.

Never-fire looks accurate on a bank that is mostly zeros. Always-fire
looks busy. Macro-F1 is the only number I am allowed to quote as
'good' without a caveat.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Confusion:
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

    def precision(self, positive: int) -> float:
        if positive == 1:
            denom = self.tp + self.fp
            return self.tp / denom if denom else 0.0
        denom = self.tn + self.fn
        return self.tn / denom if denom else 0.0

    def recall(self, positive: int) -> float:
        if positive == 1:
            denom = self.tp + self.fn
            return self.tp / denom if denom else 0.0
        denom = self.tn + self.fp
        return self.tn / denom if denom else 0.0

    def f1(self, positive: int) -> float:
        p = self.precision(positive)
        r = self.recall(positive)
        return 0.0 if (p + r) == 0 else 2 * p * r / (p + r)


def confusion(gold: list[int], pred: list[int]) -> Confusion:
    if len(gold) != len(pred):
        raise ValueError(f"length mismatch: gold={len(gold)} pred={len(pred)}")
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
    return Confusion(tp=tp, fp=fp, tn=tn, fn=fn)


def macro_f1(gold: list[int], pred: list[int]) -> float:
    table = confusion(gold, pred)
    return (table.f1(0) + table.f1(1)) / 2


def score_changes(gold: list[int], pred: list[int]) -> dict[str, float | int]:
    table = confusion(gold, pred)
    return {
        "n": table.support,
        "tp": table.tp,
        "fp": table.fp,
        "tn": table.tn,
        "fn": table.fn,
        "accuracy": table.accuracy,
        "f1_same": table.f1(0),
        "f1_change": table.f1(1),
        "macro_f1": (table.f1(0) + table.f1(1)) / 2,
    }


def never_fire(n: int) -> list[int]:
    return [0] * n


def always_fire(n: int) -> list[int]:
    return [1] * n
