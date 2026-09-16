"""Content (topic) vectors, used only to *expose* the topic confound.

These features are the thing a style-change system should try **not** to
rely on. The Easy examples are separable by content-word cosine alone;
the Hard examples are not. That contrast is the whole point of the
three-way difficulty split.
"""

from __future__ import annotations

from collections import Counter

from stylechange.distance import cosine_distance
from stylechange.lexicon import FUNCTION_WORD_SET
from stylechange.tokenize import words


def content_vector(text: str, min_len: int = 4) -> dict[str, float]:
    tokens = [
        tok
        for tok in words(text)
        if tok not in FUNCTION_WORD_SET and len(tok) >= min_len and not tok.isdigit()
    ]
    counts = Counter(tokens)
    total = sum(counts.values())
    if total == 0:
        return {}
    return {tok: count / total for tok, count in counts.items()}


def topic_distance(left: str, right: str) -> float:
    return cosine_distance(content_vector(left), content_vector(right))
