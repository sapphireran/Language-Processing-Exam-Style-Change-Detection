"""Sentence and paragraph segmentation for exam-style English prose.

PAN-style problems often store one sentence per non-empty line. This module
honours that convention when it is unambiguous, and otherwise falls back to a
lightweight sentence splitter that is conservative around common abbreviations.
"""

from __future__ import annotations

import re
from typing import Literal

Granularity = Literal["sentence", "paragraph"]

_ABBREVIATIONS = {
    "a.m",
    "approx",
    "al",
    "b.a",
    "capt",
    "cf",
    "col",
    "dept",
    "dr",
    "e.g",
    "ed",
    "eq",
    "etc",
    "fig",
    "gen",
    "gov",
    "i.e",
    "inc",
    "jr",
    "lt",
    "ltd",
    "m.a",
    "mr",
    "mrs",
    "ms",
    "mt",
    "no",
    "p.m",
    "ph.d",
    "prof",
    "rev",
    "sen",
    "sgt",
    "sr",
    "st",
    "u.k",
    "u.s",
    "univ",
    "vs",
    "vol",
}

_SENTENCE_END = re.compile(r'([.!?]+)(["\')\]]*)(\s+|$)')
_INITIAL = re.compile(r"^[A-Z]$")
_BLANK_SPLIT = re.compile(r"\n\s*\n+")


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_paragraphs(text: str) -> list[str]:
    """Split on blank lines. Single newlines stay inside a paragraph."""
    text = _normalize_newlines(text).strip()
    if not text:
        return []
    parts = [re.sub(r"\s+", " ", p).strip() for p in _BLANK_SPLIT.split(text)]
    return [p for p in parts if p]


def _is_abbreviation(token: str) -> bool:
    stripped = token.strip("\"'()[]{}").rstrip(".").lower()
    if stripped in _ABBREVIATIONS:
        return True
    if _INITIAL.match(stripped):
        return True
    return False


def _looks_line_segmented(lines: list[str]) -> bool:
    """Treat one-sentence-per-line files as already segmented."""
    if len(lines) < 2:
        return False
    ended = 0
    for line in lines:
        if re.search(r'[.!?…]["\')\]]*$', line):
            ended += 1
    return ended / len(lines) >= 0.6


def split_sentences(text: str) -> list[str]:
    """Split prose into sentences without an external NLP tokenizer."""
    text = _normalize_newlines(text).strip()
    if not text:
        return []

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if _looks_line_segmented(lines):
        return lines

    sentences: list[str] = []
    start = 0
    for match in _SENTENCE_END.finditer(text):
        before = text[start : match.start()].rstrip()
        last_token = before.split()[-1] if before.split() else ""
        if _is_abbreviation(last_token):
            continue
        end = match.end(2)
        piece = text[start:end].strip()
        if piece:
            sentences.append(re.sub(r"\s+", " ", piece))
        start = match.end()
    tail = text[start:].strip()
    if tail:
        sentences.append(re.sub(r"\s+", " ", tail))
    return sentences


def split_units(text: str, granularity: Granularity = "sentence") -> list[str]:
    """Segment a document into the units used by the detector."""
    if granularity == "paragraph":
        paragraphs = split_paragraphs(text)
        if paragraphs:
            return paragraphs
        return [text.strip()] if text.strip() else []
    return split_sentences(text)
