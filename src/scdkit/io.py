"""PAN-shaped document and truth I/O.

A problem file is plain UTF-8 text. The matching truth file is JSON::

    {"changes": [1, 0, 1]}

Optional extra keys used by this kit (ignored by a real PAN evaluator):

    authors, paragraph_authors, title, notes, difficulty
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

from .tokenize import split_paragraphs


@dataclass(frozen=True)
class Truth:
    changes: tuple[int, ...]
    authors: int | None = None
    paragraph_authors: tuple[int, ...] | None = None
    title: str | None = None
    notes: str | None = None
    difficulty: str | None = None
    extra: tuple[tuple[str, Any], ...] = ()

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"changes": list(self.changes)}
        if self.authors is not None:
            payload["authors"] = self.authors
        if self.paragraph_authors is not None:
            payload["paragraph_authors"] = list(self.paragraph_authors)
        if self.title:
            payload["title"] = self.title
        if self.notes:
            payload["notes"] = self.notes
        if self.difficulty:
            payload["difficulty"] = self.difficulty
        payload.update(dict(self.extra))
        return payload


def load_document(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def dump_document(path: str | Path, text: str) -> None:
    Path(path).write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def load_truth(path: str | Path) -> Truth:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if "changes" not in raw:
        raise ValueError(f"{path} has no 'changes' array")
    changes = tuple(int(x) for x in raw["changes"])
    if any(flag not in (0, 1) for flag in changes):
        raise ValueError(f"{path} changes must be 0/1")
    reserved = {
        "changes",
        "authors",
        "paragraph_authors",
        "title",
        "notes",
        "difficulty",
    }
    extra = tuple((k, raw[k]) for k in raw if k not in reserved)
    authors = raw.get("authors")
    paragraph_authors = raw.get("paragraph_authors")
    return Truth(
        changes=changes,
        authors=int(authors) if authors is not None else None,
        paragraph_authors=(
            tuple(int(x) for x in paragraph_authors)
            if paragraph_authors is not None
            else None
        ),
        title=raw.get("title"),
        notes=raw.get("notes"),
        difficulty=raw.get("difficulty"),
        extra=extra,
    )


def dump_truth(path: str | Path, truth: Truth | dict[str, Any]) -> None:
    payload = truth.as_dict() if isinstance(truth, Truth) else truth
    Path(path).write_text(
        json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def write_prediction(path: str | Path, changes: Iterable[int]) -> None:
    dump_truth(path, {"changes": [int(x) for x in changes]})


def pair_problems(
    document_dir: str | Path,
    truth_dir: str | Path | None = None,
) -> list[tuple[Path, Path]]:
    """Match ``problem-*.txt`` / ``*.txt`` files to neighbouring truth JSON."""
    document_dir = Path(document_dir)
    truth_dir = Path(truth_dir) if truth_dir else document_dir
    pairs: list[tuple[Path, Path]] = []
    for doc in sorted(document_dir.glob("*.txt")):
        candidates = [
            truth_dir / f"truth-{doc.stem}.json",
            truth_dir / f"{doc.stem}.json",
            truth_dir / "truth" / f"{doc.stem}.json",
            truth_dir / "labels" / f"{doc.stem}.json",
        ]
        truth = next((c for c in candidates if c.is_file()), None)
        if truth is not None:
            pairs.append((doc, truth))
    return pairs


def iter_collection(
    document_dir: str | Path,
    truth_dir: str | Path | None = None,
) -> Iterator[tuple[Path, str, Truth]]:
    for doc_path, truth_path in pair_problems(document_dir, truth_dir):
        text = load_document(doc_path)
        truth = load_truth(truth_path)
        n_para = len(split_paragraphs(text))
        if n_para == 0:
            raise ValueError(f"{doc_path} is empty")
        if len(truth.changes) != n_para - 1:
            raise ValueError(
                f"{truth_path} has {len(truth.changes)} labels for "
                f"{n_para} paragraphs in {doc_path}"
            )
        yield doc_path, text, truth
