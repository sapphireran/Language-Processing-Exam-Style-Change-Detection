"""ABA: global split is shy, adjacent floor recovers both hinges."""

from __future__ import annotations

from pathlib import Path

from kerf.detect import detect_path
from kerf.io import read_truth

PATH = (
    Path(__file__).resolve().parents[1]
    / "corpus"
    / "problem-25-cinema-pocket-statute-pocket.txt"
)


def main() -> None:
    det = detect_path(PATH)
    gold = read_truth(PATH.with_name("truth-problem-25.json")).changes
    print("Pocket / Statute / Pocket")
    print(f"gold           {gold}")
    print(f"pred           {det.changes}")
    print(f"split scores   {[round(s, 3) for s in det.split_scores]}")
    print(f"adjacent       {[round(s, 3) for s in det.adjacent]}")
    print(f"reasons        {det.cut_reason}")
    print(f"naive authors  {det.authors_guess}  (wrong: truth has 2)")
    print()
    print("Both local steps are loud, so a within-document z-peak would")
    print("fire neither. The first saw plus a two-paragraph recurse marks both.")


if __name__ == "__main__":
    main()
