"""Load the personal teaching corpus next to this file's repo root."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .features import FeatureTable
from .io import load_problem, load_truth

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CORPUS = REPO_ROOT / "examples" / "corpus"


@dataclass(frozen=True)
class TeachingDoc:
    problem_path: Path
    truth_path: Path
    units: list[str]
    changes: list[int]
    authors: int
    tier: str
    title: str
    voices: list[str]

    @property
    def stem(self) -> str:
        return self.problem_path.stem

    def table(self) -> FeatureTable:
        return FeatureTable.from_units(self.units)


def load_teaching_corpus(root: Path | None = None) -> list[TeachingDoc]:
    folder = root or DEFAULT_CORPUS
    docs: list[TeachingDoc] = []
    for path in sorted(folder.glob("problem-*.txt")):
        truth_path = folder / "truth" / f"truth-{path.stem}.json"
        if not truth_path.is_file():
            raise FileNotFoundError(truth_path)
        problem = load_problem(path)
        truth = load_truth(truth_path)
        raw = truth["raw"]
        if len(truth["changes"]) != problem.n_pairs:
            raise ValueError(
                f"{path.name}: {len(truth['changes'])} labels for {problem.n_pairs} pairs"
            )
        docs.append(
            TeachingDoc(
                problem_path=path,
                truth_path=truth_path,
                units=problem.units,
                changes=truth["changes"],
                authors=int(raw.get("authors", truth["authors"])),
                tier=str(raw.get("tier", "unspecified")),
                title=str(raw.get("title", path.stem)),
                voices=list(raw.get("voices", [])),
            )
        )
    return docs


def write_manifest(path: Path | None = None, root: Path | None = None) -> Path:
    docs = load_teaching_corpus(root)
    dest = path or (root or DEFAULT_CORPUS) / "manifest.json"
    payload = {
        "documents": [
            {
                "file": doc.problem_path.name,
                "truth": f"truth/{doc.truth_path.name}",
                "tier": doc.tier,
                "title": doc.title,
                "authors": doc.authors,
                "voices": doc.voices,
                "n_units": len(doc.units),
                "n_pairs": len(doc.changes),
                "n_changes": int(sum(doc.changes)),
            }
            for doc in docs
        ]
    }
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest
