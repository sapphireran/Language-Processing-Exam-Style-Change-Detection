"""Lightweight tokenisers. Stdlib only; no NLTK."""

from __future__ import annotations

import re
from dataclasses import dataclass

WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
SENTENCE_RE = re.compile(r"[^.!?]*[.!?]+|[^.!?]+$", re.MULTILINE)
APOSTROPHE_RE = re.compile(r"['’]")


@dataclass(frozen=True)
class Tokens:
    raw: str
    words: tuple[str, ...]
    words_lower: tuple[str, ...]
    sentences: tuple[str, ...]


def tokenize(text: str) -> Tokens:
    words = tuple(m.group(0) for m in WORD_RE.finditer(text))
    sentences = tuple(
        s.strip() for s in SENTENCE_RE.findall(text) if s and s.strip()
    )
    if not sentences and text.strip():
        sentences = (text.strip(),)
    return Tokens(
        raw=text,
        words=words,
        words_lower=tuple(w.lower() for w in words),
        sentences=sentences,
    )


def char_ngrams(text: str, n: int = 3) -> list[str]:
    """Character n-grams over a lowercased, whitespace-collapsed string."""
    compact = re.sub(r"\s+", " ", text.lower()).strip()
    if len(compact) < n:
        return [compact] if compact else []
    return [compact[i : i + n] for i in range(len(compact) - n + 1)]


def estimate_syllables(word: str) -> int:
    """Ugly but stable English syllable heuristic for readability proxies."""
    w = WORD_RE.fullmatch(word)
    if not w:
        letters = re.sub(r"[^a-zA-Z]", "", word).lower()
    else:
        letters = word.lower()
        letters = APOSTROPHE_RE.split(letters)[0]
    if not letters:
        return 1
    letters = re.sub(r"[^a-z]", "", letters)
    if not letters:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in letters:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if letters.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)
