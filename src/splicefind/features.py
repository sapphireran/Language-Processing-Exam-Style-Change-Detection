"""Stylometric feature extraction for one paragraph or a whole document.

Each paragraph becomes a named vector of length-normalised rates. The
names are part of the exam notes: if you can explain why a feature is
length-normalised, you can usually explain why raw counts would leak
topic and document length instead of style.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .function_words import (
    CONTRACTIONS,
    FIRST_PERSON,
    FUNCTION_WORDS,
    HEDGES,
    IMPERSONAL,
    INTENSIFIERS,
    SECOND_PERSON,
)
from .tokenize import (
    estimate_syllables,
    punctuation_marks,
    sentence_word_counts,
    split_paragraphs,
    split_sentences,
    tokenize_words,
)

SCALAR_NAMES: tuple[str, ...] = (
    "avg_word_len",
    "std_word_len",
    "avg_sent_len",
    "std_sent_len",
    "type_token_ratio",
    "hapax_ratio",
    "long_word_ratio",
    "short_word_ratio",
    "punct_rate",
    "comma_per_sent",
    "stop_ratio",
    "digit_ratio",
    "upper_ratio",
    "contraction_rate",
    "first_person_rate",
    "second_person_rate",
    "impersonal_rate",
    "hedge_rate",
    "intensifier_rate",
    "question_rate",
    "exclaim_rate",
    "flesch_like",
    "yule_k",
    "syllables_per_word",
)


@dataclass(frozen=True)
class FeatureVector:
    scalars: dict[str, float]
    function_words: dict[str, float]
    n_words: int
    n_sents: int
    n_chars: int

    def scalar_row(self, names: Sequence[str] = SCALAR_NAMES) -> list[float]:
        return [self.scalars.get(name, 0.0) for name in names]

    def function_row(self, names: Sequence[str] = FUNCTION_WORDS) -> list[float]:
        return [self.function_words.get(name, 0.0) for name in names]


@dataclass
class DocumentFeatures:
    paragraphs: list[str]
    vectors: list[FeatureVector] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.vectors:
            self.vectors = [extract_paragraph(paragraph) for paragraph in self.paragraphs]

    def __len__(self) -> int:
        return len(self.paragraphs)


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _std(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    var = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return var**0.5


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def yules_k(words: Sequence[str]) -> float:
    """Yule's K: vocabulary concentration. Higher means more repetition."""
    if not words:
        return 0.0
    from collections import Counter

    counts = Counter(words)
    freq_of_freq: dict[int, int] = {}
    for count in counts.values():
        freq_of_freq[count] = freq_of_freq.get(count, 0) + 1
    n_tokens = len(words)
    moment = sum((freq**2) * types for freq, types in freq_of_freq.items())
    return 10000.0 * (moment - n_tokens) / (n_tokens * n_tokens)


def flesch_like(words: Sequence[str], n_sents: int) -> float:
    if not words or n_sents <= 0:
        return 0.0
    syllables = sum(estimate_syllables(word) for word in words)
    asl = len(words) / n_sents
    asw = syllables / len(words)
    return 206.835 - 1.015 * asl - 84.6 * asw


