"""Stylometric feature extraction.

Each sentence or paragraph is turned into a :class:`FeatureVector` with:

* a dense numeric profile (length, richness, punctuation, pronouns, …)
* a function-word histogram
* character n-gram counts

The detector compares these profiles across a boundary. Short units are noisy,
so callers can :meth:`FeatureVector.merge` a window of neighbours before scoring.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import re
from typing import Iterable, Sequence

from .lexicon import (
    ACADEMIC,
    CONTRACTIONS,
    FIRST_PERSON,
    FUNCTION_INDEX,
    FUNCTION_WORDS,
    HEDGES,
    SECOND_PERSON,
    THIRD_PERSON,
)

_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")
_DIGIT = re.compile(r"\d")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_VOWEL_GROUPS = re.compile(r"[aeiouy]+", re.IGNORECASE)

DENSE_NAMES = (
    "log_chars",
    "log_words",
    "avg_word_len",
    "avg_syllables",
    "type_token",
    "hapax_ratio",
    "punct_ratio",
    "comma_ratio",
    "semicolon_ratio",
    "colon_ratio",
    "question_ratio",
    "exclaim_ratio",
    "quote_ratio",
    "dash_ratio",
    "digit_ratio",
    "upper_ratio",
    "title_ratio",
    "short_word_ratio",
    "long_word_ratio",
    "function_ratio",
    "first_person_ratio",
    "second_person_ratio",
    "third_person_ratio",
    "hedge_ratio",
    "academic_ratio",
    "contraction_ratio",
    "stop_start_ratio",
    "coord_ratio",
    "subord_ratio",
    "unique_punct_types",
)


@dataclass
class FeatureVector:
    """Stylometric snapshot of one text unit (or a merged window)."""

    dense: list[float]
    function_counts: list[float]
    char_ngrams: Counter[str]
    n_words: int
    n_chars: int

    def merge(self, other: "FeatureVector") -> "FeatureVector":
        """Pool two units as if they were one longer span."""
        total_words = self.n_words + other.n_words
        total_chars = self.n_chars + other.n_chars
        if total_words <= 0:
            return FeatureVector(
                dense=[0.0] * len(DENSE_NAMES),
                function_counts=[0.0] * len(FUNCTION_WORDS),
                char_ngrams=Counter(),
                n_words=0,
                n_chars=0,
            )
        # Re-weight rate features by word count so a 3-word sentence cannot
        # drown a 20-word neighbour.
        w1 = max(self.n_words, 1)
        w2 = max(other.n_words, 1)
        dense = [
            ((a * w1) + (b * w2)) / (w1 + w2) for a, b in zip(self.dense, other.dense)
        ]
        # log_chars / log_words should reflect the pooled span, not the mean.
        dense[0] = math.log1p(total_chars)
        dense[1] = math.log1p(total_words)
        functions = [
            a + b for a, b in zip(self.function_counts, other.function_counts)
        ]
        return FeatureVector(
            dense=dense,
            function_counts=functions,
            char_ngrams=self.char_ngrams + other.char_ngrams,
            n_words=total_words,
            n_chars=total_chars,
        )

    def function_distribution(self) -> list[float]:
        total = sum(self.function_counts)
        if total <= 0:
            return [0.0] * len(self.function_counts)
        return [c / total for c in self.function_counts]

    def char_distribution(self) -> dict[str, float]:
        total = sum(self.char_ngrams.values())
        if total <= 0:
            return {}
        return {gram: count / total for gram, count in self.char_ngrams.items()}

    def as_named_dense(self) -> dict[str, float]:
        return dict(zip(DENSE_NAMES, self.dense))


def _syllable_count(word: str) -> int:
    """Very small English syllable heuristic — good enough for relative rates."""
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 0
    groups = _VOWEL_GROUPS.findall(cleaned)
    count = len(groups)
    if cleaned.endswith("e") and not cleaned.endswith("le") and count > 1:
        count -= 1
    return max(count, 1)


def _char_ngrams(text: str, n: int = 3) -> Counter[str]:
    folded = re.sub(r"\s+", " ", text.lower())
    padded = f" {folded} "
    grams: Counter[str] = Counter()
    if len(padded) < n:
        return grams
    for i in range(len(padded) - n + 1):
        grams[padded[i : i + n]] += 1
    return grams


def extract_features(text: str) -> FeatureVector:
    """Build a stylometric vector for a single sentence or paragraph."""
    text = text.strip()
    words = _WORD.findall(text)
    tokens = [w.lower().replace("’", "'") for w in words]
    n_words = len(tokens)
    n_chars = len(text)

    types = set(tokens)
    hapax = sum(1 for _, count in Counter(tokens).items() if count == 1)
    punct = _PUNCT.findall(text)
    letters = [ch for ch in text if ch.isalpha()]
    upper = sum(1 for ch in letters if ch.isupper())

    def rate(count: int, denom: int) -> float:
        return count / denom if denom else 0.0

    short = sum(1 for w in tokens if len(w) <= 3)
    long = sum(1 for w in tokens if len(w) >= 8)
    function_hits = sum(1 for w in tokens if w in FUNCTION_INDEX)
    first = sum(1 for w in tokens if w in FIRST_PERSON)
    second = sum(1 for w in tokens if w in SECOND_PERSON)
    third = sum(1 for w in tokens if w in THIRD_PERSON)
    hedges = sum(1 for w in tokens if w in HEDGES)
    academic = sum(1 for w in tokens if w in ACADEMIC)
    contractions = sum(1 for w in tokens if w in CONTRACTIONS)
    start_function = 1.0 if tokens and tokens[0] in FUNCTION_INDEX else 0.0
    coord = sum(1 for w in tokens if w in {"and", "or", "but", "so", "yet"})
    subord = sum(
        1
        for w in tokens
        if w in {"because", "although", "though", "while", "if", "when", "unless"}
    )
    syllables = [_syllable_count(w) for w in tokens]
    unique_punct = len(set(punct))

    dense = [
        math.log1p(n_chars),
        math.log1p(n_words),
        (sum(len(w) for w in tokens) / n_words) if n_words else 0.0,
        (sum(syllables) / n_words) if n_words else 0.0,
        (len(types) / n_words) if n_words else 0.0,
        rate(hapax, n_words),
        rate(len(punct), max(n_chars, 1)),
        rate(text.count(","), max(n_chars, 1)),
        rate(text.count(";"), max(n_chars, 1)),
        rate(text.count(":"), max(n_chars, 1)),
        rate(text.count("?"), max(n_chars, 1)),
        rate(text.count("!"), max(n_chars, 1)),
        rate(text.count('"') + text.count("“") + text.count("”"), max(n_chars, 1)),
        rate(text.count("-") + text.count("—") + text.count("–"), max(n_chars, 1)),
        rate(len(_DIGIT.findall(text)), max(n_chars, 1)),
        rate(upper, max(len(letters), 1)),
        rate(sum(1 for w in words if w[:1].isupper()), n_words),
        rate(short, n_words),
        rate(long, n_words),
        rate(function_hits, n_words),
        rate(first, n_words),
        rate(second, n_words),
        rate(third, n_words),
        rate(hedges, n_words),
        rate(academic, n_words),
        rate(contractions, n_words),
        start_function,
        rate(coord, n_words),
        rate(subord, n_words),
        unique_punct / 12.0,
    ]

    function_counts = [0.0] * len(FUNCTION_WORDS)
    for token in tokens:
        idx = FUNCTION_INDEX.get(token)
        if idx is not None:
            function_counts[idx] += 1.0

    return FeatureVector(
        dense=dense,
        function_counts=function_counts,
        char_ngrams=_char_ngrams(text, n=3),
        n_words=n_words,
        n_chars=n_chars,
    )


def extract_many(units: Sequence[str]) -> list[FeatureVector]:
    return [extract_features(unit) for unit in units]


def merge_span(vectors: Sequence[FeatureVector], start: int, end: int) -> FeatureVector:
    """Merge ``vectors[start:end]`` into one profile."""
    if start >= end:
        raise ValueError("empty merge span")
    pooled = vectors[start]
    for item in vectors[start + 1 : end]:
        pooled = pooled.merge(item)
    return pooled


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / math.sqrt(na * nb)


def cosine_maps(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    keys = set(a) | set(b)
    return cosine([a.get(k, 0.0) for k in keys], [b.get(k, 0.0) for k in keys])


def l1_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


def dense_delta(left: FeatureVector, right: FeatureVector) -> list[float]:
    return [abs(x - y) for x, y in zip(left.dense, right.dense)]


def iter_named_deltas(
    left: FeatureVector, right: FeatureVector
) -> Iterable[tuple[str, float]]:
    for name, value in zip(DENSE_NAMES, dense_delta(left, right)):
        yield name, value
