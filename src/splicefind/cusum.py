"""QSUM / CUSUM traces for a single stylometric scalar.

The classic forensic CUSUM plot tracks how a feature (often sentence
length or a function-word rate) drifts from the document mean. A
persistent slope change is a cheap visual for "the second half of this
text does not behave like the first half."

For the PAN paragraph task we also emit a boundary score: the absolute
difference between the mean CUSUM increment on the left of the cut and
the mean increment on the right.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .features import FeatureVector
from .tokenize import sentence_word_counts, split_paragraphs, tokenize_words


@dataclass(frozen=True)
class CusumTrace:
    values: list[float]
    mean: float
    cusum: list[float]
    labels: list[str]


def cusum(values: Sequence[float]) -> CusumTrace:
    if not values:
        return CusumTrace(values=[], mean=0.0, cusum=[], labels=[])
    mean = sum(values) / len(values)
    running = 0.0
    series = []
    for value in values:
        running += value - mean
        series.append(running)
    return CusumTrace(values=list(values), mean=mean, cusum=series, labels=[])


def sentence_length_trace(text: str) -> CusumTrace:
    values: list[float] = []
    labels: list[str] = []
    for index, paragraph in enumerate(split_paragraphs(text), start=1):
        counts = sentence_word_counts(paragraph)
        if not counts:
            counts = [0]
        for sent_i, count in enumerate(counts, start=1):
            values.append(float(count))
            labels.append(f"p{index}.s{sent_i}")
    trace = cusum(values)
    return CusumTrace(values=trace.values, mean=trace.mean, cusum=trace.cusum, labels=labels)


def paragraph_feature_trace(vectors: Sequence[FeatureVector], name: str) -> CusumTrace:
    values = [vector.scalars.get(name, 0.0) for vector in vectors]
    trace = cusum(values)
    labels = [f"p{index}" for index in range(1, len(values) + 1)]
    return CusumTrace(values=trace.values, mean=trace.mean, cusum=trace.cusum, labels=labels)


def word_length_trace(text: str) -> CusumTrace:
    values: list[float] = []
    labels: list[str] = []
    for index, paragraph in enumerate(split_paragraphs(text), start=1):
        words = tokenize_words(paragraph)
        if not words:
            values.append(0.0)
            labels.append(f"p{index}.empty")
            continue
        values.append(sum(len(word) for word in words) / len(words))
        labels.append(f"p{index}")
    trace = cusum(values)
    return CusumTrace(values=trace.values, mean=trace.mean, cusum=trace.cusum, labels=labels)


def boundary_scores(trace: CusumTrace) -> list[float]:
    """Score each adjacent pair by a change in CUSUM slope."""
    if len(trace.cusum) < 2:
        return []
    increments = [trace.cusum[0]] + [
        trace.cusum[i] - trace.cusum[i - 1] for i in range(1, len(trace.cusum))
    ]
    scores = []
    for i in range(len(increments) - 1):
        left = _mean(increments[: i + 1])
        right = _mean(increments[i + 1 :])
        scores.append(abs(right - left))
    return scores


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def ascii_sparkline(values: Sequence[float], width: int | None = None) -> str:
    if not values:
        return ""
    glyphs = "▁▂▃▄▅▆▇█"
    lo = min(values)
    hi = max(values)
    span = hi - lo if hi != lo else 1.0
    series = list(values)
    if width is not None and len(series) > width:
        step = len(series) / width
        series = [series[int(i * step)] for i in range(width)]
    chars = []
    for value in series:
        index = int((value - lo) / span * (len(glyphs) - 1))
        chars.append(glyphs[index])
    return "".join(chars)
