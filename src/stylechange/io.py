"""PAN-shaped problem / truth / solution files.

For each document ``problem-<id>.txt`` a gold file ``truth-problem-<id>.json``
may sit beside it. The detector writes ``solution-problem-<id>.json`` with
only the ``changes`` array — extra keys on the gold file (``difficulty``,
``voices``, ``note``) are for humans and are ignored by the evaluator.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterator

PROBLEM_NAME = re.compile(r"^problem-(.+)\.txt$")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_problem(path: Path | str) -> str:
    # PAN's note: open(..., newline="") so Windows \\r\\n is preserved.
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def problem_id(path: Path) -> str:
    match = PROBLEM_NAME.match(path.name)
    if not match:
        raise ValueError(f"not a problem-*.txt file: {path.name}")
    return match.group(1)


def truth_path(problem: Path) -> Path:
    return problem.with_name(f"truth-problem-{problem_id(problem)}.json")


def solution_path(problem: Path, output_dir: Path | None = None) -> Path:
    name = f"solution-problem-{problem_id(problem)}.json"
    return (output_dir or problem.parent) / name


def write_solution(path: Path, changes: list[int]) -> None:
    dump_json(path, {"changes": list(changes)})


def iter_problems(directory: Path | str) -> Iterator[Path]:
    root = Path(directory)
    files = sorted(root.glob("problem-*.txt"))
    if not files:
        raise FileNotFoundError(f"no problem-*.txt files in {root}")
    yield from files


def load_truth(problem: Path) -> dict[str, Any] | None:
    path = truth_path(problem)
    if not path.exists():
        return None
    return load_json(path)
