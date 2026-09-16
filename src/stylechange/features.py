"""Per-unit stylometric profile.

Each comparison unit (a sentence, or a paragraph) becomes a ``FeatureVector``.
Rates are almost all *per word* so a 6-word note and a 24-word textbook
sentence can be compared. Length itself is kept as its own coordinate.

The inventory is deliberately boring: length, richness, punctuation,
closed-class rates, and a couple of exam-specific flags (arrows, digits).
Character n-grams are *not* the pairwise metric — two sentences from the
same person barely share 3-grams, so every boundary would look like a cut.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, fields

from .lexicon import (
    ACADEMIC,
    CASUAL,
    CONTRACTION_MARKERS,
    FIRST_PERSON_PL,
    FIRST_PERSON_SG,
    FUNCTION_WORDS,
    HEDGES,
    IMPERSONAL,
    IMPERSONAL_PHRASES,
    INFORMAL,
    SECOND_PERSON,
    STUDENT_PHRASES,
)

_WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?|\d+")
_PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ed|\w+en|shown|seen|made|given|taken|known|written|found)\b",
    re.IGNORECASE,
)
_ARROW = re.compile(r"->|=>|::=|::")
_VOWEL_GROUP = re.compile(r"[aeiouy]+", re.IGNORECASE)


@dataclass(frozen=True)
class FeatureVector:
    n_chars: float
    n_words: float
    mean_word_len: float
    type_token: float
    hapax_rate: float
    syllable_rate: float
    comma_rate: float
    colon_rate: float
    dash_rate: float
    question_rate: float
    exclaim_rate: float
    digit_rate: float
    function_word_rate: float
    first_person_sg: float
    first_person_pl: float
    second_person: float
    impersonal: float
    hedge_rate: float
    academic_rate: float
    informal_rate: float
    casual_rate: float
    contraction_rate: float
    passive_rate: float
    arrow_rate: float
    student_phrase: float
    uppercase_word_rate: float

    def as_array(self) -> list[float]:
        """Coordinates used for span distance (length kept as log words)."""
        return [
            math.log1p(self.n_words),
            self.mean_word_len,
            self.type_token,
            self.hapax_rate,
            self.syllable_rate,
            self.comma_rate,
            self.colon_rate,
            self.dash_rate,
            self.question_rate,
            self.exclaim_rate,
            self.digit_rate,
            self.function_word_rate,
            self.first_person_sg,
            self.first_person_pl,
            self.second_person,
            self.impersonal,
            self.hedge_rate,
            self.academic_rate,
            self.informal_rate,
            self.casual_rate,
            self.contraction_rate,
            self.passive_rate,
            self.arrow_rate,
            self.student_phrase,
            self.uppercase_word_rate,
        ]

    def named_values(self) -> dict[str, float]:
        return {item.name: float(getattr(self, item.name)) for item in fields(self)}


_FEATURE_WEIGHTS: list[float] = [
    0.25,  # log words
    0.45,  # mean word length
    0.20,  # type-token
    0.15,  # hapax
    0.20,  # syllables
    0.35,  # comma
    1.60,  # colon
    0.90,  # dash
    1.10,  # question
    0.90,  # exclaim
    1.20,  # digit
    0.40,  # function words
    2.40,  # first person sg
    2.00,  # first person pl
    1.80,  # second person
    1.80,  # impersonal one
    1.50,  # hedges
    1.70,  # academic
    2.00,  # informal
    1.80,  # casual
    2.10,  # contractions
    1.10,  # passive
    2.20,  # arrows
    2.40,  # student phrases
    0.80,  # uppercase words
]


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text)


def _syllables(word: str) -> int:
    groups = _VOWEL_GROUP.findall(word)
    count = max(1, len(groups))
    if word.lower().endswith("e") and count > 1:
        count -= 1
    return count


def _is_first_person_i(token: str, original: str) -> bool:
    """Count English *I*, not the dummy index in ``P(w_i)``."""
    lower = token.lower()
    if lower not in FIRST_PERSON_SG:
        return False
    if lower in {"me", "my", "mine", "myself"}:
        return True
    # I / I'm / I've … — require a capital I in the source span.
    return bool(re.search(r"\bI(?:['’](?:m|ve|ll|d))?\b", original))


def extract(text: str) -> FeatureVector:
    tokens = _tokens(text)
    words = [tok for tok in tokens if re.search(r"[A-Za-z]", tok)]
    n_words = max(1, len(words))
    n_chars = max(1, len(text))
    lowered = [word.lower().replace("’", "'") for word in words]
    types = set(lowered)
    hapax = sum(1 for word in types if lowered.count(word) == 1)
    lower_text = text.lower().replace("’", "'")

    def rate(count: float) -> float:
        return count / n_words

    first_sg = sum(1 for tok in _WORD.finditer(text) if _is_first_person_i(tok.group(0), text))
    first_pl = sum(1 for word in lowered if word in FIRST_PERSON_PL)
    second = sum(1 for word in lowered if word in SECOND_PERSON)
    impersonal = sum(1 for word in lowered if word in IMPERSONAL)
    hedges = sum(1 for word in lowered if word in HEDGES)
    academic = sum(1 for word in lowered if word in ACADEMIC)
    informal = sum(1 for word in lowered if word in INFORMAL)
    casual = sum(1 for word in lowered if word in CASUAL)
    function = sum(1 for word in lowered if word in FUNCTION_WORDS)
    contractions = sum(lower_text.count(mark) for mark in CONTRACTION_MARKERS)
    student = sum(1 for phrase in STUDENT_PHRASES if phrase in lower_text)
    impersonal_phrases = sum(1 for phrase in IMPERSONAL_PHRASES if phrase in lower_text)
    digits = sum(1 for tok in tokens if tok.isdigit())
    arrows = len(_ARROW.findall(text))
    uppercase = sum(1 for word in words if word.isupper() and len(word) > 1)
    syllables = sum(_syllables(word) for word in words)

    return FeatureVector(
        n_chars=float(len(text)),
        n_words=float(len(words)),
        mean_word_len=sum(len(word) for word in words) / n_words,
        type_token=len(types) / n_words,
        hapax_rate=hapax / n_words,
        syllable_rate=syllables / n_words,
        comma_rate=text.count(",") / n_chars * 20.0,
        colon_rate=text.count(":") / n_chars * 20.0,
        dash_rate=(text.count("—") + text.count("–") + text.count(" - ")) / n_chars * 20.0,
        question_rate=text.count("?") / n_chars * 20.0,
        exclaim_rate=text.count("!") / n_chars * 20.0,
        digit_rate=rate(digits),
        function_word_rate=rate(function),
        first_person_sg=rate(first_sg),
        first_person_pl=rate(first_pl),
        second_person=rate(second),
        impersonal=rate(impersonal + impersonal_phrases),
        hedge_rate=rate(hedges),
        academic_rate=rate(academic),
        informal_rate=rate(informal),
        casual_rate=rate(casual),
        contraction_rate=rate(contractions),
        passive_rate=rate(len(_PASSIVE.findall(text))),
        arrow_rate=rate(arrows),
        student_phrase=float(student),
        uppercase_word_rate=rate(uppercase),
    )


def mean_vector(vectors: list[FeatureVector]) -> list[float]:
    if not vectors:
        raise ValueError("mean_vector() needs at least one unit")
    width = len(vectors[0].as_array())
    acc = [0.0] * width
    for vector in vectors:
        for index, value in enumerate(vector.as_array()):
            acc[index] += value
    return [value / len(vectors) for value in acc]


def weighted_l1(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) != len(_FEATURE_WEIGHTS):
        raise ValueError("feature width mismatch")
    return sum(weight * abs(a - b) for weight, a, b in zip(_FEATURE_WEIGHTS, left, right))


def span_distance(left: list[FeatureVector], right: list[FeatureVector]) -> float:
    return weighted_l1(mean_vector(left), mean_vector(right))


def top_deltas(
    left: FeatureVector,
    right: FeatureVector,
    k: int = 3,
) -> list[tuple[str, float, float, float]]:
    """Largest absolute feature moves, for ``--explain``."""
    names = [
        "n_words",
        "mean_word_len",
        "type_token",
        "hapax_rate",
        "syllable_rate",
        "comma_rate",
        "colon_rate",
        "dash_rate",
        "question_rate",
        "exclaim_rate",
        "digit_rate",
        "function_word_rate",
        "first_person_sg",
        "first_person_pl",
        "second_person",
        "impersonal",
        "hedge_rate",
        "academic_rate",
        "informal_rate",
        "casual_rate",
        "contraction_rate",
        "passive_rate",
        "arrow_rate",
        "student_phrase",
        "uppercase_word_rate",
    ]
    rows: list[tuple[str, float, float, float]] = []
    for name, weight, a, b in zip(names, _FEATURE_WEIGHTS, left.as_array(), right.as_array()):
        delta = weight * abs(a - b)
        rows.append((name, a, b, delta))
    rows.sort(key=lambda row: row[3], reverse=True)
    return rows[:k]


# Binary register flags. Averaging these over a span is much more stable
# than comparing raw rates on 12-word sentences. Used only for the
# same-voice change-point (the hard *we* vs *one* case).
_REGISTER_WEIGHTS: dict[str, float] = {
    "i": 1.50,
    "we": 1.50,
    "you": 1.20,
    "one": 1.30,
    "hedge": 0.90,
    "informal": 1.20,
    "notes": 1.40,
    "question": 1.10,
}


def register_flags(vector: FeatureVector) -> dict[str, float]:
    return {
        "i": float(vector.first_person_sg > 0 or vector.student_phrase > 0),
        "we": float(vector.first_person_pl > 0),
        "you": float(vector.second_person > 0),
        "one": float(vector.impersonal > 0),
        "hedge": float(vector.hedge_rate > 0),
        "informal": float(
            vector.informal_rate > 0 or vector.casual_rate > 0 or vector.contraction_rate > 0
        ),
        "notes": float(vector.arrow_rate > 0 or vector.colon_rate > 0.25 or vector.digit_rate > 0.2),
        "question": float(vector.question_rate > 0),
    }


def register_distance(left: list[FeatureVector], right: list[FeatureVector]) -> float:
    def mean_flags(vectors: list[FeatureVector]) -> dict[str, float]:
        acc = {key: 0.0 for key in _REGISTER_WEIGHTS}
        for vector in vectors:
            for key, value in register_flags(vector).items():
                acc[key] += value
        return {key: value / len(vectors) for key, value in acc.items()}

    left_mean = mean_flags(left)
    right_mean = mean_flags(right)
    return sum(
        weight * abs(left_mean[key] - right_mean[key]) for key, weight in _REGISTER_WEIGHTS.items()
    )
