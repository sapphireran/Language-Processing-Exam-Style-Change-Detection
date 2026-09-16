#!/usr/bin/env python3
"""Lab 02 — print the fingerprint table used by the ensemble."""

from __future__ import annotations

import argparse

from _paths import DOC_DIR

from scdkit.features import extract_features
from scdkit.io import load_document
from scdkit.tokenize import split_paragraphs

COLS = (
    ("P", 3),
    ("words", 5),
    ("sent", 5),
    ("contr", 6),
    ("I", 5),
    ("we", 5),
    ("you", 5),
    ("one", 5),
    ("form", 6),
    ("cas", 5),
    ("formality", 9),
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document",
        nargs="?",
        default=str(DOC_DIR / "03_medium_cph_rent.txt"),
    )
    args = parser.parse_args()
    paragraphs = split_paragraphs(load_document(args.document))
    header = "  ".join(name.ljust(width) for name, width in COLS)
    print(header)
    print("  ".join("-" * width for _, width in COLS))
    for i, para in enumerate(paragraphs, start=1):
        f = extract_features(para)
        cells = [
            str(i),
            str(f.n_words),
            f"{f.mean_sent_len:.1f}",
            f"{f.contraction_rate:.2f}",
            f"{f.pronoun_i:.2f}",
            f"{f.pronoun_we:.2f}",
            f"{f.pronoun_you:.2f}",
            f"{f.pronoun_one:.2f}",
            f"{f.formal_rate:.2f}",
            f"{f.casual_rate:.2f}",
            f"{f.formality:.2f}",
        ]
        print("  ".join(cell.ljust(width) for cell, (_, width) in zip(cells, COLS)))
    print()
    print("Exam prompt: which two columns would still move if we rewrote every")
    print("content word as a synonym? Those are the style channels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
