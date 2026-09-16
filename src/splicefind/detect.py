"""Pairwise and ensemble style-change detectors.

The exam baseline is not a transformer. It scores every pair of
consecutive paragraphs with three cheap distances, averages them, and
applies a threshold. That is enough to talk about calibration, topic
confounds, and why F1 is the right number.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .cusum import boundary_scores, paragraph_feature_trace
from .delta import pairwise_delta
from .features import (
    DocumentFeatures,
    extract_document,
    pairwise_feature_distance,
)
from .io import Problem
from .ngrams import cosine_distance, profile
from .tokenize import split_paragraphs


@dataclass(frozen=True)
class Boundary:
    index: int
    left_preview: str
    right_preview: str
    feature_distance: float
    delta: float
    ngram_distance: float
    cusum_score: float
    ensemble: float
    decision: int
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Detection:
    paragraphs: list[str]
    changes: list[int]
    boundaries: list[Boundary]
    threshold: float
    method: str

    @property
    def n_authors_lower_bound(self) -> int:
        return 1 + sum(self.changes)


def _preview(text: str, limit: int = 72) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


def _minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if hi - lo < 1e-12:
        return [0.0 for _ in values]
    return [(value - lo) / (hi - lo) for value in values]


def pairwise_ngram_distance(paragraphs: Sequence[str], n: int = 3) -> list[float]:
    profiles = [profile(paragraph, n=n) for paragraph in paragraphs]
    return [
        cosine_distance(profiles[i], profiles[i + 1])
        for i in range(len(profiles) - 1)
    ]


def _median(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def relative_flags(
    scores: Sequence[float],
    *,
    k: float = 1.25,
    floor: float = 0.08,
    abs_min: float = 0.55,
) -> list[int]:
    """Mark intra-document outliers, plus any globally large score.

    A four-paragraph document has almost no population for z-scores, so
    the default rule asks two questions: is this boundary unusual *for
    this document*, and is the raw blend already large in absolute
    terms? A nearly flat score vector is treated as single-author.
    """
    if not scores:
        return []
    if len(scores) == 1:
        return [1 if scores[0] >= min(abs_min, 0.30) else 0]
    span = max(scores) - min(scores)
    if span < 0.09:
        return [0 for _ in scores]
    med = _median(list(scores))
    mad = _median([abs(score - med) for score in scores])
    cut = med + max(k * mad, floor)
    peak = max(scores)
    second = sorted(scores, reverse=True)[1] if len(scores) > 1 else 0.0
    unique_gap = peak - second
    flags = []
    for score in scores:
        is_unique_peak = abs(score - peak) <= 1e-12 and unique_gap >= floor
        mad_hit = score >= cut and score >= 0.40
        flags.append(1 if mad_hit or score >= abs_min or is_unique_peak else 0)
    return flags


def ensemble_scores(
    features: DocumentFeatures,
    *,
    ngram_n: int = 3,
    weight_feature: float = 3.0,
    weight_delta: float = 0.15,
    weight_ngram: float = 0.40,
    weight_cusum: float = 0.05,
) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
    feature_d = pairwise_feature_distance(features.vectors)
    delta_d = pairwise_delta(features.vectors)
    ngram_d = pairwise_ngram_distance(features.paragraphs, n=ngram_n)
    cusum_d = boundary_scores(paragraph_feature_trace(features.vectors, "avg_sent_len"))
    if len(cusum_d) != len(feature_d):
        cusum_d = cusum_d[: len(feature_d)] + [0.0] * max(0, len(feature_d) - len(cusum_d))
    blended = []
    ngram_excess = [max(0.0, distance - 0.45) for distance in ngram_d]
    for i in range(len(feature_d)):
        blended.append(
            weight_feature * feature_d[i]
            + weight_delta * delta_d[i]
            + weight_ngram * ngram_excess[i]
            + weight_cusum * min(cusum_d[i], 1.0)
        )
    return blended, feature_d, delta_d, ngram_d, cusum_d


def _reasons(
    left_index: int,
    features: DocumentFeatures,
    feature_d: float,
    delta_d: float,
    ngram_d: float,
    ensemble: float,
    threshold: float,
) -> list[str]:
    left = features.vectors[left_index]
    right = features.vectors[left_index + 1]
    notes = [
        f"ensemble={ensemble:.3f} vs threshold={threshold:.3f}",
        f"register gap={feature_d:.3f}",
        f"function-word Delta={delta_d:.3f}",
        f"char-3gram distance={ngram_d:.3f}",
    ]
    cues = []
    if abs(left.scalars["first_person_rate"] - right.scalars["first_person_rate"]) > 0.04:
        cues.append("first-person rate jumps")
    if abs(left.scalars["second_person_rate"] - right.scalars["second_person_rate"]) > 0.04:
        cues.append("address terms jump")
    if abs(left.scalars["contraction_rate"] - right.scalars["contraction_rate"]) > 0.03:
        cues.append("contraction habit changes")
    if abs(left.scalars["avg_sent_len"] - right.scalars["avg_sent_len"]) > 8:
        cues.append("sentence length regime changes")
    if abs(left.scalars["hedge_rate"] - right.scalars["hedge_rate"]) > 0.02:
        cues.append("hedging rate changes")
    if abs(left.scalars["question_rate"] - right.scalars["question_rate"]) > 0.3:
        cues.append("question density changes")
    if cues:
        notes.append("cues: " + ", ".join(cues))
    else:
        notes.append("cues: no single scalar dominates; blend of weak markers")
    return notes


def detect_features(
    features: DocumentFeatures,
    *,
    threshold: float = 0.55,
    method: str = "relative",
) -> Detection:
    if len(features.paragraphs) < 2:
        return Detection(
            paragraphs=list(features.paragraphs),
            changes=[],
            boundaries=[],
            threshold=threshold,
            method=method,
        )
    blended, feature_d, delta_d, ngram_d, cusum_d = ensemble_scores(features)
    if method == "features":
        scores = feature_d
        changes = [1 if score >= threshold else 0 for score in scores]
    elif method == "delta":
        scores = delta_d
        changes = [1 if score >= threshold else 0 for score in scores]
    elif method == "ngram":
        scores = ngram_d
        changes = [1 if score >= threshold else 0 for score in scores]
    elif method == "cusum":
        scores = cusum_d
        changes = [1 if score >= threshold else 0 for score in scores]
    elif method == "adaptive":
        scores = _minmax(blended)
        changes = [1 if score >= max(threshold, 0.60) else 0 for score in scores]
    elif method == "ensemble":
        scores = blended
        changes = [1 if score >= threshold else 0 for score in scores]
    else:
        scores = blended
        changes = relative_flags(blended, abs_min=threshold)

    boundaries = []
    for i, score in enumerate(scores):
        decision = changes[i]
        boundaries.append(
            Boundary(
                index=i,
                left_preview=_preview(features.paragraphs[i]),
                right_preview=_preview(features.paragraphs[i + 1]),
                feature_distance=feature_d[i],
                delta=delta_d[i],
                ngram_distance=ngram_d[i],
                cusum_score=cusum_d[i],
                ensemble=blended[i],
                decision=decision,
                reasons=_reasons(
                    i, features, feature_d[i], delta_d[i], ngram_d[i], blended[i], threshold
                ),
            )
        )
    return Detection(
        paragraphs=list(features.paragraphs),
        changes=changes,
        boundaries=boundaries,
        threshold=threshold,
        method=method,
    )


def detect_text(
    text: str,
    *,
    threshold: float = 0.55,
    method: str = "relative",
) -> Detection:
    return detect_features(extract_document(text), threshold=threshold, method=method)


def detect_document(
    problem: Problem,
    *,
    threshold: float = 0.55,
    method: str = "relative",
) -> Detection:
    return detect_text(problem.text, threshold=threshold, method=method)


def detect_paragraphs(
    paragraphs: Sequence[str],
    *,
    threshold: float = 0.55,
    method: str = "relative",
) -> Detection:
    text = "\n\n".join(paragraphs)
    return detect_text(text, threshold=threshold, method=method)


def always_same(text: str) -> Detection:
    paragraphs = split_paragraphs(text)
    n = max(len(paragraphs) - 1, 0)
    return Detection(
        paragraphs=paragraphs,
        changes=[0] * n,
        boundaries=[],
        threshold=1.0,
        method="always_same",
    )


def always_change(text: str) -> Detection:
    paragraphs = split_paragraphs(text)
    n = max(len(paragraphs) - 1, 0)
    return Detection(
        paragraphs=paragraphs,
        changes=[1] * n,
        boundaries=[],
        threshold=0.0,
        method="always_change",
    )
