"""PAN problem / solution IO.

A problem is a UTF-8 text file of paragraphs. A solution is a JSON object
with a `changes` array of 0/1 flags, one per paragraph boundary. I also
allow an optional `authors` array (one label per paragraph) in the truth
files so the labs can talk about author *return*, not only binary hinges.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .tokenize import paragraphs


@dataclass(frozen=True)
class Problem:
    path: Path
    text: str
    paragraphs: list[str]

    @property
    def n_paragraphs(self) -> int:
        return len(self.paragraphs)

    @property
    def n_boundaries(self) -> int:
        return max(0, self.n_paragraphs - 1)

    @property
    def stem(self) -> str:
        return self.path.stem


@dataclass(frozen=True)
class Solution:
    changes: list[int]
    authors: list[str] | None = None
    extra: dict[str, Any] | None = None

    def as_json(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"changes": [int(bit) for bit in self.changes]}
        if self.authors is not None:
            payload["authors"] = list(self.authors)
        if self.extra:
            payload.update(self.extra)
        return payload


def read_problem(path: str | Path) -> Problem:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    paras = paragraphs(text)
    if not paras:
        raise ValueError(f"{path} has no paragraphs")
    return Problem(path=path, text=text, paragraphs=paras)


def read_solution(path: str | Path) -> Solution:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "changes" not in payload:
        raise ValueError(f"{path} is missing a 'changes' array")
    changes = [int(bit) for bit in payload["changes"]]
    if any(bit not in (0, 1) for bit in changes):
        raise ValueError(f"{path} has a non-binary changes bit")
    authors = payload.get("authors")
    if authors is not None:
        authors = [str(label) for label in authors]
    extra = {key: value for key, value in payload.items() if key not in {"changes", "authors"}}
    return Solution(changes=changes, authors=authors, extra=extra or None)


def write_solution(path: str | Path, solution: Solution) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(solution.as_json(), indent=2) + "\n", encoding="utf-8")


def solution_from_changes(changes: Iterable[int]) -> Solution:
    return Solution(changes=[int(bit) for bit in changes])


def validate_pair(problem: Problem, solution: Solution) -> None:
    if len(solution.changes) != problem.n_boundaries:
        raise ValueError(
            f"{problem.path.name}: expected {problem.n_boundaries} change bits, "
            f"got {len(solution.changes)}"
        )
    if solution.authors is not None and len(solution.authors) != problem.n_paragraphs:
        raise ValueError(
            f"{problem.path.name}: expected {problem.n_paragraphs} author labels, "
            f"got {len(solution.authors)}"
        )
