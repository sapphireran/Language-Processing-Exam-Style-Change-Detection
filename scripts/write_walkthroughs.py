#!/usr/bin/env python3
"""Refresh spotlight markdown walkthroughs from live detector numbers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.report import write_walkthrough_markdown

SPOT = (
    "canal-then-lot",
    "quince-batch-then-letter",
    "two-mycologists",
    "river-three-topics",
    "spark-three-chats",
    "canal-return",
    "tidepool-gift-abstract",
    "exam-two-answers",
)


def main() -> int:
    dest = ROOT / "examples/walkthroughs"
    dest.mkdir(parents=True, exist_ok=True)
    written = 0
    for item in list_corpus():
        if not any(s in item.name for s in SPOT):
            continue
        write_walkthrough_markdown(item, dest / f"{item.name}.md")
        print("wrote", item.name)
        written += 1
    print(f"{written} walkthroughs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
