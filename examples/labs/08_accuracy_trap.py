#!/usr/bin/env python3
"""Print the table that makes accuracy sit down."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.report import render_baselines  # noqa: E402


def main() -> None:
    print(render_baselines(load_corpus(CORPUS)))


if __name__ == "__main__":
    main()
