#!/usr/bin/env python3
"""Lab 3: CUSUM sparkline. A kink is a hint, not a verdict."""

from __future__ import annotations

import argparse

from _paths import CORPUS
from splicefind.cusum import ascii_sparkline, sentence_length_trace
from splicefind.features import extract_document
from splicefind.cusum import paragraph_feature_trace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "document",
        nargs="?",
        default=str(CORPUS / "problem-08-minutes-then-chat.txt"),
    )
    args = parser.parse_args()
    text = open(args.document, encoding="utf-8", newline="").read()
    sent = sentence_length_trace(text)
    print("sentence-length values:", " ".join(f"{v:.0f}" for v in sent.values))
    print("sentence-length CUSUM: ", ascii_sparkline(sent.cusum))
    print("labels:                ", " ".join(sent.labels))
    print()
    doc = extract_document(text)
    para = paragraph_feature_trace(doc.vectors, "avg_sent_len")
    print("paragraph avg_sent_len:", " ".join(f"{v:.1f}" for v in para.values))
    print("paragraph CUSUM:       ", ascii_sparkline(para.cusum))
    print()
    print("Minutes-then-chat should jump sentence length after the cut.")
    print("Do not testify from the sparkline. Score it with labels.")


if __name__ == "__main__":
    main()
