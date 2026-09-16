#!/usr/bin/env python3
"""Run the lab sequence and the collection score in one sitting."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    "lab01_split_and_count.py",
    "lab02_feature_table.py",
    "lab03_pairwise.py",
    "lab04_cusum.py",
    "lab05_score_collection.py",
    "lab06_ablation.py",
    "lab07_topic_confound.py",
    "walkthrough_f1.py",
]


def main() -> int:
    for name in STEPS:
        print("=" * 72)
        print(name)
        print("=" * 72)
        runpy.run_path(str(HERE / name), run_name="__main__")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
