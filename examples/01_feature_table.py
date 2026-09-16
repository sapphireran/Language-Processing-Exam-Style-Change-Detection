#!/usr/bin/env python3
"""Lab 1: print the scalars you would defend in an oral."""

from __future__ import annotations

import argparse

from _paths import CORPUS
from splicefind.features import extract_document


FOCUS = (
    "avg_sent_len",
    "avg_word_len",
    "type_token_ratio",
    "first_person_rate",
    "second_person_rate",
    "impersonal_rate",
    "contraction_rate",
    "hedge_rate",
    "flesch_like",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "document",
        nargs="?",
        default=str(CORPUS / "problem-14-grandma-and-landlord.txt"),
    )
    args = parser.parse_args()
    text = open(args.document, encoding="utf-8", newline="").read()
    doc = extract_document(text)
    header = f"{'p':>3}  " + "  ".join(f"{name:>16}" for name in FOCUS)
    print(header)
    print("-" * len(header))
    for i, vector in enumerate(doc.vectors, start=1):
        cells = "  ".join(f"{vector.scalars[name]:16.3f}" for name in FOCUS)
        print(f"{i:3}  {cells}")
    print()
    print("Hand reading for 14: P1–P2 should show I/contractions;")
    print("P3–P4 should show longer sentences and a flatter first person.")


if __name__ == "__main__":
    main()
