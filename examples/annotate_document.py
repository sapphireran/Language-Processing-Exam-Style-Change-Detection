#!/usr/bin/env python3
"""Dump one document the way an oral walkthrough would."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scarfjoint.detectors import ScarfDetector  # noqa: E402
from scarfjoint.io import load_problem, load_truth, truth_path_for  # noqa: E402
from scarfjoint.report import format_detection  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument("--use-topic", action="store_true")
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    kwargs = {"use_topic": args.use_topic}
    if args.threshold is not None:
        kwargs["threshold"] = args.threshold
    doc = load_problem(args.document)
    gold = doc.gold_changes
    tpath = truth_path_for(doc.path)
    if gold is None and tpath.exists():
        gold = [int(x) for x in load_truth(tpath).get("changes", [])]
    detection = ScarfDetector(**kwargs).detect(doc.paragraphs)
    print(format_detection(detection, gold=gold))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
