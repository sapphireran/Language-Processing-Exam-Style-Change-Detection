"""Character n-gram profiles for short-paragraph authorship cues.

Character n-grams capture morphology, punctuation habits, and spelling
preferences without needing a parser. They are a standard baseline in
authorship analysis and remain useful when paragraphs are too short for
reliable type-token statistics.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable

from .tokenize import tokenize_chars


def char_ngrams(text: str, n: int = 3) -> list[str]:
    if n < 1:
        raise ValueError("n must be >= 1")
    body = tokenize_chars(text, keep_spaces=True)
    if len(body) < n:
        return [body] if body else []
    return [body[i : i + n] for i in range(len(body) - n + 1)]


def profile(text: str, n: int = 3) -> dict[str, float]:
    """L1-normalised n-gram frequencies."""
    grams = char_ngrams(text, n=n)
    if not grams:
        return {}
    counts = Counter(grams)
    total = float(sum(counts.values()))
    return {gram: count / total for gram, count in counts.items()}


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    keys = set(left) | set(right)
    dot = sum(left.get(key, 0.0) * right.get(key, 0.0) for key in keys)
    norm_left = math.sqrt(sum(value * value for value in left.values()))
    norm_right = math.sqrt(sum(value * value for value in right.values()))
    if norm_left == 0.0 or norm_right == 0.0:
        return 0.0
    return dot / (norm_left * norm_right)


def cosine_distance(left: dict[str, float], right: dict[str, float]) -> float:
    return 1.0 - cosine(left, right)


def top_ngrams(text: str, n: int = 3, k: int = 12) -> list[tuple[str, int]]:
    counts = Counter(char_ngrams(text, n=n))
    return counts.most_common(k)


def shared_mass(left: dict[str, float], right: dict[str, float]) -> float:
    """Overlapping probability mass; 1 means identical support."""
    keys = set(left) & set(right)
    return sum(min(left[key], right[key]) for key in keys)


def mean_profile(texts: Iterable[str], n: int = 3) -> dict[str, float]:
    acc: Counter[str] = Counter()
    for text in texts:
        acc.update(char_ngrams(text, n=n))
    total = float(sum(acc.values()))
    if total == 0.0:
        return {}
    return {gram: count / total for gram, count in acc.items()}
