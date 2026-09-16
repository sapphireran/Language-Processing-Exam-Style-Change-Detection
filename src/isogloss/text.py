"""Split a document into analysis units and into words.

PAN asks for sentence-level hinges. This lab's original bank uses
blank-line paragraphs as the unit so a house can speak in a short
block without a brittle sentence splitter. If a file has no blank
line, we fall back to a conservative sentence split.
"""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


def split_units(text: str) -> list[str]:
    """Return blank-line paragraphs, or sentences if the file is one block."""
    cleaned = text.replace("\r\n", "\n").strip()
    if not cleaned:
        return []
    if re.search(r"\n\s*\n", cleaned):
        return [block.strip() for block in re.split(r"\n\s*\n", cleaned) if block.strip()]
    sentences = [part.strip() for part in SENTENCE_RE.split(cleaned) if part.strip()]
    return sentences or [cleaned]


def words(text: str) -> list[str]:
    return [match.group(0) for match in WORD_RE.finditer(text)]


def lower_words(text: str) -> list[str]:
    return [token.lower() for token in words(text)]
