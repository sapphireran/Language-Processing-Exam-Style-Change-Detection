"""Load the teaching corpus from examples/corpus."""

from __future__ import annotations

import json
from pathlib import Path

from .io import Problem, read_problem

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = ROOT / "examples" / "corpus"


def corpus_dir(path: Path | str | None = None) -> Path:
    return Path(path) if path else DEFAULT_CORPUS


def iter_problems(path: Path | str | None = None) -> list[Problem]:
    folder = corpus_dir(path)
    problems = sorted(folder.glob("problem-*.txt"))
    return [read_problem(p) for p in problems]


def load_manifest(path: Path | str | None = None) -> dict:
    folder = corpus_dir(path)
    man = folder / "manifest.json"
    if not man.exists():
        return {}
    return json.loads(man.read_text(encoding="utf-8"))


def problems_by_site(path: Path | str | None = None) -> dict[str, list[Problem]]:
    buckets: dict[str, list[Problem]] = {}
    for problem in iter_problems(path):
        buckets.setdefault(problem.truth.site, []).append(problem)
    return buckets


def validate_corpus(path: Path | str | None = None) -> list[str]:
    errors: list[str] = []
    for problem in iter_problems(path):
        for err in problem.truth.validate(len(problem.units)):
            errors.append(f"{problem.problem_id}: {err}")
        if not problem.units:
            errors.append(f"{problem.problem_id}: empty")
    return errors
