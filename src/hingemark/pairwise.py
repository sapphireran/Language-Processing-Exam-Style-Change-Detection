"""Score every hinge (consecutive unit pair) in a document."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from .delta import adjacent_delta
from .features import (
    REGISTER_COMPARE_SCALE,
    REGISTER_COMPARE_WEIGHT,
    REGISTER_NAMES,
    UnitFeatures,
    extract_many,
)
from .ngrams import char_ngrams, cosine_distance
from .tokenize import Mode, split_units

DEFAULT_BLEND = (0.72, 0.16, 0.06, 0.06)


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def register_gap(left: UnitFeatures, right: UnitFeatures) -> float:
    """Weighted L1 on scaled register channels. Not min-maxed.

    Document-level min-max made a 1-word length difference look like a
    full-scale style change on short teaching texts. Rates already live
    on a comparable scale; length is divided by a fixed constant.
    """
    raw = 0.0
    for name, a, b in zip(REGISTER_NAMES, left.register_vector(), right.register_vector()):
        scale = REGISTER_COMPARE_SCALE[name]
        weight = REGISTER_COMPARE_WEIGHT[name]
        raw += weight * abs(a - b) / scale
    # Unused channels used to sit in the denominator and squash a real
    # person or vocative flip down to 0.03. Squash the raw sum instead.
    return raw / (1.15 + raw)


@dataclass(frozen=True)
class Hinge:
    index: int
    left: str
    right: str
    register_gap: float
    fw_distance: float
    char_distance: float
    delta: float
    blend: float
    drivers: tuple[str, ...]


def score_hinges(
    text: str,
    *,
    mode: Mode = "lines",
    blend_weights: tuple[float, float, float, float] = DEFAULT_BLEND,
) -> list[Hinge]:
    units = split_units(text, mode=mode)
    return score_unit_hinges(units, blend_weights=blend_weights)


def score_unit_hinges(
    units: Sequence[str],
    *,
    blend_weights: tuple[float, float, float, float] = DEFAULT_BLEND,
) -> list[Hinge]:
    if len(units) < 2:
        return []
    feats = extract_many(units)
    return score_feature_hinges(units, feats, blend_weights=blend_weights)


def score_feature_hinges(
    units: Sequence[str],
    feats: Sequence[UnitFeatures],
    *,
    blend_weights: tuple[float, float, float, float] = DEFAULT_BLEND,
) -> list[Hinge]:
    deltas = adjacent_delta(feats)
    w_reg, w_fw, w_ch, w_de = blend_weights
    hinges: list[Hinge] = []
    for i, (left, right) in enumerate(zip(feats, feats[1:])):
        gap = register_gap(left, right)
        fw = 1.0 - _cosine(left.function_vector(), right.function_vector())
        ch = 0.45 * cosine_distance(char_ngrams(left.text), char_ngrams(right.text))
        de = deltas[i] if i < len(deltas) else 0.0
        # Delta on a 4-unit document is heavy-tailed; squash it.
        de_n = de / (1.0 + de)
        blend = w_reg * gap + w_fw * fw + w_ch * ch + w_de * de_n
        drivers = _top_register_drivers(left, right)
        hinges.append(
            Hinge(
                index=i,
                left=units[i],
                right=units[i + 1],
                register_gap=gap,
                fw_distance=fw,
                char_distance=ch,
                delta=de,
                blend=blend,
                drivers=drivers,
            )
        )
    return hinges


def _top_register_drivers(left: UnitFeatures, right: UnitFeatures, k: int = 3) -> tuple[str, ...]:
    pairs = []
    for name, a, b in zip(REGISTER_NAMES, left.register_vector(), right.register_vector()):
        pairs.append((abs(a - b), name, a, b))
    pairs.sort(reverse=True)
    out = []
    for mag, name, a, b in pairs[:k]:
        if mag <= 0:
            continue
        out.append(f"{name}:{a:.3f}->{b:.3f}")
    return tuple(out)
