"""Closed-set stylometric features for paragraph-level comparison.

The inventory is deliberately interpretable: function words, punctuation
rates, lexical richness, pronoun person, a few suffixes, and a handful of
discourse markers. That is the feature family most exam questions expect
you to name before anyone mentions transformers.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from collections import Counter
from collections.abc import Iterable, Sequence

import numpy as np

from style_change.tokenize import Document, Paragraph, split_paragraphs

# Closed-class words used as authorship markers since Mosteller & Wallace.
FUNCTION_WORDS: tuple[str, ...] = (
    "a",
    "about",
    "after",
    "all",
    "also",
    "an",
    "and",
    "any",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "down",
    "each",
    "for",
    "from",
    "had",
    "has",
    "have",
    "her",
    "him",
    "his",
    "how",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "just",
    "like",
    "may",
    "more",
    "most",
    "no",
    "not",
    "now",
    "of",
    "on",
    "one",
    "only",
    "or",
    "other",
    "our",
    "out",
    "over",
    "own",
    "same",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "will",
    "with",
    "would",
    "you",
    "your",
    "however",
    "therefore",
    "thus",
)

FIRST_PERSON = frozenset({"i", "me", "my", "mine", "we", "us", "our", "ours", "i'm", "i've", "i'd", "i'll", "we're", "we've"})
SECOND_PERSON = frozenset({"you", "your", "yours", "you're", "you've", "you'd", "you'll"})
THIRD_PERSON = frozenset(
    {
        "he",
        "him",
        "his",
        "she",
        "her",
        "hers",
        "they",
        "them",
        "their",
        "theirs",
        "it",
        "its",
        "he's",
        "she's",
        "they're",
    }
)
CONTRACTIONS = re.compile(
    r"\b(?:['’](?:t|re|ve|ll|d|m|s)|n't)\b|"
    r"\b(?:I'm|I've|I'd|I'll|you're|you've|we're|they're|don't|doesn't|didn't|"
    r"can't|won't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't|"
    r"wouldn't|couldn't|shouldn't|it's|that's|there's|what's)\b",
    re.IGNORECASE,
)
CONTRAST = frozenset({"however", "although", "though", "yet", "nevertheless", "nonetheless", "whereas"})
INFER = frozenset({"therefore", "thus", "hence", "accordingly", "consequently", "thereby"})
CASUAL = frozenset({"anyway", "yeah", "yep", "kinda", "gonna", "wanna", "pretty", "really", "literally", "okay", "ok", "stuff", "things"})
MODALS = frozenset({"can", "could", "may", "might", "must", "shall", "should", "will", "would"})
NEGATION = frozenset({"not", "no", "never", "neither", "nobody", "nothing", "n't"})
DETERMINERS = frozenset({"the", "a", "an", "this", "that", "these", "those", "some", "any", "each", "every"})
PREPOSITIONS = frozenset(
    {
        "in",
        "on",
        "at",
        "by",
        "for",
        "from",
        "to",
        "of",
        "with",
        "about",
        "into",
        "through",
        "after",
        "over",
        "between",
        "under",
    }
)
SCALAR_NAMES: tuple[str, ...] = (
    "words_per_sentence",
    "std_words_per_sentence",
    "chars_per_word",
    "std_chars_per_word",
    "type_token_ratio",
    "hapax_ratio",
    "dislegomena_ratio",
    "yules_k",
    "honores_r",
    "uppercase_ratio",
    "digit_ratio",
    "contraction_ratio",
    "punct_per_word",
    "comma_per_word",
    "semicolon_per_word",
    "colon_per_word",
    "question_per_word",
    "exclaim_per_word",
    "quote_per_word",
    "dash_per_word",
    "paren_per_word",
    "suffix_ing",
    "suffix_ed",
    "suffix_ly",
    "suffix_tion",
    "suffix_ness",
    "suffix_ment",
    "suffix_able",
    "first_person",
    "second_person",
    "third_person",
    "discourse_contrast",
    "discourse_infer",
    "discourse_casual",
    "modal_ratio",
    "negation_ratio",
    "determiner_ratio",
    "preposition_ratio",
)

# Compact subset used for distance-based detection. Full function-word
# vectors are kept for inspection; in a 5–8 paragraph exam document they
# are too sparse and too high-dimensional for cosine to stay meaningful.
DETECTION_FEATURES: tuple[str, ...] = (
    "words_per_sentence",
    "std_words_per_sentence",
    "chars_per_word",
    "type_token_ratio",
    "contraction_ratio",
    "first_person",
    "second_person",
    "third_person",
    "discourse_contrast",
    "discourse_infer",
    "discourse_casual",
    "question_per_word",
    "exclaim_per_word",
    "semicolon_per_word",
    "comma_per_word",
    "colon_per_word",
    "modal_ratio",
    "negation_ratio",
    "determiner_ratio",
    "preposition_ratio",
    "punct_per_word",
)

STYLE_AXIS_NAMES: tuple[str, ...] = ("formality", "address", "rhythm", "procedure")


def _column(table: FeatureTable, name: str) -> np.ndarray:
    if table.matrix.size == 0:
        return np.zeros(0, dtype=np.float64)
    if name not in table.names:
        return np.zeros(table.matrix.shape[0], dtype=np.float64)
    return table.matrix[:, list(table.names).index(name)]


def style_axes(table: FeatureTable) -> np.ndarray:
    """Map a feature table into a 4-D interpretable style space.

    High-dimensional z-scored cosine is a poor exam-document metric:
    five or six paragraphs cannot support a 100-D covariance. These
    four axes keep the geometry small enough that a jump is readable.
    """
    if table.matrix.shape[0] == 0:
        return np.zeros((0, len(STYLE_AXIS_NAMES)), dtype=np.float64)

    def c(name: str) -> np.ndarray:
        return _column(table, name)

    formality = (
        4.0 * c("discourse_infer")
        + 4.0 * c("discourse_contrast")
        + 6.0 * c("semicolon_per_word")
        - 8.0 * c("contraction_ratio")
        - 6.0 * c("first_person")
        - 5.0 * c("second_person")
        - 8.0 * c("discourse_casual")
        - 6.0 * c("question_per_word")
        - 5.0 * c("exclaim_per_word")
    )
    address = c("first_person") + c("second_person") + c("question_per_word") + c("exclaim_per_word")
    rhythm = c("words_per_sentence") / 20.0
    procedure = 4.0 * c("colon_per_word") + 3.0 * c("digit_ratio")
    return np.column_stack([formality, address, rhythm, procedure])


def _safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den else default


def _yules_k(freq: Counter[str], n_tokens: int) -> float:
    if n_tokens < 2:
        return 0.0
    counts_of_counts = Counter(freq.values())
    moment = sum(i * i * v_i for i, v_i in counts_of_counts.items())
    return 1e4 * (moment - n_tokens) / (n_tokens * n_tokens)


def _honores_r(vocab: int, hapax: int, n_tokens: int) -> float:
    if n_tokens < 2 or vocab == 0:
        return 0.0
    hapax_share = hapax / vocab
    if hapax_share >= 0.999:
        hapax_share = 0.999
    return 100.0 * math.log(n_tokens) / (1.0 - hapax_share)


def _count_chars(text: str, chars: str) -> int:
    return sum(text.count(ch) for ch in chars)


def paragraph_scalars(paragraph: Paragraph) -> dict[str, float]:
    """Compute the non-function-word half of the feature vector."""
    words = paragraph.words
    n_words = len(words)
    lower = [word.lower() for word in words]
    freq = Counter(lower)
    vocab = len(freq)
    hapax = sum(1 for count in freq.values() if count == 1)
    dis = sum(1 for count in freq.values() if count == 2)

    sentence_lengths = [len(tokenize_words_local(sentence)) for sentence in paragraph.sentences]
    if not sentence_lengths:
        sentence_lengths = [n_words]
    word_lengths = [len(word) for word in words] or [0]

    text = paragraph.text
    letters = sum(ch.isalpha() for ch in text) or 1

    return {
        "words_per_sentence": float(np.mean(sentence_lengths)),
        "std_words_per_sentence": float(np.std(sentence_lengths)),
        "chars_per_word": float(np.mean(word_lengths)),
        "std_chars_per_word": float(np.std(word_lengths)),
        "type_token_ratio": _safe_div(vocab, n_words),
        "hapax_ratio": _safe_div(hapax, vocab),
        "dislegomena_ratio": _safe_div(dis, vocab),
        "yules_k": _yules_k(freq, n_words),
        "honores_r": _honores_r(vocab, hapax, n_words),
        "uppercase_ratio": sum(ch.isupper() for ch in text) / letters,
        "digit_ratio": sum(ch.isdigit() for ch in text) / max(len(text), 1),
        "contraction_ratio": _safe_div(len(CONTRACTIONS.findall(text)), n_words),
        "punct_per_word": _safe_div(sum(not ch.isalnum() and not ch.isspace() for ch in text), n_words),
        "comma_per_word": _safe_div(_count_chars(text, ","), n_words),
        "semicolon_per_word": _safe_div(_count_chars(text, ";"), n_words),
        "colon_per_word": _safe_div(_count_chars(text, ":"), n_words),
        "question_per_word": _safe_div(_count_chars(text, "?"), n_words),
        "exclaim_per_word": _safe_div(_count_chars(text, "!"), n_words),
        "quote_per_word": _safe_div(_count_chars(text, "\"'“”‘’"), n_words),
        "dash_per_word": _safe_div(_count_chars(text, "-–—"), n_words),
        "paren_per_word": _safe_div(_count_chars(text, "()"), n_words),
        "suffix_ing": _safe_div(sum(w.endswith("ing") for w in lower), n_words),
        "suffix_ed": _safe_div(sum(w.endswith("ed") for w in lower), n_words),
        "suffix_ly": _safe_div(sum(w.endswith("ly") for w in lower), n_words),
        "suffix_tion": _safe_div(sum(w.endswith("tion") for w in lower), n_words),
        "suffix_ness": _safe_div(sum(w.endswith("ness") for w in lower), n_words),
        "suffix_ment": _safe_div(sum(w.endswith("ment") for w in lower), n_words),
        "suffix_able": _safe_div(sum(w.endswith("able") or w.endswith("ible") for w in lower), n_words),
        "first_person": _safe_div(sum(w in FIRST_PERSON for w in lower), n_words),
        "second_person": _safe_div(sum(w in SECOND_PERSON for w in lower), n_words),
        "third_person": _safe_div(sum(w in THIRD_PERSON for w in lower), n_words),
        "discourse_contrast": _safe_div(sum(w in CONTRAST for w in lower), n_words),
        "discourse_infer": _safe_div(sum(w in INFER for w in lower), n_words),
        "discourse_casual": _safe_div(sum(w in CASUAL for w in lower), n_words),
        "modal_ratio": _safe_div(sum(w in MODALS for w in lower), n_words),
        "negation_ratio": _safe_div(sum(w in NEGATION or w.endswith("n't") for w in lower), n_words),
        "determiner_ratio": _safe_div(sum(w in DETERMINERS for w in lower), n_words),
        "preposition_ratio": _safe_div(sum(w in PREPOSITIONS for w in lower), n_words),
    }


def tokenize_words_local(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)


def function_word_rates(paragraph: Paragraph) -> dict[str, float]:
    lower = [word.lower() for word in paragraph.words]
    n_words = len(lower)
    counts = Counter(lower)
    return {f"fw_{word}": _safe_div(counts[word], n_words) for word in FUNCTION_WORDS}


def feature_names() -> tuple[str, ...]:
    return SCALAR_NAMES + tuple(f"fw_{word}" for word in FUNCTION_WORDS)


def vectorize_paragraph(paragraph: Paragraph) -> np.ndarray:
    scalars = paragraph_scalars(paragraph)
    rates = function_word_rates(paragraph)
    names = feature_names()
    values = [scalars.get(name, rates.get(name, 0.0)) for name in names]
    return np.asarray(values, dtype=np.float64)


@dataclass(frozen=True)
class FeatureTable:
    """Paragraph feature matrix with stable column names."""

    names: tuple[str, ...]
    matrix: np.ndarray
    paragraph_indices: tuple[int, ...]

    def zscored(self, eps: float = 1e-8) -> np.ndarray:
        if self.matrix.size == 0:
            return self.matrix
        mu = self.matrix.mean(axis=0)
        sd = self.matrix.std(axis=0)
        sd = np.where(sd < eps, 1.0, sd)
        return (self.matrix - mu) / sd

    def subset(self, names: Sequence[str]) -> FeatureTable:
        lookup = {name: i for i, name in enumerate(self.names)}
        missing = [name for name in names if name not in lookup]
        if missing:
            raise KeyError(f"unknown feature names: {missing}")
        columns = [lookup[name] for name in names]
        return FeatureTable(tuple(names), self.matrix[:, columns], self.paragraph_indices)

    def as_rows(self) -> list[dict[str, float]]:
        rows = []
        for row in self.matrix:
            rows.append({name: float(value) for name, value in zip(self.names, row, strict=True)})
        return rows

    def top_differences(self, left: int, right: int, k: int = 8) -> list[tuple[str, float, float, float]]:
        """Return features with the largest absolute z-score gap between two rows."""
        if self.matrix.shape[0] < 2:
            return []
        scaled = self.zscored()
        delta = np.abs(scaled[left] - scaled[right])
        order = np.argsort(delta)[::-1][:k]
        rows = []
        for idx in order:
            rows.append(
                (
                    self.names[int(idx)],
                    float(self.matrix[left, idx]),
                    float(self.matrix[right, idx]),
                    float(delta[idx]),
                )
            )
        return rows


class FeatureExtractor:
    """Extract a closed stylometric vector for every paragraph."""

    def __init__(self, min_words: int = 1) -> None:
        self.min_words = min_words
        self.names = feature_names()

    def extract_document(self, document: Document) -> FeatureTable:
        kept: list[Paragraph] = [
            paragraph for paragraph in document.paragraphs if paragraph.word_count >= self.min_words
        ]
        if not kept:
            return FeatureTable(self.names, np.zeros((0, len(self.names))), ())
        matrix = np.vstack([vectorize_paragraph(paragraph) for paragraph in kept])
        return FeatureTable(self.names, matrix, tuple(p.index for p in kept))

    def extract_text(self, text: str, source: str | None = None) -> tuple[Document, FeatureTable]:
        document = split_paragraphs(text, source=source)
        return document, self.extract_document(document)

    def extract_many(self, paragraphs: Sequence[Paragraph]) -> FeatureTable:
        return FeatureTable(
            self.names,
            np.vstack([vectorize_paragraph(p) for p in paragraphs]) if paragraphs else np.zeros((0, len(self.names))),
            tuple(p.index for p in paragraphs),
        )


def describe_features(table: FeatureTable, indices: Iterable[int] | None = None) -> str:
    """Human-readable snapshot of a few headline features."""
    highlight = (
        "words_per_sentence",
        "chars_per_word",
        "type_token_ratio",
        "contraction_ratio",
        "first_person",
        "second_person",
        "discourse_casual",
        "discourse_infer",
        "comma_per_word",
        "semicolon_per_word",
    )
    rows = []
    chosen = list(indices) if indices is not None else list(range(table.matrix.shape[0]))
    header = "para " + " ".join(f"{name:>16}" for name in highlight)
    rows.append(header)
    name_index = {name: i for i, name in enumerate(table.names)}
    for row_i in chosen:
        values = [
            f"{table.matrix[row_i, name_index[name]]:16.3f}" if name in name_index else f"{0:16.3f}"
            for name in highlight
        ]
        rows.append(f"{table.paragraph_indices[row_i]:>4} " + " ".join(values))
    return "\n".join(rows)
