#!/usr/bin/env python3
"""Show the closed vector on either side of a known cut."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from examscd.detect import pair_distance  # noqa: E402
from examscd.features import style_dict  # noqa: E402
from examscd.io import read_text, read_truth  # noqa: E402
from examscd.tokenize import split_units  # noqa: E402

from _paths import DOCS  # noqa: E402


def dump_cut(stem: str) -> None:
    text = read_text(DOCS / f"{stem}.txt")
    truth = read_truth(DOCS / "truth" / f"{stem}.json")
    units = split_units(text, truth.granularity)
    cuts = [i for i, flag in enumerate(truth.changes) if flag]
    print(f"\n## {stem}  cuts at pair {cuts}")
    for idx in cuts:
        left, right = units[idx], units[idx + 1]
        print(f"\nL[{idx}]: {left.replace(chr(10), ' ')[:110]}")
        print(f"R[{idx+1}]: {right.replace(chr(10), ' ')[:110]}")
        raw = pair_distance(left, right)
        print(
            f"  ngram={raw['ngram']:.3f}  fwL1={raw['function_l1']:.3f}  "
            f"style={raw['style_l2']:.3f}  len={raw['length_jump']:.3f}  "
            f"combined={raw['combined']:.3f}"
        )
        a, b = style_dict(left), style_dict(right)
        keys = ["mean_unit_len", "first_person", "contraction_rate", "connective_rate", "imperative_rate"]
        for key in keys:
            print(f"  {key:<18} L={a[key]:.3f}  R={b[key]:.3f}")


def main() -> int:
    for stem in ("02_recipe_then_maillard", "05_same_topic_hard", "08_sms_essay_mix"):
        dump_cut(stem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
