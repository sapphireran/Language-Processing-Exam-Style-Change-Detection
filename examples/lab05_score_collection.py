#!/usr/bin/env python3
"""Lab 05 — score the bundled collection the way PAN scores a test set."""

from __future__ import annotations

from _paths import DOC_DIR, TRUTH_DIR

from scdkit.evaluate import evaluate_collection, format_table


def main() -> int:
    score = evaluate_collection(DOC_DIR, TRUTH_DIR, method="ensemble")
    print(format_table(score))
    print()
    print("Remember: macro-F1 averages *document* F1s. The four-paragraph")
    print("landlord letter counts as much as the five-paragraph board-game thread.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
