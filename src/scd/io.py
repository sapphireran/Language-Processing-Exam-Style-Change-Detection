"""PAN-shaped problem / truth / solution I/O."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PROBLEM_NAME = re.compile(r"^problem-(.+)\.txt$")
TRUTH_NAME = re.compile(r"^truth-problem-(.+)\.json$")
SOLUTION_NAME = re.compile(r"^solution-problem-(.+)\.json$")


class FormatError(ValueError):
    """Raised when a problem, truth, or solution file is inconsistent."""


@dataclass(frozen=True)
class Truth:
    authors: int
    changes: list[int]


def problem_id(name: str | Path) -> str:
    """Return the problem id from a problem, truth, or solution filename."""
    filename = Path(name).name
    for pattern in (PROBLEM_NAME, TRUTH_NAME, SOLUTION_NAME):
        match = pattern.match(filename)
        if match:
            return match.group(1)
    raise FormatError(f"unrecognised filename: {filename}")


def read_text(path: str | Path) -> str:
    """Read a text file without converting newlines."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def read_problem(path: str | Path) -> str:
    text = read_text(path)
    if not text.strip():
        raise FormatError(f"empty problem file: {path}")
    return text


def _as_bit(value: object, *, index: int, path: Path) -> int:
    if value is True:
        return 1
    if value is False:
        return 0
    if value in (0, 1, 0.0, 1.0, "0", "1"):
        return int(value)
    raise FormatError(f"{path}: changes[{index}] is not a binary value: {value!r}")


def _parse_changes(raw: object, *, path: Path) -> list[int]:
    if not isinstance(raw, list):
        raise FormatError(f"{path}: 'changes' must be a list")
    return [_as_bit(item, index=i, path=path) for i, item in enumerate(raw)]


def read_truth(path: str | Path) -> Truth:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise FormatError(f"{path}: truth root must be an object")
    if "changes" not in payload:
        raise FormatError(f"{path}: missing 'changes'")
    if "authors" not in payload:
        raise FormatError(f"{path}: missing 'authors'")
    authors = payload["authors"]
    if not isinstance(authors, int) or isinstance(authors, bool) or authors < 1:
        raise FormatError(f"{path}: 'authors' must be an integer >= 1")
    changes = _parse_changes(payload["changes"], path=path)
    if authors == 1 and any(changes):
        raise FormatError(f"{path}: single-author truth must be all zeros")
    if authors >= 2 and not any(changes):
        raise FormatError(f"{path}: multi-author truth must contain a change")
    return Truth(authors=authors, changes=changes)


def read_solution(path: str | Path) -> list[int]:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "changes" not in payload:
        raise FormatError(f"{path}: solution must be an object with 'changes'")
    return _parse_changes(payload["changes"], path=path)


def write_solution(path: str | Path, changes: Iterable[int]) -> None:
    path = Path(path)
    bits = [int(bit) for bit in changes]
    if any(bit not in (0, 1) for bit in bits):
        raise FormatError(f"solution changes must be 0/1, got {bits}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"changes": bits}, indent=2) + "\n",
        encoding="utf-8",
    )


def write_truth(path: str | Path, authors: int, changes: Iterable[int]) -> None:
    path = Path(path)
    bits = [int(bit) for bit in changes]
    truth = Truth(authors=authors, changes=bits)
    # Re-run the same consistency rules as the reader.
    if truth.authors == 1 and any(truth.changes):
        raise FormatError("single-author truth must be all zeros")
    if truth.authors >= 2 and not any(truth.changes):
        raise FormatError("multi-author truth must contain a change")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"authors": truth.authors, "changes": truth.changes}, indent=2)
        + "\n",
        encoding="utf-8",
    )


def write_problem(path: str | Path, units: Iterable[str]) -> None:
    """Write one unit per line, with a trailing newline."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [unit.replace("\n", " ").strip() for unit in units]
    if not lines or any(not line for line in lines):
        raise FormatError("refusing to write an empty unit")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def list_problems(directory: str | Path) -> list[Path]:
    directory = Path(directory)
    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and PROBLEM_NAME.match(path.name)
    )
    return files


def paired_paths(directory: str | Path) -> list[tuple[Path, Path]]:
    """Return (problem, truth) pairs; skip problems that have no truth file."""
    directory = Path(directory)
    pairs = []
    for problem in list_problems(directory):
        truth = directory / f"truth-problem-{problem_id(problem)}.json"
        if truth.exists():
            pairs.append((problem, truth))
    return pairs


def check_alignment(n_units: int, changes: list[int], *, path: str | Path) -> None:
    expected = max(n_units - 1, 0)
    if n_units < 1:
        raise FormatError(f"{path}: a document must have at least one unit")
    if n_units == 1 and changes:
        raise FormatError(f"{path}: a one-unit document cannot have pair labels")
    if len(changes) != expected:
        raise FormatError(
            f"{path}: expected {expected} pair labels for {n_units} units, "
            f"got {len(changes)}"
        )


def reconstruct_authors(changes: list[int]) -> list[int]:
    """Turn pairwise change bits into 1-based author-run indices."""
    authors = [1]
    current = 1
    for bit in changes:
        if bit:
            current += 1
        authors.append(current)
    return authors
