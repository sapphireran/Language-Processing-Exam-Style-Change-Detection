"""Load the bundled teaching corpus from examples/corpus."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .io import Problem, Truth, read_problem, read_truth, truth_path_for
from .tokenize import Mode

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = REPO_ROOT / "examples" / "corpus"


@dataclass(frozen=True)
class CorpusItem:
    problem: Problem
    truth: Truth
    split: str
    note: str

    @property
    def name(self) -> str:
        return self.problem.stem


def load_manifest(corpus_dir: Path | None = None) -> dict:
    root = Path(corpus_dir) if corpus_dir else DEFAULT_CORPUS
    return json.loads((root / "manifest.json").read_text(encoding="utf-8"))


def iter_corpus(
    corpus_dir: Path | None = None,
    *,
    mode: Mode = "lines",
    splits: tuple[str, ...] | None = None,
) -> Iterator[CorpusItem]:
    root = Path(corpus_dir) if corpus_dir else DEFAULT_CORPUS
    manifest = load_manifest(root)
    wanted = set(splits) if splits else None
    for entry in manifest["documents"]:
        if wanted and entry["split"] not in wanted:
            continue
        problem_path = root / entry["file"]
        truth_dir = root / entry.get("truth_dir", "truth")
        problem = read_problem(problem_path, mode=mode)
        truth = read_truth(truth_path_for(problem_path, truth_dir))
        if len(truth.changes) != problem.n_hinges:
            raise ValueError(
                f"{problem.stem}: changes={len(truth.changes)} hinges={problem.n_hinges}"
            )
        if truth.authors is not None and len(truth.authors) != len(problem.units):
            raise ValueError(
                f"{problem.stem}: authors={len(truth.authors)} units={len(problem.units)}"
            )
        yield CorpusItem(
            problem=problem,
            truth=truth,
            split=entry["split"],
            note=entry.get("note", ""),
        )


def list_corpus(
    corpus_dir: Path | None = None,
    *,
    mode: Mode = "lines",
    splits: tuple[str, ...] | None = None,
) -> list[CorpusItem]:
    return list(iter_corpus(corpus_dir, mode=mode, splits=splits))
