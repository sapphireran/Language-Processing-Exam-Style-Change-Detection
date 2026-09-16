"""Lab 10: write HTML reports for every teaching document."""

from _paths import REPORTS
from inkfold.cli import main as cli_main


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    cli_main(["report", "--out", str(REPORTS)])


if __name__ == "__main__":
    main()
