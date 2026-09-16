"""Lightweight tokenization aimed at exam-style English documents.

The splitter is deterministic and dependency-free. PAN-style files (one
paragraph per non-empty line) and blank-line-separated prose both work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'”’)]*\s+(?=[\"'“‘(A-Z])")
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?|[^\sA-Za-z0-9]")


@dataclass(frozen=True)
class Paragraph:
    """One paragraph plus the tokens used by the feature extractor."""

    index: int
    text: str
    sentences: tuple[str, ...] = field(compare=False)
    words: tuple[str, ...] = field(compare=False)
    tokens: tuple[str, ...] = field(compare=False)

    @property
    def word_count(self) -> int:
        return len(self.words)


@dataclass(frozen=True)
class Document:
    """A document viewed as an ordered list of paragraphs."""

    text: str
    paragraphs: tuple[Paragraph, ...]
    source: str | None = None

    def __len__(self) -> int:
        return len(self.paragraphs)


def split_sentences(text: str) -> tuple[str, ...]:
    """Split a paragraph into sentences with a conservative regex."""
    stripped = text.strip()
    if not stripped:
        return ()
    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(stripped) if part.strip()]
    return tuple(parts)


def tokenize_words(text: str) -> tuple[str, ...]:
    """Alphabetic words, keeping internal apostrophes (don't, I'll)."""
    return tuple(match.group(0) for match in WORD_RE.finditer(text))


def tokenize_surface(text: str) -> tuple[str, ...]:
    """Words, numbers, and single punctuation marks."""
    return tuple(match.group(0) for match in TOKEN_RE.finditer(text))


def _paragraph_strings(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    if "\n\n" in normalized:
        chunks = re.split(r"\n\s*\n+", normalized)
    else:
        chunks = normalized.split("\n")
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def split_paragraphs(text: str, source: str | None = None) -> Document:
    """Turn raw text into a :class:`Document`.

    Blank-line blocks are preferred. If the file has no blank line, each
    non-empty line is treated as its own paragraph (common in shared-task
    dumps).
    """
    paragraphs: list[Paragraph] = []
    for index, chunk in enumerate(_paragraph_strings(text)):
        paragraphs.append(
            Paragraph(
                index=index,
                text=chunk,
                sentences=split_sentences(chunk),
                words=tokenize_words(chunk),
                tokens=tokenize_surface(chunk),
            )
        )
    return Document(text=text, paragraphs=tuple(paragraphs), source=source)
