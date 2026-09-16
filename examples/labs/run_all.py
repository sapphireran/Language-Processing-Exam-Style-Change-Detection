"""Run every numbered lab as a script."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = sorted(
    p for p in HERE.glob("*.py") if p.name[:1].isdigit() and p.name.endswith(".py")
)


def main() -> int:
    sys.path.insert(0, str(HERE))
    failed = 0
    for script in SCRIPTS:
        print(f"\n===== {script.name} =====")
        try:
            runpy.run_path(str(script), run_name="__main__")
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
            if code != 0:
                print(f"{script.name} exited {code}", file=sys.stderr)
                failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"{script.name} crashed: {exc}", file=sys.stderr)
            failed += 1
    print(f"\n{len(SCRIPTS) - failed}/{len(SCRIPTS)} labs ok")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
