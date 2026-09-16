#!/usr/bin/env python3
"""Print the live scoreboard and the accuracy-trap numbers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inkfold.corpus import iter_problems  # noqa: E402
from inkfold.evaluate import accuracy_trap_demo, score_folder  # noqa: E402
from inkfold.report import format_scoreboard  # noqa: E402


def main() -> int:
    problems = iter_problems()
    folder = score_folder(problems)
    print(format_scoreboard(folder), end="")
    print()
    trap = accuracy_trap_demo(problems)
    print("# accuracy trap")
    for key, val in trap.items():
        print(f"  {key:22s} {val}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
