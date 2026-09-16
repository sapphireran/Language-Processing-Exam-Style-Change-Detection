"""Paragraph fingerprints: function words, character 3-grams, and a dense style vector."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .lexicons import (
    ACADEMIC_MARKERS,
    BOOSTERS,
    CONTRACTIONS,
    FIRST_PERSON,
    FUNCTION_WORDS,
    HEDGES,
    IMPERATIVE_HINTS,
    INFORMAL_MARKERS,
    SECOND_PERSON,
    THIRD_PERSON,
    function_word_index,
)
from .richness import Richness, richness
from .tokenize import Tokens, char_ngrams, estimate_syllables, tokenize

_FW_INDEX = function_word_index()
_FW_N = len(FUNCTION_WORDS)
_CONTRACTION_SET = {c.lower() for c in CONTRACTIONS}


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _punct_rate(text: str, chars: str, n_chars: int) -> float:
    return _safe_div(sum(text.count(ch) for ch in chars), n_chars)


@dataclass
class ParagraphFeatures:
    text: str
    tokens: Tokens
    function_word_rel: tuple[float, ...]
    char_trigrams: dict[str, float]
    richness: Richness
    mean_word_len: float
    std_word_len: float
    mean_sent_len: float
    std_sent_len: float
    comma_rate: float
    period_rate: float
    question_rate: float
    exclaim_rate: float
    semicolon_rate: float
    colon_rate: float
    dash_rate: float
    apostrophe_rate: float
    uppercase_ratio: float
    digit_ratio: float
    contraction_rate: float
    first_person_rate: float
    second_person_rate: float
    third_person_rate: float
    hedge_rate: float
    booster_rate: float
    academic_rate: float
    informal_rate: float
    imperative_rate: float
    syllables_per_word: float
    flesch_proxy: float
    dense: tuple[float, ...] = field(repr=False)

    @property
    def n_words(self) -> int:
        return len(self.tokens.words)


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    var = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return var**0.5


def extract_features(text: str) -> ParagraphFeatures:
    tokens = tokenize(text)
    words_l = tokens.words_lower
    n = len(words_l)
    fw_counts = [0.0] * _FW_N
    for w in words_l:
        idx = _FW_INDEX.get(w)
        if idx is not None:
            fw_counts[idx] += 1.0
    fw_rel = tuple(_safe_div(c, n) for c in fw_counts)

    grams = char_ngrams(text, 3)
    gram_counts = Counter(grams)
    gram_total = sum(gram_counts.values()) or 1
    gram_rel = {g: c / gram_total for g, c in gram_counts.items()}

    word_lens = [float(len(w)) for w in tokens.words]
    sent_lens = []
    for sent in tokens.sentences:
        sent_lens.append(float(len(tokenize(sent).words)))

    n_chars = max(len(text), 1)
    letters = sum(1 for ch in text if ch.isalpha())
    upper = sum(1 for ch in text if ch.isupper())
    digits = sum(1 for ch in text if ch.isdigit())

    rich = richness(words_l)
    syll = sum(estimate_syllables(w) for w in tokens.words)
    spw = _safe_div(syll, n)
    mean_sent = _safe_div(sum(sent_lens), len(sent_lens))
    flesch = 206.835 - 1.015 * mean_sent - 84.6 * spw

    dense = (
        rich.guiraud,
        rich.hapax_ratio,
        rich.yule_k / 100.0,
        _safe_div(sum(word_lens), len(word_lens)),
        _std(word_lens),
        mean_sent,
        _std(sent_lens),
        _punct_rate(text, ",", n_chars),
        _punct_rate(text, ".", n_chars),
        _punct_rate(text, "?", n_chars),
        _punct_rate(text, "!", n_chars),
        _punct_rate(text, ";", n_chars),
        _punct_rate(text, ":", n_chars),
        _punct_rate(text, "—-", n_chars),
        _punct_rate(text, "'’", n_chars),
        _safe_div(upper, letters),
        _safe_div(digits, n_chars),
        _safe_div(sum(1 for w in words_l if w in _CONTRACTION_SET), n),
        _safe_div(sum(1 for w in words_l if w in FIRST_PERSON), n),
        _safe_div(sum(1 for w in words_l if w in SECOND_PERSON), n),
        _safe_div(sum(1 for w in words_l if w in THIRD_PERSON), n),
        _safe_div(sum(1 for w in words_l if w in HEDGES), n),
        _safe_div(sum(1 for w in words_l if w in BOOSTERS), n),
        _safe_div(sum(1 for w in words_l if w in ACADEMIC_MARKERS), n),
        _safe_div(sum(1 for w in words_l if w in INFORMAL_MARKERS), n),
        _safe_div(sum(1 for w in words_l if w in IMPERATIVE_HINTS), n),
        spw,
        flesch / 100.0,
    )

    return ParagraphFeatures(
        text=text,
        tokens=tokens,
        function_word_rel=fw_rel,
        char_trigrams=gram_rel,
        richness=rich,
        mean_word_len=_safe_div(sum(word_lens), len(word_lens)),
        std_word_len=_std(word_lens),
        mean_sent_len=mean_sent,
        std_sent_len=_std(sent_lens),
        comma_rate=_punct_rate(text, ",", n_chars),
        period_rate=_punct_rate(text, ".", n_chars),
        question_rate=_punct_rate(text, "?", n_chars),
        exclaim_rate=_punct_rate(text, "!", n_chars),
        semicolon_rate=_punct_rate(text, ";", n_chars),
        colon_rate=_punct_rate(text, ":", n_chars),
        dash_rate=_punct_rate(text, "—-", n_chars),
        apostrophe_rate=_punct_rate(text, "'’", n_chars),
        uppercase_ratio=_safe_div(upper, letters),
        digit_ratio=_safe_div(digits, n_chars),
        contraction_rate=_safe_div(sum(1 for w in words_l if w in _CONTRACTION_SET), n),
        first_person_rate=_safe_div(sum(1 for w in words_l if w in FIRST_PERSON), n),
        second_person_rate=_safe_div(sum(1 for w in words_l if w in SECOND_PERSON), n),
        third_person_rate=_safe_div(sum(1 for w in words_l if w in THIRD_PERSON), n),
        hedge_rate=_safe_div(sum(1 for w in words_l if w in HEDGES), n),
        booster_rate=_safe_div(sum(1 for w in words_l if w in BOOSTERS), n),
        academic_rate=_safe_div(sum(1 for w in words_l if w in ACADEMIC_MARKERS), n),
        informal_rate=_safe_div(sum(1 for w in words_l if w in INFORMAL_MARKERS), n),
        imperative_rate=_safe_div(sum(1 for w in words_l if w in IMPERATIVE_HINTS), n),
        syllables_per_word=spw,
        flesch_proxy=flesch,
        dense=dense,
    )


def content_types(words_lower: tuple[str, ...]) -> set[str]:
    fw = set(FUNCTION_WORDS)
    return {w for w in words_lower if w not in fw and len(w) > 2}
