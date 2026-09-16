#!/usr/bin/env python3
"""Grid a fixed threshold on Easy+Medium, then report Hard+Control honestly."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.corpus import load_teaching_corpus
from seamtrace.detectors import ThresholdDetector
from seamtrace.evaluate import score_pairs


def pool(docs, detector, tiers: set[str]):
    gold: list[int] = []
    pred: list[int] = []
    for doc in docs:
        if doc.tier not in tiers:
            continue
        gold.extend(doc.changes)
        pred.extend(detector.predict(doc.table()))
    return score_pairs(gold, pred)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--grid", default="0.30,0.34,0.38,0.42,0.46")
    args = p.parse_args()
    docs = load_teaching_corpus()
    tune = {"easy", "medium"}
    hold = {"hard", "control"}
    print(f"{'tau':>6}  {'tune':>6}  {'hold':>6}  {'hard':>6}  {'ctrl':>6}")
    for raw in args.grid.split(","):
        tau = float(raw)
        det = ThresholdDetector(threshold=tau)
        t = pool(docs, det, tune)
        h = pool(docs, det, hold)
        hard = pool(docs, det, {"hard"})
        ctrl = pool(docs, det, {"control"})
        print(
            f"{tau:6.2f}  {t.macro_f1:6.3f}  {h.macro_f1:6.3f}  "
            f"{hard.macro_f1:6.3f}  {ctrl.macro_f1:6.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
