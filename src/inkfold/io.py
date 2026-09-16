"""PAN-flavoured problem / truth I/O for the teaching corpus."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .tokenize import units_from_text


@dataclass
class Truth:
    authors: int
    changes: list[int]
    site: str = "unspecified"
    title: str = ""
    voices: list[str] = field(default_factory=list)
    expected_error: str | None = None
    notes: str = ""
    return_author: bool = False

    def validate(self, n_units: int) -> list[str]:
        errors = []
        if len(self.changes) != max(n_units - 1, 0):
            errors.append(
                f"changes length {len(self.changes)} != n_units-1 ({n_units - 1})"
            )
        if any(c not in (0, 1) for c in self.changes):
            errors.append("changes must be a 0/1 list")
        naive = 1 + sum(self.changes) if n_units else 0
        if self.return_author and self.authors == naive:
            errors.append("return_author is set but authors == 1+sum(changes)")
        if not self.return_author and n_units and self.authors != naive:
            errors.append(
                f"authors {self.authors} != 1+sum(changes) {naive} (set return_author)"
            )
        return errors


@dataclass
class Problem:
    path: Path
    problem_id: str
    units: list[str]
    truth: Truth

    @property
    def text(self) -> str:
        return "\n".join(self.units) + "\n"


def read_problem_text(path: Path | str) -> list[str]:
    return units_from_text(Path(path).read_text(encoding="utf-8"))


def read_truth(path: Path | str) -> Truth:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return _truth_from_dict(raw)


def _truth_from_dict(raw: dict[str, Any]) -> Truth:
    return Truth(
        authors=int(raw["authors"]),
        changes=[int(c) for c in raw["changes"]],
        site=str(raw.get("site", "unspecified")),
        title=str(raw.get("title", "")),
        voices=list(raw.get("voices", [])),
        expected_error=raw.get("expected_error"),
        notes=str(raw.get("notes", "")),
        return_author=bool(raw.get("return_author", False)),
    )


def read_problem(problem_path: Path | str, truth_path: Path | str | None = None) -> Problem:
    path = Path(problem_path)
    units = read_problem_text(path)
    if truth_path is None:
        truth_path = _default_truth_path(path)
    truth = read_truth(truth_path)
    return Problem(path=path, problem_id=path.stem, units=units, truth=truth)


def _default_truth_path(problem_path: Path) -> Path:
    name = problem_path.name
    if name.startswith("problem-"):
        truth_name = "truth-" + name.replace(".txt", ".json")
    else:
        truth_name = f"truth-{problem_path.stem}.json"
    sibling = problem_path.parent / truth_name
    if sibling.exists():
        return sibling
    nested = problem_path.parent / "truth" / truth_name
    return nested


def write_prediction(path: Path | str, detection_or_truth: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(detection_or_truth, indent=2) + "\n", encoding="utf-8")


def write_truth(path: Path | str, truth: Truth) -> None:
    payload = {
        "authors": truth.authors,
        "changes": truth.changes,
        "site": truth.site,
        "title": truth.title,
        "voices": truth.voices,
        "expected_error": truth.expected_error,
        "notes": truth.notes,
        "return_author": truth.return_author,
    }
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_problem(path: Path | str, units: list[str]) -> None:
    Path(path).write_text("\n".join(units) + "\n", encoding="utf-8")
