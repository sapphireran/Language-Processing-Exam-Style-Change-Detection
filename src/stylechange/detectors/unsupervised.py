from __future__ import annotations

from typing import Any

import numpy as np

from ..features import extract_document, pairwise_euclidean, zscore_rows
from .base import Detector


class UnsupervisedDetector(Detector):
    """Within-document z-scored Euclidean jump detector."""

    name = "unsupervised"

    def __init__(self, k: float = 0.75, floor: float = 1e-6) -> None:
        self.k = float(k)
        self.floor = float(floor)

    def distances(self, sentences: list[str]) -> np.ndarray:
        matrix = extract_document(sentences)
        if len(matrix) < 2:
            return np.zeros(0, dtype=float)
        if len(matrix) == 2:
            # Degenerate z-score; fall back to raw Euclidean.
            return pairwise_euclidean(matrix)
        z = zscore_rows(matrix, floor=self.floor)
        return pairwise_euclidean(z)

    def predict_document(self, sentences: list[str]) -> list[int]:
        probs = self.predict_proba_document(sentences)
        return [int(p >= 0.5) for p in probs]

    def predict_proba_document(self, sentences: list[str]) -> list[float]:
        distances = self.distances(sentences)
        if distances.size == 0:
            return []
        if distances.size == 1:
            # One pair: any non-zero distance is a change candidate.
            return [float(1.0 if distances[0] > 0 else 0.0)]
        mean = float(distances.mean())
        std = float(distances.std())
        if std < self.floor:
            return [0.0 for _ in distances]
        threshold = mean + self.k * std
        # Smooth a probability via a logistic around the threshold.
        scaled = (distances - threshold) / (std + self.floor)
        return [float(1.0 / (1.0 + np.exp(-x))) for x in scaled]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "k": self.k, "floor": self.floor}

    def from_dict(self, payload: dict[str, Any]) -> Detector:
        self.k = float(payload.get("k", 0.75))
        self.floor = float(payload.get("floor", 1e-6))
        return self
