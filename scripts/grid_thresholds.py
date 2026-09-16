#!/usr/bin/env python3
"""Sweep τ after the fact. Not a claim that we did this before looking."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inkfold.corpus import iter_problems  # noqa: E402
from inkfold.detectors import EnsembleDetector  # noqa: E402
from inkfold.evaluate import score_folder  # noqa: E402


def main() -> int:
    problems = iter_problems()
    print(f"{'τ':>6} {'acc':>7} {'macroF1':>8} {'meanF1':>8} {'fp':>4} {'fn':>4}")
    for tau in (0.20, 0.24, 0.28, 0.30, 0.32, 0.36, 0.40, 0.45):
        folder = score_folder(problems, EnsembleDetector(threshold=tau))
        s = folder.overall
        print(
            f"{tau:6.2f} {s.accuracy:7.3f} {s.macro_f1:8.3f} "
            f"{folder.mean_macro_f1():8.3f} {s.fp:4d} {s.fn:4d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
