#!/usr/bin/env python3
"""Lab 03 — CUSUM peak vs gold hinge."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.cusum import cusum_trace
from hingemark.io import read_problem, read_truth, truth_path_for
from hingemark.pairwise import score_unit_hinges


def main() -> int:
    path = ROOT / "examples/corpus/problem-22-canal-return.txt"
    problem = read_problem(path)
    truth = read_truth(truth_path_for(path, ROOT / "examples/corpus/truth"))
    hinges = score_unit_hinges(problem.units)
    scores = [h.blend for h in hinges]
    trace = cusum_trace(scores)
    print("scores", [round(s, 3) for s in scores])
    print("cusum ", [round(v, 3) for v in trace.values])
    print("peak  ", trace.peak_index, "value", round(trace.peak_value, 3))
    print("gold  ", list(truth.changes))
    print("note: two snaps (A-B and B-A). CUSUM peak is a picture, not a cut.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
