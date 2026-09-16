#!/usr/bin/env python3
"""Compare formality jumps with topic Jaccard on every gold boundary.

On these short teaching paragraphs, content-word Jaccard is *saturated*
(almost every pair looks topically distant). Formality jump is what
actually peaks at the easy joins. That is the point of the plot.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scarfjoint.detectors import ScarfDetector  # noqa: E402
from scarfjoint.io import iter_corpus  # noqa: E402


def main() -> int:
    docs = iter_corpus(ROOT / "examples" / "corpus")
    detector = ScarfDetector()
    print(f"{'doc':<42} {'i':>2} gold  formality  topic  combined  pred")
    print("-" * 88)
    for doc in docs:
        detection = detector.detect(doc.paragraphs)
        gold = doc.gold_changes or []
        for boundary, bit in zip(detection.boundaries, gold, strict=True):
            scores = boundary.scores
            print(
                f"{doc.path.name:<42} {boundary.index:>2}  {bit}   "
                f"{scores.formality_jump:7.3f}  {scores.topic:5.3f}  "
                f"{scores.combined:7.3f}    {boundary.predicted}"
            )
        print()
    print(
        "Read down a document: easy gold=1 rows should show a formality "
        "spike. Topic stays high on gold=0 rows as well; do not let it vote."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
