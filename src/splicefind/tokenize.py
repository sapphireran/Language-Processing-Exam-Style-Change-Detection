"""Light tokenisation helpers used by the exam toolkit.

The splitters are deterministic and dependency-free so oral-exam
walkthroughs can be reproduced on any machine. They are *not* a
linguistic parser: they exist to make stylometric counts inspectable.
"""

from __future__ import annotations

import re
from typing import Iterable

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:[.,]\d+)?")
_VOWEL_GROUP = re.compile(r"[aeiouy]+", re.IGNORECASE)
_BLANK = re.compile(r"\n\s*\n")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def split_paragraphs(text: str) -> list[str]:
    """Split a PAN-style document on blank lines, keeping order."""
    if text == "":
        return []
    chunks = [chunk.strip() for chunk in _BLANK.split(text.replace("\r\n", "\n"))]
    return [chunk for chunk in chunks if chunk]


def split_sentences(paragraph: str) -> list[str]:
    """Split a paragraph into coarse sentence-like units."""
    cleaned = " ".join(paragraph.strip().split())
    if not cleaned:
        return []
    parts = [part.strip() for part in _SENT_SPLIT.split(cleaned) if part.strip()]
    return parts or [cleaned]


def tokenize_words(text: str) -> list[str]:
    """Lower-cased word tokens, keeping contractions as one token."""
    return [match.group(0).lower() for match in _WORD.finditer(text)]


def tokenize_chars(text: str, *, keep_spaces: bool = False) -> str:
    """Normalise a string for character n-gram profiles."""
    lowered = text.lower()
    if keep_spaces:
        return re.sub(r"\s+", " ", lowered).strip()
    return re.sub(r"\s+", "", lowered)


def punctuation_marks(text: str) -> list[str]:
    return _PUNCT.findall(text)


def estimate_syllables(word: str) -> int:
    """Cheap English syllable estimate used for a Flesch-like score."""
    letters = re.sub(r"[^a-z]", "", word.lower())
    if not letters:
        return 0
    groups = _VOWEL_GROUP.findall(letters)
    count = len(groups)
    if letters.endswith("e") and not letters.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(count, 1)


def sentence_word_counts(paragraph: str) -> list[int]:
    return [len(tokenize_words(sentence)) for sentence in split_sentences(paragraph)]


def flatten_words(paragraphs: Iterable[str]) -> list[str]:
    words: list[str] = []
    for paragraph in paragraphs:
        words.extend(tokenize_words(paragraph))
    return words
