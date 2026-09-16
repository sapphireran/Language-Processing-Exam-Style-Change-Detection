"""Quote holdout last. The blade was set on the other twenty-one files."""

from __future__ import annotations

from examples.corpus.bank import HOLDOUT, by_code
from kerf.metrics import hinge_macro_f1, score_directory


def main() -> None:
    bundle = score_directory("examples/corpus")
    codes = by_code()
    hold_p, hold_g, in_p, in_g = [], [], [], []
    print(f"holdout codes: {', '.join(sorted(HOLDOUT))}")
    print()
    print(f"{'id':<42} {'split':<8} {'gold':<8} {'pred':<8} f1")
    for row in bundle["rows"]:
        code = row["id"].replace("problem-", "").split("-")[0]
        doc = codes[code]
        bucket = "holdout" if doc.holdout else "in-band"
        gold = "".join(str(x) for x in row["gold"])
        pred = "".join(str(x) for x in row["pred"])
        print(f"{row['id']:<42} {bucket:<8} {gold:<8} {pred:<8} {row['macro_f1']:.2f}")
        (hold_p if doc.holdout else in_p).extend(row["pred"])
        (hold_g if doc.holdout else in_g).extend(row["gold"])
    ih, hh = hinge_macro_f1(in_p, in_g), hinge_macro_f1(hold_p, hold_g)
    print()
    print(f"in-band  macro-F1 {ih.macro_f1:.3f}  acc {ih.accuracy:.3f}")
    print(f"holdout  macro-F1 {hh.macro_f1:.3f}  acc {hh.accuracy:.3f}")


if __name__ == "__main__":
    main()
