#!/usr/bin/env python3
"""Lab 4: score the eighteen-document personal corpus."""

from __future__ import annotations

import argparse
from collections import defaultdict

from _paths import CORPUS, require_corpus
from splicefind.detect import always_same, detect_text
from splicefind.evaluate import collection_report, format_score, score_document
from splicefind.io import load_collection


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--method", default="relative")
    args = parser.parse_args()
    require_corpus()
    collection = load_collection(CORPUS)
    scores = []
    dummy = []
    by_band: dict[str, list] = defaultdict(list)
    for problem, truth in collection.pairs():
        if truth is None:
            continue
        detection = detect_text(
            problem.text, threshold=args.threshold, method=args.method
        )
        score = score_document(truth.changes, detection.changes, problem.problem_id)
        scores.append(score)
        dummy.append(
            score_document(
                truth.changes, always_same(problem.text).changes, problem.problem_id
            )
        )
        by_band[truth.difficulty or "unspecified"].append(score)
        print(format_score(score))
    print()
    summary = collection_report(scores)
    dummy_summary = collection_report(dummy)
    print(
        f"ensemble  macro F1={summary['macro_f1']:.3f}  "
        f"micro F1={summary['micro_f1']:.3f}  acc={summary['mean_accuracy']:.3f}"
    )
    print(
        f"always-0  macro F1={dummy_summary['macro_f1']:.3f}  "
        f"micro F1={dummy_summary['micro_f1']:.3f}  acc={dummy_summary['mean_accuracy']:.3f}"
    )
    print()
    print("by band (macro F1):")
    for band, band_scores in sorted(by_band.items()):
        print(f"  {band:<14} {collection_report(band_scores)['macro_f1']:.3f}  n={len(band_scores)}")
    print()
    print("Demo scores on a tiny hand-written set. Not a leaderboard.")


if __name__ == "__main__":
    main()
