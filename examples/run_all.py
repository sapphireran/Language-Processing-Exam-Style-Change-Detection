#!/usr/bin/env python3
"""Run every lab script in exam order."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = [
    "00_split_and_count.py",
    "01_feature_table.py",
    "02_pairwise_scores.py",
    "03_cusum_trace.py",
    "04_score_corpus.py",
    "05_calibrate_threshold.py",
    "06_ablate_channels.py",
    "07_topic_confound.py",
    "08_pan_roundtrip.py",
    "09_generate_synthetic.py",
    "10_write_reports.py",
]


def main() -> None:
    for name in SCRIPTS:
        path = HERE / name
        print()
        print("=" * 72)
        print(name)
        print("=" * 72)
        runpy.run_path(str(path), run_name="__main__")
    print()
    print(f"ran {len(SCRIPTS)} example scripts")


if __name__ == "__main__":
    sys.exit(main())
