#!/usr/bin/env python3
"""Lab 07 — topic Jaccard versus style Delta on easy vs hard documents."""

from __future__ import annotations

from _paths import DOC_DIR, TRUTH_DIR

from scdkit.detect import explain_document
from scdkit.io import iter_collection


def main() -> int:
    print(f"{'document':<32} pair  gold  topic  delta  form   note")
    for path, text, truth in iter_collection(DOC_DIR, TRUTH_DIR):
        if path.stem not in {
            "02_easy_bikes_then_vellum",
            "04_hard_circadian",
            "09_magnets_kid_vs_paper",
            "01_single_ferns",
        }:
            continue
        detection = explain_document(text)
        for pair, gold in zip(detection.pairs, truth.changes, strict=True):
            note = ""
            if gold == 1 and pair.topic < 0.75:
                note = "style change, shared topic"
            elif gold == 1 and pair.topic >= 0.75:
                note = "style + topic both jump"
            elif gold == 0 and pair.topic >= 0.85:
                note = "same author, new nouns"
            print(
                f"{path.stem:<32} {pair.index + 1}->{pair.index + 2}   {gold}   "
                f"{pair.topic:5.2f} {pair.delta:6.2f} {pair.formality:5.2f}  {note}"
            )
    print()
    print("The easy PAN split lets a topic model look like a style model.")
    print("The hard split is the one that earns the method its name.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
