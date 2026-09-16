"""PAN-shaped problem and truth files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .paragraphs import split_paragraphs


@dataclass(frozen=True)
class ProblemDocument:
    path: Path
    text: str
    paragraphs: tuple[str, ...]
    truth: dict | None = None

    @property
    def problem_id(self) -> str:
        name = self.path.name
        if name.startswith("problem-") and name.endswith(".txt"):
            return name[len("problem-") : -len(".txt")]
        return self.path.stem

    @property
    def gold_changes(self) -> list[int] | None:
        if not self.truth:
            return None
        changes = self.truth.get("changes")
        if changes is None:
            return None
        return [int(x) for x in changes]


def load_problem(path: str | Path, truth: dict | None = None) -> ProblemDocument:
    path = Path(path)
    # PAN asks for newline="" so Windows CR is not rewritten away.
    with path.open("r", encoding="utf-8", newline="") as handle:
        text = handle.read()
    paragraphs = tuple(split_paragraphs(text))
    return ProblemDocument(path=path, text=text, paragraphs=paragraphs, truth=truth)


def load_truth(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_solution(path: str | Path, changes: list[int]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"changes": [int(x) for x in changes]}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def truth_path_for(problem_path: str | Path) -> Path:
    path = Path(problem_path)
    return path.with_name(f"truth-problem-{path.name[len('problem-'):]}" if path.name.startswith("problem-") else f"truth-{path.name}").with_suffix(".json")


def solution_name_for(problem_path: str | Path) -> str:
    path = Path(problem_path)
    if path.name.startswith("problem-") and path.name.endswith(".txt"):
        ident = path.name[len("problem-") : -len(".txt")]
        return f"solution-problem-{ident}.json"
    return f"solution-{path.stem}.json"


def iter_corpus(root: str | Path) -> list[ProblemDocument]:
    root = Path(root)
    problems = sorted(root.rglob("problem-*.txt"))
    docs: list[ProblemDocument] = []
    for problem in problems:
        tpath = truth_path_for(problem)
        truth = load_truth(tpath) if tpath.exists() else None
        docs.append(load_problem(problem, truth=truth))
    return docs
