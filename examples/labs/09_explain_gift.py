"""Lab 09: gift authorship — hedges out, shall/must in."""

from _paths import CORPUS
from inkfold.explain import explain_document, format_explain
from inkfold.io import read_problem


def main() -> None:
    problem = read_problem(CORPUS / "problem-24-gift-abstract.txt")
    print(format_explain(problem, explain_document(problem)))


if __name__ == "__main__":
    main()
