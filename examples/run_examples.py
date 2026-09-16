#!/usr/bin/env python3
"""Score every bundled example document and print a compact report.

This is the script the README points at for a first run. It stays inside
the repository: no PAN zip download, no network, no extra packages.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stylechange import StyleChangeDetector, evaluate_changes  # noqa: E402
from stylechange.io import iter_problems  # noqa: E402

DOC_DIR = Path(__file__).resolve().parent / "documents"


def main() -> int:
    sentence_detector = StyleChangeDetector(granularity="sentence")
    paragraph_detector = StyleChangeDetector(granularity="paragraph", threshold=0.28)

    gold: list[list[int]] = []
    pred: list[list[int]] = []

    print(f"Example documents in {DOC_DIR}\n")
    print(f"{'id':<28} {'gold':<28} {'pred':<28} match")
    print("-" * 96)

    for problem in iter_problems(DOC_DIR):
        granularity = "sentence"
        detector = sentence_detector
        if problem.truth and problem.truth.extra.get("granularity") == "paragraph":
            granularity = "paragraph"
            detector = paragraph_detector
        prediction = detector.predict(problem.text)
        truth = problem.truth.changes if problem.truth else []
        ok = prediction.changes == truth
        gold.append(truth)
        pred.append(prediction.changes)
        print(
            f"{problem.problem_id:<28} {str(truth):<28} {str(prediction.changes):<28} "
            f"{'yes' if ok else 'no':>5}  ({granularity})"
        )

    result = evaluate_changes(gold, pred)
    print()
    print(
        f"collection macro-F1={result.macro_f1:.3f}  "
        f"accuracy={result.accuracy:.3f}  "
        f"P={result.precision:.3f}  R={result.recall:.3f}  "
        f"pairs={result.pairs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
