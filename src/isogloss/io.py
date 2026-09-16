"""PAN-shaped problem I/O.

A problem file is `problem-<id>-<slug>.txt` or `problem-<id>.txt`.
Truth is `truth-problem-<id>.json` next to it, or under `truth/`.
The detector reads only the text. Extra JSON keys are for the lab.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .text import split_units

PROBLEM_NAME = re.compile(r"^problem-(\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class Problem:
    path: Path
    ident: str
    text: str
    units: list[str]
    truth: dict | None

    @property
    def n_units(self) -> int:
        return len(self.units)

    @property
    def n_hinges(self) -> int:
        return max(0, self.n_units - 1)

    @property
    def gold(self) -> list[int] | None:
        if not self.truth:
            return None
        changes = self.truth.get("changes")
        if changes is None:
            return None
        return [int(x) for x in changes]


def problem_id(path: Path) -> str:
    match = PROBLEM_NAME.match(path.name)
    if not match:
        raise ValueError(f"not a problem file: {path.name}")
    return match.group(1)


def read_text(path: Path) -> str:
    # PAN asks for newline="" so Windows files do not grow extra breaks.
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _truth_candidates(problem_path: Path, ident: str) -> list[Path]:
    parent = problem_path.parent
    candidates = [
        parent / f"truth-problem-{ident}.json",
        parent / "truth" / f"truth-problem-{ident}.json",
        parent / f"truth-problem-{ident.zfill(2)}.json",
        *sorted(parent.glob(f"truth-problem-{ident}*.json")),
    ]
    truth_dir = parent / "truth"
    if truth_dir.is_dir():
        candidates.extend(sorted(truth_dir.glob(f"truth-problem-{ident}*.json")))
    return candidates


def read_truth(problem_path: Path, ident: str) -> dict | None:
    seen: set[Path] = set()
    for candidate in _truth_candidates(problem_path, ident):
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return None


def read_problem(path: Path | str) -> Problem:
    path = Path(path)
    ident = problem_id(path)
    text = read_text(path)
    return Problem(
        path=path,
        ident=ident,
        text=text,
        units=split_units(text),
        truth=read_truth(path, ident),
    )


def iter_problems(folder: Path | str) -> Iterator[Problem]:
    folder = Path(folder)
    paths = sorted(
        p for p in folder.glob("problem-*.txt") if p.is_file()
    )
    for path in paths:
        yield read_problem(path)


def write_solution(path: Path | str, changes: list[int]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"changes": [int(x) for x in changes]}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def solution_name(ident: str) -> str:
    return f"solution-problem-{ident}.json"
