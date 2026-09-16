#!/usr/bin/env python3
"""Fit the decision threshold on synthetic exam answers, then score the hand files.

The stylometric detector is unsupervised at prediction time. Calibration only
chooses the cutoff. This script shows the loop you would run if you later
swap in PAN training files.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stylechange import StyleChangeDetector, evaluate_changes  # noqa: E402
from stylechange.generate import generate_split  # noqa: E402
from stylechange.io import iter_problems  # noqa: E402

DOC_DIR = Path(__file__).resolve().parent / "documents"


def main() -> int:
    synthetic = generate_split(n_per_level=10, seed=21)
    detector = StyleChangeDetector()
    before = detector.threshold
    threshold = detector.calibrate(
        [doc.text for doc in synthetic],
        [doc.truth.changes for doc in synthetic],
    )
    print(f"calibrated threshold: {before:.3f} -> {threshold:.3f}")
    print(f"synthetic documents:  {len(synthetic)}")

    by_level: dict[str, tuple[list[list[int]], list[list[int]]]] = {}
    for doc in synthetic:
        gold, pred = by_level.setdefault(doc.difficulty, ([], []))
        gold.append(doc.truth.changes)
        pred.append(detector.predict_changes(doc.text))

    print("\nsynthetic hold-in scores (same split the threshold was fit on):")
    for level in ("easy", "medium", "hard", "single"):
        gold, pred = by_level[level]
        result = evaluate_changes(gold, pred)
        print(
            f"  {level:<8} macro-F1={result.macro_f1:.3f}  "
            f"acc={result.accuracy:.3f}  pairs={result.pairs}"
        )

    gold = []
    pred = []
    print("\nhand-written example documents (not used for calibration):")
    for problem in iter_problems(DOC_DIR):
        if problem.truth is None:
            continue
        if problem.truth.extra.get("granularity") == "paragraph":
            continue
        guess = detector.predict_changes(problem.text)
        gold.append(problem.truth.changes)
        pred.append(guess)
        mark = "ok" if guess == problem.truth.changes else "diff"
        print(f"  {problem.problem_id:<24} {mark:4}  gold={problem.truth.changes}  pred={guess}")

    result = evaluate_changes(gold, pred)
    print(
        f"\nhand-file macro-F1={result.macro_f1:.3f}  "
        f"accuracy={result.accuracy:.3f}  pairs={result.pairs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
