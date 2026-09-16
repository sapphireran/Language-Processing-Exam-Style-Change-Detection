#!/usr/bin/env python3
"""Fit on train, score every detector on every difficulty split."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.detectors import (  # noqa: E402
    AlwaysZeroDetector,
    EnsembleDetector,
    LogisticDetector,
    ThresholdDetector,
    UnsupervisedDetector,
)
from stylechange.evaluate import evaluate_aligned  # noqa: E402
from stylechange.io import load_problem_dir  # noqa: E402


def predict_map(detector, problems):
    return {item.pid: detector.predict_document(item.sentences) for item in problems}


def gold_map(problems):
    return {item.pid: item.changes or [] for item in problems}


def main() -> int:
    train = load_problem_dir(ROOT / "data" / "synthetic", require_truth=True, split="train")
    if not train:
        print("no train problems; did you generate data/synthetic?", file=sys.stderr)
        return 2

    logistic = LogisticDetector()
    logistic.fit(train)
    threshold = ThresholdDetector()
    threshold.fit(train)
    ensemble = EnsembleDetector()
    ensemble.fit(train)

    detectors = [
        AlwaysZeroDetector(),
        UnsupervisedDetector(),
        threshold,
        logistic,
        ensemble,
    ]

    print(f"{'split':<8} {'detector':<14} {'acc':>6} {'f1_0':>6} {'f1_1':>6} {'macro':>6} {'io':>3}")
    print("-" * 56)
    for difficulty in ("easy", "medium", "hard"):
        problems = load_problem_dir(ROOT / "data" / "synthetic" / difficulty, require_truth=True)
        gold = gold_map(problems)
        for detector in detectors:
            result = evaluate_aligned(gold, predict_map(detector, problems))
            p = result.pooled
            print(
                f"{difficulty:<8} {detector.name:<14} "
                f"{p['accuracy']:6.3f} {p['f1_0']:6.3f} {p['f1_1']:6.3f} "
                f"{p['macro_f1']:6.3f} {len(result.io_failures):3d}"
            )
        print()
    print("Train documents:", len(train))
    print("Threshold k after sweep:", round(threshold.k, 3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
