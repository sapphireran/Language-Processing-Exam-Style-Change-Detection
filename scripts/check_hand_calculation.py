#!/usr/bin/env python3
"""Lock the 16/4 accuracy trap to six decimal places."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.handcalc import trap_numbers

EXPECTED = {
    "accuracy": 0.8,
    "hold_precision": 0.8,
    "hold_recall": 1.0,
    "hold_f1": 2 * 0.8 * 1.0 / 1.8,
    "change_f1": 0.0,
    "macro_f1": 0.5 * (0.0 + 2 * 0.8 * 1.0 / 1.8),
    "tn": 16.0,
    "fn": 4.0,
    "tp": 0.0,
    "fp": 0.0,
}


def main() -> int:
    nums = trap_numbers()
    bad = []
    for key, want in EXPECTED.items():
        got = nums[key]
        if not math.isclose(got, want, rel_tol=0, abs_tol=1e-9):
            bad.append(f"{key}: got {got} want {want}")
    if bad:
        print("FAIL")
        print("\n".join(bad))
        return 1
    print("ok 16/4 trap: accuracy=0.800 macro-F1=0.444...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
