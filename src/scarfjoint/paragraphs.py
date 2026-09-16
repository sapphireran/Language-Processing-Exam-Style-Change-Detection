"""Blank-line paragraph splitting, matching the PAN input convention."""

from __future__ import annotations


def split_paragraphs(text: str) -> list[str]:
    """Split a document on runs of blank lines.

    PAN documents use a blank line as the paragraph boundary, and a
    paragraph is defined to be single-author. Consecutive newlines are
    collapsed. Leading and trailing empty chunks are dropped.

    Reading files with ``open(path, "r", newline="")`` (see :mod:`scarfjoint.io`)
    keeps ``\\r\\n`` from being rewritten before this split runs.
    """
    if not text:
        return []
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    chunks: list[str] = []
    buf: list[str] = []
    empty_run = 0
    started = False
    for line in normalized.split("\n"):
        if line.strip() == "":
            empty_run += 1
            if started and empty_run >= 1 and buf:
                paragraph = " ".join(part.strip() for part in buf).strip()
                if paragraph:
                    chunks.append(paragraph)
                buf = []
            continue
        started = True
        empty_run = 0
        buf.append(line)
    if buf:
        paragraph = " ".join(part.strip() for part in buf).strip()
        if paragraph:
            chunks.append(paragraph)
    return chunks
