"""PAN-shaped JSON I/O plus a tiny truth record for the study files."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Truth:
    path: Path
    granularity: str
    changes: list[int]
    authors: list[int] = field(default_factory=list)
    notes: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def multi_author(self) -> bool:
        if self.authors:
            return len(set(self.authors)) > 1
        return any(self.changes)


def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_truth(path: str | Path) -> Truth:
    data = read_json(path)
    changes = [int(x) for x in data.get("changes", [])]
    authors = [int(x) for x in data.get("authors", [])]
    granularity = str(data.get("granularity", "sentence"))
    notes = str(data.get("notes", ""))
    return Truth(
        path=Path(path),
        granularity=granularity,
        changes=changes,
        authors=authors,
        notes=notes,
        raw=data,
    )


def write_solution(
    path: str | Path,
    changes: list[int],
    authors: list[int] | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {"changes": [int(x) for x in changes]}
    if authors is not None:
        payload["authors"] = [int(x) for x in authors]
    if extra:
        payload.update(extra)
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")
