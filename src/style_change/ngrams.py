"""Character n-gram profiles.

Character 3-grams survive messy tokenization and pick up spelling habits,
punctuation, and morphology that word lists miss. They are also the first
feature family I would mention in an exam answer after function words.
"""

from __future__ import annotations

from collections import Counter


def char_ngrams(text: str, n: int = 3) -> Counter[str]:
    folded = " ".join(text.lower().split())
    if len(folded) < n:
        return Counter({folded: 1} if folded else {})
    return Counter(folded[i : i + n] for i in range(len(folded) - n + 1))


def normalized_profile(counts: Counter[str]) -> dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {}
    return {gram: value / total for gram, value in counts.items()}


def aligned_vectors(
    left: dict[str, float],
    right: dict[str, float],
) -> tuple[list[float], list[float]]:
    keys = sorted(set(left) | set(right))
    return [left.get(k, 0.0) for k in keys], [right.get(k, 0.0) for k in keys]
