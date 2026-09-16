"""Paragraph / sentence / word splitters with no third-party tokenizer.

The exam format is the PAN one: a document is paragraphs separated by one or
more blank lines. I keep the splitter tiny so I can write it on a whiteboard
and so the labs do not hide a spaCy pipeline behind a one-liner.
"""

from __future__ import annotations

import re

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_BLANK_RE = re.compile(r"\n\s*\n+")


def paragraphs(text: str) -> list[str]:
    """Split a PAN-style document into non-empty paragraphs."""
    chunks = [chunk.strip() for chunk in _BLANK_RE.split(text.strip())]
    return [chunk for chunk in chunks if chunk]


def sentences(text: str) -> list[str]:
    """Very small sentence splitter. Abbreviations will fool it; that is fine."""
    text = text.strip()
    if not text:
        return []
    parts = [part.strip() for part in _SENTENCE_RE.split(text)]
    return [part for part in parts if part]


def words(text: str) -> list[str]:
    """Alphabetic tokens, keeping simple English contractions."""
    return [match.group(0).lower() for match in _WORD_RE.finditer(text)]


def word_count(text: str) -> int:
    return len(words(text))


def char_count(text: str) -> int:
    return len(text)


def sentence_lengths(text: str) -> list[int]:
    return [len(words(sentence)) for sentence in sentences(text)]
