#!/usr/bin/env python3
"""Run the baseline detector on every packaged example document."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from style_change.detectors import StyleChangeDetector
from style_change.evaluate import evaluate_document
from style_change.io import load_document, load_labels
from style_change.visualize import format_report

DOC_DIR = Path(__file__).resolve().parent / "documents"
LABEL_DIR = DOC_DIR / "labels"


def main() -> int:
    detector = StyleChangeDetector()
    print("Style change demo")
    print("=" * 72)
    failures = 0
    for label_path in sorted(LABEL_DIR.glob("*.json")):
        labels = load_labels(label_path)
        document_path = DOC_DIR / labels["document"]
        document = load_document(document_path)
        table, result = detector.detect_document(document)
        report = evaluate_document(
            result,
            gold_authors=labels["authors"],
            gold_multi=labels.get("multi_author"),
            gold_changes=labels.get("changes"),
        )
        print()
        print(document_path.name)
        print("-" * 72)
        print(format_report(document, table, result, preview_chars=72))
        print()
        print(report.summary())
        # Soft checks used by the demo, not by pytest.
        if result.multi_author != labels["multi_author"]:
            print("WARN: Task 1 disagrees with gold")
            failures += 1
    print()
    print(json.dumps({"task1_mismatches": failures}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
