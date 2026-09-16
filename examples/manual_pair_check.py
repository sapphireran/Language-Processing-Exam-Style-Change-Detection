#!/usr/bin/env python3
"""Recompute the paper worked examples with the live feature extractor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.features import as_dict, extract_sentence  # noqa: E402

PAIRS = [
    {
        "name": "Example A — Mira → Jules",
        "gold": 1,
        "left": ("mira", "However, the bloom remains relatively unstable although the pour is slow."),
        "right": ("jules", "I don't wait that long; I just go for it!"),
        "watch": (
            "contraction_rate",
            "first_person_rate",
            "hedge_rate",
            "subord_marker_rate",
            "exclamation_rate",
            "word_count",
        ),
    },
    {
        "name": "Example B — Hale → Nell",
        "gold": 1,
        "left": ("hale", "Water mass was 15.0 g and bloom time was 45 s."),
        "right": ("nell", "The kettle ticked; the filter breathed a faint paper sweetness."),
        "watch": ("digit_rate", "semicolon_rate", "first_person_rate", "contraction_rate", "word_count"),
    },
    {
        "name": "Example C — Mira → Mira (should be quiet)",
        "gold": 0,
        "left": ("mira", "A modest bloom suggests that degassing remains relatively active."),
        "right": ("mira", "However, the subsequent drawdown appears somewhat slower than expected."),
        "watch": ("hedge_rate", "contraction_rate", "first_person_rate", "word_count", "nominalization_rate"),
    },
]


def main() -> int:
    for pair in PAIRS:
        left = as_dict(extract_sentence(pair["left"][1]))
        right = as_dict(extract_sentence(pair["right"][1]))
        print(pair["name"], f"(gold change={pair['gold']})")
        print(f"  {pair['left'][0]}:  {pair['left'][1]}")
        print(f"  {pair['right'][0]}: {pair['right'][1]}")
        print(f"  {'feature':<22} {'left':>8} {'right':>8} {'|d|':>8}")
        for feature in pair["watch"]:
            delta = abs(left[feature] - right[feature])
            print(f"  {feature:<22} {left[feature]:8.3f} {right[feature]:8.3f} {delta:8.3f}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
