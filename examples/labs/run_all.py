#!/usr/bin/env python3
"""Run the revision circuit. Fail on the first script that exits non-zero."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = [
    "00_split_and_count.py",
    "01_feature_table.py",
    "02_ncd_by_hand.py",
    "03_score_one.py",
    "04_score_corpus.py",
    "05_calibrate.py",
    "06_ablate.py",
    "07_topic_confound.py",
    "08_accuracy_trap.py",
    "09_explain_gift.py",
    "10_write_reports.py",
]


def main() -> int:
    for name in SCRIPTS:
        print("=" * 72)
        print(name)
        print("=" * 72)
        result = subprocess.run([sys.executable, str(HERE / name)], check=False)
        if result.returncode != 0:
            print(f"{name} failed with {result.returncode}", file=sys.stderr)
            return result.returncode
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
