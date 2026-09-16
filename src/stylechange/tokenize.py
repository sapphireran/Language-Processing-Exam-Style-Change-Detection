"""Split a document into the units the detector will compare.

PAN 2023 scored *paragraph* pairs. Later editions scored *sentence* pairs.
The bundled exam files use one sentence per line (no blank lines) unless
the name says ``paragraph``. ``auto`` picks:

- paragraph, if the file contains a blank line
- one unit per non-empty line, if every line already looks like a unit
- otherwise a light punctuation splitter
"""

from __future__ import annotations

import re
from typing import Literal

Granularity = Literal["auto", "sentence", "paragraph"]

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(\[])")
_BLANK = re.compile(r"\n\s*\n")


def split_paragraphs(text: str) -> list[str]:
    chunks = _BLANK.split(text.replace("\r\n", "\n").strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def split_sentences(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    parts = _SENT_SPLIT.split(text)
    return [part.strip() for part in parts if part.strip()]


def _looks_like_line_units(lines: list[str]) -> bool:
    """True when the author already put one comparison unit on each line."""
    if len(lines) < 2:
        return False
    # A wrapped paragraph dumped as many short lines usually has
    # several lines that do not end in sentence punctuation.
    ended = sum(1 for line in lines if line[-1] in ".!?:" or "->" in line)
    return ended >= max(2, int(0.6 * len(lines)))


def segment(text: str, granularity: Granularity = "auto") -> list[str]:
    """Return the ordered units the ``changes`` array is aligned to."""
    raw = text.replace("\r\n", "\n")
    if granularity == "paragraph":
        return split_paragraphs(raw)

    paragraphs = split_paragraphs(raw)
    has_blank = len(paragraphs) > 1

    if granularity == "auto" and has_blank:
        return paragraphs

    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    if granularity in {"auto", "sentence"} and not has_blank and _looks_like_line_units(lines):
        return lines

    if granularity == "sentence" and has_blank:
        units: list[str] = []
        for paragraph in paragraphs:
            units.extend(split_sentences(paragraph))
        return units

    return split_sentences(raw)
