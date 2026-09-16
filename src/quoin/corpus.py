"""Load the original example bank that lives under examples/corpus/."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .io import Problem, Solution, read_problem, read_solution, validate_pair

DEFAULT_CORPUS = Path(__file__).resolve().parents[2] / "examples" / "corpus"


@dataclass(frozen=True)
class Item:
    problem: Problem
    truth: Solution
    meta: dict

    @property
    def name(self) -> str:
        return self.problem.stem

    @property
    def band(self) -> str:
        return str(self.meta.get("band", "unspecified"))

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.name))


@dataclass(frozen=True)
class Corpus:
    root: Path
    items: list[Item]
    manifest: dict

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def by_band(self, band: str) -> list[Item]:
        return [item for item in self.items if item.band == band]

    def get(self, name: str) -> Item:
        for item in self.items:
            if item.name == name or item.problem.path.name == name:
                return item
        raise KeyError(name)


def _truth_path(root: Path, problem_path: Path) -> Path:
    return root / "truth" / f"truth-{problem_path.name.replace('.txt', '.json')}"


def load_corpus(root: str | Path | None = None) -> Corpus:
    root = Path(root) if root is not None else DEFAULT_CORPUS
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items: list[Item] = []
    for entry in manifest["documents"]:
        problem = read_problem(root / entry["file"])
        truth = read_solution(_truth_path(root, problem.path))
        validate_pair(problem, truth)
        items.append(Item(problem=problem, truth=truth, meta=entry))
    return Corpus(root=root, items=items, manifest=manifest)
