"""Lab 05: sweep τ. This is a sensitivity picture, not a second training loop."""

from inkfold.corpus import iter_problems
from inkfold.detectors import EnsembleDetector
from inkfold.evaluate import score_folder


def main() -> None:
    problems = iter_problems()
    print(f"{'τ':>6} {'acc':>7} {'macroF1':>8} {'meanF1':>8} {'fp':>4} {'fn':>4}")
    for tau in (0.20, 0.25, 0.30, 0.35, 0.40, 0.45):
        folder = score_folder(problems, EnsembleDetector(threshold=tau))
        s = folder.overall
        print(f"{tau:6.2f} {s.accuracy:7.3f} {s.macro_f1:8.3f} {folder.mean_macro_f1():8.3f} {s.fp:4d} {s.fn:4d}")
    print("Default τ=0.30 was picked on this folder. Say that in the oral.")


if __name__ == "__main__":
    main()
