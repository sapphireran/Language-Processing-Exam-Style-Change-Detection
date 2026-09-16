#!/usr/bin/env python3
"""Lab 06 — drop each blend channel and watch mean macro-F1 move."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.detectors import DEFAULT_THRESHOLD, threshold_detect
from hingemark.evaluate import score_corpus
from hingemark.pairwise import DEFAULT_BLEND, score_unit_hinges


def mean_f1(weights: tuple[float, float, float, float]) -> float:
    items = list_corpus()
    rows = []
    for item in items:
        hinges = score_unit_hinges(item.problem.units, blend_weights=weights)
        pred = threshold_detect(hinges, threshold=DEFAULT_THRESHOLD).changes
        rows.append((item.name, item.truth.changes, pred))
    return score_corpus(rows).mean_macro_f1


def main() -> int:
    names = ("register", "function-word", "char", "delta")
    print(f"full blend {DEFAULT_BLEND}: {mean_f1(DEFAULT_BLEND):.3f}")
    for i, name in enumerate(names):
        dropped = list(DEFAULT_BLEND)
        dropped[i] = 0.0
        rest = sum(dropped)
        norm = tuple(w / rest for w in dropped) if rest else DEFAULT_BLEND
        print(f"drop {name:14s} {norm}: {mean_f1(norm):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
