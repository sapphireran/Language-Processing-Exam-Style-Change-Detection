#!/usr/bin/env python3
"""Write SVG CUSUM figures for the notes / walkthrough."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.cusum import cusum_points  # noqa: E402
from examscd.render import cusum_svg  # noqa: E402
from examscd.tokenize import split_sentences  # noqa: E402

from _paths import DOCS  # noqa: E402


def lengths(name: str) -> list[int]:
    text = (DOCS / name).read_text(encoding="utf-8")
    return [len(s.split()) for s in split_sentences(text)]


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    cases = [
        ("memorised", [4, 5, 4, 5, 18, 16, 17, 19], "Memorised CUSUM series (docs/04)"),
        ("recipe", lengths("02_recipe_then_maillard.txt"), "CUSUM — recipe then Maillard"),
        ("commute", lengths("01_single_commute.txt"), "CUSUM — single-author commute (control)"),
    ]
    for stem, values, title in cases:
        dest = out / f"cusum_{stem}.svg"
        cusum_svg(values, dest, title=title, change_slots=cusum_points(values))
        print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
