#!/usr/bin/env python3
"""Print the three compressed lengths so the formula card can be finished by hand."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.io import read_problem  # noqa: E402
from quoin.ncd import compressed_len, cross_gain, ncd  # noqa: E402
from quoin.tokenize import word_count  # noqa: E402


def show(label: str, left: str, right: str) -> None:
    c_left = compressed_len(left)
    c_right = compressed_len(right)
    c_both = compressed_len(left + "\n" + right)
    print(f"## {label}")
    print(f"words     {word_count(left)} / {word_count(right)}")
    print(f"C(x)      {c_left}")
    print(f"C(y)      {c_right}")
    print(f"C(xy)     {c_both}")
    print(f"NCD       {ncd(left, right):.4f}   = (C(xy) - min(C(x),C(y))) / max(C(x),C(y))")
    print(f"gain      {cross_gain(left, right):.4f}")
    print()


def main() -> None:
    problem = read_problem(CORPUS / "problem-01-press-then-notice.txt")
    p = problem.paragraphs
    show("press vs press (should be cheaper)", p[0], p[1])
    show("notice vs notice (should be cheaper)", p[2], p[3])
    show("press vs notice (the exam hinge)", p[1], p[2])


if __name__ == "__main__":
    main()
