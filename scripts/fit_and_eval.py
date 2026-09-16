#!/usr/bin/env python3
"""Fit logistic + threshold models and write solution files for every split."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.detectors import LogisticDetector, ThresholdDetector, UnsupervisedDetector  # noqa: E402
from stylechange.detectors import save_model  # noqa: E402
from stylechange.evaluate import evaluate_dirs  # noqa: E402
from stylechange.io import load_problem_dir, solution_path, write_solution  # noqa: E402


def dump_solutions(detector, problems, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for problem in problems:
        write_solution(solution_path(out_dir, problem.pid), detector.predict_document(problem.sentences))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT / "data" / "synthetic"))
    parser.add_argument("--models", default=str(ROOT / "models"))
    parser.add_argument("--output", default=str(ROOT / "output"))
    args = parser.parse_args()

    train = load_problem_dir(args.root, require_truth=True, split="train")
    logistic = LogisticDetector().fit(train)
    threshold = ThresholdDetector().fit(train)
    unsupervised = UnsupervisedDetector()

    models = Path(args.models)
    save_model(logistic, models / "logistic.json")
    save_model(threshold, models / "threshold.json")
    save_model(unsupervised, models / "unsupervised.json")

    for difficulty in ("easy", "medium", "hard"):
        problems = load_problem_dir(Path(args.root) / difficulty, require_truth=True)
        for name, detector in (
            ("always0", None),
            ("unsupervised", unsupervised),
            ("threshold", threshold),
            ("logistic", logistic),
        ):
            out = Path(args.output) / f"{difficulty}-{name}"
            if name == "always0":
                from stylechange.detectors import AlwaysZeroDetector

                dump_solutions(AlwaysZeroDetector(), problems, out)
            else:
                dump_solutions(detector, problems, out)
            result = evaluate_dirs(str(Path(args.root) / difficulty), str(out))
            print(f"{difficulty}-{name}: macro_f1={result.pooled['macro_f1']:.3f} acc={result.pooled['accuracy']:.3f}")
    print(f"models written under {models}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
