"""Inspect the hard same-well document (Caliper then Seminar)."""

from __future__ import annotations

from pathlib import Path

from kerf.report import document_report

ROOT = Path(__file__).resolve().parents[1] / "corpus"
PATH = ROOT / "problem-16-stilling-caliper-then-seminar.txt"


def main() -> None:
    print(document_report(PATH))


if __name__ == "__main__":
    main()
