#!/usr/bin/env python3
"""One document through the detector, with gold bits beside the guess."""

from __future__ import annotations

import argparse

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402
from quoin.evaluate import safe_f1  # noqa: E402
from quoin.io import read_problem  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="problem-01-press-then-notice")
    args = parser.parse_args()
    corpus = load_corpus(CORPUS)
    try:
        item = corpus.get(args.name)
        problem, gold = item.problem, item.truth.changes
        band = item.band
    except KeyError:
        problem = read_problem(args.name)
        gold = None
        band = "?"
    detector = QuoinDetector()
    rows = detector.boundaries(problem.paragraphs)
    print(f"{problem.path.name}   band={band}   t={detector.threshold}")
    print(f"{'b':>3} {'quoin':>7} {'reg':>7} {'res':>7} pred gold")
    pred = []
    for row in rows:
        g = "" if gold is None else str(gold[row.index])
        pred.append(row.pred)
        print(
            f"{row.index:3d} {row.quoin:7.3f} {row.register_l1:7.3f} "
            f"{row.residual:7.3f} {row.pred:4d} {g:>4}"
        )
    if gold is not None:
        print(f"F1 {safe_f1(gold, pred):.3f}   gold {gold}   pred {pred}")


if __name__ == "__main__":
    main()
