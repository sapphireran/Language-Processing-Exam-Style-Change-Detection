#!/usr/bin/env python3
"""Write a markdown score table into examples/reports/."""

from __future__ import annotations

from _paths import CORPUS, REPORTS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.report import render_markdown  # noqa: E402


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    text = render_markdown(load_corpus(CORPUS))
    path = REPORTS / "live-results.md"
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
