#!/usr/bin/env python3
"""Lab 07 — topic held vs topic moved."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.detectors import DEFAULT_THRESHOLD, threshold_detect
from hingemark.evaluate import score_pairs
from hingemark.pairwise import score_unit_hinges


def score_named(name: str):
    item = next(it for it in list_corpus() if name in it.name)
    pred = threshold_detect(
        score_unit_hinges(item.problem.units), threshold=DEFAULT_THRESHOLD
    ).changes
    report = score_pairs(item.truth.changes, pred)
    return item, pred, report


def main() -> int:
    held, pred_h, rh = score_named("quince-batch-then-letter")
    moved, pred_m, rm = score_named("river-three-topics")
    print(f"{held.name} gold={list(held.truth.changes)} pred={list(pred_h)} mF1={rh.macro_f1:.3f}")
    print(f"{moved.name} gold={list(moved.truth.changes)} pred={list(pred_m)} mF1={rm.macro_f1:.3f}")
    if pred_h == held.truth.changes and sum(pred_m) == 0:
        print("ok: same-topic register snap found; topic-only control stayed quiet.")
        return 0
    print("not the teaching inequality — check the blender.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
