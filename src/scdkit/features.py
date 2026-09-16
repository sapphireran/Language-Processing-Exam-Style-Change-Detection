"""Paragraph-level stylometric fingerprints.

Every number here is something you can compute by hand on a short exam
snippet. The vector is deliberately mixed:

* lexical / morphological (word length, suffixes, n-grams)
* syntactic-lite (sentence length, punctuation, questions)
* register (contractions, connectives, pronouns)
* richness (TTR, hapax)

Content words are kept *out* of the default comparison vector so the
baseline does not cheat with topic on the easy PAN split. Topic overlap
is computed separately as ``content_jaccard`` for the confound lab.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Mapping

from .function_words import (
    CASUAL_MARKERS,
    CONTRACTION_TOKENS,
    FIRST_PERSON,
    FORMAL_CONNECTIVES,
    FUNCTION_WORDS,
    HEDGES,
    INCLUSIVE_WE,
    SECOND_PERSON,
    SUFFIX_BINS,
)
from .ngrams import char_ngrams, l2_normalize
from .tokenize import lowercase_words, split_sentences, split_words

_PUNCT = re.compile(r"[.,;:!?\"'—–-]")
_CONTENT_RE = re.compile(r"^[a-z]{3,}$")
_IMPERSONAL_ONE = re.compile(
    r"\b(?:if\s+one|one's|one\s+(?:may|might|must|should|can|could|would|"
    r"will|does|is|has|needs|prefers?|hesitate[sd]?|cannot|can't))\b",
    re.IGNORECASE,
)

FUNCTION_SET = frozenset(FUNCTION_WORDS)
CONTRACTION_SET = frozenset(CONTRACTION_TOKENS)
FORMAL_SET = frozenset(FORMAL_CONNECTIVES)
CASUAL_SET = frozenset(CASUAL_MARKERS)
HEDGE_SET = frozenset(HEDGES)


@dataclass(frozen=True)
class ParagraphFeatures:
    text: str
    n_chars: int
    n_words: int
    n_sents: int
    n_types: int
    mean_word_len: float
    mean_sent_len: float
    ttr: float
    hapax_ratio: float
    contraction_rate: float
    question_rate: float
    exclaim_rate: float
    digit_rate: float
    upper_word_rate: float
    comma_per_word: float
    semicolon_per_word: float
    punct_per_word: float
    pronoun_i: float
    pronoun_we: float
    pronoun_you: float
    pronoun_one: float
    formal_rate: float
    casual_rate: float
    hedge_rate: float
    formality: float
    suffix_rates: tuple[float, ...]
    function_counts: tuple[float, ...]
    function_freqs: tuple[float, ...]
    char_profile: Mapping[str, float] = field(repr=False)
    content_types: frozenset[str] = field(repr=False)

    def numeric_vector(self, include_function_words: bool = True) -> tuple[float, ...]:
        """Dense comparable vector used by the pairwise detector."""
        core = (
            self.mean_word_len / 8.0,
            self.mean_sent_len / 25.0,
            self.ttr,
            self.hapax_ratio,
            self.contraction_rate,
            self.question_rate,
            self.exclaim_rate,
            self.digit_rate,
            self.upper_word_rate,
            self.comma_per_word,
            self.semicolon_per_word * 4.0,
            self.punct_per_word,
            self.pronoun_i,
            self.pronoun_we,
            self.pronoun_you,
            self.pronoun_one,
            self.formal_rate * 3.0,
            self.casual_rate * 3.0,
            self.hedge_rate * 2.0,
            self.formality,
            *self.suffix_rates,
        )
        if include_function_words:
            return core + self.function_freqs
        return core

    def as_dict(self) -> dict[str, float | int]:
        payload: dict[str, float | int] = {
            "n_chars": self.n_chars,
            "n_words": self.n_words,
            "n_sents": self.n_sents,
            "n_types": self.n_types,
            "mean_word_len": round(self.mean_word_len, 4),
            "mean_sent_len": round(self.mean_sent_len, 4),
            "ttr": round(self.ttr, 4),
            "hapax_ratio": round(self.hapax_ratio, 4),
            "contraction_rate": round(self.contraction_rate, 4),
            "question_rate": round(self.question_rate, 4),
            "exclaim_rate": round(self.exclaim_rate, 4),
            "digit_rate": round(self.digit_rate, 4),
            "upper_word_rate": round(self.upper_word_rate, 4),
            "comma_per_word": round(self.comma_per_word, 4),
            "semicolon_per_word": round(self.semicolon_per_word, 4),
            "punct_per_word": round(self.punct_per_word, 4),
            "pronoun_i": round(self.pronoun_i, 4),
            "pronoun_we": round(self.pronoun_we, 4),
            "pronoun_you": round(self.pronoun_you, 4),
            "pronoun_one": round(self.pronoun_one, 4),
            "formal_rate": round(self.formal_rate, 4),
            "casual_rate": round(self.casual_rate, 4),
            "hedge_rate": round(self.hedge_rate, 4),
            "formality": round(self.formality, 4),
        }
        for name, rate in zip(SUFFIX_BINS, self.suffix_rates, strict=True):
            payload[f"suffix_{name}"] = round(rate, 4)
        return payload


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def extract_features(text: str) -> ParagraphFeatures:
    words = split_words(text)
    lower = [w.lower() for w in words]
    sents = split_sentences(text)
    n_words = len(words)
    n_sents = max(1, len(sents))
    counts = Counter(lower)
    n_types = len(counts)
    hapax = sum(1 for value in counts.values() if value == 1)
    mean_word_len = _safe_div(sum(len(w) for w in words), n_words)
    mean_sent_len = _safe_div(n_words, n_sents)
    ttr = _safe_div(n_types, n_words)
    # Guiraud-style damping so very short paragraphs are not 1.0 TTR by default.
    ttr_damped = _safe_div(n_types, math.sqrt(n_words)) / 6.0 if n_words else 0.0
    ttr_damped = max(0.0, min(1.5, ttr_damped))

    contraction_rate = _safe_div(
        sum(1 for w in lower if w in CONTRACTION_SET),
        n_words,
    )
    question_rate = _safe_div(text.count("?"), n_sents)
    exclaim_rate = _safe_div(text.count("!"), n_sents)
    digit_rate = _safe_div(sum(1 for w in words if w[0].isdigit()), n_words)
    upper_word_rate = _safe_div(
        sum(1 for w in words if w.isalpha() and w.isupper() and len(w) > 1),
        n_words,
    )
    comma_per_word = _safe_div(text.count(","), n_words)
    semicolon_per_word = _safe_div(text.count(";"), n_words)
    punct_per_word = _safe_div(len(_PUNCT.findall(text)), n_words)

    pronoun_i = _safe_div(sum(1 for w in lower if w in FIRST_PERSON), n_words)
    pronoun_we = _safe_div(sum(1 for w in lower if w in INCLUSIVE_WE), n_words)
    pronoun_you = _safe_div(sum(1 for w in lower if w in SECOND_PERSON), n_words)
    pronoun_one = _safe_div(len(_IMPERSONAL_ONE.findall(text)), n_words)
    formal_rate = _safe_div(sum(1 for w in lower if w in FORMAL_SET), n_words)
    casual_rate = _safe_div(sum(1 for w in lower if w in CASUAL_SET), n_words)
    hedge_rate = _safe_div(sum(1 for w in lower if w in HEDGE_SET), n_words)

    deontic = _safe_div(sum(1 for w in lower if w in {"must", "shall", "should"}), n_words)
    formality = (
        1.8 * formal_rate
        + 0.45 * (mean_sent_len / 20.0)
        + 0.35 * (mean_word_len / 6.0)
        + 0.20 * (1.0 - contraction_rate)
        + 1.0 * semicolon_per_word
        + 0.8 * pronoun_one
        + 0.25 * pronoun_we
        + 0.6 * deontic
        - 2.0 * casual_rate
        - 1.4 * contraction_rate
        - 1.1 * pronoun_i
        - 0.6 * question_rate
        - 0.5 * exclaim_rate
    )

    suffix_rates = tuple(
        _safe_div(sum(1 for w in lower if w.endswith(suffix) and len(w) > len(suffix) + 1), n_words)
        for suffix in SUFFIX_BINS
    )
    function_counts = tuple(float(counts.get(word, 0)) for word in FUNCTION_WORDS)
    function_freqs = tuple(_safe_div(c, n_words) for c in function_counts)

    content = frozenset(
        w
        for w in lower
        if _CONTENT_RE.match(w)
        and w not in FUNCTION_SET
        and w not in CONTRACTION_SET
        and w not in CASUAL_SET
        and w not in FORMAL_SET
    )
    return ParagraphFeatures(
        text=text,
        n_chars=len(text),
        n_words=n_words,
        n_sents=n_sents,
        n_types=n_types,
        mean_word_len=mean_word_len,
        mean_sent_len=mean_sent_len,
        ttr=ttr_damped if n_words else ttr,
        hapax_ratio=_safe_div(hapax, n_types),
        contraction_rate=contraction_rate,
        question_rate=question_rate,
        exclaim_rate=exclaim_rate,
        digit_rate=digit_rate,
        upper_word_rate=upper_word_rate,
        comma_per_word=comma_per_word,
        semicolon_per_word=semicolon_per_word,
        punct_per_word=punct_per_word,
        pronoun_i=pronoun_i,
        pronoun_we=pronoun_we,
        pronoun_you=pronoun_you,
        pronoun_one=pronoun_one,
        formal_rate=formal_rate,
        casual_rate=casual_rate,
        hedge_rate=hedge_rate,
        formality=formality,
        suffix_rates=suffix_rates,
        function_counts=function_counts,
        function_freqs=function_freqs,
        char_profile=l2_normalize(char_ngrams(text, n=3)),
        content_types=content,
    )


def extract_many(paragraphs: list[str]) -> list[ParagraphFeatures]:
    return [extract_features(p) for p in paragraphs]
