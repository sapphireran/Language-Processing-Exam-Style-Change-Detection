"""Paper-sized calculations that must stay exact."""

from __future__ import annotations

from .evaluate import accuracy_trap, score_pairs


def trap_numbers() -> dict[str, float]:
    trap = accuracy_trap()
    report = score_pairs(trap.gold, trap.pred)
    return {
        "accuracy": report.accuracy,
        "hold_precision": report.hold.precision,
        "hold_recall": report.hold.recall,
        "hold_f1": report.hold.f1,
        "change_f1": report.change.f1,
        "macro_f1": report.macro_f1,
        "tn": float(report.tn),
        "fn": float(report.fn),
        "tp": float(report.tp),
        "fp": float(report.fp),
    }


def type_token_ratio(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)
