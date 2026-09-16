#!/usr/bin/env python3
"""Score every bundled problem and print the collection table."""

from __future__ import annotations

from pathlib import Path

from stylechange.evaluate import evaluate_collection, format_collection

HERE = Path(__file__).resolve().parent
DOCS = HERE / "documents"


def main() -> int:
    score = evaluate_collection(DOCS)
    print(format_collection(score))
    return 0 if score.n_exact == len(score.documents) else 1


if __name__ == "__main__":
    raise SystemExit(main())
