#!/usr/bin/env python3
"""The 16-stay / 4-change accuracy trap from the notes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.evaluate import score_pairs
from seamtrace.handcalc import macro_f1_from_cells

GOLD = [0] * 16 + [1] * 4
NEVER = [0] * 20
ALWAYS = [1] * 20


def main() -> int:
    never = score_pairs(GOLD, NEVER)
    always = score_pairs(GOLD, ALWAYS)
    print("support: 16 stay, 4 change")
    print(
        f"never-fire  acc={never.accuracy:.3f}  macro-F1={never.macro_f1:.3f}  "
        f"F1-change={never.f1_1:.3f}"
    )
    print(
        f"always-fire acc={always.accuracy:.3f}  macro-F1={always.macro_f1:.3f}  "
        f"F1-change={always.f1_1:.3f}"
    )
    print(f"handcalc    macro-F1={macro_f1_from_cells(0, 0, 16, 4):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
