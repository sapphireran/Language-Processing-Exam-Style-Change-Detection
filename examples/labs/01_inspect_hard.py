"""Inspect the hard same-topic file I use on the oral."""

import _paths  # noqa: F401

from isogloss.cli import main
from _paths import problem

if __name__ == "__main__":
    raise SystemExit(main(["inspect", str(problem(19)), "--features"]))
