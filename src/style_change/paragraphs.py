"""Paragraph segmentation for exam-style problem files.

PAN-style problems sometimes use a single newline between paragraphs and
sometimes a blank line. This splitter prefers blank lines when they exist,
then falls back to single newlines so both layouts work.
"""

from __future__ import annotations

from .tokenize import normalize_newlines


def split_paragraphs(text: str) -> list[str]:
    """Return non-empty paragraphs, preserving original wording."""
    body = normalize_newlines(text).strip()
    if not body:
        return []
    if "\n\n" in body:
        chunks = body.split("\n\n")
    else:
        chunks = body.split("\n")
    paragraphs = [" ".join(chunk.split()) for chunk in chunks]
    return [p for p in paragraphs if p]


def adjacent_pairs(paragraphs: list[str]) -> list[tuple[str, str]]:
    return list(zip(paragraphs, paragraphs[1:], strict=False))
