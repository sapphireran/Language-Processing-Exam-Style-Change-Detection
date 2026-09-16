"""Lab 03: CUSUM on first-person. A picture, not an answer."""

from _paths import CORPUS
from inkfold.cusum import format_cusum
from inkfold.io import read_problem


def main() -> None:
    problem = read_problem(CORPUS / "problem-01-kiln-then-notice.txt")
    print(format_cusum(problem.units))
    print()
    print("Check the six-rate L1 at that peak before you trust it.")


if __name__ == "__main__":
    main()
