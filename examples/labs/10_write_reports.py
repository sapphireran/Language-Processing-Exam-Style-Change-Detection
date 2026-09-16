#!/usr/bin/env python3
"""Lab 10 — HTML reports for the spotlight files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.corpus import list_corpus
from hingemark.report import write_html_report

SPOT = (
    "canal-then-lot",
    "quince-batch-then-letter",
    "two-mycologists",
    "river-three-topics",
    "canal-return",
    "tidepool-gift-abstract",
)


def main() -> int:
    dest = ROOT / "examples/reports"
    dest.mkdir(parents=True, exist_ok=True)
    items = [it for it in list_corpus() if any(s in it.name for s in SPOT)]
    for item in items:
        write_html_report(item, dest / f"{item.name}.html")
        print("wrote", item.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
