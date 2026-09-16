"""PAN 2023-style problem / truth / solution files.

The official task stores one document in ``problem-X.txt`` and the
boundary labels in ``truth-problem-X.json``. A submitted system writes
``solution-problem-X.json`` with a ``changes`` array of 0/1 decisions,
one per pair of consecutive paragraphs.

This module only implements that on-disk contract so exam examples can
be scored with the same file layout. It does not download PAN data.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .tokenize import split_paragraphs


@dataclass(frozen=True)
class Problem:
    problem_id: str
    text: str
    path: Path | None = None

    @property
    def paragraphs(self) -> list[str]:
        return split_paragraphs(self.text)

    @property
    def n_boundaries(self) -> int:
        return max(len(self.paragraphs) - 1, 0)


@dataclass(frozen=True)
class Truth:
    problem_id: str
    changes: list[int]
    authors: int | None = None
    path: Path | None = None
    notes: str | None = None
    difficulty: str | None = None
    title: str | None = None

    def as_json(self) -> dict[str, object]:
        payload: dict[str, object] = {"changes": list(self.changes)}
        if self.authors is not None:
            payload["authors"] = self.authors
        if self.notes:
            payload["notes"] = self.notes
        if self.difficulty:
            payload["difficulty"] = self.difficulty
        if self.title:
            payload["title"] = self.title
        return payload


@dataclass
class Collection:
    problems: list[Problem] = field(default_factory=list)
    truths: dict[str, Truth] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.problems)

    def pairs(self) -> Iterator[tuple[Problem, Truth | None]]:
        for problem in self.problems:
            yield problem, self.truths.get(problem.problem_id)


def _read_text(path: Path) -> str:
    # PAN's note: open with newline="" so Windows files stay intact.
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def infer_problem_id(path: Path) -> str:
    name = path.stem
    for prefix in ("problem-", "solution-problem-", "truth-problem-"):
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


def load_problem(path: Path | str, problem_id: str | None = None) -> Problem:
    path = Path(path)
    return Problem(
        problem_id=problem_id or infer_problem_id(path),
        text=_read_text(path),
        path=path,
    )


def load_truth(path: Path | str, problem_id: str | None = None) -> Truth:
    path = Path(path)
    payload = json.loads(_read_text(path))
    changes = [int(flag) for flag in payload.get("changes", [])]
    authors = payload.get("authors")
    return Truth(
        problem_id=problem_id or infer_problem_id(path),
        changes=changes,
        authors=int(authors) if authors is not None else None,
        path=path,
        notes=payload.get("notes"),
        difficulty=payload.get("difficulty"),
        title=payload.get("title"),
    )


def write_solution(path: Path | str, changes: list[int]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"changes": [int(flag) for flag in changes]}, indent=2) + "\n",
        encoding="utf-8",
    )


def write_truth(path: Path | str, truth: Truth) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(truth.as_json(), indent=2) + "\n", encoding="utf-8")


def write_problem(path: Path | str, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def load_collection(root: Path | str) -> Collection:
    """Load a folder of problem-*.txt plus optional truth-*.json files."""
    root = Path(root)
    if not root.is_dir():
        raise FileNotFoundError(root)
    problems = []
    for path in sorted(root.glob("problem-*.txt")):
        problems.append(load_problem(path))
    if not problems:
        # Also accept a flat corpus of *.txt that is not PAN-prefixed.
        for path in sorted(root.glob("*.txt")):
            if path.name.startswith("truth-"):
                continue
            problems.append(load_problem(path))
    truths: dict[str, Truth] = {}
    truth_dirs = [root, root / "truth", root / "labels"]
    for folder in truth_dirs:
        if not folder.is_dir():
            continue
        for path in folder.glob("truth-*.json"):
            truth = load_truth(path)
            truths[truth.problem_id] = truth
        for path in folder.glob("*.json"):
            if path.name.startswith("solution-"):
                continue
            if path.stem in truths or path.name.startswith("manifest"):
                continue
            try:
                truth = load_truth(path)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
            truths.setdefault(truth.problem_id, truth)
    return Collection(problems=problems, truths=truths)


def load_solutions(root: Path | str) -> dict[str, list[int]]:
    root = Path(root)
    solutions: dict[str, list[int]] = {}
    for path in sorted(root.glob("solution-*.json")):
        payload = json.loads(_read_text(path))
        solutions[infer_problem_id(path)] = [int(flag) for flag in payload["changes"]]
    return solutions
