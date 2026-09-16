"""Register vector and bag features for one teaching unit or span."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from . import lexicon
from .tokenize import char_ngrams, punctuation_chars, tokens_of_units, word_tokens

# Mean unit length is recorded for the hand table but is *not* part of
# the exam L1. Sentence length is too topic-sensitive on six-line docs.
LENGTH_SCALE = 20.0


@dataclass(frozen=True)
class RegisterVector:
    """Six closed-class rates you can count on paper.

    Order is fixed so the formula card and ``as_tuple()`` agree:

    1. first-person singular rate (I / me / my / I'm …)
    2. second-person rate (you / your)
    3. contraction rate
    4. formal-modal rate (shall / must / hereby / …)
    5. hedge rate
    6. first-person plural rate (we / our)

    Mean unit length is kept on the object for the hand table and CUSUM
    sketches. It does not enter ``l1``.
    """

    first_person: float
    second_person: float
    contraction: float
    formal: float
    hedge: float
    we_person: float
    length: float = 0.0
    vocative: float = 0.0
    tokens: int = 0
    units: int = 0

    NAMES: tuple[str, ...] = (
        "first_person",
        "second_person",
        "contraction",
        "formal",
        "hedge",
        "we_person",
    )

    def as_tuple(self) -> tuple[float, ...]:
        return (
            self.first_person,
            self.second_person,
            self.contraction,
            self.formal,
            self.hedge,
            self.we_person,
        )

    def l1(self, other: "RegisterVector") -> float:
        return sum(abs(a - b) for a, b in zip(self.as_tuple(), other.as_tuple()))

    def labelled(self) -> dict[str, float]:
        return {
            "first_person": self.first_person,
            "second_person": self.second_person,
            "contraction": self.contraction,
            "formal": self.formal,
            "hedge": self.hedge,
            "length": self.length,
            "we_person": self.we_person,
            "vocative": self.vocative,
        }


@dataclass
class UnitFeatures:
    text: str
    tokens: list[str]
    register: RegisterVector
    function_counts: list[float]
    char3: dict[str, float]
    punct_rate: float
    digit_rate: float
    question: float


@dataclass
class SpanFeatures:
    units: list[str]
    register: RegisterVector
    function_counts: list[float]
    char3: dict[str, float]
    unit_features: list[UnitFeatures] = field(default_factory=list)


def _rate(count: int, n: int) -> float:
    return count / n if n else 0.0


def extract_register(units: Sequence[str]) -> RegisterVector:
    tokens = tokens_of_units(units)
    n = len(tokens)
    mean_len = (n / len(units)) if units else 0.0
    return RegisterVector(
        first_person=_rate(sum(t in lexicon.FIRST_PERSON for t in tokens), n),
        second_person=_rate(sum(t in lexicon.SECOND_PERSON for t in tokens), n),
        contraction=_rate(sum(t in lexicon.CONTRACTIONS for t in tokens), n),
        formal=_rate(sum(t in lexicon.FORMAL for t in tokens), n),
        hedge=_rate(sum(t in lexicon.HEDGES for t in tokens), n),
        we_person=_rate(sum(t in lexicon.WE_PERSON for t in tokens), n),
        length=mean_len / LENGTH_SCALE,
        vocative=_rate(sum(t in lexicon.VOCATIVES for t in tokens), n),
        tokens=n,
        units=len(units),
    )


def function_counts(tokens: Iterable[str], smooth: float = 0.5) -> list[float]:
    counts = [smooth] * lexicon.N_FUNCTION_WORDS
    for tok in tokens:
        idx = lexicon.FUNCTION_WORD_INDEX.get(tok)
        if idx is not None:
            counts[idx] += 1.0
    return counts


def char3_counts(text: str, damp: bool = True) -> dict[str, float]:
    bag: dict[str, float] = {}
    for gram in char_ngrams(text, 3):
        bag[gram] = bag.get(gram, 0.0) + 1.0
    if damp:
        for key, val in list(bag.items()):
            # log1p damping so a repeated letter does not dominate.
            bag[key] = _log1p(val)
    return bag


def _log1p(x: float) -> float:
    # Local log1p so features.py stays stdlib and easy to hand-check.
    import math

    return math.log1p(x)


def extract_unit(text: str) -> UnitFeatures:
    tokens = word_tokens(text)
    n = len(tokens)
    digits = sum(ch.isdigit() for ch in text)
    chars = max(len(text), 1)
    return UnitFeatures(
        text=text,
        tokens=tokens,
        register=extract_register([text]),
        function_counts=function_counts(tokens),
        char3=char3_counts(text),
        punct_rate=len(punctuation_chars(text)) / chars,
        digit_rate=digits / chars,
        question=1.0 if "?" in text else 0.0,
    )


def extract_span(units: Sequence[str]) -> SpanFeatures:
    feats = [extract_unit(u) for u in units]
    return SpanFeatures(
        units=list(units),
        register=extract_register(units),
        function_counts=function_counts(tokens_of_units(units)),
        char3=char3_counts(" ".join(units)),
        unit_features=feats,
    )


def register_table(units: Sequence[str]) -> list[dict[str, float | str | int]]:
    rows = []
    for i, unit in enumerate(units, start=1):
        reg = extract_register([unit])
        row: dict[str, float | str | int] = {"unit": i, "text": unit}
        row.update(reg.labelled())
        row["tokens"] = reg.tokens
        rows.append(row)
    return rows
