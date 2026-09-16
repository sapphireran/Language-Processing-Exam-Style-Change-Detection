#!/usr/bin/env python3
"""Score every document in the personal bank."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402
from quoin.report import render_table, score_corpus  # noqa: E402


def main() -> None:
    corpus = load_corpus(CORPUS)
    detector = QuoinDetector()
    rows = score_corpus(corpus, detector)
    bands = {item.name: item.band for item in corpus}
    print(render_table(rows, bands))


if __name__ == "__main__":
    main()
