#!/usr/bin/env python3
"""Put eight exam-explainable baselines on every study file."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.compare import compare_methods, format_table  # noqa: E402
from examscd.io import read_text, read_truth  # noqa: E402

from _paths import load_manifest  # noqa: E402


def main() -> int:
    for item in load_manifest():
        text = read_text(item["text"])
        truth = read_truth(item["truth"])
        print(f"\n## {item['id']}  gold={truth.changes}")
        rows = compare_methods(text, truth.changes, granularity=truth.granularity)
        print(format_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
