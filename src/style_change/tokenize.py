"""Lightweight token and sentence splitters.

These are exam-friendly approximations, not a full linguistic pipeline.
They keep the toolkit free of NLTK/spaCy so the notes stay runnable on a
plain Python install.
"""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+(?:\.\d+)?")
SENT_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)", re.MULTILINE)
APOSTROPHE_RE = re.compile(r"[A-Za-z]+'[A-Za-z]+")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def words(text: str) -> list[str]:
    return [m.group(0).lower() for m in WORD_RE.finditer(text)]


def raw_words(text: str) -> list[str]:
    return [m.group(0) for m in WORD_RE.finditer(text)]


def sentences(text: str) -> list[str]:
    found = [s.strip() for s in SENT_RE.findall(text) if s.strip()]
    return found or ([text.strip()] if text.strip() else [])


def contractions(text: str) -> list[str]:
    return APOSTROPHE_RE.findall(text)
