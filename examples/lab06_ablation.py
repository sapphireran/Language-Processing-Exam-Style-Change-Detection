#!/usr/bin/env python3
"""Lab 06 — drop one ensemble channel at a time.

This is a cheap leave-one-family-out: we reuse the same pair scores and
re-decide without that channel's vote. It is not a retrained model.
"""

from __future__ import annotations

from _paths import DOC_DIR, TRUTH_DIR

from scdkit.detect import THRESHOLDS, explain_document
from scdkit.evaluate import evaluate_predictions, format_table
from scdkit.io import iter_collection

CHANNELS = (
    "formality",
    "contraction",
    "person",
    "pronoun",
    "register",
    "marker",
    "delta",
    "char",
    "sentlen",
    "cusum",
)


def _decide(pair, dropped: str | None) -> int:
    votes = strong = 0
    for name in CHANNELS:
        if name == dropped:
            continue
        value = getattr(pair, name if name != "sentlen" else "sentlen")
        if value >= THRESHOLDS[f"{name}_strong"]:
            votes += 1
            strong += 1
        elif value >= THRESHOLDS[name]:
            votes += 1
    return 1 if (strong >= 1 or votes >= 2) else 0


def _run(dropped: str | None):
    items = []
    for path, text, truth in iter_collection(DOC_DIR, TRUTH_DIR):
        detection = explain_document(text)
        pred = [_decide(pair, dropped) for pair in detection.pairs]
        items.append((path.name, list(truth.changes), pred, truth.difficulty))
    return evaluate_predictions(items)


def main() -> int:
    print("dropped     macro-F1  micro-F1")
    print("---------   --------  --------")
    full = _run(None)
    print(f"{'none':<10}  {full.macro_f1:8.3f}  {full.micro.f1:8.3f}")
    for name in CHANNELS:
        score = _run(name)
        print(f"{name:<10}  {score.macro_f1:8.3f}  {score.micro.f1:8.3f}")
    print()
    print("Full collection (no drop):")
    print(format_table(full))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
