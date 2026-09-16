"""Stylometric profiles for one paragraph.

Each profile is a mix of:
- scalar rates that survive length differences (TTR, mean word length, …)
- a function-word relative-frequency vector
- a character 3-gram relative-frequency vector
- a punctuation relative-frequency vector

Topic-bearing content words are deliberately *not* part of the style
profile. See ``stylechange.topic`` for the contrastive content vector used
in the Easy-vs-Hard leakage walkthrough.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from stylechange.lexicon import (
    FIRST_PERSON_PLURAL,
    FIRST_PERSON_SINGULAR,
    FUNCTION_WORD_SET,
    FUNCTION_WORDS,
    HEDGE_MARKERS,
    NOMINALIZATION_SUFFIXES,
    PUNCT_COUNTS,
    SECOND_PERSON,
)
from stylechange.tokenize import char_ngrams, sentences, words

SCALAR_NAMES: tuple[str, ...] = (
    "avg_word_len",
    "word_len_mad",
    "type_token_ratio",
    "hapax_ratio",
    "avg_sentence_len",
    "sentence_len_mad",
    "short_word_ratio",
    "long_word_ratio",
    "contraction_ratio",
    "digit_ratio",
    "uppercase_ratio",
    "stopword_ratio",
    "first_person_sg_rate",
    "first_person_pl_rate",
    "second_person_rate",
    "hedge_rate",
    "nominalization_rate",
    "punct_rate",
    "exclaim_rate",
    "question_rate",
    "semicolon_rate",
    "casualness",
)

# Length-sensitive rates (TTR, hapax, MADs) are noisy on short paragraphs.
# Distance uses this stabler subset plus the signed casualness axis.
CORE_SCALAR_NAMES: tuple[str, ...] = (
    "avg_word_len",
    "avg_sentence_len",
    "short_word_ratio",
    "long_word_ratio",
    "contraction_ratio",
    "first_person_sg_rate",
    "second_person_rate",
    "hedge_rate",
    "nominalization_rate",
    "exclaim_rate",
    "semicolon_rate",
    "casualness",
)


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _mean(values: list[float]) -> float:
    return _safe_div(sum(values), len(values))


def _mad(values: list[float]) -> float:
    if not values:
        return 0.0
    centre = _mean(values)
    return _mean([abs(v - centre) for v in values])


def _relative(counter: Counter[str], vocab: Iterable[str] | None = None) -> dict[str, float]:
    total = sum(counter.values())
    keys = list(vocab) if vocab is not None else list(counter)
    if total == 0:
        return {key: 0.0 for key in keys}
    return {key: counter.get(key, 0) / total for key in keys}


@dataclass(frozen=True)
class StyleProfile:
    """Bundle of stylometric views on a single paragraph."""

    text: str
    tokens: tuple[str, ...]
    scalars: dict[str, float]
    function_words: dict[str, float]
    punct: dict[str, float]
    char_trigrams: dict[str, float] = field(repr=False)

    @property
    def n_tokens(self) -> int:
        return len(self.tokens)


def extract_scalars(text: str, tokens: list[str]) -> dict[str, float]:
    sent_list = sentences(text)
    sent_lens = [float(len(words(sent))) for sent in sent_list] or [0.0]
    lengths = [float(len(tok)) for tok in tokens]
    types = Counter(tokens)
    hapaxes = sum(1 for count in types.values() if count == 1)
    letters = [ch for ch in text if ch.isalpha()]
    uppercase = sum(1 for ch in letters if ch.isupper())

    scalars = {
        "avg_word_len": _mean(lengths),
        "word_len_mad": _mad(lengths),
        "type_token_ratio": _safe_div(len(types), len(tokens)),
        "hapax_ratio": _safe_div(hapaxes, len(tokens)),
        "avg_sentence_len": _mean(sent_lens),
        "sentence_len_mad": _mad(sent_lens),
        "short_word_ratio": _safe_div(sum(1 for tok in tokens if len(tok) <= 3), len(tokens)),
        "long_word_ratio": _safe_div(sum(1 for tok in tokens if len(tok) >= 8), len(tokens)),
        "contraction_ratio": _safe_div(sum(1 for tok in tokens if "'" in tok), len(tokens)),
        "digit_ratio": _safe_div(sum(1 for ch in text if ch.isdigit()), max(len(text), 1)),
        "uppercase_ratio": _safe_div(uppercase, len(letters)),
        "stopword_ratio": _safe_div(sum(1 for tok in tokens if tok in FUNCTION_WORD_SET), len(tokens)),
        "first_person_sg_rate": _safe_div(
            sum(1 for tok in tokens if tok in FIRST_PERSON_SINGULAR), len(tokens)
        ),
        "first_person_pl_rate": _safe_div(
            sum(1 for tok in tokens if tok in FIRST_PERSON_PLURAL), len(tokens)
        ),
        "second_person_rate": _safe_div(
            sum(1 for tok in tokens if tok in SECOND_PERSON), len(tokens)
        ),
        "hedge_rate": _safe_div(sum(1 for tok in tokens if tok in HEDGE_MARKERS), len(tokens)),
        "nominalization_rate": _safe_div(
            sum(1 for tok in tokens if tok.endswith(NOMINALIZATION_SUFFIXES)),
            len(tokens),
        ),
        "punct_rate": _safe_div(sum(1 for ch in text if ch in ",.;:!?"), max(len(tokens), 1)),
        "exclaim_rate": _safe_div(text.count("!"), max(len(tokens), 1)),
        "question_rate": _safe_div(text.count("?"), max(len(tokens), 1)),
        "semicolon_rate": _safe_div(text.count(";"), max(len(tokens), 1)),
    }
    scalars["casualness"] = (
        3.0 * scalars["contraction_ratio"]
        + 2.5 * scalars["first_person_sg_rate"]
        + 1.5 * scalars["second_person_rate"]
        + 2.0 * scalars["exclaim_rate"]
        + 0.8 * scalars["short_word_ratio"]
        - 2.0 * scalars["nominalization_rate"]
        - 1.5 * scalars["hedge_rate"]
        - 1.2 * scalars["semicolon_rate"]
        - 0.12 * scalars["avg_word_len"]
        - 0.015 * scalars["avg_sentence_len"]
    )
    return scalars


def extract_profile(text: str, trigram_limit: int = 80) -> StyleProfile:
    """Build a style profile. ``trigram_limit`` keeps sparse tails small."""
    tokens = words(text)
    punct_counter = Counter()
    for name, mark in PUNCT_COUNTS:
        punct_counter[name] = text.count(mark)
    trigram_counter = Counter(char_ngrams(text, 3))
    if trigram_limit and len(trigram_counter) > trigram_limit:
        trigram_counter = Counter(dict(trigram_counter.most_common(trigram_limit)))

    return StyleProfile(
        text=text,
        tokens=tuple(tokens),
        scalars=extract_scalars(text, tokens),
        function_words=_relative(Counter(tok for tok in tokens if tok in FUNCTION_WORD_SET), FUNCTION_WORDS),
        punct=_relative(punct_counter, [name for name, _ in PUNCT_COUNTS]),
        char_trigrams=_relative(trigram_counter),
    )


def scalar_vector(profile: StyleProfile) -> list[float]:
    return [profile.scalars[name] for name in SCALAR_NAMES]
