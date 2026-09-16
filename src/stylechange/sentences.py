"""Sentence segmentation for running prose and one-sentence-per-line files."""

from __future__ import annotations

import re

from .lexicon import ABBREVIATIONS

_ABBREV_RE = re.compile(
    r"\b(" + "|".join(re.escape(item) for item in ABBREVIATIONS) + r")\.",
    re.IGNORECASE,
)
_INITIAL_RE = re.compile(r"\b([A-Z])\.")
_ELLIPSIS_RE = re.compile(r"\.{3,}")
_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[\"'(A-Z0-9])")


def _looks_line_segmented(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return False
    # A single wrapped paragraph usually has one very long line or many
    # short wrap fragments that do not end in terminal punctuation.
    terminal = sum(1 for line in lines if line[-1] in ".!?\"'")
    return terminal >= max(2, int(0.7 * len(lines))) and all(len(line) < 600 for line in lines)


def split_sentences(text: str, *, prefer_lines: bool = True) -> list[str]:
    """Split `text` into sentences.

    Synthetic study files in this repo are one sentence per line. Running
    prose falls back to a conservative abbreviation-aware splitter.
    """
    if text is None:
        return []
    normalised = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalised:
        return []
    if prefer_lines and _looks_line_segmented(normalised):
        return [line.strip() for line in normalised.splitlines() if line.strip()]
    return _split_running(normalised)


def _split_running(text: str) -> list[str]:
    # Collapse single newlines that are just wrapping; keep paragraph gaps.
    collapsed = re.sub(r"\n(?!\n)", " ", text)
    collapsed = re.sub(r"[ \t]+", " ", collapsed).strip()
    protected = _ELLIPSIS_RE.sub("…", collapsed)
    protected = _ABBREV_RE.sub(r"\1<ABBR>", protected)
    protected = _INITIAL_RE.sub(r"\1<ABBR>", protected)
    protected = re.sub(r"\b(e)\.(g)\.", r"\1<ABBR>\2<ABBR>", protected, flags=re.I)
    protected = re.sub(r"\b(i)\.(e)\.", r"\1<ABBR>\2<ABBR>", protected, flags=re.I)
    protected = re.sub(r"\bU\.S\.", "U<ABBR>S<ABBR>", protected)
    protected = re.sub(r"\bU\.K\.", "U<ABBR>K<ABBR>", protected)
    parts = _SPLIT_RE.split(protected)
    sentences = []
    for part in parts:
        restored = part.replace("<ABBR>", ".").strip()
        if restored:
            sentences.append(restored)
    return sentences
