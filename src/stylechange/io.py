"""PAN-shaped problem I/O plus the extra study keys we store in truth files."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .sentences import split_sentences

PROBLEM_RE = re.compile(r"problem-(\d+)\.txt$", re.I)
TRUTH_RE = re.compile(r"truth-problem-(\d+)\.json$", re.I)
SOLUTION_RE = re.compile(r"solution-problem-(\d+)\.json$", re.I)


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def problem_id(path: str | Path) -> str:
    name = Path(path).name
    for pattern in (PROBLEM_RE, TRUTH_RE, SOLUTION_RE):
        match = pattern.search(name)
        if match:
            return match.group(1)
    raise ValueError(f"cannot parse problem id from {path}")


def load_document(path: str | Path, *, prefer_lines: bool = True) -> list[str]:
    text = _read_text(Path(path))
    return split_sentences(text, prefer_lines=prefer_lines)


def load_changes(path: str | Path) -> list[int]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        payload = json.load(handle)
    changes = payload.get("changes")
    if not isinstance(changes, list):
        raise ValueError(f"{path} has no changes array")
    return [int(item) for item in changes]


def write_solution(path: str | Path, changes: Iterable[int]) -> None:
    _write_json(Path(path), {"changes": [int(item) for item in changes]})


def write_truth(
    path: str | Path,
    changes: Iterable[int],
    *,
    authors: int | None = None,
    author_ids: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    payload: dict[str, Any] = {"changes": [int(item) for item in changes]}
    if authors is not None:
        payload["authors"] = int(authors)
    if author_ids is not None:
        payload["author_ids"] = list(author_ids)
        payload["authors"] = payload.get("authors", len(set(author_ids)))
    if extra:
        payload.update(extra)
    _write_json(Path(path), payload)


@dataclass
class Problem:
    pid: str
    path: Path
    sentences: list[str]
    changes: list[int] | None = None
    truth_path: Path | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def n_pairs(self) -> int:
        return max(0, len(self.sentences) - 1)

    def assert_aligned(self) -> None:
        if self.changes is not None and len(self.changes) != self.n_pairs:
            raise ValueError(
                f"problem {self.pid}: {len(self.sentences)} sentences but "
                f"{len(self.changes)} change labels"
            )


def _iter_problem_files(root: Path) -> list[Path]:
    files = sorted(root.rglob("problem-*.txt"))
    # Prefer direct children when both a parent and a split folder match.
    return files


def load_manifest(root: str | Path) -> dict[str, Any] | None:
    path = Path(root) / "manifest.json"
    if not path.is_file():
        parent = Path(root).parent / "manifest.json"
        path = parent if parent.is_file() else path
    if not path.is_file():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_problem_dir(
    root: str | Path,
    *,
    require_truth: bool = False,
    split: str | None = None,
    difficulty: str | None = None,
) -> list[Problem]:
    root_path = Path(root)
    manifest = load_manifest(root_path)
    problems: list[Problem] = []
    for problem_path in _iter_problem_files(root_path):
        pid = problem_id(problem_path)
        truth_path = problem_path.with_name(f"truth-problem-{pid}.json")
        if not truth_path.is_file():
            # shared-task layout sometimes uses a sibling truths folder
            alt = problem_path.parent / f"truth-problem-{pid}.json"
            truth_path = alt
        meta: dict[str, Any] = {}
        changes = None
        if truth_path.is_file():
            with truth_path.open("r", encoding="utf-8", newline="") as handle:
                payload = json.load(handle)
            changes = [int(item) for item in payload.get("changes", [])]
            meta = {key: value for key, value in payload.items() if key != "changes"}
        elif require_truth:
            raise FileNotFoundError(truth_path)

        if manifest and "problems" in manifest:
            entry = manifest["problems"].get(f"{problem_path.parent.name}/{problem_path.name}")
            if entry:
                meta = {**entry, **meta}

        if split and meta.get("split") not in {None, split}:
            continue
        if difficulty and difficulty not in {problem_path.parent.name, meta.get("difficulty")}:
            continue

        problem = Problem(
            pid=pid,
            path=problem_path,
            sentences=load_document(problem_path),
            changes=changes,
            truth_path=truth_path if truth_path.is_file() else None,
            meta=meta,
        )
        problem.assert_aligned()
        problems.append(problem)
    return problems


def solution_path(output_dir: str | Path, pid: str) -> Path:
    return Path(output_dir) / f"solution-problem-{pid}.json"
