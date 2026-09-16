#!/usr/bin/env python3
"""Grid-search a threshold on the same bank I will quote. Say that out loud."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.calibrate import best_threshold, grid_search_threshold  # noqa: E402
from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402


def main() -> None:
    corpus = load_corpus(CORPUS)
    detector = QuoinDetector()
    documents = []
    for item in corpus:
        scores = [row.quoin for row in detector.boundaries(item.problem.paragraphs)]
        documents.append((item.truth.changes, scores))
    rows = grid_search_threshold(documents)
    winner = best_threshold(rows)
    print(f"{'t':>6} {'macro-F1':>9} {'micro-F1':>9} {'n_pred':>7}")
    print("-" * 36)
    for row in rows:
        mark = "  <--" if row.threshold == winner.threshold else ""
        print(f"{row.threshold:6.2f} {row.macro_f1:9.3f} {row.micro_f1:9.3f} {row.n_pred:7d}{mark}")
    print()
    print(f"best t on THIS bank: {winner.threshold:.2f} (macro-F1 {winner.macro_f1:.3f})")
    print(f"code default:        {detector.threshold:.2f}")
    print("These two numbers being close is a convenience, not a proof.")


if __name__ == "__main__":
    main()
