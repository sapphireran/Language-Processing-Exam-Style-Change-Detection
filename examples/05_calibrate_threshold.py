#!/usr/bin/env python3
"""Lab 5: sweep thresholds. Accuracy peak is the wrong prize."""

from __future__ import annotations

from _paths import CORPUS, require_corpus
from splicefind.calibrate import format_sweep, sweep_thresholds
from splicefind.io import load_collection


def main() -> None:
    require_corpus()
    points = sweep_thresholds(load_collection(CORPUS))
    print(format_sweep(points))
    print()
    print("Starred row is macro-F1 max. If accuracy likes a higher cut,")
    print("that is the majority-class costume from the notes.")


if __name__ == "__main__":
    main()
