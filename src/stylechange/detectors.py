"""Unsupervised change detectors operating on consecutive paragraph pairs."""

from __future__ import annotations

from dataclasses import dataclass

from stylechange.distance import pair_distance
from stylechange.features import StyleProfile, extract_profile
from stylechange.paragraphs import split_paragraphs


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    centre = _mean(values)
    variance = sum((v - centre) ** 2 for v in values) / (len(values) - 1)
    return variance**0.5


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


@dataclass
class Detection:
    changes: list[int]
    distances: list[float]
    components: list[dict[str, float]]
    threshold: float
    profiles: list[StyleProfile]


class ThresholdDetector:
    """Label a boundary as a change if combined distance exceeds ``threshold``."""

    def __init__(self, threshold: float = 0.33) -> None:
        self.threshold = threshold

    def predict_paragraphs(self, paragraphs: list[str]) -> Detection:
        profiles = [extract_profile(p) for p in paragraphs]
        components = [
            pair_distance(profiles[i], profiles[i + 1]) for i in range(len(profiles) - 1)
        ]
        distances = [part["combined"] for part in components]
        changes = [1 if dist > self.threshold else 0 for dist in distances]
        return Detection(
            changes=changes,
            distances=distances,
            components=components,
            threshold=self.threshold,
            profiles=profiles,
        )

    def predict_text(self, text: str) -> Detection:
        return self.predict_paragraphs(split_paragraphs(text))


class AdaptiveDetector:
    """Document-relative threshold: mean + ``k`` standard deviations.

    A fixed global cut-off is brittle when a whole document is written in a
    compressed register (Hard). Comparing each boundary to the document's
    own distance distribution is the unsupervised analogue of "this jump is
    unusual *here*".
    """

    def __init__(self, k: float = 0.65, floor: float = 0.30) -> None:
        self.k = k
        self.floor = floor

    def predict_paragraphs(self, paragraphs: list[str]) -> Detection:
        profiles = [extract_profile(p) for p in paragraphs]
        components = [
            pair_distance(profiles[i], profiles[i + 1]) for i in range(len(profiles) - 1)
        ]
        distances = [part["combined"] for part in components]
        adaptive = max(self.floor, _mean(distances) + self.k * _std(distances))
        # Single-boundary documents have std = 0; fall back to the floor so
        # a large unique jump can still fire.
        if len(distances) == 1:
            adaptive = max(self.floor, distances[0] * 0.5)
        changes = [1 if dist > adaptive else 0 for dist in distances]
        return Detection(
            changes=changes,
            distances=distances,
            components=components,
            threshold=adaptive,
            profiles=profiles,
        )

    def predict_text(self, text: str) -> Detection:
        return self.predict_paragraphs(split_paragraphs(text))


def smooth_changes(changes: list[int], distances: list[float], radius: int = 1) -> list[int]:
    """Optional majority smooth. Off by default; useful as an exam variant."""
    if radius <= 0 or len(changes) <= 2:
        return list(changes)
    smoothed = list(changes)
    for i in range(len(changes)):
        lo = max(0, i - radius)
        hi = min(len(changes), i + radius + 1)
        window = changes[lo:hi]
        if sum(window) > len(window) / 2:
            smoothed[i] = 1
        elif sum(window) < len(window) / 2:
            smoothed[i] = 0
        else:
            smoothed[i] = 1 if distances[i] >= _median(distances[lo:hi]) else 0
    return smoothed
