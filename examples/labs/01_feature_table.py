#!/usr/bin/env python3
"""Print the tally sheet I would almost do on paper."""

from __future__ import annotations

import argparse

from _paths import CORPUS  # noqa: E402

from quoin.features import vectorize  # noqa: E402
from quoin.io import read_problem  # noqa: E402
from quoin.ncd import compressed_len  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(CORPUS / "problem-01-press-then-notice.txt"))
    args = parser.parse_args()
    problem = read_problem(args.path)
    print(problem.path.name)
    print(
        f"{'i':>3} {'words':>6} {'sent':>6} {'ttr':>6} {'contr':>7} "
        f"{'form':>7} {'inf':>7} {'C':>6}"
    )
    for i, paragraph in enumerate(problem.paragraphs):
        vec = vectorize(paragraph)
        print(
            f"{i:3d} {vec.n_words:6d} {vec.shape['mean_sentence']:6.1f} "
            f"{vec.shape['ttr']:6.3f} {vec.shape['contraction']:7.3f} "
            f"{vec.shape['formal']:7.3f} {vec.shape['informal']:7.3f} "
            f"{compressed_len(paragraph):6d}"
        )
    print()
    print("Look for shall / hereby in 'form', gonna / kinda in 'inf',")
    print("and a jump in mean sentence length at the house change.")


if __name__ == "__main__":
    main()
