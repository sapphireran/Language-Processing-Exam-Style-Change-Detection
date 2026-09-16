"""Same Caliper hand, two topics (trap) versus a real house jump (easy)."""

from __future__ import annotations

from pathlib import Path

from kerf.report import document_report

ROOT = Path(__file__).resolve().parents[1] / "corpus"


def main() -> None:
    print("=== EASY: house and topic both jump ===")
    print(document_report(ROOT / "problem-05-caliper-well-then-placard-booth.txt"))
    print("=== TRAP: only the topic jumps ===")
    print(document_report(ROOT / "problem-20-caliper-well-then-caliper-booth.txt"))


if __name__ == "__main__":
    main()
