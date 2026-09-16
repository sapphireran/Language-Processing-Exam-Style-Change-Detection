#!/usr/bin/env python3
"""Print units, truth cuts, and reconstructed author runs.

Default target is the pinned easy document from the worked example
(docs/06-worked-example.md). Pass a problem path to inspect another file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.io import check_alignment, problem_id, read_problem, read_truth, reconstruct_authors
from scd.sentences import split_units

DEFAULT = ROOT / "examples" / "data" / "easy" / "problem-1.txt"


def inspect(problem: Path, *, mode: str) -> None:
    units = split_units(read_problem(problem), mode=mode)
    truth_path = problem.with_name(f"truth-problem-{problem_id(problem)}.json")
    truth = read_truth(truth_path)
    check_alignment(len(units), truth.changes, path=truth_path)
    runs = reconstruct_authors(truth.changes)

    print(f"file     {problem.relative_to(ROOT)}")
    print(f"units    {len(units)}")
    print(f"authors  {truth.authors}  (reconstructed max run = {max(runs)})")
    print(f"changes  {truth.changes}")
    print()
    for i, unit in enumerate(units):
        print(f"[{i + 1}] run {runs[i]}")
        print(f"    {unit}")
        if i < len(truth.changes):
            label = "STYLE CHANGE" if truth.changes[i] else "same author"
            print(f"    ---- {label} ----")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", nargs="?", default=str(DEFAULT))
    parser.add_argument("--mode", default="line")
    args = parser.parse_args()
    inspect(Path(args.problem), mode=args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
