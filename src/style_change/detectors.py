"""Paragraph-pair style-change detectors."""

from __future__ import annotations

from dataclasses import dataclass

from .distances import cosine_distance, jensen_shannon
from .features import extract_profile
from .lexicons import FUNCTION_WORDS
from .ngrams import aligned_vectors, char_ngrams, normalized_profile
from .tokenize import words


def _function_word_vector(text: str) -> list[float]:
    tokens = words(text)
    if not tokens:
        return [0.0] * len(FUNCTION_WORDS)
    freq = {word: 0 for word in FUNCTION_WORDS}
    for token in tokens:
        if token in freq:
            freq[token] += 1
    return [freq[word] / len(tokens) for word in sorted(FUNCTION_WORDS)]


def stylometric_distances(paragraphs: list[str]) -> list[float]:
    if len(paragraphs) < 2:
        return []
    scaled = [extract_profile(p).scaled_vector() for p in paragraphs]
    return [
        cosine_distance(scaled[i], scaled[i + 1])
        for i in range(len(scaled) - 1)
    ]


def char3_distances(paragraphs: list[str]) -> list[float]:
    profiles = [normalized_profile(char_ngrams(p, n=3)) for p in paragraphs]
    distances = []
    for left, right in zip(profiles, profiles[1:], strict=False):
        a, b = aligned_vectors(left, right)
        distances.append(cosine_distance(a, b))
    return distances


def function_word_distances(paragraphs: list[str]) -> list[float]:
    vectors = [_function_word_vector(p) for p in paragraphs]
    return [
        jensen_shannon(vectors[i], vectors[i + 1])
        for i in range(len(vectors) - 1)
    ]


def adaptive_threshold(
    distances: list[float],
    sensitivity: float = 0.42,
    floor: float = 0.34,
    tight_range: float = 0.08,
) -> float:
    """Pick a cut using an absolute floor plus the document's own range.

    A tiny range used to mean "predict all zeros". That is wrong when every
    boundary is a change: the distances are all high and close together.
    Rules:

    - if the whole document sits below `floor`, predict no changes
    - if the range is tight and the cluster is above `floor`, predict all
      changes
    - otherwise cut at a fraction of the range, never below `floor`
    """
    if not distances:
        return 1.0
    lo, hi = min(distances), max(distances)
    if hi < floor:
        return floor
    if (hi - lo) < tight_range:
        return lo if lo >= floor else floor
    return max(floor, lo + sensitivity * (hi - lo))


def apply_threshold(distances: list[float], threshold: float) -> list[int]:
    return [1 if value >= threshold else 0 for value in distances]


@dataclass
class StyleChangeDetector:
    name: str
    sensitivity: float = 0.42
    threshold: float | None = None
    floor: float = 0.34

    def distances(self, paragraphs: list[str]) -> list[float]:
        raise NotImplementedError

    def predict(self, paragraphs: list[str]) -> list[int]:
        scores = self.distances(paragraphs)
        cut = self.threshold if self.threshold is not None else adaptive_threshold(
            scores, self.sensitivity, floor=self.floor
        )
        return apply_threshold(scores, cut)


class StylometricDetector(StyleChangeDetector):
    def __init__(self, **kwargs: float | None) -> None:
        super().__init__(name="stylometric", **kwargs)

    def distances(self, paragraphs: list[str]) -> list[float]:
        return stylometric_distances(paragraphs)


class Char3Detector(StyleChangeDetector):
    def __init__(self, **kwargs: float | None) -> None:
        super().__init__(name="char3", **kwargs)

    def distances(self, paragraphs: list[str]) -> list[float]:
        return char3_distances(paragraphs)


class FunctionWordDetector(StyleChangeDetector):
    def __init__(self, **kwargs: float | None) -> None:
        super().__init__(name="function_word", **kwargs)

    def distances(self, paragraphs: list[str]) -> list[float]:
        return function_word_distances(paragraphs)


class EnsembleDetector(StyleChangeDetector):
    """Weighted mix of stylometry, character 3-grams, and function words."""

    def __init__(
        self,
        weights: tuple[float, float, float] = (0.45, 0.35, 0.20),
        **kwargs: float | None,
    ) -> None:
        super().__init__(name="ensemble", **kwargs)
        self.weights = weights

    def distances(self, paragraphs: list[str]) -> list[float]:
        stylo = stylometric_distances(paragraphs)
        chars = char3_distances(paragraphs)
        func = function_word_distances(paragraphs)
        w0, w1, w2 = self.weights
        weight_sum = w0 + w1 + w2
        return [
            (w0 * a + w1 * b + w2 * c) / weight_sum
            for a, b, c in zip(stylo, chars, func, strict=True)
        ]


DETECTORS = {
    "ensemble": EnsembleDetector,
    "stylometric": StylometricDetector,
    "char3": Char3Detector,
    "function_word": FunctionWordDetector,
}


def build_detector(
    name: str = "ensemble",
    threshold: float | None = None,
    sensitivity: float = 0.42,
) -> StyleChangeDetector:
    if name not in DETECTORS:
        known = ", ".join(sorted(DETECTORS))
        raise ValueError(f"unknown detector {name!r}; choose from {known}")
    return DETECTORS[name](threshold=threshold, sensitivity=sensitivity)
