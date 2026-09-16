"""Run labs 00–10 in order."""

from __future__ import annotations

import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = sorted(HERE.glob("[0-9][0-9]_*.py"))


def main() -> None:
    for script in SCRIPTS:
        print("=" * 72)
        print(script.name)
        print("=" * 72)
        runpy.run_path(str(script), run_name="__main__")
        print()


if __name__ == "__main__":
    main()
