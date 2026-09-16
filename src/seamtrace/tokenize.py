"""Conservative tokenisers. No language-model tokenizer, no NLTK.

Exam notes treat a *word* as a run of letters or digits, optionally
containing an internal apostrophe (`don't`, `it's`). Punctuation is
kept separately so comma rate and question rate stay independent of
the word stream.
"""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
ABBREV_PROTECT = (
    "Dr.",
    "Mr.",
    "Mrs.",
    "Ms.",
    "Prof.",
    "e.g.",
    "i.e.",
    "etc.",
    "vs.",
    "Fig.",
    "Eq.",
    "No.",
    "St.",
    "Ave.",
    "Inc.",
    "Ltd.",
    "U.S.",
    "U.K.",
    "Ph.D.",
)


def words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def raw_tokens(text: str) -> list[str]:
    return [m.group(0) for m in WORD_RE.finditer(text)]


def sentences_from_prose(text: str) -> list[str]:
    """Split running prose when a file is not already one unit per line."""
    protected = text.strip()
    if not protected:
        return []
    for i, abbr in enumerate(ABBREV_PROTECT):
        protected = protected.replace(abbr, f"__ABBR{i}__")
    parts = SENTENCE_SPLIT_RE.split(protected)
    restored: list[str] = []
    for part in parts:
        for i, abbr in enumerate(ABBREV_PROTECT):
            part = part.replace(f"__ABBR{i}__", abbr)
        piece = part.strip()
        if piece:
            restored.append(piece)
    return restored


def char_ngrams(text: str, n: int = 3) -> list[str]:
    compact = re.sub(r"\s+", " ", text.lower()).strip()
    if len(compact) < n:
        return [compact] if compact else []
    return [compact[i : i + n] for i in range(len(compact) - n + 1)]
