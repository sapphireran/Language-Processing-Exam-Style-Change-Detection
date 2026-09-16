"""Normalized Compression Distance and cross-compression gain.

Kolmogorov complexity K(x) is the length of the shortest program that emits
x. We cannot compute K. A real compressor C(x) is an *upper bound*. zlib is
a dull, reproducible stand-in.

Normalized Compression Distance (Li, Vitányi, Cilibrasi, and others):

    NCD(x, y) = (C(xy) - min(C(x), C(y))) / max(C(x), C(y))

If x and y share regularities — favourite function words, a punctuation
habit, a clause rhythm — the compressor's sliding window reuses them when
it sees the concatenation, so C(xy) stays closer to max(C(x), C(y)) and
NCD stays small. If they were written in different houses, the second
paragraph looks like new data and NCD rises.

Cross-compression gain is the same idea flipped:

    gain(x, y) = (C(x) + C(y) - C(xy)) / (C(x) + C(y))

High gain means the pair shared a dictionary. I report both in the labs
because one of them is easier to compute by hand on a short string.

Caveats I want on the oral card:

* Short paragraphs: zlib's header and a cold dictionary dominate C(x).
  NCD on 20-word chat lines is mostly noise. That is why Quoin also uses
  character n-grams and function words.
* Topic words compress too. Two paragraphs about quoins will share the
  string "quoin" even if the authors differ. Closed-class features are
  the counterweight.
* zlib is not the best compressor, just the one in the standard library.
"""

from __future__ import annotations

import zlib

# zlib always emits a small header. Subtracting it does not make C a true
# Kolmogorov estimator, but it stops two empty strings looking infinitely
# far apart just because each carries 8 bytes of wrapper.
_HEADER = len(zlib.compress(b"", 9))


def compressed_len(text: str, level: int = 9) -> int:
    """Byte length of zlib(text), with the empty-input header removed."""
    raw = zlib.compress(text.encode("utf-8"), level)
    return max(1, len(raw) - _HEADER)


def ncd(left: str, right: str, level: int = 9) -> float:
    """Normalized Compression Distance in a slightly padded [0, 1.5] range."""
    c_left = compressed_len(left, level)
    c_right = compressed_len(right, level)
    c_both = compressed_len(left + "\n" + right, level)
    denom = max(c_left, c_right)
    score = (c_both - min(c_left, c_right)) / denom
    return max(0.0, min(1.5, score))


def cross_gain(left: str, right: str, level: int = 9) -> float:
    """Fraction of the two separate bit-budgets recovered by concatenating."""
    c_left = compressed_len(left, level)
    c_right = compressed_len(right, level)
    c_both = compressed_len(left + "\n" + right, level)
    denom = c_left + c_right
    return max(0.0, min(1.0, (c_left + c_right - c_both) / denom))


def ncd_matrix(texts: list[str]) -> list[list[float]]:
    """All-pairs NCD. Useful for the 'author return' walkthrough."""
    size = len(texts)
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i, size):
            if i == j:
                matrix[i][j] = ncd(texts[i], texts[i])
            else:
                value = ncd(texts[i], texts[j])
                matrix[i][j] = value
                matrix[j][i] = value
    return matrix
