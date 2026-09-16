#!/usr/bin/env python3
"""Lab 8: write PAN-shaped files and read them back."""

from __future__ import annotations

import tempfile
from pathlib import Path

from splicefind.cli import main as cli_main
from splicefind.io import load_collection, write_problem, write_truth
from splicefind.io import Truth


def main() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        incoming = root / "in"
        outgoing = root / "out"
        incoming.mkdir()
        write_problem(
            incoming / "problem-42.txt",
            "I don't trust the latch.\n\nOne may nevertheless oil it and wait.\n",
        )
        write_truth(
            incoming / "truth-problem-42.json",
            Truth(problem_id="42", changes=[1], authors=2, difficulty="easy"),
        )
        assert cli_main(["detect-dir", "-i", str(incoming), "-o", str(outgoing)]) == 0
        collection = load_collection(incoming)
        problem, truth = next(collection.pairs())
        assert problem.n_boundaries == 1
        assert truth is not None and truth.changes == [1]
        solution = (outgoing / "solution-problem-42.json").read_text(encoding="utf-8")
        print("wrote", outgoing / "solution-problem-42.json")
        print(solution)
        print("PAN-shaped roundtrip ok.")


if __name__ == "__main__":
    main()
