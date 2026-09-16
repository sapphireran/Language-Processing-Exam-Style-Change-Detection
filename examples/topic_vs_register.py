#!/usr/bin/env python3
"""Compare content-word shift with function-word distance on Easy vs Hard."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.corpus import load_teaching_corpus
from seamtrace.explain import _content_shift
from seamtrace.pairwise import score_document


def main() -> int:
    print(f"{'doc':<32} {'tier':<8} {'pair':>4} {'gold':>4} {'topic':>6} {'fw':>6}")
    for doc in load_teaching_corpus():
        if doc.tier not in {"easy", "hard"}:
            continue
        rows = score_document(doc.table())
        for i, row in enumerate(rows):
            topic = _content_shift(doc.units[i], doc.units[i + 1])
            print(
                f"{doc.stem:<32} {doc.tier:<8} {i:4} {doc.changes[i]:4} "
                f"{topic:6.2f} {row.function_words:6.2f}"
            )
    print()
    print("Exam reading: Easy gold seams should show high topic AND high fw.")
    print("Hard gold seams should show modest topic and a fw/Delta move.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
