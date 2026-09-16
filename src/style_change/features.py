"""Stylometric profiles for a single paragraph."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import asdict, dataclass, fields

from .lexicons import (
    ARTICLES,
    CONNECTIVES,
    FIRST_PERSON,
    FUNCTION_WORDS,
    HEDGES,
    INTENSIFIERS,
    PERSONAL_PRONOUNS,
    PREPOSITIONS,
)
from .tokenize import contractions, raw_words, sentences, words


def _rate(count: int, total: int) -> float:
    return 0.0 if total == 0 else count / total


def _mean(values: list[float]) -> float:
    return 0.0 if not values else sum(values) / len(values)


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    return (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5


def _yules_k(freq: Counter[str], n_tokens: int) -> float:
    if n_tokens == 0:
        return 0.0
    # K = 10^4 * (sum i^2 V_i - N) / N^2
    by_freq: Counter[int] = Counter(freq.values())
    moment = sum((k ** 2) * v for k, v in by_freq.items())
    return 1e4 * (moment - n_tokens) / (n_tokens ** 2)


def _honores_r(n_tokens: int, vocab: int, hapax: int) -> float:
    if n_tokens == 0 or vocab == 0:
        return 0.0
    denom = 1.0 - (hapax / vocab)
    if denom <= 1e-12:
        return 0.0
    return 100.0 * math.log(n_tokens) / denom


def _vowel_groups(word: str) -> int:
    groups = 0
    prev_vowel = False
    for char in word.lower():
        is_vowel = char in "aeiouy"
        if is_vowel and not prev_vowel:
            groups += 1
        prev_vowel = is_vowel
    return max(1, groups) if word.isalpha() else 0


@dataclass(frozen=True)
class StylometricProfile:
    type_token_ratio: float
    hapax_ratio: float
    avg_word_len: float
    std_word_len: float
    avg_sent_len: float
    std_sent_len: float
    comma_rate: float
    period_rate: float
    exclaim_rate: float
    question_rate: float
    semicolon_rate: float
    colon_rate: float
    dash_rate: float
    quote_rate: float
    contraction_rate: float
    function_word_rate: float
    pronoun_rate: float
    first_person_rate: float
    article_rate: float
    preposition_rate: float
    hedge_rate: float
    intensifier_rate: float
    connective_rate: float
    uppercase_word_rate: float
    digit_rate: float
    long_word_rate: float
    short_word_rate: float
    yules_k: float
    honores_r: float
    avg_vowel_groups: float
    commas_per_sentence: float

    def vector(self) -> list[float]:
        return [getattr(self, field.name) for field in fields(self)]

    def as_dict(self) -> dict[str, float]:
        return asdict(self)

    @staticmethod
    def names() -> list[str]:
        return [field.name for field in fields(StylometricProfile)]


def extract_profile(text: str) -> StylometricProfile:
    tokens = words(text)
    surface = raw_words(text)
    sents = sentences(text)
    n_tokens = len(tokens)
    n_chars = max(1, len(text))
    freq = Counter(tokens)
    vocab = len(freq)
    hapax = sum(1 for count in freq.values() if count == 1)
    word_lens = [len(tok) for tok in tokens]
    sent_lens = [len(words(sent)) for sent in sents]
    n_sents = max(1, len(sents))

    return StylometricProfile(
        type_token_ratio=_rate(vocab, n_tokens),
        hapax_ratio=_rate(hapax, vocab),
        avg_word_len=_mean(word_lens),
        std_word_len=_std(word_lens),
        avg_sent_len=_mean(sent_lens),
        std_sent_len=_std(sent_lens),
        comma_rate=text.count(",") / n_chars,
        period_rate=text.count(".") / n_chars,
        exclaim_rate=text.count("!") / n_chars,
        question_rate=text.count("?") / n_chars,
        semicolon_rate=text.count(";") / n_chars,
        colon_rate=text.count(":") / n_chars,
        dash_rate=(text.count("—") + text.count(" - ") + text.count("--")) / n_chars,
        quote_rate=(text.count('"') + text.count("'")) / n_chars,
        contraction_rate=_rate(len(contractions(text)), n_tokens),
        function_word_rate=_rate(sum(1 for t in tokens if t in FUNCTION_WORDS), n_tokens),
        pronoun_rate=_rate(sum(1 for t in tokens if t in PERSONAL_PRONOUNS), n_tokens),
        first_person_rate=_rate(sum(1 for t in tokens if t in FIRST_PERSON), n_tokens),
        article_rate=_rate(sum(1 for t in tokens if t in ARTICLES), n_tokens),
        preposition_rate=_rate(sum(1 for t in tokens if t in PREPOSITIONS), n_tokens),
        hedge_rate=_rate(sum(1 for t in tokens if t in HEDGES), n_tokens),
        intensifier_rate=_rate(sum(1 for t in tokens if t in INTENSIFIERS), n_tokens),
        connective_rate=_rate(sum(1 for t in tokens if t in CONNECTIVES), n_tokens),
        uppercase_word_rate=_rate(sum(1 for t in surface if t[:1].isupper()), n_tokens),
        digit_rate=_rate(sum(1 for t in tokens if any(ch.isdigit() for ch in t)), n_tokens),
        long_word_rate=_rate(sum(1 for t in tokens if len(t) >= 7), n_tokens),
        short_word_rate=_rate(sum(1 for t in tokens if len(t) <= 3), n_tokens),
        yules_k=_yules_k(freq, n_tokens),
        honores_r=_honores_r(n_tokens, vocab, hapax),
        avg_vowel_groups=_mean([_vowel_groups(t) for t in tokens]) if tokens else 0.0,
        commas_per_sentence=text.count(",") / n_sents,
    )
