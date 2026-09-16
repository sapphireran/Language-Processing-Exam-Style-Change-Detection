#!/usr/bin/env python3
"""Hand calculation from docs/07."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.evaluate import boundary_report  # noqa: E402


def main() -> int:
    gold = [0, 0, 1, 0, 0]
    pred = [0, 1, 1, 0, 0]
    report = boundary_report(gold, pred)
    print("gold", gold)
    print("pred", pred)
    print()
    print("class 1 (change)")
    print(f"  P={report.precision_1:.3f}  R={report.recall_1:.3f}  F1={report.f1_1:.3f}")
    print("class 0 (same)")
    print(f"  P={report.precision_0:.3f}  R={report.recall_0:.3f}  F1={report.f1_0:.3f}")
    print(f"macro-F1 {report.macro_f1:.3f}   (19/21 ≈ 0.762)")
    print()
    clean = boundary_report([0, 0, 0, 0], [0, 0, 0, 0])
    print("empty-class convention: all-zero vs all-zero →", f"{clean.macro_f1:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
