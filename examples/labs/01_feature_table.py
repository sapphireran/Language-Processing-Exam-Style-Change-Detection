#!/usr/bin/env python3
"""Lab 01 — register table for quince-letter vs River control."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.features import extract
from hingemark.io import read_problem

SHOW = ("i_rate", "you_rate", "vocative_rate", "digit_rate", "semi_rate", "hedge_rate")


def dump(label: str, path: Path) -> None:
    problem = read_problem(path)
    print(f"\n== {label} ==")
    print(f"{'i':>2} " + " ".join(f"{n:>12}" for n in SHOW) + "  text")
    for i, unit in enumerate(problem.units):
        feat = extract(unit)
        vals = " ".join(f"{getattr(feat, n):12.3f}" for n in SHOW)
        print(f"{i:02d} {vals}  {unit[:48]}")


def main() -> int:
    dump("medium quince (should move at hinge 2)", ROOT / "examples/corpus/problem-08-quince-batch-then-letter.txt")
    dump("control River (should not move)", ROOT / "examples/corpus/problem-19-river-three-topics.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
