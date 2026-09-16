"""Print split scores next to adjacent steps for one return and one collage."""

from __future__ import annotations

from pathlib import Path

from kerf.detect import detect_path
from kerf.io import read_truth

ROOT = Path(__file__).resolve().parents[1] / "corpus"
FILES = (
    "problem-24-stilling-caliper-placard-caliper.txt",
    "problem-25-cinema-pocket-statute-pocket.txt",
    "problem-27-stilling-four-houses.txt",
)


def main() -> None:
    for name in FILES:
        path = ROOT / name
        det = detect_path(path)
        code = name.removeprefix("problem-").split("-", 1)[0]
        gold = read_truth(ROOT / f"truth-problem-{code}.json").changes
        print(f"# {name}")
        print(f"gold {gold}  pred {det.changes}")
        print("i  split  adjacent  gold pred reason")
        for i, (s, a, g, p, r) in enumerate(
            zip(det.split_scores, det.adjacent, gold, det.changes, det.cut_reason)
        ):
            print(f"{i}  {s:5.3f}  {a:8.3f}   {g}    {p}   {r or '-'}")
        print()


if __name__ == "__main__":
    main()
