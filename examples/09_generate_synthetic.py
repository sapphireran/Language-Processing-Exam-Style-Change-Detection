#!/usr/bin/env python3
"""Lab 9: emit a tiny synthetic easy/medium/hard split and score it."""

from __future__ import annotations

from _paths import GENERATED
from splicefind.cli import main as cli_main


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    target = GENERATED / "synthetic-split"
    assert (
        cli_main(
            [
                "generate",
                "-o",
                str(target),
                "--easy",
                "4",
                "--medium",
                "4",
                "--hard",
                "4",
                "--seed",
                "23",
            ]
        )
        == 0
    )
    assert cli_main(["score-corpus", str(target), "--threshold", "0.50"]) == 0
    print(f"files live under {target} (gitignored).")


if __name__ == "__main__":
    main()
