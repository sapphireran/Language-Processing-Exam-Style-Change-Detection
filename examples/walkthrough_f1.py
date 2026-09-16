#!/usr/bin/env python3
"""Worked F1 arithmetic for a three-boundary document.

Gold 1 0 1 and a hypothetical prediction 1 1 0:

    TP=1  FP=1  FN=1  TN=0
    P = 1/2    R = 1/2    F1 = 1/2

If the system instead emits all zeros, TP=0 FP=0 FN=2 and F1 = 0,
*unless* gold is also all zeros, in which case PAN-style document F1 is 1.
"""

from __future__ import annotations

from scdkit.evaluate import binary_scores, macro_f1


def show(name: str, gold: list[int], pred: list[int]) -> None:
    s = binary_scores(gold, pred)
    print(
        f"{name:28} gold={gold} pred={pred}  "
        f"P={s.precision:.2f} R={s.recall:.2f} F1={s.f1:.2f}  "
        f"tp={s.tp} fp={s.fp} tn={s.tn} fn={s.fn}"
    )


def main() -> int:
    show("mixed error", [1, 0, 1], [1, 1, 0])
    show("perfect", [1, 0, 1], [1, 0, 1])
    show("all-zero on a change doc", [1, 0, 1], [0, 0, 0])
    show("all-zero on single author", [0, 0, 0], [0, 0, 0])
    show("false alarm only", [0, 0, 0], [0, 1, 0])
    print()
    print(
        "macro-F1 of the five rows above:",
        f"{macro_f1([([1,0,1],[1,1,0]), ([1,0,1],[1,0,1]), ([1,0,1],[0,0,0]), ([0,0,0],[0,0,0]), ([0,0,0],[0,1,0])]):.3f}",
    )
    print("That last average is why one sloppy single-author document hurts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
