"""PAN-style problem / truth / solution files.

A problem is a UTF-8 ``.txt`` file whose paragraphs are separated by a
blank line. A truth file is JSON::

    {"authors": 2, "changes": [0, 1, 0]}

A solution file only needs the ``changes`` array.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from stylechange.paragraphs import split_paragraphs


@dataclass(frozen=True)
class Problem:
    problem_id: str
    path: Path
    text: str
    paragraphs: list[str]


@dataclass(frozen=True)
class Truth:
    problem_id: str
    path: Path
    authors: int | None
    changes: list[int]


def _problem_id_from_name(name: str) -> str:
    stem = Path(name).stem
    for prefix in ("truth-problem-", "solution-problem-", "problem-"):
        if stem.startswith(prefix):
            return stem[len(prefix) :]
    return stem


def load_problem(path: str | Path) -> Problem:
    path = Path(path)
    # open(..., newline="") matches the PAN reading note.
    with path.open("r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    return Problem(
        problem_id=_problem_id_from_name(path.name),
        path=path,
        text=text,
        paragraphs=split_paragraphs(text),
    )


def load_truth(path: str | Path) -> Truth:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    changes = [int(x) for x in payload["changes"]]
    authors = payload.get("authors")
    return Truth(
        problem_id=_problem_id_from_name(path.name),
        path=path,
        authors=int(authors) if authors is not None else None,
        changes=changes,
    )


def write_solution(path: str | Path, changes: list[int]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"changes": changes}, indent=2) + "\n", encoding="utf-8")


def iter_problems(directory: str | Path) -> Iterator[Problem]:
    directory = Path(directory)
    for path in sorted(directory.glob("problem-*.txt")):
        yield load_problem(path)


def load_split(directory: str | Path) -> list[tuple[Problem, Truth | None]]:
    directory = Path(directory)
    rows: list[tuple[Problem, Truth | None]] = []
    for problem in iter_problems(directory):
        truth_path = directory / f"truth-problem-{problem.problem_id}.json"
        truth = load_truth(truth_path) if truth_path.exists() else None
        rows.append((problem, truth))
    return rows
