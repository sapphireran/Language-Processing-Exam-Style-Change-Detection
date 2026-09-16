#!/usr/bin/env python3
"""Walk one problem sentence-by-sentence (or paragraph-by-paragraph)."""

from __future__ import annotations

import argparse
from pathlib import Path

from stylechange.detector import debug_scores, detect, explain_lines
from stylechange.io import load_problem, load_truth, problem_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "documents" / "problem-exam-takehome.txt",
    )
    parser.add_argument("--granularity", default="auto")
    parser.add_argument("--threshold", type=float, default=1.00)
    parser.add_argument("--debug-voices", action="store_true")
    args = parser.parse_args()

    text = load_problem(args.document)
    detection = detect(
        text,
        granularity=args.granularity,  # type: ignore[arg-type]
        threshold=args.threshold,
    )
    print(args.document.name)
    truth = load_truth(args.document)
    if truth is not None:
        gold = [int(x) for x in truth["changes"]]
        print(f"id:     {problem_id(args.document)}")
        print(f"gold:   {gold}")
        print(f"pred:   {detection.changes}")
        print(f"match:  {gold == detection.changes}")
        if truth.get("note"):
            print(f"note:   {truth['note']}")
        print()
    if args.debug_voices:
        print("\n".join(debug_scores(detection)))
        print()
    print("\n".join(explain_lines(detection)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
