#!/usr/bin/env python3
"""Read a PAN-shaped folder, write solution-*.json, and rescore them.

This is the shape a shared-task submission would produce: for every
``problem-X.txt``, emit ``solution-problem-X.json`` with a ``changes`` array.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from stylechange.evaluate import evaluate_collection, format_collection
from stylechange.io import iter_problems, load_json, solution_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent / "documents",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="stylechange-pan-") as tmp:
        out = Path(tmp)
        score = evaluate_collection(args.directory, output_dir=out)
        print(format_collection(score))
        print()
        for problem in iter_problems(args.directory):
            written = solution_path(problem, out)
            payload = load_json(written)
            print(f"{written.name}: {payload['changes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
