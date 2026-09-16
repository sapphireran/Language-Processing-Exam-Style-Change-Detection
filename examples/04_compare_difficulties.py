#!/usr/bin/env python3
"""Train on one band, test on every band — the 3×3 leakage table.

Expected pattern (docs/04-baselines-and-models.md):

  * train easy → test hard : largest drop (topic cues fail)
  * train hard → test easy : smaller drop (style still fires when
    topic also moves)
  * diagonal : best score for that band's own distribution

A single headline F1 cannot replace this table.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.evaluate import evaluate_directory
from scd.generate import TRAIN_ID_MAX
from scd.models import predict_directory, train_logreg

DATA = ROOT / "examples" / "data"
OUT = ROOT / "models" / "band-transfer"
BANDS = ("easy", "medium", "hard")
HOLD_MIN = TRAIN_ID_MAX + 1


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    table: dict[tuple[str, str], float] = {}
    for train_band in BANDS:
        model = train_logreg(
            DATA, bands=(train_band,), seed=0, id_min=1, id_max=TRAIN_ID_MAX
        )
        for test_band in BANDS:
            dest = OUT / f"{train_band}-to-{test_band}"
            predict_directory(model, DATA / test_band, dest, id_min=HOLD_MIN)
            scores = evaluate_directory(dest, DATA / test_band, id_min=HOLD_MIN)
            table[(train_band, test_band)] = scores.macro_f1

    header = f"{'train\\\\test':<12}" + "".join(f"{band:>10}" for band in BANDS)
    print(header)
    print("-" * len(header))
    for train_band in BANDS:
        cells = "".join(f"{table[(train_band, test)]:>10.3f}" for test in BANDS)
        print(f"{train_band:<12}{cells}")

    drop = table[("easy", "easy")] - table[("easy", "hard")]
    reverse = table[("hard", "hard")] - table[("hard", "easy")]
    print()
    print(f"easy→hard drop:  {drop:+.3f}   (topic leakage penalty)")
    print(f"hard→easy drop:  {reverse:+.3f}   (style-only model on easier data)")
    print()
    if drop > 0.05:
        print("The easy-trained model lost more on hard than a rounding error.")
        print("That is the point of the three-band design.")
    else:
        print("No easy→hard drop. Either the hard band is too loud or the")
        print("easy band is too small — inspect scd.generate personas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
