"""Print the liar table so I cannot quote accuracy alone."""

import _paths  # noqa: F401

from isogloss.cli import main
from _paths import CORPUS

if __name__ == "__main__":
    raise SystemExit(main(["score", str(CORPUS)]))
