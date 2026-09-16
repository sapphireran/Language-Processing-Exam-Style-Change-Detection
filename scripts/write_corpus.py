#!/usr/bin/env python3
"""Write problem / truth / manifest files from examples.corpus.bank."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

from corpus.bank import changes_from_authors, iter_documents  # noqa: E402

CORPUS = ROOT / "examples" / "corpus"
TRUTH = CORPUS / "truth"


def main() -> int:
    TRUTH.mkdir(parents=True, exist_ok=True)
    documents = []
    for doc in iter_documents():
        slug = f"problem-{doc['id']}-{doc['slug']}"
        text_path = CORPUS / f"{slug}.txt"
        truth_path = TRUTH / f"truth-{slug}.json"
        changes = changes_from_authors(doc["authors"])
        text_path.write_text("\n".join(doc["units"]) + "\n", encoding="utf-8")
        payload = {
            "changes": changes,
            "authors": doc["authors"],
            "split": doc["split"],
            "note": doc["note"],
        }
        truth_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        documents.append(
            {
                "id": doc["id"],
                "slug": doc["slug"],
                "split": doc["split"],
                "file": text_path.name,
                "truth_dir": "truth",
                "n_units": len(doc["units"]),
                "n_hinges": len(changes),
                "n_authors": len(set(doc["authors"])),
                "n_authors_from_changes": 1 + sum(changes),
                "returning_author": len(set(doc["authors"])) != 1 + sum(changes),
                "note": doc["note"],
            }
        )
    manifest = {
        "title": "HingeMark teaching corpus",
        "unit": "one sentence per line",
        "documents": documents,
    }
    (CORPUS / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {len(documents)} documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
