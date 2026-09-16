#!/usr/bin/env python3
"""Same-voice topic jumps should be quieter than house jumps."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402


def main() -> None:
    corpus = load_corpus(CORPUS)
    detector = QuoinDetector()
    print(f"{'band':<10} {'document':<42} {'mean Q':>7} {'pred':>6} {'gold':>6}")
    print("-" * 76)
    for band in ("easy", "trap", "hard", "control"):
        for item in corpus.by_band(band):
            rows = detector.boundaries(item.problem.paragraphs)
            pred = sum(r.pred for r in rows)
            gold = sum(item.truth.changes)
            mean_q = sum(r.quoin for r in rows) / len(rows)
            print(f"{band:<10} {item.name:<42} {mean_q:7.3f} {pred:6d} {gold:6d}")
        print()
    easy_changes = []
    trap_same = []
    for item in corpus.by_band("easy"):
        for row, gold in zip(detector.boundaries(item.problem.paragraphs), item.truth.changes):
            if gold == 1:
                easy_changes.append(row.quoin)
    for item in corpus.by_band("trap"):
        for row, gold in zip(detector.boundaries(item.problem.paragraphs), item.truth.changes):
            if gold == 0:
                trap_same.append(row.quoin)
    print(f"mean Q on easy gold-changes: {sum(easy_changes)/len(easy_changes):.3f}")
    print(f"mean Q on trap same-house hinges: {sum(trap_same)/len(trap_same):.3f}")
    print("Compare those two, not the per-file means: chat varies inside one house")
    print("and will pull a file-mean up without being an author change.")


if __name__ == "__main__":
    main()
