#!/usr/bin/env python3
"""Write problem-*.txt, truth-*.json, and manifest.json from the bank."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples" / "corpus"))
sys.path.insert(0, str(ROOT / "src"))

from bank import DOCUMENTS, manifest  # noqa: E402
from inkfold.io import Truth, write_problem, write_truth  # noqa: E402


def main() -> int:
    dest = ROOT / "examples" / "corpus"
    truth_dir = dest / "truth"
    truth_dir.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("problem-*.txt"):
        old.unlink()
    for old in truth_dir.glob("truth-*.json"):
        old.unlink()

    for doc in DOCUMENTS:
        write_problem(dest / f"{doc['id']}.txt", doc["units"])
        truth = Truth(
            authors=doc["authors"],
            changes=list(doc["changes"]),
            site=doc["site"],
            title=doc["title"],
            voices=list(doc["voices"]),
            expected_error=doc.get("expected_error"),
            notes=doc.get("notes", ""),
            return_author=bool(doc.get("return_author", False)),
        )
        errors = truth.validate(len(doc["units"]))
        if errors:
            raise SystemExit(f"{doc['id']}: {errors}")
        write_truth(truth_dir / f"truth-{doc['id']}.json", truth)

    (dest / "manifest.json").write_text(json.dumps(manifest(), indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(DOCUMENTS)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
