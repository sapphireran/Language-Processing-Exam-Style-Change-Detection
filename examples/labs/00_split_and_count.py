"""Lab 00: see the units the rest of the kit will use."""

from _paths import CORPUS
from inkfold.io import read_problem
from inkfold.tokenize import word_tokens


def main() -> None:
    problem = read_problem(CORPUS / "problem-01-kiln-then-notice.txt")
    print(f"{problem.problem_id}  n={len(problem.units)}  gold={problem.truth.changes}")
    for i, unit in enumerate(problem.units, start=1):
        toks = word_tokens(unit)
        print(f"{i:2d}  tok={len(toks):2d}  {unit}")


if __name__ == "__main__":
    main()
