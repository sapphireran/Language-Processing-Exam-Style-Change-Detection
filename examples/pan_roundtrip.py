#!/usr/bin/env python3
"""Write a PAN-style directory from the bundled examples, then evaluate it.

Useful as a checklist before you point the same CLI at a real PAN unzip::

    python examples/pan_roundtrip.py
    stylechange evaluate /tmp/stylechange-pan-in --output /tmp/stylechange-pan-out
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stylechange.cli import main as cli_main  # noqa: E402
from stylechange.io import iter_problems  # noqa: E402

DOC_DIR = Path(__file__).resolve().parent / "documents"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("/tmp/stylechange-pan-in"))
    parser.add_argument("--output", type=Path, default=Path("/tmp/stylechange-pan-out"))
    args = parser.parse_args()

    if args.input.exists():
        shutil.rmtree(args.input)
    args.input.mkdir(parents=True)
    copied = 0
    for problem in iter_problems(DOC_DIR):
        if problem.truth and problem.truth.extra.get("granularity") == "paragraph":
            continue
        shutil.copy2(problem.path, args.input / problem.path.name)
        truth = problem.path.with_name(f"truth-problem-{problem.problem_id}.json")
        if truth.exists():
            shutil.copy2(truth, args.input / truth.name)
        copied += 1

    print(f"copied {copied} sentence-level problems to {args.input}")
    return cli_main(["evaluate", str(args.input), "--output", str(args.output)])


if __name__ == "__main__":
    raise SystemExit(main())
