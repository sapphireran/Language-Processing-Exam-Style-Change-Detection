"""Lightweight tokenizers. No NLTK / spaCy — the exam baseline stays portable."""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+")
SENT_RE = re.compile(r"(?<=[.!?])\s+")
NON_LETTER_RE = re.compile(r"[^a-z]+")
WS_RE = re.compile(r"\s+")


def words(text: str) -> list[str]:
    """Lowercased word tokens, keeping internal apostrophes (can't, it's)."""
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def sentences(text: str) -> list[str]:
    """Very small sentence splitter on ``.!?`` followed by whitespace."""
    stripped = text.strip()
    if not stripped:
        return []
    parts = [part.strip() for part in SENT_RE.split(stripped) if part.strip()]
    return parts or [stripped]


def char_stream(text: str) -> str:
    """Lowercase letters and single spaces, padded so edge n-grams are stable."""
    lowered = text.lower()
    compact = NON_LETTER_RE.sub(" ", lowered)
    compact = WS_RE.sub(" ", compact).strip()
    if not compact:
        return ""
    return f" {compact} "


def char_ngrams(text: str, n: int = 3) -> list[str]:
    stream = char_stream(text)
    if len(stream) < n:
        return []
    return [stream[i : i + n] for i in range(len(stream) - n + 1)]
