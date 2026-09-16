"""Score the holdout codes once. Do not retune after."""

import _paths  # noqa: F401

from isogloss.cli import main
from _paths import CORPUS

if __name__ == "__main__":
    raise SystemExit(main(["holdout", str(CORPUS), "--ids", "4,10,16,22,26,30"]))
