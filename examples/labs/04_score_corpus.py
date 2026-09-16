#!/usr/bin/env python3
"""Lab 04 — full curriculum table."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.detectors import DEFAULT_THRESHOLD
from hingemark.report import evaluate_items, format_corpus_table


def main() -> int:
    items = list_corpus()
    scored = evaluate_items(items)
    print(format_corpus_table(items, scored, DEFAULT_THRESHOLD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
