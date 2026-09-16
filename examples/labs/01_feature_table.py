"""Lab 01: six exam rates on the kiln document, plus the hand table."""

from _paths import CORPUS
from inkfold.handcalc import format_table
from inkfold.io import read_problem


def main() -> None:
    problem = read_problem(CORPUS / "problem-01-kiln-then-notice.txt")
    print(format_table(problem.units))
    print()
    print("Fold after unit 3: left is stall (I, ctr), right is notice (frm).")


if __name__ == "__main__":
    main()
