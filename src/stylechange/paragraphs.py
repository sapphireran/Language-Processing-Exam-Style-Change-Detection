"""Paragraph segmentation for the exam-style style-change task.

PAN-style problems treat a blank line as the paragraph boundary. A single
paragraph is assumed to be single-author; style changes are only legal
*between* paragraphs.
"""

from __future__ import annotations


def split_paragraphs(text: str) -> list[str]:
    """Split a document on blank lines and drop empty blocks.

    Consecutive newlines of any mix of ``\\n`` / ``\\r`` count as a boundary.
    Inner wrapping newlines inside a paragraph are collapsed to spaces so
    feature extractors see a single linear string.
    """
    if not text:
        return []

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    chunks: list[str] = []
    for raw_block in normalized.split("\n\n"):
        lines = [line.strip() for line in raw_block.split("\n")]
        block = " ".join(part for part in lines if part)
        if block:
            chunks.append(block)
    return chunks


def pair_boundaries(paragraphs: list[str]) -> list[tuple[str, str]]:
    """Return consecutive paragraph pairs, one per candidate change site."""
    return list(zip(paragraphs, paragraphs[1:]))
