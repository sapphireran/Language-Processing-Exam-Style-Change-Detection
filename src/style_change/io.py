"""Read problem texts / gold files and write solution JSON."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .paragraphs import split_paragraphs

PROBLEM_NAME = re.compile(r"^problem-(?P<id>.+)\.txt$")
TRUTH_NAME = re.compile(r"^truth-problem-(?P<id>.+)\.json$")
SOLUTION_NAME = "solution-problem-{id}.json"


@dataclass(frozen=True)
class Problem:
    problem_id: str
    text: str
    paragraphs: list[str]
    gold_changes: list[int] | None = None
    authors: int | None = None
    source_path: Path | None = None

    @property
    def n_boundaries(self) -> int:
        return max(0, len(self.paragraphs) - 1)


def _read_text(path: Path) -> str:
    # newline="" keeps the same bytes-to-lines behaviour exam validators expect.
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def load_problem(path: str | Path, truth_path: str | Path | None = None) -> Problem:
    problem_path = Path(path)
    match = PROBLEM_NAME.match(problem_path.name)
    if not match:
        raise ValueError(f"expected problem-*.txt, got {problem_path.name}")
    problem_id = match.group("id")
    text = _read_text(problem_path)
    paragraphs = split_paragraphs(text)

    gold_changes = None
    authors = None
    if truth_path is None:
        candidate = problem_path.with_name(f"truth-problem-{problem_id}.json")
        if candidate.exists():
            truth_path = candidate
    if truth_path is not None:
        payload = json.loads(Path(truth_path).read_text(encoding="utf-8"))
        gold_changes = [int(v) for v in payload["changes"]]
        authors = payload.get("authors")
        if len(gold_changes) != max(0, len(paragraphs) - 1):
            raise ValueError(
                f"{problem_path.name}: gold has {len(gold_changes)} labels "
                f"but {len(paragraphs)} paragraphs"
            )

    return Problem(
        problem_id=problem_id,
        text=text,
        paragraphs=paragraphs,
        gold_changes=gold_changes,
        authors=authors,
        source_path=problem_path,
    )


def load_problem_dir(directory: str | Path) -> list[Problem]:
    root = Path(directory)
    problems = []
    for path in sorted(root.glob("problem-*.txt")):
        problems.append(load_problem(path))
    if not problems:
        raise FileNotFoundError(f"no problem-*.txt files in {root}")
    return problems


def write_solution(
    output_dir: str | Path,
    problem_id: str,
    changes: list[int],
) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / SOLUTION_NAME.format(id=problem_id)
    dest.write_text(
        json.dumps({"changes": [int(v) for v in changes]}, indent=2) + "\n",
        encoding="utf-8",
    )
    return dest


def load_solution(path: str | Path) -> list[int]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return [int(v) for v in payload["changes"]]


def load_solution_dir(directory: str | Path) -> dict[str, list[int]]:
    root = Path(directory)
    solutions: dict[str, list[int]] = {}
    for path in sorted(root.glob("solution-problem-*.json")):
        problem_id = path.name.removeprefix("solution-problem-").removesuffix(".json")
        solutions[problem_id] = load_solution(path)
    return solutions
