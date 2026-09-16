#!/usr/bin/env python3
"""Lab 00 — units and hinges on the canal file."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.io import read_problem, read_truth, truth_path_for


def main() -> int:
    path = ROOT / "examples/corpus/problem-01-canal-then-lot.txt"
    problem = read_problem(path)
    truth = read_truth(truth_path_for(path, ROOT / "examples/corpus/truth"))
    print(f"{path.name}: {len(problem.units)} units, {problem.n_hinges} hinges")
    for i, unit in enumerate(problem.units):
        print(f"{i:02d}  {unit}")
    print("gold", list(truth.changes))
    print("authors", list(truth.authors or ()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
