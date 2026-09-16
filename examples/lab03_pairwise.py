#!/usr/bin/env python3
"""Lab 03 — adjacent distances, including the topic-confound channel."""

from __future__ import annotations

import argparse

from pathlib import Path

from _paths import DOC_DIR, TRUTH_DIR

from scdkit.detect import explain_document
from scdkit.io import load_document, load_truth


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document",
        nargs="?",
        default=str(DOC_DIR / "02_easy_bikes_then_vellum.txt"),
    )
    args = parser.parse_args()
    detection = explain_document(load_document(args.document))
    gold = None
    truth_path = TRUTH_DIR / f"{Path(args.document).stem}.json"
    if truth_path.is_file():
        gold = list(load_truth(truth_path).changes)
    print("pair   gold pred  form   reg   pron  contr  char  topic  reasons")
    for pair in detection.pairs:
        g = "-" if gold is None else str(gold[pair.index])
        print(
            f"{pair.index + 1}->{pair.index + 2}    {g:>3} {pair.change:>4}  "
            f"{pair.formality:5.2f} {pair.register:5.2f} {pair.pronoun:5.2f} "
            f"{pair.contraction:5.2f} {pair.char:5.2f} {pair.topic:5.2f}  "
            f"{'; '.join(pair.reasons) or '—'}"
        )
    print()
    print("On the easy document, `topic` and `form` should both spike at the")
    print("same boundary. On 04_hard_circadian, `topic` should stay high")
    print("everywhere (same content words) while Delta / formality still move.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
