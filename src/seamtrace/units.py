"""Turn a document into ordered units.

PAN-style teaching files in this repo use one sentence per non-empty
line. Running prose (no line breaks between sentences) is split with
the conservative sentence splitter. Blank lines never become units.
"""

from __future__ import annotations

from .tokenize import sentences_from_prose


def split_units(text: str, *, mode: str = "auto") -> list[str]:
    if mode not in {"auto", "lines", "prose", "paragraphs"}:
        raise ValueError(f"unknown unit mode: {mode}")
    raw = text.replace("\r\n", "\n").replace("\r", "\n")
    if mode == "lines":
        return [line.strip() for line in raw.split("\n") if line.strip()]
    if mode == "paragraphs":
        chunks = re_split_paragraphs(raw)
        return [chunk for chunk in chunks if chunk]
    if mode == "prose":
        return sentences_from_prose(raw)
    lines = [line.strip() for line in raw.split("\n") if line.strip()]
    if len(lines) >= 2:
        return lines
    return sentences_from_prose(raw)


def re_split_paragraphs(text: str) -> list[str]:
    parts = []
    buf: list[str] = []
    for line in text.split("\n"):
        if line.strip():
            buf.append(line.strip())
        elif buf:
            parts.append(" ".join(buf))
            buf = []
    if buf:
        parts.append(" ".join(buf))
    return parts
