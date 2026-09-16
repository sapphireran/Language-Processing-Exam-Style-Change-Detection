"""Resolve study files relative to this folder."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE / "documents"
MANIFEST = DOCS / "manifest.json"


def load_manifest() -> list[dict[str, Path]]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = []
    for item in data["documents"]:
        rows.append(
            {
                "id": item["id"],
                "text": DOCS / item["text"],
                "truth": DOCS / item["truth"],
            }
        )
    return rows
