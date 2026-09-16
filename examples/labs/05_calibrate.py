#!/usr/bin/env python3
"""Lab 05 — threshold grid, top six rows."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.calibrate import grid_thresholds
from hingemark.corpus import list_corpus


def main() -> int:
    rows = grid_thresholds(list_corpus())
    print(f"{'tau':>6} {'mean F1':>8} {'micro F1':>8} {'acc':>6}")
    for row in rows[:6]:
        print(
            f"{row.threshold:6.2f} {row.mean_macro_f1:8.3f} "
            f"{row.micro_macro_f1:8.3f} {row.mean_accuracy:6.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
