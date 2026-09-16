"""Tiny tokenizer. One teaching unit is one non-empty line."""

from __future__ import annotations

import re
from typing import Iterable

_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+")
_SENT = re.compile(r"(?<=[.!?])\s+")


def units_from_text(text: str) -> list[str]:
    """Split a problem file into teaching units.

    Prefer one non-empty line per unit (the house format). Fall back to a
    naive sentence split only when the file is a single paragraph.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) >= 2:
        return lines
    if not lines:
        return []
    bits = [s.strip() for s in _SENT.split(lines[0]) if s.strip()]
    return bits or lines


def word_tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD.finditer(text)]


def tokens_of_units(units: Iterable[str]) -> list[str]:
    out: list[str] = []
    for unit in units:
        out.extend(word_tokens(unit))
    return out


def char_ngrams(text: str, n: int = 3) -> list[str]:
    """Lowercased character n-grams, spaces kept, digits kept."""
    s = " ".join(text.lower().split())
    if len(s) < n:
        return [s] if s else []
    return [s[i : i + n] for i in range(len(s) - n + 1)]


def punctuation_chars(text: str) -> list[str]:
    return [ch for ch in text if ch in ".,;:!?—–-()\"'"]
