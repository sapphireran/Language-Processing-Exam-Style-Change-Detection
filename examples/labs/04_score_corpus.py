"""Lab 04: the live scoreboard."""

from inkfold.corpus import iter_problems
from inkfold.evaluate import score_folder
from inkfold.report import format_scoreboard


def main() -> None:
    print(format_scoreboard(score_folder(iter_problems())), end="")


if __name__ == "__main__":
    main()
