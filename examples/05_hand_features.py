#!/usr/bin/env python3
"""Programmatic counterpart to the paper-and-pencil worked example.

docs/06-worked-example.md counts contractions and length by hand on
easy/problem-1.txt. This script prints the library's exact pairwise
cues so the note and the code cannot silently drift.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.features import pairwise_feature_map, unit_feature_map, words
from scd.io import read_problem, read_truth
from scd.sentences import split_units

PROBLEM = ROOT / "examples" / "data" / "easy" / "problem-1.txt"
TRUTH = ROOT / "examples" / "data" / "easy" / "truth-problem-1.json"

UNIT_CUES = (
    "n_words",
    "avg_word_len",
    "contraction_rate",
    "first_person_rate",
    "second_person_rate",
    "function_word_rate",
    "exclaim",
)
PAIR_CUES = (
    "abs_contraction_rate",
    "abs_first_person_rate",
    "abs_n_words",
    "fw_cosine",
    "char_tri_cosine",
    "jaccard",
    "length_ratio",
)


def main() -> int:
    units = split_units(read_problem(PROBLEM), mode="line")
    changes = read_truth(TRUTH).changes
    print("Pinned easy/problem-1 — one sentence per line")
    print()
    for i, unit in enumerate(units, start=1):
        feats = unit_feature_map(unit)
        print(f"S{i}  ({len(words(unit))} tokens)")
        print(f"    {unit}")
        for name in UNIT_CUES:
            print(f"    {name:<22} {feats[name]:7.3f}")
        print()

    print("Pairwise cues  (the change should be pair 2–3, not the length jump)")
    print()
    widest_length = None
    onset_pairs: list[int] = []
    for i in range(len(units) - 1):
        pair = pairwise_feature_map(units[i], units[i + 1])
        left = unit_feature_map(units[i])
        right = unit_feature_map(units[i + 1])
        label = "CHANGE" if changes[i] else "same"
        print(f"pair {i + 1}–{i + 2}  truth={changes[i]} ({label})")
        for name in PAIR_CUES:
            print(f"    {name:<22} {pair[name]:7.3f}")
        print()
        if widest_length is None or pair["abs_n_words"] > widest_length[1]:
            widest_length = (i, pair["abs_n_words"])
        left_casual = left["contraction_rate"] > 0 or left["first_person_rate"] > 0
        right_casual = right["contraction_rate"] > 0 or right["first_person_rate"] > 0
        if left_casual != right_casual:
            onset_pairs.append(i)

    assert widest_length is not None
    print(
        f"largest |Δ n_words| is pair {widest_length[0] + 1}–{widest_length[0] + 2} "
        f"({widest_length[1]:.1f} words)"
    )
    if onset_pairs == [1]:
        print("casual-register onset (contraction / first person from zero) is pair 2–3")
        print("Those are different pairs: length is not the style-change task.")
    else:
        print(f"casual-register onset pairs: {[i + 1 for i in onset_pairs]} — re-check the pin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
