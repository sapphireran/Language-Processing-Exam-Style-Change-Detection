#!/usr/bin/env python3
"""Lab 09 — gift abstract vs exam paste."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.explain import explain_document, format_explanation
from hingemark.io import read_problem, read_truth, truth_path_for


def show(name: str) -> None:
    path = ROOT / "examples/corpus" / f"{name}.txt"
    problem = read_problem(path)
    truth = read_truth(truth_path_for(path, ROOT / "examples/corpus/truth"))
    print(format_explanation(explain_document(problem.text, gold=truth.changes, authors=truth.authors)))
    print()


def main() -> int:
    show("problem-25-tidepool-gift-abstract")
    show("problem-26-exam-two-answers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
