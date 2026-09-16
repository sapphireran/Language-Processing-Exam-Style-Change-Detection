"""PAN-shaped problem / truth files. Nothing official is downloaded."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .text import split_paragraphs


@dataclass(frozen=True)
class Problem:
    path: Path
    paragraphs: list[str]

    @property
    def n_hinges(self) -> int:
        return max(0, len(self.paragraphs) - 1)


@dataclass(frozen=True)
class Truth:
    path: Path
    changes: list[int]
    authors: int | None = None

    def as_bool(self) -> list[bool]:
        return [bool(c) for c in self.changes]


def read_problem(path: str | Path) -> Problem:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return Problem(path=path, paragraphs=split_paragraphs(text))


def read_truth(path: str | Path) -> Truth:
    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    changes = [int(c) for c in raw["changes"]]
    authors = raw.get("authors")
    if authors is not None:
        authors = int(authors)
    return Truth(path=path, changes=changes, authors=authors)


def write_prediction(path: str | Path, changes: list[int], authors: int | None = None) -> None:
    path = Path(path)
    payload: dict[str, object] = {"changes": [int(c) for c in changes]}
    if authors is not None:
        payload["authors"] = int(authors)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def paired_files(directory: str | Path) -> list[tuple[Path, Path]]:
    """Match ``problem-*.txt`` with ``truth-problem-*.json`` in one folder."""
    directory = Path(directory)
    pairs: list[tuple[Path, Path]] = []
    for problem in sorted(directory.glob("problem-*.txt")):
        stem = problem.name.removeprefix("problem-").removesuffix(".txt")
        truth = directory / f"truth-problem-{stem}.json"
        if not truth.exists():
            # also accept truth-problem-01.json next to problem-01-slug.txt
            prefix = stem.split("-", 1)[0]
            alt = directory / f"truth-problem-{prefix}.json"
            if alt.exists():
                truth = alt
            else:
                continue
        pairs.append((problem, truth))
    return pairs
