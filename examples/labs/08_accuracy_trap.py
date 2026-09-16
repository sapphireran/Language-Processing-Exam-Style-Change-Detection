#!/usr/bin/env python3
"""Lab 08 — print the 16/4 trap."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.handcalc import trap_numbers


def main() -> int:
    nums = trap_numbers()
    print("TN={tn:.0f} FP={fp:.0f} FN={fn:.0f} TP={tp:.0f}".format(**nums))
    print(f"accuracy   {nums['accuracy']:.3f}")
    print(f"hold F1    {nums['hold_f1']:.3f}")
    print(f"change F1  {nums['change_f1']:.3f}")
    print(f"macro-F1   {nums['macro_f1']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
