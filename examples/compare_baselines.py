#!/usr/bin/env python3
"""Score every built-in detector on the synthetic sample splits."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from style_change.detectors import DETECTORS, build_detector  # noqa: E402
from style_change.evaluate import evaluate_changes  # noqa: E402
from style_change.io import load_problem_dir  # noqa: E402

SPLITS = ("easy", "medium", "hard", "single_author")


def score_split(split: str, detector_name: str) -> tuple[float, float, int]:
    problems = load_problem_dir(ROOT / "examples/sample_problems" / split)
    detector = build_detector(detector_name)
    gold = {p.problem_id: p.gold_changes for p in problems}
    pred = {p.problem_id: detector.predict(p.paragraphs) for p in problems}
    result = evaluate_changes(gold, pred)
    return result.mean_macro_f1, result.pooled_macro_f1, len(result.documents)


def main() -> int:
    header = f"{'split':<16} {'detector':<16} {'mean F1':>8} {'pooled F1':>10} {'n':>4}"
    print(header)
    print("-" * len(header))
    for split in SPLITS:
        for name in sorted(DETECTORS):
            mean_f1, pooled_f1, n_docs = score_split(split, name)
            print(f"{split:<16} {name:<16} {mean_f1:8.3f} {pooled_f1:10.3f} {n_docs:4d}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
