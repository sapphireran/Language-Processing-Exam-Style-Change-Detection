#!/usr/bin/env python3
"""Run labs 00–10 in order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABS = sorted(p for p in HERE.glob("[0-9][0-9]_*.py"))


def main() -> int:
    for lab in LABS:
        print(f"\n##### {lab.name} #####")
        proc = subprocess.run([sys.executable, str(lab)], cwd=str(HERE.parents[1]))
        if proc.returncode != 0:
            print(f"FAIL {lab.name}", file=sys.stderr)
            return proc.returncode
    print("\nall labs ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
