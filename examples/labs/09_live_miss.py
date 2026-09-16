"""The one hinge kerf still misses: Seminar → Pocket on document 27."""

from __future__ import annotations

from pathlib import Path

from kerf.detect import detect_path
from kerf.io import read_truth
from kerf.metrics import hinge_macro_f1

PATH = (
    Path(__file__).resolve().parents[1] / "corpus" / "problem-27-stilling-four-houses.txt"
)


def main() -> None:
    det = detect_path(PATH)
    gold = read_truth(PATH.with_name("truth-problem-27.json")).changes
    scores = hinge_macro_f1(det.changes, gold)
    print("houses: Caliper, Placard, Seminar, Pocket")
    print(f"gold    {gold}")
    print(f"pred    {det.changes}")
    print(f"split   {[round(s, 3) for s in det.split_scores]}")
    print(f"adj     {[round(s, 3) for s in det.adjacent]}")
    print(f"reasons {det.cut_reason}")
    print(f"macro-F1 {scores.macro_f1:.3f}  fn={scores.fn}")
    print()
    print("Last hinge sits inside the same-house adjacent cloud.")
    print("Catching it would start cutting document 13's last same-house step.")


if __name__ == "__main__":
    main()
