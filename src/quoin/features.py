"""Stylometric vectors that stay cheap enough to compute on paper.

The oral-exam rule I set for myself: every coordinate must be something I
can define in one sentence and estimate with a tally sheet. No POS tagger,
no embeddings, no download.

Channels
--------
character 3-grams
    Authorship's workhorse. They catch punctuation-adjacent habits
    ("the ", "; I", "'s ") without committing to a lexicon.
function-word profile
    Relative frequencies of a closed list. Topic-light by construction.
shape
    Mean sentence length, comma rate, semicolon rate, question rate,
    contraction rate, informal-marker rate, formal-marker rate,
    type-token ratio, hapax rate, uppercase-word rate.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .lexicon import CONTRACTIONS, FORMAL_MARKERS, FUNCTION_WORDS, INFORMAL, PUNCT_CHARS
from .tokenize import sentence_lengths, words

_FUNCTION_INDEX = {word: index for index, word in enumerate(FUNCTION_WORDS)}


@dataclass(frozen=True)
class FeatureVector:
    ngrams: dict[str, float]
    function: tuple[float, ...]
    shape: dict[str, float]
    n_words: int
    n_chars: int

    def shape_values(self, keys: Iterable[str] | None = None) -> list[float]:
        keys = tuple(keys) if keys is not None else tuple(sorted(self.shape))
        return [self.shape[key] for key in keys]


def _char_ngrams(text: str, n: int = 3) -> dict[str, float]:
    folded = " ".join(text.lower().split())
    if len(folded) < n:
        return {folded: 1.0} if folded else {}
    counts: Counter[str] = Counter(folded[i : i + n] for i in range(len(folded) - n + 1))
    total = sum(counts.values()) or 1
    return {gram: count / total for gram, count in counts.items()}


def _function_profile(tokens: list[str]) -> tuple[float, ...]:
    if not tokens:
        return tuple(0.0 for _ in FUNCTION_WORDS)
    counts = Counter(tokens)
    total = len(tokens)
    return tuple(counts[word] / total for word in FUNCTION_WORDS)


def _rate(tokens: list[str], lexicon: Iterable[str]) -> float:
    if not tokens:
        return 0.0
    bag = set(lexicon)
    return sum(1 for token in tokens if token in bag) / len(tokens)


def _punct_rate(text: str, mark: str) -> float:
    if not text:
        return 0.0
    return text.count(mark) / len(text)


def _type_token(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def _hapax_rate(tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    return sum(1 for value in counts.values() if value == 1) / len(tokens)


def _uppercase_rate(text: str) -> float:
    tokens = [token for token in text.split() if any(ch.isalpha() for ch in token)]
    if not tokens:
        return 0.0
    return sum(1 for token in tokens if token[:1].isupper()) / len(tokens)


def vectorize(text: str) -> FeatureVector:
    tokens = words(text)
    lengths = sentence_lengths(text)
    mean_sentence = sum(lengths) / len(lengths) if lengths else 0.0
    shape = {
        "mean_sentence": mean_sentence,
        "comma": _punct_rate(text, ","),
        "semicolon": _punct_rate(text, ";"),
        "colon": _punct_rate(text, ":"),
        "question": _punct_rate(text, "?"),
        "exclaim": _punct_rate(text, "!"),
        "dash": _punct_rate(text, "—") + _punct_rate(text, "-"),
        "paren": _punct_rate(text, "(") + _punct_rate(text, ")"),
        "contraction": _rate(tokens, CONTRACTIONS),
        "informal": _rate(tokens, INFORMAL),
        "formal": _rate(tokens, FORMAL_MARKERS),
        "ttr": _type_token(tokens),
        "hapax": _hapax_rate(tokens),
        "uppercase": _uppercase_rate(text),
        "mean_word": (sum(len(token) for token in tokens) / len(tokens)) if tokens else 0.0,
    }
    return FeatureVector(
        ngrams=_char_ngrams(text),
        function=_function_profile(tokens),
        shape=shape,
        n_words=len(tokens),
        n_chars=len(text),
    )


def cosine_distance(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 1.0
    keys = set(left) | set(right)
    dot = sum(left.get(key, 0.0) * right.get(key, 0.0) for key in keys)
    norm_left = math.sqrt(sum(value * value for value in left.values()))
    norm_right = math.sqrt(sum(value * value for value in right.values()))
    if norm_left == 0.0 or norm_right == 0.0:
        return 1.0
    cosine = max(-1.0, min(1.0, dot / (norm_left * norm_right)))
    return 1.0 - cosine


def l1_distance(left: Iterable[float], right: Iterable[float]) -> float:
    return sum(abs(a - b) for a, b in zip(left, right, strict=True))


def shape_l1(left: FeatureVector, right: FeatureVector) -> float:
    keys = (
        "mean_sentence",
        "comma",
        "semicolon",
        "question",
        "contraction",
        "informal",
        "formal",
        "ttr",
        "mean_word",
    )
    # Sentence length lives on a different scale than rates. Divide it by 40
    # so a 8-word vs 28-word habit does not drown the punctuation channels.
    scaled_left = []
    scaled_right = []
    for key in keys:
        scale = 40.0 if key == "mean_sentence" else (8.0 if key == "mean_word" else 1.0)
        scaled_left.append(left.shape[key] / scale)
        scaled_right.append(right.shape[key] / scale)
    return l1_distance(scaled_left, scaled_right)


def function_l1(left: FeatureVector, right: FeatureVector) -> float:
    return l1_distance(left.function, right.function)


def register_vector(vec: FeatureVector) -> dict[str, float]:
    """A short 'house' axis: formality, length, and a few mouth-feel rates.

    This is the channel I trust more than NCD on 80-word original paragraphs.
    zlib saturates there; a handful of register knobs still move.
    """
    return {
        "sent": vec.shape["mean_sentence"] / 40.0,
        "contr": vec.shape["contraction"] * 8.0,
        "informal": vec.shape["informal"] * 10.0,
        "formal": vec.shape["formal"] * 8.0,
        "semi": vec.shape["semicolon"] * 15.0,
        "question": vec.shape["question"] * 8.0,
        "exclaim": vec.shape["exclaim"] * 8.0,
        "ttr": vec.shape["ttr"],
    }


def register_l1(left: FeatureVector, right: FeatureVector) -> float:
    a = register_vector(left)
    b = register_vector(right)
    return sum(abs(a[key] - b[key]) for key in a)


def pairwise_feature_distance(left: FeatureVector, right: FeatureVector) -> dict[str, float]:
    return {
        "char_cosine": cosine_distance(left.ngrams, right.ngrams),
        "function_l1": function_l1(left, right),
        "shape_l1": shape_l1(left, right),
        "register_l1": register_l1(left, right),
    }


def punct_inventory(text: str) -> dict[str, int]:
    return {mark: text.count(mark) for mark in PUNCT_CHARS}
