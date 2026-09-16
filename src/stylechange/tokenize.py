"""Tiny deterministic tokenisers. No external NLP stack."""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def words(text: str) -> list[str]:
    """Return word tokens, keeping internal apostrophes (`don't`)."""
    return WORD_RE.findall(text.replace("\u2019", "'"))


def lower_words(text: str) -> list[str]:
    return [token.lower() for token in words(text)]


def punctuation_chars(text: str) -> list[str]:
    return PUNCT_RE.findall(text)


def count_syllables(word: str) -> int:
    """Cheap vowel-group syllable estimate for Flesch-style scores."""
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 1
    groups = re.findall(r"[aeiouy]+", cleaned)
    n = len(groups)
    if cleaned.endswith("e") and not cleaned.endswith(("le", "ie")) and n > 1:
        n -= 1
    return max(1, n)
