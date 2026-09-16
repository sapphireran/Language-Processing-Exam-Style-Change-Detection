"""Split a teaching document into units.

The bundled corpus uses one sentence per line so gold `changes` arrays are
unambiguous. Free-form text can be split on blank-line paragraphs or on a
conservative sentence boundary heuristic.
"""

from __future__ import annotations

import re
from typing import Literal

Mode = Literal["lines", "paragraphs", "sentences"]

_ABBREV = {
    "dr",
    "mr",
    "mrs",
    "ms",
    "prof",
    "sr",
    "jr",
    "vs",
    "etc",
    "e.g",
    "i.e",
    "fig",
    "no",
    "vol",
    "pp",
    "al",
    "st",
    "ave",
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")


def split_units(text: str, mode: Mode = "lines") -> list[str]:
    """Return non-empty units from `text` using `mode`."""
    if mode == "lines":
        return [ln.strip() for ln in text.splitlines() if ln.strip()]
    if mode == "paragraphs":
        chunks = re.split(r"\n\s*\n", text.strip())
        return [re.sub(r"\s+", " ", c).strip() for c in chunks if c.strip()]
    if mode == "sentences":
        return split_sentences(text)
    raise ValueError(f"unknown split mode: {mode!r}")


def split_sentences(text: str) -> list[str]:
    """Conservative sentence split. Protects a small abbreviation list."""
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    pieces: list[str] = []
    start = 0
    for match in _SENT_SPLIT.finditer(text):
        end = match.start() + 1
        candidate = text[start:end].strip()
        if _looks_like_abbrev_break(candidate):
            continue
        if candidate:
            pieces.append(candidate)
            start = match.end()
    tail = text[start:].strip()
    if tail:
        pieces.append(tail)
    return pieces


def _looks_like_abbrev_break(candidate: str) -> bool:
    token = re.split(r"\s+", candidate)[-1].rstrip("\"')")
    core = token[:-1].lower() if token.endswith(".") else token.lower()
    return core in _ABBREV


_WORD = re.compile(r"[a-z]+n't|[a-z]+'[a-z]+|[a-z]+")


def word_tokens(text: str) -> list[str]:
    """Lowercased alphabetic tokens plus a few kept contractions."""
    return _WORD.findall(text.lower())


def raw_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:n't|'ll|'re|'ve|'d|'m|'s)?|\d+|[^\w\s]", text)
