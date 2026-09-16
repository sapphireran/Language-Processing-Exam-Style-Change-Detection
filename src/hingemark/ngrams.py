"""Character n-grams as a cheap morphological channel."""

from __future__ import annotations

import math
import re
from collections import Counter

_KEEP = re.compile(r"[^a-z ]+")


def char_ngrams(text: str, n: int = 3) -> Counter[str]:
    folded = _KEEP.sub(" ", text.lower())
    folded = re.sub(r"\s+", " ", folded).strip()
    padded = f" {folded} "
    if len(padded) < n:
        return Counter({padded: 1})
    return Counter(padded[i : i + n] for i in range(len(padded) - n + 1))


def cosine_counter(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def cosine_distance(a: Counter[str], b: Counter[str]) -> float:
    return 1.0 - cosine_counter(a, b)
