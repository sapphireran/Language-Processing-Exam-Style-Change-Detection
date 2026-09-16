"""Character n-gram profiles (the Koppel-style cue I actually use).

Character 3-grams leak morphology, punctuation habits, and function-word
shapes without committing me to a tokenizer. On short exam snippets they
are more stable than word unigrams, which is why the pair distance puts
them first.
"""

from __future__ import annotations

import math
from collections import Counter


def char_ngrams(text: str, n: int = 3) -> Counter[str]:
    """Lowercased character n-grams with a single-space pad on each side."""
    if n < 1:
        raise ValueError("n must be >= 1")
    padded = f" {text.lower().strip()} "
    if len(padded) < n:
        return Counter([padded])
    return Counter(padded[i : i + n] for i in range(len(padded) - n + 1))


def cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b[k] for k in a.keys() & b.keys())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def cosine_distance(a: Counter[str], b: Counter[str]) -> float:
    return 1.0 - cosine(a, b)


def char_ngram_distance(left: str, right: str, n: int = 3) -> float:
    return cosine_distance(char_ngrams(left, n), char_ngrams(right, n))


def kl_divergence(p: Counter[str], q: Counter[str], floor: float = 0.5) -> float:
    """Smoothed KL(p || q) over the union of keys. Used by the window walkthrough."""
    keys = set(p) | set(q)
    if not keys:
        return 0.0
    ps = sum(p.values()) + floor * len(keys)
    qs = sum(q.values()) + floor * len(keys)
    total = 0.0
    for key in keys:
        pk = (p[key] + floor) / ps
        qk = (q[key] + floor) / qs
        total += pk * math.log(pk / qk)
    return total
