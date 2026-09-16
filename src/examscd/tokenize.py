"""Sentence and paragraph splitters that stay exam-explainable.

I deliberately avoid a statistical sentence model. The exam documents in
this repo are written so that one of two things is true:

1. Each non-empty line is already one sentence (the study-note convention).
2. Paragraphs are separated by a blank line.

A lightweight fallback splitter still exists for pasted prose, but it is
a regex, not spaCy. If a sentence boundary is legally interesting, write
the study file as one sentence per line.
"""

from __future__ import annotations

import re

_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'“])')
_ABBREV_DOT = re.compile(
    r"\b(?:e\.g|i\.e|vs|etc|Dr|Mr|Ms|Mrs|Prof|Fig|Eq|No)\.$",
    re.IGNORECASE,
)


def split_paragraphs(text: str) -> list[str]:
    """Split on blank lines. Isolated lines become their own paragraphs."""
    blocks = re.split(r"\n\s*\n", text.strip())
    return [block.strip() for block in blocks if block.strip()]


def _looks_like_line_sentences(lines: list[str]) -> bool:
    if len(lines) < 2:
        return False
    ended = sum(1 for line in lines if line[-1] in ".?!…")
    return ended >= max(2, int(0.6 * len(lines)))


def split_sentences(text: str) -> list[str]:
    """Prefer one-sentence-per-line files; otherwise use a regex split."""
    raw = text.replace("\r\n", "\n").strip()
    if not raw:
        return []
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    if _looks_like_line_sentences(lines):
        return lines
    # Collapse newlines so wrapped prose still splits on punctuation.
    collapsed = re.sub(r"\s+", " ", raw)
    parts = _SENT_SPLIT.split(collapsed)
    sentences = [part.strip() for part in parts if part.strip()]
    # Re-join a trailing abbreviation that the regex cut too early.
    merged: list[str] = []
    for part in sentences:
        if merged and _ABBREV_DOT.search(merged[-1]):
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)
    return merged


def split_units(text: str, granularity: str = "sentence") -> list[str]:
    """Split a document into the units a detector will score."""
    key = granularity.strip().lower()
    if key in {"sentence", "s", "sent"}:
        return split_sentences(text)
    if key in {"paragraph", "p", "para"}:
        return split_paragraphs(text)
    raise ValueError(f"unknown granularity: {granularity!r}")
