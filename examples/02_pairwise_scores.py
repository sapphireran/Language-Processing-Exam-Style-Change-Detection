#!/usr/bin/env python3
"""Lab 2: three distances plus the ensemble on one document."""

from __future__ import annotations

import argparse

from pathlib import Path

from _paths import CORPUS
from splicefind.detect import detect_text
from splicefind.io import infer_problem_id, load_truth


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "document",
        nargs="?",
        default=str(CORPUS / "problem-14-grandma-and-landlord.txt"),
    )
    parser.add_argument("--threshold", type=float, default=0.55)
    args = parser.parse_args()
    path = Path(args.document)
    text = path.read_text(encoding="utf-8")
    detection = detect_text(text, threshold=args.threshold)
    pid = infer_problem_id(path)
    truth_path = CORPUS / "truth" / f"truth-problem-{pid}.json"
    gold = load_truth(truth_path).changes if truth_path.is_file() else None

    print(f"{'i':>3}  feat   delta  ngram  cusum   ens  pred  gold")
    for boundary in detection.boundaries:
        g = "" if gold is None else str(gold[boundary.index])
        print(
            f"{boundary.index:3}  {boundary.feature_distance:5.3f}  "
            f"{boundary.delta:5.3f}  {boundary.ngram_distance:5.3f}  "
            f"{boundary.cusum_score:5.3f}  {boundary.ensemble:5.3f}  "
            f"{boundary.decision:4}  {g:>4}"
        )
        print(f"     L: {boundary.left_preview}")
        print(f"     R: {boundary.right_preview}")


if __name__ == "__main__":
    main()
