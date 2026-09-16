"""Multi-channel CUSUM for style drift.

CUSUM (cumulative sum of deviations from a local mean) is the classic
forensic-linguistics toy for sentence-length or word-length habit. A
change of author often shows up as a slope change, not just a single
spike. This module is for explanation and as one weak vote in the
ensemble — CUSUM alone is too coarse for paragraph-level PAN labels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .features import ParagraphFeatures


@dataclass(frozen=True)
class CusumSeries:
    name: str
    values: tuple[float, ...]
    mean: float
    deviations: tuple[float, ...]
    cusum: tuple[float, ...]


def cusum(values: Sequence[float]) -> CusumSeries:
    if not values:
        return CusumSeries("empty", (), 0.0, (), ())
    mean = sum(values) / len(values)
    deviations = tuple(v - mean for v in values)
    running = 0.0
    path: list[float] = []
    for dev in deviations:
        running += dev
        path.append(running)
    return CusumSeries(
        name="series",
        values=tuple(values),
        mean=mean,
        deviations=deviations,
        cusum=tuple(path),
    )


def _adjacent_slope(path: Sequence[float]) -> list[float]:
    if len(path) < 2:
        return []
    return [abs(path[i + 1] - path[i]) for i in range(len(path) - 1)]


def word_length_cusum(features: Sequence[ParagraphFeatures]) -> CusumSeries:
    series = cusum([feat.mean_word_len for feat in features])
    return CusumSeries(
        "mean_word_len",
        series.values,
        series.mean,
        series.deviations,
        series.cusum,
    )


def sentence_length_cusum(features: Sequence[ParagraphFeatures]) -> CusumSeries:
    series = cusum([feat.mean_sent_len for feat in features])
    return CusumSeries(
        "mean_sent_len",
        series.values,
        series.mean,
        series.deviations,
        series.cusum,
    )


def formality_cusum(features: Sequence[ParagraphFeatures]) -> CusumSeries:
    series = cusum([feat.formality for feat in features])
    return CusumSeries(
        "formality",
        series.values,
        series.mean,
        series.deviations,
        series.cusum,
    )


def cusum_change_scores(features: Sequence[ParagraphFeatures]) -> list[float]:
    """Normalised adjacent |ΔCUSUM| averaged over three channels."""
    if len(features) < 2:
        return []
    channels = [
        word_length_cusum(features),
        sentence_length_cusum(features),
        formality_cusum(features),
    ]
    slopes = [_adjacent_slope(ch.cusum) for ch in channels]
    n = len(features) - 1
    scores = []
    for i in range(n):
        parts = []
        for slope, channel in zip(slopes, channels, strict=True):
            scale = max(0.15, abs(channel.mean) * 0.25 + 0.15)
            parts.append(slope[i] / scale)
        scores.append(sum(parts) / len(parts))
    return scores


def svg_polyline(
    series: CusumSeries,
    width: int = 420,
    height: int = 140,
    stroke: str = "#255f8a",
) -> str:
    """Tiny dependency-free sparkline for lab notes."""
    if not series.cusum:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"></svg>'
    vals = series.cusum
    lo, hi = min(vals), max(vals)
    span = hi - lo if hi != lo else 1.0
    pad = 12
    inner_w = width - 2 * pad
    inner_h = height - 2 * pad
    points = []
    for i, value in enumerate(vals):
        x = pad + (i / max(1, len(vals) - 1)) * inner_w
        y = pad + (1.0 - (value - lo) / span) * inner_h
        points.append(f"{x:.1f},{y:.1f}")
    zero_y = pad + (1.0 - (0.0 - lo) / span) * inner_h
    labels = "".join(
        f'<text x="{pad + (i / max(1, len(vals) - 1)) * inner_w:.1f}" '
        f'y="{height - 2}" font-size="9" text-anchor="middle">{i + 1}</text>'
        for i in range(len(vals))
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#f7f4ee"/>'
        f'<line x1="{pad}" y1="{zero_y:.1f}" x2="{width - pad}" y2="{zero_y:.1f}" '
        f'stroke="#cbbba0" stroke-dasharray="3 3"/>'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="2" points="{" ".join(points)}"/>'
        f'<text x="{pad}" y="10" font-size="10" fill="#255f8a">{series.name} CUSUM</text>'
        f"{labels}</svg>"
    )
