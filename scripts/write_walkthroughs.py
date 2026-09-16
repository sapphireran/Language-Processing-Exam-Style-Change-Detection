#!/usr/bin/env python3
"""Write explain dumps for the documents the oral names."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from inkfold.corpus import iter_problems  # noqa: E402
from inkfold.explain import explain_document, format_explain  # noqa: E402

ORAL = {
    "problem-01-kiln-then-notice",
    "problem-13-two-bellfounders",
    "problem-19-stall-three-topics",
    "problem-21-chat-three-topics",
    "problem-22-kiln-return",
    "problem-24-gift-abstract",
}


def main() -> int:
    dest = Path(__file__).resolve().parents[1] / "examples" / "walkthroughs"
    dest.mkdir(parents=True, exist_ok=True)
    written = 0
    for problem in iter_problems():
        if problem.problem_id not in ORAL:
            continue
        text = format_explain(problem, explain_document(problem))
        (dest / f"{problem.problem_id}.md").write_text(text + "\n", encoding="utf-8")
        written += 1
    (dest / "README.md").write_text(
        "Explain dumps for the six documents the oral should name.\n"
        "Regenerate with `PYTHONPATH=src python3 scripts/write_walkthroughs.py`.\n",
        encoding="utf-8",
    )
    print(f"wrote {written} walkthroughs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
