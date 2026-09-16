#!/usr/bin/env python3
"""Split a PAN-style file and refuse to count hinges as n."""

from __future__ import annotations

from _paths import CORPUS, ROOT  # noqa: E402

from quoin.io import read_problem  # noqa: E402
from quoin.tokenize import word_count  # noqa: E402

FILES = [
    "problem-01-press-then-notice.txt",
    "problem-19-press-three-topics.txt",
    "problem-27-solo-press.txt",
]


def main() -> None:
    print(f"repo {ROOT}")
    print(f"{'file':<42} {'paras':>5} {'hinges':>7} {'words':>6}")
    print("-" * 64)
    for name in FILES:
        problem = read_problem(CORPUS / name)
        words = sum(word_count(p) for p in problem.paragraphs)
        print(f"{name:<42} {problem.n_paragraphs:5d} {problem.n_boundaries:7d} {words:6d}")
        for i, paragraph in enumerate(problem.paragraphs):
            preview = " ".join(paragraph.split())[:72]
            print(f"   [{i}] {word_count(paragraph):3d}w  {preview}...")
        print()
    print("hinges are n_paragraphs - 1. The last paragraph has no right neighbour.")


if __name__ == "__main__":
    main()
