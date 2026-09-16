#!/usr/bin/env python3
"""Score every teaching split with the default threshold detector."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.cli import main as cli_main  # noqa: E402

SPLITS = ("easy", "medium", "hard", "control")


def main() -> int:
    data = ROOT / "examples" / "data"
    for name in SPLITS:
        print(f"===== {name} =====")
        code = cli_main(["eval", str(data / name)])
        if code:
            return code
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