def extract_paragraph(paragraph: str) -> FeatureVector:
    words = tokenize_words(paragraph)
    sentences = split_sentences(paragraph)
    n_words = len(words)
    n_sents = max(len(sentences), 1)
    n_chars = len(paragraph)
    word_lens = [len(word) for word in words]
    sent_lens = sentence_word_counts(paragraph) or [0]
    types = set(words)
    hapax = sum(1 for word in types if words.count(word) == 1)
    punct = punctuation_marks(paragraph)
    letters = [char for char in paragraph if char.isalpha()]
    upper = sum(1 for char in letters if char.isupper())
    digits = sum(1 for char in paragraph if char.isdigit())
    stop = sum(1 for word in words if word in FUNCTION_WORDS)
    fw = {word: 0.0 for word in FUNCTION_WORDS}
    if n_words:
        from collections import Counter

        counts = Counter(words)
        for word in FUNCTION_WORDS:
            fw[word] = counts[word] / n_words

    scalars = {
        "avg_word_len": _mean(word_lens),
        "std_word_len": _std(word_lens),
        "avg_sent_len": _mean(sent_lens),
        "std_sent_len": _std(sent_lens),
        "type_token_ratio": _safe_div(len(types), n_words),
        "hapax_ratio": _safe_div(hapax, n_words),
        "long_word_ratio": _safe_div(sum(1 for length in word_lens if length >= 7), n_words),
        "short_word_ratio": _safe_div(sum(1 for length in word_lens if length <= 3), n_words),
        "punct_rate": _safe_div(len(punct), max(n_chars, 1)),
        "comma_per_sent": _safe_div(paragraph.count(","), n_sents),
        "stop_ratio": _safe_div(stop, n_words),
        "digit_ratio": _safe_div(digits, max(n_chars, 1)),
        "upper_ratio": _safe_div(upper, max(len(letters), 1)),
        "contraction_rate": _safe_div(sum(1 for word in words if word in CONTRACTIONS), n_words),
        "first_person_rate": _safe_div(sum(1 for word in words if word in FIRST_PERSON), n_words),
        "second_person_rate": _safe_div(sum(1 for word in words if word in SECOND_PERSON), n_words),
        "impersonal_rate": _safe_div(sum(1 for word in words if word in IMPERSONAL), n_words),
        "hedge_rate": _safe_div(sum(1 for word in words if word in HEDGES), n_words),
        "intensifier_rate": _safe_div(sum(1 for word in words if word in INTENSIFIERS), n_words),
        "question_rate": _safe_div(paragraph.count("?"), n_sents),
        "exclaim_rate": _safe_div(paragraph.count("!"), n_sents),
        "flesch_like": flesch_like(words, n_sents),
        "yule_k": yules_k(words),
        "syllables_per_word": _safe_div(
            sum(estimate_syllables(word) for word in words), n_words
        ),
    }
    return FeatureVector(
        scalars=scalars,
        function_words=fw,
        n_words=n_words,
        n_sents=n_sents,
        n_chars=n_chars,
    )


def extract_document(text: str) -> DocumentFeatures:
    return DocumentFeatures(paragraphs=split_paragraphs(text))


def zscore_columns(rows: Sequence[Sequence[float]]) -> list[list[float]]:
    if not rows:
        return []
    width = len(rows[0])
    means = []
    stds = []
    for col in range(width):
        values = [row[col] for row in rows]
        mean = _mean(values)
        std = _std(values)
        means.append(mean)
        stds.append(std if std > 1e-12 else 1.0)
    return [
        [(row[col] - means[col]) / stds[col] for col in range(width)] for row in rows
    ]


def cosine_distance(left: Sequence[float], right: Sequence[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = sum(a * a for a in left) ** 0.5
    norm_right = sum(b * b for b in right) ** 0.5
    if norm_left == 0.0 or norm_right == 0.0:
        return 0.0
    cosine = max(-1.0, min(1.0, dot / (norm_left * norm_right)))
    return 1.0 - cosine


def manhattan(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(abs(a - b) for a, b in zip(left, right))


def pairwise_feature_distance(vectors: Sequence[FeatureVector]) -> list[float]:
    """Cosine distance between adjacent z-scored scalar vectors."""
    if len(vectors) < 2:
        return []
    rows = zscore_columns([vector.scalar_row() for vector in vectors])
    return [cosine_distance(rows[i], rows[i + 1]) for i in range(len(rows) - 1)]


def pairwise_function_delta(vectors: Sequence[FeatureVector]) -> list[float]:
    """Burrows-like mean absolute z-difference on function-word rates."""
    if len(vectors) < 2:
        return []
    rows = zscore_columns([vector.function_row() for vector in vectors])
    width = len(rows[0])
    deltas = []
    for i in range(len(rows) - 1):
        deltas.append(manhattan(rows[i], rows[i + 1]) / width)
    return deltas


def feature_table(vectors: Sequence[FeatureVector], names: Sequence[str] = SCALAR_NAMES) -> list[dict[str, float]]:
    return [{name: vector.scalars[name] for name in names} for vector in vectors]


def named_diffs(left: FeatureVector, right: FeatureVector) -> list[tuple[str, float]]:
    diffs = [
        (name, abs(left.scalars[name] - right.scalars[name]))
        for name in SCALAR_NAMES
    ]
    diffs.sort(key=lambda item: item[1], reverse=True)
    return diffs


def iter_paragraphs(text: str) -> Iterable[str]:
    return split_paragraphs(text)
