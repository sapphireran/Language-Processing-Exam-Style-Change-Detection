"""Stylometric unit features and pairwise change cues."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Sequence

import numpy as np

FUNCTION_WORDS: tuple[str, ...] = (
    "the",
    "of",
    "and",
    "to",
    "a",
    "in",
    "that",
    "it",
    "is",
    "was",
    "for",
    "on",
    "with",
    "as",
    "be",
    "this",
    "by",
    "at",
    "have",
    "from",
    "or",
    "one",
    "had",
    "not",
    "but",
    "what",
    "all",
    "were",
    "when",
    "we",
    "there",
    "can",
    "an",
    "your",
    "which",
    "their",
    "said",
    "if",
    "do",
    "will",
    "about",
    "how",
    "up",
    "out",
    "them",
    "then",
    "she",
    "some",
    "so",
    "these",
    "would",
    "other",
    "into",
    "has",
    "more",
    "her",
    "like",
    "him",
    "could",
    "no",
    "than",
    "been",
    "its",
    "who",
    "now",
    "my",
    "over",
    "did",
    "only",
    "may",
    "well",
    "however",
    "therefore",
    "moreover",
    "subsequently",
    "via",
    "just",
    "really",
    "pretty",
)

FIRST_PERSON = {
    "i",
    "me",
    "my",
    "mine",
    "we",
    "us",
    "our",
    "ours",
    "i'm",
    "i've",
    "i'll",
    "i'd",
    "we're",
    "we've",
    "we'll",
    "we'd",
}
SECOND_PERSON = {"you", "your", "yours", "you're", "you've", "you'll", "you'd"}
CONTRACTION_TAIL = re.compile(r"(n't|'re|'ve|'ll|'d|'m)$", re.I)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")
PUNCT_CHARS = set(".,;:!?()[]{}\"'`-—–/")

SCALAR_FEATURES: tuple[str, ...] = (
    "n_chars",
    "n_words",
    "avg_word_len",
    "short_word_rate",
    "long_word_rate",
    "ttr",
    "hapax_rate",
    "upper_rate",
    "digit_rate",
    "punct_rate",
    "comma",
    "semi",
    "colon",
    "dash",
    "qmark",
    "exclaim",
    "paren",
    "quote",
    "function_word_rate",
    "first_person_rate",
    "second_person_rate",
    "contraction_rate",
)

PAIR_SIMILARITIES: tuple[str, ...] = (
    "char_bi_cosine",
    "char_tri_cosine",
    "jaccard",
    "length_ratio",
    "fw_cosine",
)


def _fw_name(word: str) -> str:
    return f"fw_{word}"


UNIT_FEATURE_NAMES: tuple[str, ...] = SCALAR_FEATURES + tuple(
    _fw_name(word) for word in FUNCTION_WORDS
)


def pairwise_feature_names() -> list[str]:
    return [f"abs_{name}" for name in UNIT_FEATURE_NAMES] + list(PAIR_SIMILARITIES)


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def _safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


def _char_ngrams(text: str, n: int) -> Counter[str]:
    folded = re.sub(r"\s+", " ", text.lower()).strip()
    if len(folded) < n:
        return Counter()
    return Counter(folded[i : i + n] for i in range(len(folded) - n + 1))


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    keys = set(left) | set(right)
    vec_a = np.array([left[k] for k in keys], dtype=float)
    vec_b = np.array([right[k] for k in keys], dtype=float)
    norm_a = float(np.linalg.norm(vec_a))
    norm_b = float(np.linalg.norm(vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))


def _jaccard(left: Sequence[str], right: Sequence[str]) -> float:
    set_a = {token.lower() for token in left}
    set_b = {token.lower() for token in right}
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _is_contraction(token: str) -> bool:
    return bool(CONTRACTION_TAIL.search(token))


def unit_feature_map(text: str) -> dict[str, float]:
    tokens = words(text)
    lowered = [token.lower() for token in tokens]
    n_words = len(tokens)
    n_chars = len(text)
    letters = [ch for ch in text if ch.isalpha()]
    word_lens = [len(token) for token in tokens]
    types = Counter(lowered)

    values: dict[str, float] = {
        "n_chars": float(n_chars),
        "n_words": float(n_words),
        "avg_word_len": float(np.mean(word_lens)) if word_lens else 0.0,
        "short_word_rate": _safe_div(sum(length <= 3 for length in word_lens), n_words),
        "long_word_rate": _safe_div(sum(length >= 7 for length in word_lens), n_words),
        "ttr": _safe_div(len(types), n_words),
        "hapax_rate": _safe_div(sum(1 for count in types.values() if count == 1), n_words),
        "upper_rate": _safe_div(sum(ch.isupper() for ch in letters), len(letters)),
        "digit_rate": _safe_div(sum(ch.isdigit() for ch in text), n_chars),
        "punct_rate": _safe_div(sum(ch in PUNCT_CHARS for ch in text), n_chars),
        "comma": _safe_div(text.count(","), n_chars),
        "semi": _safe_div(text.count(";"), n_chars),
        "colon": _safe_div(text.count(":"), n_chars),
        "dash": _safe_div(text.count("-") + text.count("—") + text.count("–"), n_chars),
        "qmark": _safe_div(text.count("?"), n_chars),
        "exclaim": _safe_div(text.count("!"), n_chars),
        "paren": _safe_div(text.count("(") + text.count(")"), n_chars),
        "quote": _safe_div(sum(text.count(q) for q in "\"'"), n_chars),
        "function_word_rate": _safe_div(
            sum(token in FUNCTION_WORDS for token in lowered), n_words
        ),
        "first_person_rate": _safe_div(
            sum(token in FIRST_PERSON for token in lowered), n_words
        ),
        "second_person_rate": _safe_div(
            sum(token in SECOND_PERSON for token in lowered), n_words
        ),
        "contraction_rate": _safe_div(
            sum(_is_contraction(token) for token in tokens), n_words
        ),
    }
    fw_counts = Counter(token for token in lowered if token in FUNCTION_WORDS)
    for word in FUNCTION_WORDS:
        values[_fw_name(word)] = _safe_div(fw_counts[word], n_words)
    return values


def unit_features(text: str) -> np.ndarray:
    values = unit_feature_map(text)
    return np.array([values[name] for name in UNIT_FEATURE_NAMES], dtype=float)


def function_word_histogram(text: str) -> Counter[str]:
    lowered = [token.lower() for token in words(text)]
    return Counter(token for token in lowered if token in FUNCTION_WORDS)


def pairwise_feature_map(left: str, right: str) -> dict[str, float]:
    map_a = unit_feature_map(left)
    map_b = unit_feature_map(right)
    values = {
        f"abs_{name}": abs(map_a[name] - map_b[name]) for name in UNIT_FEATURE_NAMES
    }
    words_a = words(left)
    words_b = words(right)
    values["char_bi_cosine"] = _cosine(_char_ngrams(left, 2), _char_ngrams(right, 2))
    values["char_tri_cosine"] = _cosine(_char_ngrams(left, 3), _char_ngrams(right, 3))
    values["jaccard"] = _jaccard(words_a, words_b)
    n_a = len(words_a)
    n_b = len(words_b)
    values["length_ratio"] = _safe_div(min(n_a, n_b), max(n_a, n_b))
    values["fw_cosine"] = _cosine(function_word_histogram(left), function_word_histogram(right))
    return values


def pairwise_features(left: str, right: str) -> np.ndarray:
    values = pairwise_feature_map(left, right)
    return np.array([values[name] for name in pairwise_feature_names()], dtype=float)


def document_pair_matrix(units: Sequence[str]) -> np.ndarray:
    if len(units) < 2:
        return np.zeros((0, len(pairwise_feature_names())), dtype=float)
    rows = [pairwise_features(units[i], units[i + 1]) for i in range(len(units) - 1)]
    return np.vstack(rows)
