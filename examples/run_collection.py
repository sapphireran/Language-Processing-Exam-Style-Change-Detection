#!/usr/bin/env python3
"""Score every study document with the exam baseline."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.detect import detect_document  # noqa: E402
from examscd.evaluate import adjusted_rand_index, boundary_report  # noqa: E402
from examscd.io import read_text, read_truth  # noqa: E402

from _paths import load_manifest  # noqa: E402


def main() -> int:
    rows = load_manifest()
    print(f"{'id':<28} {'pairs':>5} {'macro-F1':>9} {'F1-chg':>7} {'ARI':>6}  pred")
    print("-" * 78)
    f1s = []
    for item in rows:
        text = read_text(item["text"])
        truth = read_truth(item["truth"])
        result = detect_document(text, granularity=truth.granularity)
        if len(result.changes) != len(truth.changes):
            print(f"{item['id']:<28} PAIR MISMATCH pred={len(result.changes)} gold={len(truth.changes)}")
            return 2
        report = boundary_report(truth.changes, result.changes)
        ari = (
            adjusted_rand_index(truth.authors, result.authors)
            if truth.authors and result.authors
            else float("nan")
        )
        f1s.append(report.macro_f1)
        pred = "".join(str(x) for x in result.changes) or "∅"
        ari_s = f"{ari:.3f}" if ari == ari else "  n/a"
        print(
            f"{item['id']:<28} {len(truth.changes):>5} {report.macro_f1:>9.3f} "
            f"{report.f1_1:>7.3f} {ari_s:>6}  {pred}"
        )
    print("-" * 78)
    print(f"collection mean macro-F1: {sum(f1s) / len(f1s):.3f}  (toy files, not a PAN score)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
