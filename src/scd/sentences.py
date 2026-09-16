"""Unitisation helpers. Toy files are one unit per line."""

from __future__ import annotations

import re

_SENT_SPLIT = re.compile(
    r"(?<=[.!?])\s+(?=[\"'(]*[A-Z0-9])"
)
_PARAGRAPH_SPLIT = re.compile(r"\r?\n\s*\r?\n")


def split_lines(text: str) -> list[str]:
    """One unit per non-empty line. Preserves intra-line spaces."""
    units = []
    for raw_line in re.split(r"\r?\n", text):
        line = raw_line.strip()
        if line:
            units.append(line)
    return units


def split_paragraphs(text: str) -> list[str]:
    units = []
    for block in _PARAGRAPH_SPLIT.split(text.strip()):
        paragraph = re.sub(r"\s+", " ", block).strip()
        if paragraph:
            units.append(paragraph)
    return units


def split_sentences(text: str) -> list[str]:
    """Lightweight sentence splitter for free-form text.

    The synthetic corpus is stored one unit per line, so production
    example code should prefer ``mode="line"``. This splitter exists
    for the exam-note discussion of off-by-one bugs and for any
    pasted paragraph.
    """
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    pieces = []
    for paragraph in split_paragraphs(text) or [text]:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        chunks = _SENT_SPLIT.split(paragraph)
        pieces.extend(chunk.strip() for chunk in chunks if chunk.strip())
    return pieces


def split_units(text: str, mode: str = "line") -> list[str]:
    if mode == "line":
        return split_lines(text)
    if mode == "sentence":
        return split_sentences(text)
    if mode == "paragraph":
        return split_paragraphs(text)
    raise ValueError(f"unknown unit mode: {mode!r}")
