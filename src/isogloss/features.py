"""Closed-class rates. Nouns are not invited.

Each channel is a rate (count / n_words) except the two shape
channels, which are raw magnitudes. A house is a habit on this
short list. A topic is a habit on the nouns we refuse to count.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Iterable

from .text import lower_words

I_SET = frozenset({"i", "me", "my", "mine", "i'm", "i'll", "i'd", "i've"})
WE_SET = frozenset({"we", "us", "our", "ours", "we're", "we'll", "we'd", "we've"})
YOU_SET = frozenset({"you", "your", "yours", "you're", "you'll", "you'd", "you've"})
ONE_SET = frozenset({"one", "one's"})
DEONTIC = frozenset(
    {
        "shall",
        "must",
        "ought",
        "required",
        "forbidden",
        "mandatory",
        "may",
        "cannot",
        "mustn't",
    }
)
HEDGE = frozenset(
    {
        "maybe",
        "perhaps",
        "possibly",
        "roughly",
        "almost",
        "quite",
        "rather",
        "somewhat",
    }
)
HEDGE_PHRASES = ("sort of", "kind of", "a bit", "i guess", "a little")
FORMAL = frozenset(
    {
        "however",
        "therefore",
        "thus",
        "moreover",
        "accordingly",
        "nevertheless",
        "hence",
    }
)
ORAL = frozenset({"so", "anyway", "yeah", "then", "ok", "okay"})
PAST_COPULA = frozenset({"was", "were"})
ARTICLE_THE = frozenset({"the"})
# Shape, not a word class, but still closed: how the hand *moves*.
# Digits belong here because Flint writes quantities as numerals and
# the other houses write them as words or not at all.


CHANNELS = (
    "i_rate",
    "we_rate",
    "you_rate",
    "one_rate",
    "contraction_rate",
    "deontic_rate",
    "hedge_rate",
    "formal_rate",
    "oral_rate",
    "past_copula_rate",
    "the_rate",
    "digit_rate",
    "mean_word_len",
    "n_words",
    "question_rate",
)


@dataclass(frozen=True)
class FeatureRow:
    i_rate: float
    we_rate: float
    you_rate: float
    one_rate: float
    contraction_rate: float
    deontic_rate: float
    hedge_rate: float
    formal_rate: float
    oral_rate: float
    past_copula_rate: float
    the_rate: float
    digit_rate: float
    mean_word_len: float
    n_words: float
    question_rate: float

    def as_tuple(self) -> tuple[float, ...]:
        return tuple(getattr(self, name) for name in CHANNELS)

    def as_dict(self) -> dict[str, float]:
        return {name: getattr(self, name) for name in CHANNELS}


def _rate(count: int, n: int) -> float:
    return count / n if n else 0.0


def _contraction_count(tokens: list[str]) -> int:
    return sum(1 for token in tokens if "'" in token)


def extract(text: str) -> FeatureRow:
    tokens = lower_words(text)
    n = len(tokens)
    lowered = text.lower()
    phrase_hedges = sum(lowered.count(phrase) for phrase in HEDGE_PHRASES)
    letters = [token for token in tokens if token[0].isalpha()]
    digits = [token for token in tokens if token[0].isdigit()]
    mean_len = sum(len(token) for token in letters) / len(letters) if letters else 0.0
    questions = text.count("?")
    n_sents = max(1, text.count(".") + text.count("!") + text.count("?"))
    return FeatureRow(
        i_rate=_rate(sum(1 for t in tokens if t in I_SET), n),
        we_rate=_rate(sum(1 for t in tokens if t in WE_SET), n),
        you_rate=_rate(sum(1 for t in tokens if t in YOU_SET), n),
        one_rate=_rate(sum(1 for t in tokens if t in ONE_SET), n),
        contraction_rate=_rate(_contraction_count(tokens), n),
        deontic_rate=_rate(sum(1 for t in tokens if t in DEONTIC), n),
        hedge_rate=_rate(sum(1 for t in tokens if t in HEDGE) + phrase_hedges, n),
        formal_rate=_rate(sum(1 for t in tokens if t in FORMAL), n),
        oral_rate=_rate(sum(1 for t in tokens if t in ORAL), n),
        past_copula_rate=_rate(sum(1 for t in tokens if t in PAST_COPULA), n),
        the_rate=_rate(sum(1 for t in tokens if t in ARTICLE_THE), n),
        digit_rate=_rate(len(digits), n),
        mean_word_len=mean_len,
        n_words=float(n),
        question_rate=questions / n_sents,
    )


def extract_many(units: Iterable[str]) -> list[FeatureRow]:
    return [extract(unit) for unit in units]


def matrix(rows: Iterable[FeatureRow]) -> list[list[float]]:
    return [list(row.as_tuple()) for row in rows]


def channel_index(name: str) -> int:
    return CHANNELS.index(name)


def field_names() -> tuple[str, ...]:
    return tuple(f.name for f in fields(FeatureRow))
