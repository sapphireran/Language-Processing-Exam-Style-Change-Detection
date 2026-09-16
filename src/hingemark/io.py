"""PAN-shaped problem / truth / solution files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .tokenize import Mode, split_units


@dataclass(frozen=True)
class Problem:
    path: Path
    text: str
    units: tuple[str, ...]

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def n_hinges(self) -> int:
        return max(len(self.units) - 1, 0)


@dataclass(frozen=True)
class Truth:
    path: Path
    changes: tuple[int, ...]
    authors: tuple[int, ...] | None
    meta: dict[str, Any]

    @property
    def n_authors_from_changes(self) -> int:
        return 1 + sum(self.changes)

    @property
    def returning_author(self) -> bool:
        if self.authors is None:
            return False
        return len(set(self.authors)) != self.n_authors_from_changes


def read_problem(path: str | Path, mode: Mode = "lines") -> Problem:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    units = tuple(split_units(text, mode=mode))
    if len(units) < 2:
        raise ValueError(f"{p} needs at least two units, got {len(units)}")
    return Problem(path=p, text=text, units=units)


def read_truth(path: str | Path) -> Truth:
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    changes = tuple(int(x) for x in raw["changes"])
    authors = tuple(int(x) for x in raw["authors"]) if "authors" in raw else None
    meta = {k: v for k, v in raw.items() if k not in {"changes", "authors"}}
    return Truth(path=p, changes=changes, authors=authors, meta=meta)


def write_solution(path: str | Path, changes: Sequence[int]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {"changes": [int(x) for x in changes]}
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def truth_path_for(problem: Path, truth_dir: Path | None = None) -> Path:
    name = problem.name
    if name.startswith("problem-"):
        truth_name = "truth-" + name.replace(".txt", ".json")
    else:
        truth_name = problem.stem + ".json"
    if truth_dir is None:
        sibling = problem.parent / "truth" / truth_name
        if sibling.exists():
            return sibling
        return problem.parent / truth_name
    return Path(truth_dir) / truth_name
