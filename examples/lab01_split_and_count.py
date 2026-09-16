#!/usr/bin/env python3
"""Lab 01 — split a document and count the cheap stylometric handles.

Run::

    python examples/lab01_split_and_count.py examples/documents/02_easy_bikes_then_vellum.txt
"""

from __future__ import annotations

import argparse

from _paths import DOC_DIR, SRC  # noqa: F401

from scdkit.io import load_document
from scdkit.tokenize import split_paragraphs, split_sentences, split_words


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document",
        nargs="?",
        default=str(DOC_DIR / "02_easy_bikes_then_vellum.txt"),
    )
    args = parser.parse_args()
    paragraphs = split_paragraphs(load_document(args.document))
    print(f"{len(paragraphs)} paragraphs  (gold changes length should be {len(paragraphs) - 1})")
    print()
    for i, para in enumerate(paragraphs, start=1):
        words = split_words(para)
        sents = split_sentences(para)
        mean_w = sum(len(w) for w in words) / len(words) if words else 0
        print(f"P{i}  sents={len(sents):2d}  words={len(words):3d}  mean_word_len={mean_w:.2f}")
        print(f"    {sents[0][:88]}{'…' if sents and len(sents[0]) > 88 else ''}")
    print()
    print("Exam prompt: why is a paragraph splitter part of the *task definition*,")
    print("not just a preprocessing detail?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
