"""Per-unit stylometric features.

Scalars are rates or lengths. The function-word vector is a normalised
bag over a closed list. Character trigrams capture orthography and
punctuation habits that word bags miss (e.g. `...`, ` — `, `!!`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .lexicon import (
    CONTRACTIONS,
    FIRST_PERSON,
    FUNCTION_WORDS,
    HEDGES,
    MODALS,
    PRONOUNS,
    SECOND_PERSON,
    function_word_index,
)
from .tokenize import char_ngrams, words

_FW_INDEX = function_word_index()

SCALAR_NAMES: tuple[str, ...] = (
    "n_chars",
    "n_words",
    "avg_word_len",
    "ttr",
    "hapax_rate",
    "punct_rate",
    "comma_rate",
    "stop_rate",
    "question_mark",
    "exclaim_mark",
    "ellipsis_rate",
    "digit_rate",
    "upper_rate",
    "pronoun_rate",
    "first_person_rate",
    "second_person_rate",
    "modal_rate",
    "hedge_rate",
    "contraction_rate",
    "long_word_rate",
    "starts_lower",
)


@dataclass(frozen=True)
class UnitFeatures:
    text: str
    scalars: dict[str, float]
    function_words: tuple[float, ...]
    trigrams: dict[str, float]

    def scalar_vector(self, names: Iterable[str] = SCALAR_NAMES) -> tuple[float, ...]:
        return tuple(self.scalars[name] for name in names)


@dataclass
class FeatureTable:
    units: list[UnitFeatures] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.units)

    @classmethod
    def from_units(cls, units: list[str]) -> "FeatureTable":
        return cls([extract_unit_features(unit) for unit in units])


def extract_unit_features(text: str) -> UnitFeatures:
    tokens = words(text)
    n_words = len(tokens)
    n_chars = len(text)
    types = set(tokens)
    hapax = sum(1 for tok in types if tokens.count(tok) == 1)
    punct = sum(1 for ch in text if ch in ".,;:!?—–-()[]{}\"'")
    commas = text.count(",")
    questions = text.count("?")
    exclams = text.count("!")
    ellipses = text.count("...") + text.count("…")
    digits = sum(ch.isdigit() for ch in text)
    uppers = sum(ch.isupper() for ch in text if ch.isalpha())
    letters = sum(ch.isalpha() for ch in text)

    def rate(count: int, denom: int) -> float:
        return count / denom if denom else 0.0

    fw_counts = [0.0] * len(FUNCTION_WORDS)
    for tok in tokens:
        idx = _FW_INDEX.get(tok)
        if idx is not None:
            fw_counts[idx] += 1.0
    # Light add-k: enough to avoid zero vectors, not enough to wash the list.
    smoothed = [c + 0.05 for c in fw_counts]
    fw_total = sum(smoothed)
    fw_vec = tuple(c / fw_total for c in smoothed)

    grams = char_ngrams(text, 3)
    gram_counts: dict[str, float] = {}
    for gram in grams:
        gram_counts[gram] = gram_counts.get(gram, 0.0) + 1.0
    gram_total = sum(gram_counts.values()) or 1.0
    gram_vec = {g: c / gram_total for g, c in gram_counts.items()}

    scalars = {
        "n_chars": float(n_chars),
        "n_words": float(n_words),
        "avg_word_len": (sum(len(t) for t in tokens) / n_words) if n_words else 0.0,
        "ttr": rate(len(types), n_words),
        "hapax_rate": rate(hapax, n_words),
        "punct_rate": rate(punct, n_chars),
        "comma_rate": rate(commas, n_chars),
        "stop_rate": rate(text.count("."), max(n_words, 1)),
        "question_mark": float(questions > 0),
        "exclaim_mark": float(exclams > 0),
        "ellipsis_rate": rate(ellipses, max(n_chars, 1)),
        "digit_rate": rate(digits, n_chars),
        "upper_rate": rate(uppers, letters),
        "pronoun_rate": rate(sum(t in PRONOUNS for t in tokens), n_words),
        "first_person_rate": rate(sum(t in FIRST_PERSON for t in tokens), n_words),
        "second_person_rate": rate(sum(t in SECOND_PERSON for t in tokens), n_words),
        "modal_rate": rate(sum(t in MODALS for t in tokens), n_words),
        "hedge_rate": rate(sum(t in HEDGES for t in tokens), n_words),
        "contraction_rate": rate(sum(t in CONTRACTIONS for t in tokens), n_words),
        "long_word_rate": rate(sum(len(t) >= 7 for t in tokens), n_words),
        "starts_lower": float(bool(text) and text[0].islower()),
    }
    return UnitFeatures(text=text, scalars=scalars, function_words=fw_vec, trigrams=gram_vec)
