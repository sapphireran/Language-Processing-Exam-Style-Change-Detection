"""Hand stylometric features. Names are part of the public contract."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np

from . import lexicon
from .tokenize import count_syllables, lower_words, punctuation_chars, words

FEATURE_NAMES: tuple[str, ...] = (
    "char_count",
    "word_count",
    "avg_word_len",
    "std_word_len",
    "long_word_rate",
    "short_word_rate",
    "type_token_ratio",
    "hapax_ratio",
    "punct_rate",
    "comma_rate",
    "semicolon_rate",
    "colon_rate",
    "question_rate",
    "exclamation_rate",
    "paren_rate",
    "quote_rate",
    "dash_rate",
    "uppercase_rate",
    "digit_rate",
    "function_word_rate",
    "first_person_rate",
    "second_person_rate",
    "third_person_rate",
    "article_rate",
    "hedge_rate",
    "intensifier_rate",
    "coord_conj_rate",
    "subord_marker_rate",
    "contraction_rate",
    "nominalization_rate",
    "ly_adverb_rate",
    "passive_be_rate",
    "latinate_rate",
    "avg_syllables",
    "flesch_reading_ease",
)

FEATURE_INDEX = {name: index for index, name in enumerate(FEATURE_NAMES)}


def _rate(count: float, denom: float) -> float:
    return float(count) / denom if denom else 0.0


def _is_contraction(token: str) -> bool:
    folded = token.replace("\u2019", "'")
    return any(folded.endswith(tail) or tail.lower() in folded.lower() for tail in ("n't", "'re", "'ll", "'ve", "'d", "'m"))


def _has_suffix(token: str, suffixes: Iterable[str]) -> bool:
    return any(token.endswith(suffix) and len(token) > len(suffix) + 2 for suffix in suffixes)


def extract_sentence(sentence: str) -> np.ndarray:
    """Return a 1-D float vector aligned with FEATURE_NAMES."""
    raw = sentence or ""
    tokens = words(raw)
    lowered = [token.lower() for token in tokens]
    n_words = len(tokens)
    n_chars = len(raw)
    lengths = np.array([len(token) for token in tokens], dtype=float) if tokens else np.array([])

    punct = punctuation_chars(raw)
    n_punct = len(punct)
    comma = raw.count(",")
    semicolon = raw.count(";")
    colon = raw.count(":")
    question = raw.count("?")
    exclaim = raw.count("!")
    paren = raw.count("(") + raw.count(")")
    quote = sum(raw.count(mark) for mark in ('"', "“", "”"))
    dash = sum(raw.count(mark) for mark in ("—", "–", " - ", "--"))
    # Hyphens inside words are weaker style; count standalone / long dashes mainly.
    dash += raw.count(" — ") + raw.count(" – ")

    uppercase = sum(1 for token in tokens if token[:1].isupper())
    digits = sum(ch.isdigit() for ch in raw)

    function = sum(1 for token in lowered if token in lexicon.FUNCTION_WORDS)
    first = sum(1 for token in lowered if token in lexicon.FIRST_PERSON)
    second = sum(1 for token in lowered if token in lexicon.SECOND_PERSON)
    third = sum(1 for token in lowered if token in lexicon.THIRD_PERSON)
    articles = sum(1 for token in lowered if token in lexicon.ARTICLES)
    hedges = sum(1 for token in lowered if token in lexicon.HEDGES)
    intens = sum(1 for token in lowered if token in lexicon.INTENSIFIERS)
    coords = sum(1 for token in lowered if token in lexicon.COORD_CONJ)
    subords = sum(1 for token in lowered if token in lexicon.SUBORD_MARKERS)
    contractions = sum(1 for token in tokens if _is_contraction(token))
    nominals = sum(1 for token in lowered if _has_suffix(token, lexicon.NOMINAL_SUFFIXES))
    ly_adverbs = sum(
        1
        for token in lowered
        if token.endswith("ly") and token not in lexicon.LY_STOP and len(token) > 3
    )
    be_count = sum(1 for token in lowered if token in lexicon.BE_FORMS)
    pastish = sum(
        1
        for token in lowered
        if (token.endswith("ed") or token.endswith("en")) and token not in {"the", "then", "when"}
    )
    passive = 1.0 if be_count and pastish else 0.0
    latinate = sum(1 for token in lowered if _has_suffix(token, lexicon.LATINATE_SUFFIXES))

    syllables = [count_syllables(token) for token in tokens]
    avg_syll = float(sum(syllables) / n_words) if n_words else 0.0
    # Single-sentence Flesch: sentences = 1. Relative ordering is the signal.
    if n_words:
        flesch = 206.835 - 1.015 * n_words - 84.6 * avg_syll
    else:
        flesch = 0.0

    unique = set(lowered)
    hapax = sum(1 for token in unique if lowered.count(token) == 1)

    avg_len = float(lengths.mean()) if n_words else 0.0
    std_len = float(lengths.std(ddof=0)) if n_words else 0.0

    values = (
        float(n_chars),
        float(n_words),
        avg_len,
        std_len,
        _rate(sum(1 for length in lengths if length >= 6), n_words),
        _rate(sum(1 for length in lengths if length <= 3), n_words),
        _rate(len(unique), n_words),
        _rate(hapax, n_words),
        _rate(n_punct, n_chars),
        _rate(comma, n_words),
        _rate(semicolon, n_words),
        _rate(colon, n_words),
        _rate(question, n_words),
        _rate(exclaim, n_words),
        _rate(paren, n_words),
        _rate(quote, n_words),
        _rate(dash, n_words),
        _rate(uppercase, n_words),
        _rate(digits, n_chars),
        _rate(function, n_words),
        _rate(first, n_words),
        _rate(second, n_words),
        _rate(third, n_words),
        _rate(articles, n_words),
        _rate(hedges, n_words),
        _rate(intens, n_words),
        _rate(coords, n_words),
        _rate(subords, n_words),
        _rate(contractions, n_words),
        _rate(nominals, n_words),
        _rate(ly_adverbs, n_words),
        passive,
        _rate(latinate, n_words),
        avg_syll,
        float(flesch),
    )
    vector = np.asarray(values, dtype=float)
    if vector.shape != (len(FEATURE_NAMES),):
        raise RuntimeError("feature vector drifted from FEATURE_NAMES")
    return vector


def extract_document(sentences: list[str]) -> np.ndarray:
    """Stack sentence vectors into an (n, d) array."""
    if not sentences:
        return np.zeros((0, len(FEATURE_NAMES)), dtype=float)
    return np.vstack([extract_sentence(sentence) for sentence in sentences])


def as_dict(vector: np.ndarray) -> dict[str, float]:
    return {name: float(vector[index]) for index, name in enumerate(FEATURE_NAMES)}


def zscore_rows(matrix: np.ndarray, *, floor: float = 1e-6) -> np.ndarray:
    """Column-wise z-score, typically inside one document."""
    if matrix.size == 0:
        return matrix
    mean = matrix.mean(axis=0)
    std = matrix.std(axis=0)
    std = np.where(std < floor, 1.0, std)
    return (matrix - mean) / std


def pairwise_euclidean(matrix: np.ndarray) -> np.ndarray:
    if len(matrix) < 2:
        return np.zeros(0, dtype=float)
    deltas = matrix[1:] - matrix[:-1]
    return np.linalg.norm(deltas, axis=1)
