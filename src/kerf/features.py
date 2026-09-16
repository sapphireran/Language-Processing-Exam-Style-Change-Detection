"""Closed-class and shape features. Nouns are deliberately ignored.

The oral rule: if a feature moves when you swap the topic and keep the
author, it is not a style feature. That is why this vector is almost
entirely function words, pronouns, punctuation, and sentence geometry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .text import contraction_count, lower_words, split_sentences, words

# High-frequency closed-class items. Order is part of the public vector.
FUNCTION_WORDS: tuple[str, ...] = (
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "by",
    "from",
    "as",
    "at",
    "that",
    "this",
    "it",
    "is",
    "was",
    "were",
    "be",
    "been",
    "have",
    "has",
    "had",
    "i",
    "you",
    "we",
    "they",
    "my",
    "your",
    "our",
    "shall",
    "must",
    "may",
    "however",
    "any",
    "such",
    "if",
    "not",
    "no",
    "so",
    "then",
    "than",
    "into",
    "about",
    "over",
    "after",
    "before",
    "because",
    "when",
    "where",
    "who",
    "which",
    "there",
    "here",
    "would",
    "could",
    "should",
    "might",
    "will",
    "can",
    "do",
    "did",
    "does",
    "just",
    "only",
    "also",
    "even",
    "still",
    "already",
    "perhaps",
    "anyway",
    "honestly",
    "really",
    "very",
    "more",
    "most",
    "less",
    "own",
    "same",
    "other",
    "each",
    "every",
    "both",
    "few",
    "many",
    "much",
    "some",
    "these",
    "those",
    "one",
    "two",
    "all",
    "its",
    "their",
    "his",
    "her",
)

HEDGES = frozenset(
    {"may", "might", "perhaps", "however", "suggest", "suggests", "likely", "possible", "ordinary"}
)
PAST_BE = frozenset({"was", "were"})


@dataclass(frozen=True)
class FeatureVector:
    """Rates and a few raw shape numbers. ``as_weighted`` is what the saw uses."""

    rates: dict[str, float] = field(default_factory=dict)
    n_words: int = 0
    n_sentences: int = 0

    def as_weighted(self) -> list[tuple[str, float, float]]:
        """Return (name, value, weight) triples in a stable order."""
        items: list[tuple[str, float, float]] = []
        for word in FUNCTION_WORDS:
            items.append((f"fw:{word}", self.rates.get(f"fw:{word}", 0.0), _fw_weight(word)))
        for name, weight in SHAPE_WEIGHTS:
            items.append((name, self.rates.get(name, 0.0), weight))
        return items

    def values(self) -> list[float]:
        return [value * weight for _, value, weight in self.as_weighted()]

    def names(self) -> list[str]:
        return [name for name, _, _ in self.as_weighted()]


# Pronouns and deontic verbs carry the house voices in this toy bank.
# Content-ish leftovers stay at weight 1 so they can still move a little.
_HEAVY = {
    "i": 2.6,
    "you": 2.8,
    "we": 2.2,
    "my": 2.2,
    "your": 2.6,
    "our": 1.8,
    "shall": 3.4,
    "must": 2.8,
    "may": 2.0,
    "however": 2.4,
    "any": 1.8,
    "such": 1.8,
    "anyway": 2.8,
    "honestly": 2.8,
    "was": 1.6,
    "were": 1.6,
    "the": 1.3,
    "and": 1.2,
    "it": 1.2,
    "will": 1.6,
    "can": 1.4,
    "if": 1.3,
}

SHAPE_WEIGHTS: tuple[tuple[str, float], ...] = (
    ("contraction", 3.2),
    ("question", 2.4),
    ("dash", 1.8),
    ("semicolon", 1.6),
    ("colon", 1.2),
    ("comma", 0.8),
    ("digit", 1.7),
    ("mean_sent", 2.2),
    ("std_sent", 1.0),
    ("mean_word", 1.1),
    ("ttr", 0.9),
    ("first_person", 2.4),
    ("second_person", 2.6),
    ("hedge", 2.0),
    ("passive_ish", 1.5),
    ("uppercase_ratio", 0.6),
)


def _fw_weight(word: str) -> float:
    return _HEAVY.get(word, 1.0)


def extract(paragraph: str) -> FeatureVector:
    tokens = words(paragraph)
    lowered = [t.lower() for t in tokens]
    n = max(len(lowered), 1)
    sents = split_sentences(paragraph)
    sent_lens = [len(words(s)) for s in sents] or [len(tokens)]
    mean_sent = sum(sent_lens) / len(sent_lens)
    if len(sent_lens) > 1:
        mu = mean_sent
        var = sum((x - mu) ** 2 for x in sent_lens) / (len(sent_lens) - 1)
        std_sent = var**0.5
    else:
        std_sent = 0.0
    counts: dict[str, int] = {w: 0 for w in FUNCTION_WORDS}
    for tok in lowered:
        if tok in counts:
            counts[tok] += 1
    rates: dict[str, float] = {f"fw:{w}": counts[w] / n for w in FUNCTION_WORDS}
    types = {t.lower() for t in tokens}
    first = counts["i"] + counts["my"] + counts["we"] + counts["our"]
    second = counts["you"] + counts["your"]
    hedge = sum(1 for t in lowered if t in HEDGES)
    passive = 0
    for i, tok in enumerate(lowered[:-1]):
        if tok in PAST_BE and lowered[i + 1].endswith("ed"):
            passive += 1
    letters = [ch for ch in paragraph if ch.isalpha()]
    upper = sum(1 for ch in letters if ch.isupper()) / max(len(letters), 1)
    rates.update(
        {
            "contraction": contraction_count(paragraph) / n,
            "question": paragraph.count("?") / max(len(sents), 1),
            "dash": (paragraph.count("—") + paragraph.count(" - ")) / n,
            "semicolon": paragraph.count(";") / n,
            "colon": paragraph.count(":") / n,
            "comma": paragraph.count(",") / n,
            "digit": sum(ch.isdigit() for ch in paragraph) / max(len(paragraph), 1),
            "mean_sent": mean_sent / 40.0,
            "std_sent": std_sent / 20.0,
            "mean_word": (sum(len(t) for t in tokens) / n) / 8.0,
            "ttr": len(types) / n,
            "first_person": first / n,
            "second_person": second / n,
            "hedge": hedge / n,
            "passive_ish": passive / n,
            "uppercase_ratio": upper,
        }
    )
    return FeatureVector(rates=rates, n_words=len(tokens), n_sentences=len(sents))


def extract_many(paragraphs: Iterable[str]) -> list[FeatureVector]:
    return [extract(p) for p in paragraphs]


def mean_vector(vectors: list[FeatureVector]) -> list[float]:
    if not vectors:
        return []
    cols = list(zip(*(v.values() for v in vectors)))
    return [sum(col) / len(col) for col in cols]
