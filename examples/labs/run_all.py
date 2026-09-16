"""Run every lab script. Used by the revision circuit and by tests."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

LABS = (
    "01_inspect_hard.py",
    "02_trap_vs_easy.py",
    "03_split_vs_adjacent.py",
    "04_never_fire_liar.py",
    "05_hand_split.py",
    "06_return_aba.py",
    "07_house_fingerprint.py",
    "08_holdout.py",
    "09_live_miss.py",
    "10_formula_check.py",
)


def main() -> int:
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    for name in LABS:
        print("=" * 72)
        print(name)
        print("=" * 72)
        runpy.run_path(str(here / name), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
