#!/usr/bin/env python3
"""Band-by-band evaluation of the teaching corpus, with and without topic."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scarfjoint.detectors import ScarfDetector  # noqa: E402
from scarfjoint.evaluate import document_scores, mean_bundle  # noqa: E402
from scarfjoint.io import iter_corpus  # noqa: E402
from scarfjoint.report import format_metrics  # noqa: E402


def _run(detector: ScarfDetector, docs) -> None:
    by_band: dict[str, list] = defaultdict(list)
    for doc in docs:
        pred = detector.detect(doc.paragraphs).changes
        gold = doc.gold_changes
        if gold is None:
            continue
        bundle = document_scores(gold, pred)
        band = str(doc.truth.get("band", "unknown")) if doc.truth else "unknown"
        by_band[band].append(bundle)
        print("  " + format_metrics(f"{band}/{doc.path.name}", bundle))
    print()
    for band in ("easy", "medium", "hard", "single_author"):
        if band not in by_band:
            continue
        summary = mean_bundle(by_band[band])
        print(
            f"  {band:14s}  n={int(summary['documents'])}  "
            f"F1={summary['f1']:.3f}  macro-F1={summary['macro_f1']:.3f}  "
            f"exact={summary['exact_match']:.3f}"
        )
    overall = mean_bundle([b for group in by_band.values() for b in group])
    print(
        f"  {'overall':14s}  n={int(overall['documents'])}  "
        f"F1={overall['f1']:.3f}  macro-F1={overall['macro_f1']:.3f}  "
        f"exact={overall['exact_match']:.3f}"
    )


def main() -> int:
    docs = iter_corpus(ROOT / "examples" / "corpus")
    print(f"corpus: {len(docs)} documents\n")
    print("Default detector (topic does not vote)")
    _run(ScarfDetector(), docs)
    print("\nLeakage mode (--use-topic)")
    _run(ScarfDetector(use_topic=True), docs)
    print(
        "\nOn this short-paragraph corpus, Jaccard topic distance is "
        "saturated, so leakage mode usually gets *worse*. That is a lab "
        "result, not a PAN result."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
