#!/usr/bin/env python3
"""Lab 04 — CUSUM of word length, sentence length, and formality."""

from __future__ import annotations

import argparse
from pathlib import Path

from _paths import DOC_DIR, REPORT_DIR

from scdkit.cusum import (
    formality_cusum,
    sentence_length_cusum,
    svg_polyline,
    word_length_cusum,
)
from scdkit.features import extract_many
from scdkit.io import load_document
from scdkit.tokenize import split_paragraphs


def _print(series) -> None:
    print(f"{series.name:14} mean={series.mean:6.2f}  path=" + " ".join(f"{v:+6.2f}" for v in series.cusum))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document",
        nargs="?",
        default=str(DOC_DIR / "08_minutes_then_slack.txt"),
    )
    parser.add_argument("--svg-out", default="")
    args = parser.parse_args()
    feats = extract_many(split_paragraphs(load_document(args.document)))
    series = (
        word_length_cusum(feats),
        sentence_length_cusum(feats),
        formality_cusum(feats),
    )
    for s in series:
        _print(s)
    dest = Path(args.svg_out) if args.svg_out else REPORT_DIR / f"cusum_{Path(args.document).stem}.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        "<div>\n" + "\n".join(svg_polyline(s) for s in series) + "\n</div>\n",
        encoding="utf-8",
    )
    print(f"wrote {dest}")
    print()
    print("Exam prompt: CUSUM uses the document mean as its baseline. Why does")
    print("that make a one-change document easier to see than a document that")
    print("alternates every paragraph?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
