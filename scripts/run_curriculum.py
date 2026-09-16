#!/usr/bin/env python3
"""Score every split and print a compact summary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.detectors import DEFAULT_THRESHOLD
from hingemark.evaluate import score_pairs
from hingemark.report import detect_item, evaluate_items, format_corpus_table


def main() -> int:
    items = list_corpus()
    scored = evaluate_items(items)
    print(format_corpus_table(items, scored, DEFAULT_THRESHOLD))
    print()
    splits: dict[str, list[float]] = {}
    for item in items:
        pred = detect_item(item).changes
        report = score_pairs(item.truth.changes, pred)
        splits.setdefault(item.split, []).append(report.macro_f1)
    print(f"{'split':<10} {'n':>3} {'mean mF1':>9}")
    for split, vals in splits.items():
        print(f"{split:<10} {len(vals):3d} {sum(vals)/len(vals):9.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
