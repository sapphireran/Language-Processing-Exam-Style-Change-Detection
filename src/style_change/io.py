"""Load exam-style documents and JSON label files."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Any

from style_change.tokenize import Document, split_paragraphs


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_document(path: str | Path) -> Document:
    source = str(path)
    return split_paragraphs(read_text(path), source=source)


def load_labels(path: str | Path) -> dict[str, Any]:
    """Load a label JSON object.

    Expected keys (all optional except ``authors`` or ``changes``):

    - ``authors``: list[int] gold author id per paragraph
    - ``changes``: list[bool] gold style change after paragraph i
    - ``multi_author``: bool
    - ``notes``: free text
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"label file must be a JSON object: {path}")
    return payload


def dump_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
