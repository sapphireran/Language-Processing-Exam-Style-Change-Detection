"""PAN-compatible problem / truth / solution I/O.

A problem directory looks like::

    problem-12.txt
    truth-problem-12.json   # training / validation only

and a detector writes::

    solution-problem-12.json
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import re
from typing import Iterator

PROBLEM_NAME = re.compile(r"^problem-(.+)\.txt$", re.IGNORECASE)
TRUTH_NAME = re.compile(r"^truth-problem-(.+)\.json$", re.IGNORECASE)
SOLUTION_NAME = re.compile(r"^solution-problem-(.+)\.json$", re.IGNORECASE)


@dataclass(frozen=True)
class Solution:
    """Binary change labels between consecutive units."""

    changes: list[int]
    authors: int | None = None
    extra: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        payload = {"changes": [int(c) for c in self.changes]}
        if self.authors is not None:
            payload["authors"] = int(self.authors)
        payload.update(self.extra)
        return payload


@dataclass(frozen=True)
class Problem:
    problem_id: str
    text: str
    path: Path
    truth: Solution | None = None

    @property
    def name(self) -> str:
        return f"problem-{self.problem_id}"


def _read_text(path: Path) -> str:
    # newline="" matches the PAN reading note and keeps Windows files intact.
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _load_solution_payload(path: Path) -> Solution:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if "changes" not in raw:
        raise ValueError(f"{path} is missing a 'changes' array")
    changes = [int(c) for c in raw["changes"]]
    authors = raw.get("authors")
    extra = {k: v for k, v in raw.items() if k not in {"changes", "authors"}}
    return Solution(changes=changes, authors=authors, extra=extra)


def load_problem(path: str | Path, truth_path: str | Path | None = None) -> Problem:
    """Load one ``problem-X.txt`` and an optional gold file."""
    path = Path(path)
    match = PROBLEM_NAME.match(path.name)
    problem_id = match.group(1) if match else path.stem
    truth = None
    if truth_path is not None:
        truth = _load_solution_payload(Path(truth_path))
    else:
        sibling = path.with_name(f"truth-problem-{problem_id}.json")
        if sibling.exists():
            truth = _load_solution_payload(sibling)
    return Problem(problem_id=problem_id, text=_read_text(path), path=path, truth=truth)


def write_solution(path: str | Path, solution: Solution) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(solution.to_json(), indent=2) + "\n", encoding="utf-8")
    return path


def solution_path_for(problem: Problem, output_dir: str | Path) -> Path:
    return Path(output_dir) / f"solution-problem-{problem.problem_id}.json"


def iter_problems(input_dir: str | Path) -> Iterator[Problem]:
    """Yield every ``problem-*.txt`` in a directory, attaching gold if present."""
    directory = Path(input_dir)
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    files = sorted(p for p in directory.iterdir() if PROBLEM_NAME.match(p.name))
    for path in files:
        yield load_problem(path)


def iter_solutions(directory: str | Path) -> dict[str, Solution]:
    directory = Path(directory)
    found: dict[str, Solution] = {}
    for path in sorted(directory.iterdir()):
        match = SOLUTION_NAME.match(path.name) or TRUTH_NAME.match(path.name)
        if not match:
            continue
        found[match.group(1)] = _load_solution_payload(path)
    return found
