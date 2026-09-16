#!/usr/bin/env python3
"""Print scalar features for each unit of one teaching document."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.features import FeatureTable
from seamtrace.io import load_problem

SHOW = (
    "n_words",
    "avg_word_len",
    "ttr",
    "first_person_rate",
    "second_person_rate",
    "contraction_rate",
    "hedge_rate",
    "digit_rate",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path")
    args = p.parse_args()
    problem = load_problem(args.path)
    table = FeatureTable.from_units(problem.units)
    header = f"{'i':>3}  " + "  ".join(f"{name:>16}" for name in SHOW)
    print(header)
    for i, unit in enumerate(table.units):
        cells = "  ".join(f"{unit.scalars[name]:16.3f}" for name in SHOW)
        print(f"{i:3}  {cells}")
        print(f"     {unit.text[:88]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
