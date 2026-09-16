#!/usr/bin/env python3
"""Print house-author feature cards from the live extractor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.features import FEATURE_NAMES, as_dict, extract_sentence  # noqa: E402

SAMPLES = {
    "mira": (
        "A growing body of observational work suggests that late-evening "
        "surface temperatures remain relatively high when canopy cover is "
        "sparse, although the size of that association varies by street width."
    ),
    "jules": (
        "I don't grind the beans before I put the kettle on, and then I "
        "remember while the water's already roaring."
    ),
    "hale": "Water mass was 15.0 g. Bloom time was 45 s. Drawdown was recorded at 3:10.",
    "nell": (
        "By the time the kettle clicked, the paper filter had taken on the "
        "faint sweet smell of a wet envelope; even the mug looked briefly "
        "ceremonial."
    ),
}

FOCUS = (
    "word_count",
    "contraction_rate",
    "first_person_rate",
    "hedge_rate",
    "digit_rate",
    "semicolon_rate",
    "passive_be_rate",
    "nominalization_rate",
    "exclamation_rate",
    "flesch_reading_ease",
)


def main() -> int:
    rows = {name: as_dict(extract_sentence(text)) for name, text in SAMPLES.items()}
    print("House-author samples (original card sentences)\n")
    for name, text in SAMPLES.items():
        print(f"[{name}] {text}\n")
    header = f"{'feature':<24}" + "".join(f"{name:>10}" for name in SAMPLES)
    print(header)
    print("-" * len(header))
    for feature in FOCUS:
        print(f"{feature:<24}" + "".join(f"{rows[name][feature]:10.3f}" for name in SAMPLES))
    print("\nFull vectors are available via: stylechange features --text '...'")
    print(f"Extractor dimension: {len(FEATURE_NAMES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
