#!/usr/bin/env python3
"""Walk the gift-abstract file the way I would in an oral."""

from __future__ import annotations

from _paths import CORPUS  # noqa: E402

from quoin.corpus import load_corpus  # noqa: E402
from quoin.detectors import QuoinDetector  # noqa: E402
from quoin.explain import explain_document  # noqa: E402
from quoin.evaluate import safe_f1  # noqa: E402


def main() -> None:
    item = load_corpus(CORPUS).get("problem-24-gift-abstract")
    detector = QuoinDetector()
    print(explain_document(item.problem, detector))
    pred = detector.predict(item.problem.paragraphs)
    print(f"gold {item.truth.changes}")
    print(f"pred {pred}")
    print(f"F1   {safe_f1(item.truth.changes, pred):.3f}")
    print()
    print("The gift is paragraph 2 (zero-based). Hinges 1 and 2 should want to fire.")
    print("Hinge 0 is two student paragraphs and should want to stay dark.")


if __name__ == "__main__":
    main()
