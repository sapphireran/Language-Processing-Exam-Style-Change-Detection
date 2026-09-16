#!/usr/bin/env python3
"""Print stylometric columns and ensemble distances for one problem file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from style_change.detectors import build_detector  # noqa: E402
from style_change.io import load_problem  # noqa: E402
from style_change.report import distance_table, feature_table, problem_card  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=str(ROOT / "examples/sample_problems/easy/problem-001.txt"),
    )
    parser.add_argument("--detector", default="ensemble")
    args = parser.parse_args()
    problem = load_problem(args.path)
    detector = build_detector(args.detector)
    pred = detector.predict(problem.paragraphs)
    print(problem_card(problem, pred=pred))
    print()
    print(feature_table(problem.paragraphs))
    print()
    print(distance_table(problem.paragraphs, detector=detector))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
