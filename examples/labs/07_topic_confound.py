"""Lab 07: three controls side by side."""

from inkfold.corpus import iter_problems
from inkfold.detectors import EnsembleDetector


def main() -> None:
    det = EnsembleDetector()
    print(f"{'id':40s} {'gold':22s} {'pred':22s} err")
    for problem in iter_problems():
        if problem.truth.site != "control":
            continue
        pred = det.detect(problem.units).changes
        print(
            f"{problem.problem_id:40s} {str(problem.truth.changes):22s} "
            f"{str(pred):22s} {problem.truth.expected_error}"
        )
    print()
    print("Stall and notice stay quiet. Chat is allowed to jitter.")


if __name__ == "__main__":
    main()
