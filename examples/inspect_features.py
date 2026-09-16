#!/usr/bin/env python3
"""Print the features that most separate two adjacent paragraphs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from style_change.features import FeatureExtractor
from style_change.io import load_document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    parser.add_argument("--k", type=int, default=8, help="how many features to show")
    args = parser.parse_args()

    document = load_document(args.document)
    table = FeatureExtractor(min_words=1).extract_document(document)
    print(f"{args.document}  paragraphs={table.matrix.shape[0]}  features={len(table.names)}")
    if table.matrix.shape[0] < 2:
        print("need at least two paragraphs")
        return 1
    for left in range(table.matrix.shape[0] - 1):
        right = left + 1
        print()
        print(f"paragraph {table.paragraph_indices[left]} -> {table.paragraph_indices[right]}")
        for name, a, b, delta in table.top_differences(left, right, k=args.k):
            print(f"  {name:28} {a:9.4f}  {b:9.4f}  |z-gap|={delta:6.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
