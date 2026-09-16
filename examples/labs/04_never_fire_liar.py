"""Show why accuracy is the never-fire liar on this bank."""

from __future__ import annotations

from kerf.metrics import score_directory


def main() -> None:
    bundle = score_directory("examples/corpus")
    o, n, a = bundle["overall"], bundle["never"], bundle["always"]
    print(f"hinges: {bundle['n_hinges']}  docs: {bundle['n_docs']}")
    print(f"{'predictor':<14} {'macro-F1':>8} {'hinge-acc':>9} {'f1-chg':>7} {'f1-same':>8}")
    for name, s in (("never-fire", n), ("always-fire", a), ("kerf", o)):
        print(f"{name:<14} {s.macro_f1:8.3f} {s.accuracy:9.3f} {s.f1_change:7.3f} {s.f1_same:8.3f}")
    print()
    print("Never-fire accuracy is high because most hinges are zeros.")
    print("That is why the table leads with macro-F1.")


if __name__ == "__main__":
    main()
