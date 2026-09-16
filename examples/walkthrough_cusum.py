#!/usr/bin/env python3
"""Hand calculation from docs/04, then the same arithmetic on a study file."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.cusum import ascii_cusum, cusum_points, cusum_series, mean  # noqa: E402
from examscd.tokenize import split_sentences  # noqa: E402

from _paths import DOCS  # noqa: E402


def show(title: str, values: list[int]) -> None:
    mu = mean([float(v) for v in values])
    incs = [v - mu for v in values]
    series = cusum_series(values)
    print(f"\n=== {title} ===")
    print(f"x      {values}")
    print(f"mean   {mu:.4f}")
    print(f"x-μ    {[round(v, 3) for v in incs]}")
    print(f"S      {[round(v, 3) for v in series]}")
    print(f"hits   {cusum_points(values)}")
    print(ascii_cusum(values))


def main() -> int:
    # The series I memorise. Mean 11, cut after sentence 4.
    show("memorised series (docs/04)", [4, 5, 4, 5, 18, 16, 17, 19])
    text = (DOCS / "02_recipe_then_maillard.txt").read_text(encoding="utf-8")
    values = [len(s.split()) for s in split_sentences(text)]
    show("02_recipe_then_maillard", values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
