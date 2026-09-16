"""Lab 02: hinge scores. The gold cut should be the peak."""

from _paths import CORPUS
from inkfold.detectors import EnsembleDetector, adjacent_scores, hinge_scores
from inkfold.io import read_problem


def main() -> None:
    problem = read_problem(CORPUS / "problem-01-kiln-then-notice.txt")
    print(f"gold {problem.truth.changes}")
    print(f"{'cut':>4} {'adj':>7} {'hinge':>7} {'regL1':>7} {'fw':>7}")
    for a, h in zip(adjacent_scores(problem.units), hinge_scores(problem.units)):
        print(
            f"{h.index:4d} {a.score:7.3f} {h.score:7.3f} "
            f"{h.channels['register_l1']:7.3f} {h.channels['function_cosine_distance']:7.3f}"
        )
    det = EnsembleDetector().detect(problem.units)
    print("pred", det.changes, "authors_naive", det.authors)


if __name__ == "__main__":
    main()
