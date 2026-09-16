"""Lexical richness statistics that survive a short paragraph better than raw TTR."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Richness:
    n_tokens: int
    n_types: int
    ttr: float
    guiraud: float
    hapax_ratio: float
    dislegomena_ratio: float
    yule_k: float
    honore_r: float


def richness(words_lower: tuple[str, ...]) -> Richness:
    n = len(words_lower)
    if n == 0:
        return Richness(0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    counts = Counter(words_lower)
    v = len(counts)
    freq_of_freq = Counter(counts.values())
    hapax = freq_of_freq.get(1, 0)
    dis = freq_of_freq.get(2, 0)
    ttr = v / n
    guiraud = v / math.sqrt(n)
    hapax_ratio = hapax / v if v else 0.0
    dis_ratio = dis / v if v else 0.0
    # Yule's K = 10^4 * (sum i^2 V_i - N) / N^2
    sum_i2_vi = sum((i * i) * vi for i, vi in freq_of_freq.items())
    yule_k = 10000.0 * (sum_i2_vi - n) / (n * n) if n else 0.0
    # Honoré's R = 100 * ln(N) / (1 - V1/V); undefined if every type is a hapax.
    if v and hapax < v:
        honore = 100.0 * math.log(n) / (1.0 - (hapax / v))
    else:
        honore = 0.0
    return Richness(
        n_tokens=n,
        n_types=v,
        ttr=ttr,
        guiraud=guiraud,
        hapax_ratio=hapax_ratio,
        dislegomena_ratio=dis_ratio,
        yule_k=yule_k,
        honore_r=honore,
    )
