"""Per-unit stylometric fingerprints.

Register scalars are the teaching channel: person, contraction, hedge,
punctuation, and length. Function-word histograms are the closed-class
channel used by intra-document Delta. Neither channel uses topic words
on purpose.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .lexicon import (
    CONTRACTION_MARKERS,
    FIRST_PERSON,
    FUNCTION_INDEX,
    FUNCTION_WORDS,
    HEDGES,
    INCLUSIVE_WE,
    INFORMAL,
    PASSIVE_AUX,
    SECOND_PERSON,
    SHALL_MUST,
    VOCATIVES,
)
from .tokenize import word_tokens

REGISTER_NAMES: tuple[str, ...] = (
    "mean_word_len",
    "words_per_unit",
    "comma_rate",
    "semi_rate",
    "question_rate",
    "exclaim_rate",
    "digit_rate",
    "upper_ratio",
    "lower_start",
    "i_rate",
    "you_rate",
    "we_rate",
    "contraction_rate",
    "hedge_rate",
    "passive_rate",
    "informal_rate",
    "fw_ratio",
    "shall_rate",
    "vocative_rate",
)

# Rate channels stay on a 0–1 scale. Length is divided so a two-word
# jitter cannot outrank a person or contraction flip.
REGISTER_COMPARE_SCALE: dict[str, float] = {
    "mean_word_len": 8.0,
    "words_per_unit": 25.0,
    "comma_rate": 1.0,
    "semi_rate": 1.0,
    "question_rate": 1.0,
    "exclaim_rate": 1.0,
    "digit_rate": 1.0,
    "upper_ratio": 1.0,
    "lower_start": 1.0,
    "i_rate": 1.0,
    "you_rate": 1.0,
    "we_rate": 1.0,
    "contraction_rate": 1.0,
    "hedge_rate": 1.0,
    "passive_rate": 1.0,
    "informal_rate": 1.0,
    "fw_ratio": 1.0,
    "shall_rate": 1.0,
    "vocative_rate": 1.0,
}

REGISTER_COMPARE_WEIGHT: dict[str, float] = {
    "mean_word_len": 0.35,
    "words_per_unit": 0.15,
    "comma_rate": 0.55,
    "semi_rate": 0.80,
    "question_rate": 1.10,
    "exclaim_rate": 1.10,
    "digit_rate": 0.85,
    "upper_ratio": 0.25,
    "lower_start": 1.00,
    "i_rate": 1.25,
    "you_rate": 1.25,
    "we_rate": 1.00,
    "contraction_rate": 1.25,
    "hedge_rate": 1.10,
    "passive_rate": 0.85,
    "informal_rate": 1.10,
    "fw_ratio": 0.45,
    "shall_rate": 1.15,
    "vocative_rate": 1.20,
}


@dataclass(frozen=True)
class UnitFeatures:
    text: str
    words: tuple[str, ...]
    n_chars: int
    n_words: int
    mean_word_len: float
    comma_rate: float
    semi_rate: float
    question_rate: float
    exclaim_rate: float
    digit_rate: float
    upper_ratio: float
    lower_start: float
    i_rate: float
    you_rate: float
    we_rate: float
    contraction_rate: float
    hedge_rate: float
    passive_rate: float
    informal_rate: float
    fw_ratio: float
    shall_rate: float
    vocative_rate: float
    ttr: float
    function_counts: tuple[int, ...] = field(repr=False)

    def register_vector(self) -> tuple[float, ...]:
        return (
            self.mean_word_len,
            float(self.n_words),
            self.comma_rate,
            self.semi_rate,
            self.question_rate,
            self.exclaim_rate,
            self.digit_rate,
            self.upper_ratio,
            self.lower_start,
            self.i_rate,
            self.you_rate,
            self.we_rate,
            self.contraction_rate,
            self.hedge_rate,
            self.passive_rate,
            self.informal_rate,
            self.fw_ratio,
            self.shall_rate,
            self.vocative_rate,
        )

    def function_vector(self, smooth: float = 0.35) -> tuple[float, ...]:
        """Smoothed function-word rates.

        Raw cosine on a 10-word sentence is a trap: two same-author lines
        that happen to share no closed-class word look orthogonal. Additive
        smoothing keeps that pair near the prior and only a real shift moves.
        """
        dim = len(self.function_counts)
        n = max(self.n_words, 1)
        return tuple((c + smooth) / (n + smooth * dim) for c in self.function_counts)


def extract(text: str) -> UnitFeatures:
    words = tuple(word_tokens(text))
    n_words = len(words)
    n_chars = len(text)
    letters = [ch for ch in text if ch.isalpha()]
    upper = sum(1 for ch in letters if ch.isupper())
    stripped = text.lstrip()
    lower_start = 1.0 if stripped and stripped[0].islower() else 0.0
    denom = max(n_words, 1)
    counts = [0] * len(FUNCTION_WORDS)
    for w in words:
        idx = FUNCTION_INDEX.get(w)
        if idx is not None:
            counts[idx] += 1
    contractions = sum(text.lower().count(mark) for mark in CONTRACTION_MARKERS)
    unique = len(set(words))
    return UnitFeatures(
        text=text,
        words=words,
        n_chars=n_chars,
        n_words=n_words,
        mean_word_len=(sum(len(w) for w in words) / denom) if words else 0.0,
        comma_rate=text.count(",") / denom,
        semi_rate=text.count(";") / denom,
        question_rate=text.count("?") / denom,
        exclaim_rate=text.count("!") / denom,
        digit_rate=sum(ch.isdigit() for ch in text) / max(n_chars, 1),
        upper_ratio=(upper / len(letters)) if letters else 0.0,
        lower_start=lower_start,
        i_rate=sum(w in FIRST_PERSON for w in words) / denom,
        you_rate=sum(w in SECOND_PERSON for w in words) / denom,
        we_rate=sum(w in INCLUSIVE_WE for w in words) / denom,
        contraction_rate=contractions / denom,
        hedge_rate=sum(w in HEDGES for w in words) / denom,
        passive_rate=sum(w in PASSIVE_AUX for w in words) / denom,
        informal_rate=sum(w in INFORMAL for w in words) / denom,
        fw_ratio=sum(counts) / denom,
        shall_rate=sum(w in SHALL_MUST for w in words) / denom,
        vocative_rate=sum(w in VOCATIVES for w in words) / denom,
        ttr=unique / denom,
        function_counts=tuple(counts),
    )


def extract_many(units: Iterable[str]) -> list[UnitFeatures]:
    return [extract(u) for u in units]
