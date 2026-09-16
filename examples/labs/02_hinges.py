#!/usr/bin/env python3
"""Lab 02 — blend table for one easy hit and one hard miss."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.explain import explain_document, format_explanation
from hingemark.io import read_problem, read_truth, truth_path_for


def show(rel: str) -> None:
    path = ROOT / rel
    problem = read_problem(path)
    truth = read_truth(truth_path_for(path, ROOT / "examples/corpus/truth"))
    exp = explain_document(problem.text, gold=truth.changes, authors=truth.authors)
    print(format_explanation(exp))
    print()


def main() -> int:
    show("examples/corpus/problem-01-canal-then-lot.txt")
    show("examples/corpus/problem-13-two-mycologists.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
