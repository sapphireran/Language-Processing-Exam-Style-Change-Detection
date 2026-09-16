"""Character n-gram profiles and cosine geometry.

Character 3-grams are the workhorse lexical fingerprint of modern
stylometry: they pick up morphology, punctuation habits, and common
function-word chunks without a parser. Cosine on L2-normalised counts
is the usual comparison.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable, Mapping

_WS = re.compile(r"\s+")


def char_ngrams(text: str, n: int = 3) -> Counter[str]:
    folded = _WS.sub(" ", text.lower()).strip()
    if len(folded) < n:
        return Counter({folded: 1} if folded else {})
    return Counter(folded[i : i + n] for i in range(len(folded) - n + 1))


def word_ngrams(words: Iterable[str], n: int = 2) -> Counter[str]:
    seq = [w.lower() for w in words]
    if len(seq) < n:
        return Counter()
    return Counter(" ".join(seq[i : i + n]) for i in range(len(seq) - n + 1))


def l2_normalize(counts: Mapping[str, float]) -> dict[str, float]:
    norm = math.sqrt(sum(value * value for value in counts.values()))
    if norm == 0:
        return {}
    return {key: value / norm for key, value in counts.items()}


def cosine_similarity(
    left: Mapping[str, float],
    right: Mapping[str, float],
) -> float:
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    dot = 0.0
    for key, value in left.items():
        other = right.get(key)
        if other:
            dot += value * other
    return max(-1.0, min(1.0, dot))


def cosine_distance(
    left: Mapping[str, float],
    right: Mapping[str, float],
) -> float:
    return 1.0 - cosine_similarity(left, right)


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    a = set(left)
    b = set(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
