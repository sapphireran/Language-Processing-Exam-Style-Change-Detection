#!/usr/bin/env python3
"""Walk one document boundary-by-boundary.

Use this when you want to *see* the stylometric jump, not just the 0/1 labels.
The default file is the exam-answer mash-up: student prose, pasted textbook,
lecture notes.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stylechange import StyleChangeDetector  # noqa: E402
from stylechange.io import load_problem  # noqa: E402

DEFAULT = Path(__file__).resolve().parent / "documents" / "problem-exam-answer-shift.txt"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT)
    parser.add_argument("--granularity", choices=("sentence", "paragraph"), default="sentence")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--window", type=int, default=2)
    args = parser.parse_args()

    problem = load_problem(args.path)
    kwargs = {"granularity": args.granularity, "window": args.window}
    if args.threshold is not None:
        kwargs["threshold"] = args.threshold
    detector = StyleChangeDetector(**kwargs)
    prediction = detector.predict(problem.text, explain=True)

    gold = problem.truth.changes if problem.truth else None
    print(f"file:   {args.path}")
    print(f"units:  {len(prediction.units)}")
    print(f"pred:   {prediction.changes}")
    if gold is not None:
        print(f"gold:   {gold}")
    print()

    for item in prediction.explanations:
        gold_bit = ""
        if gold is not None and item.index < len(gold):
            gold_bit = "  gold=" + ("CHANGE" if gold[item.index] else "same")
        mark = "CHANGE" if item.change else "same  "
        print(f"boundary {item.index}  {mark}  score={item.score:.3f}{gold_bit}")
        print(f"  left : {item.left_text}")
        print(f"  right: {item.right_text}")
        print(
            "  mix  : "
            + "  ".join(
                f"{name}={item.parts[name]:.3f}"
                for name in ("register", "function", "personal", "academic", "telegram")
                if name in item.parts
            )
        )
        if item.register_left:
            print(
                "  axis : "
                + "  ".join(
                    f"{name} {item.register_left[name]:.2f}->{item.register_right[name]:.2f}"
                    for name in ("personal", "academic", "telegram")
                )
            )
        print(
            "  top Δ: "
            + ", ".join(f"{name}={delta:.3f}" for name, delta in item.top_deltas[:4])
        )
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
