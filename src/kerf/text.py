"""Light tokenisation. No model, no download, no language-id."""

from __future__ import annotations

import re

_ABBREV = re.compile(
    r"\b(?:Mr|Mrs|Ms|Dr|Prof|St|vs|etc|e\.g|i\.e|No|Fig|al)\.$",
    re.IGNORECASE,
)
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“])")
_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?")
_CONTRACTION = re.compile(
    r"\b(?:(?:[A-Za-z]+)'(?:t|re|ve|ll|d|s|m)|n't)\b",
    re.IGNORECASE,
)


def split_paragraphs(text: str) -> list[str]:
    chunks = [p.strip() for p in re.split(r"\n\s*\n", text.strip())]
    return [c for c in chunks if c]


def split_sentences(paragraph: str) -> list[str]:
    """Split on end punctuation. Keep a trailing abbreviation attached."""
    paragraph = paragraph.strip()
    if not paragraph:
        return []
    raw = _SENT_SPLIT.split(paragraph)
    out: list[str] = []
    buf = ""
    for piece in raw:
        piece = piece.strip()
        if not piece:
            continue
        if buf:
            candidate = f"{buf} {piece}"
        else:
            candidate = piece
        if _ABBREV.search(buf.strip() if buf else ""):
            buf = candidate
            continue
        if buf:
            out.append(buf)
        buf = piece
    if buf:
        out.append(buf)
    return out


def words(text: str) -> list[str]:
    return [m.group(0) for m in _WORD.finditer(text)]


def lower_words(text: str) -> list[str]:
    return [w.lower() for w in words(text)]


def contraction_count(text: str) -> int:
    return len(_CONTRACTION.findall(text))
