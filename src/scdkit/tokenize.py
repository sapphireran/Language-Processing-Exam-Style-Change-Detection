"""Lightweight tokenisation for exam-sized English documents.

The kit stays dependency-free. These splitters are good enough for
stylometry on clean paragraphs and are themselves an exam talking point:
you should be able to say what they get wrong (abbreviations, decimals,
dialogue, Markdown leftovers) and why that still rarely flips a
paragraph-level decision.
"""

from __future__ import annotations

import re

_BLANK_SPLIT = re.compile(r"\n\s*\n")
_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_ABBREV = re.compile(
    r"\b(?:Dr|Mr|Mrs|Ms|Prof|vs|etc|e\.g|i\.e|Fig|Eq|No)\.$",
    re.IGNORECASE,
)


def split_paragraphs(text: str) -> list[str]:
    """Split a document into paragraphs.

    Blank lines are the preferred boundary (the format used by the
    bundled examples). If the text is a single block with several
    non-empty lines, fall back to one paragraph per line so PAN-style
    dumps still parse.
    """
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not cleaned:
        return []
    blocks = [part.strip() for part in _BLANK_SPLIT.split(cleaned) if part.strip()]
    if len(blocks) == 1:
        lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
        if len(lines) > 1:
            return lines
    return blocks


def split_sentences(text: str) -> list[str]:
    """Approximate sentence split on ``.!?`` followed by whitespace."""
    text = text.strip()
    if not text:
        return []
    pieces = _SENT_SPLIT.split(text)
    merged: list[str] = []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        if merged and _ABBREV.search(merged[-1]):
            merged[-1] = f"{merged[-1]} {piece}"
        else:
            merged.append(piece)
    if merged and merged[-1] and merged[-1][-1] not in ".!?":
        # Keep fragments (notes, SMS) as their own "sentence".
        pass
    return merged


def split_words(text: str) -> list[str]:
    """Return alphanumeric tokens, keeping internal apostrophes."""
    return _WORD_RE.findall(text)


def lowercase_words(text: str) -> list[str]:
    return [word.lower() for word in split_words(text)]


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
