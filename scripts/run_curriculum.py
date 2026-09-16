#!/usr/bin/env python3
"""Score the teaching corpus by tier and detector."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.corpus import load_teaching_corpus
from seamtrace.detectors import AdaptiveDetector, EnsembleDetector, ThresholdDetector
from seamtrace.evaluate import PairMetrics, score_pairs
from seamtrace.explain import explain_document
from seamtrace.report import format_metrics

DETECTORS = {
    "threshold": lambda args: ThresholdDetector(threshold=args.threshold),
    "adaptive": lambda args: AdaptiveDetector(k=args.k),
    "ensemble": lambda args: EnsembleDetector(threshold=args.threshold, k=args.k),
}


def _pool(docs, detector) -> tuple[dict[str, PairMetrics], PairMetrics, dict[str, int]]:
    by_tier_gold: dict[str, list[int]] = defaultdict(list)
    by_tier_pred: dict[str, list[int]] = defaultdict(list)
    labels: dict[str, int] = defaultdict(int)
    for doc in docs:
        pred = detector.predict(doc.table())
        by_tier_gold[doc.tier].extend(doc.changes)
        by_tier_pred[doc.tier].extend(pred)
        by_tier_gold["all"].extend(doc.changes)
        by_tier_pred["all"].extend(pred)
        for row in explain_document(
            doc.table(), pred, doc.changes, threshold=getattr(detector, "threshold", 0.42)
        ):
            labels[row.label] += 1
    metrics = {
        tier: score_pairs(by_tier_gold[tier], by_tier_pred[tier])
        for tier in by_tier_gold
    }
    return metrics, metrics["all"], dict(labels)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--detector", default="all", choices=["all", *DETECTORS])
    p.add_argument("--threshold", type=float, default=0.42)
    p.add_argument("--k", type=float, default=0.85)
    args = p.parse_args()
    docs = load_teaching_corpus()
    print(f"# {len(docs)} teaching documents\n")
    names = DETECTORS if args.detector == "all" else {args.detector: DETECTORS[args.detector]}
    order = ["easy", "medium", "hard", "control", "collage", "all"]
    for name, factory in names.items():
        detector = factory(args)
        metrics, _, labels = _pool(docs, detector)
        print(f"## {detector.name}")
        for tier in order:
            if tier in metrics:
                print(" ", format_metrics(f"{tier:8}", metrics[tier]))
        print("  labels:", ", ".join(f"{k}={v}" for k, v in sorted(labels.items())))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
