from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from ..evaluate import macro_f1
from ..features import extract_document, pairwise_euclidean, zscore_rows
from ..io import Problem
from .base import Detector


class ThresholdDetector(Detector):
    """Sweep k on labeled documents; apply the unsupervised rule at test time."""

    name = "threshold"

    def __init__(self, k: float = 0.75, floor: float = 1e-6) -> None:
        self.k = float(k)
        self.floor = float(floor)
        self.fitted_ = False

    def _label_distances(self, distances: np.ndarray, k: float) -> list[int]:
        if distances.size == 0:
            return []
        if distances.size == 1:
            return [int(distances[0] > 0)]
        mean = float(distances.mean())
        std = float(distances.std())
        if std < self.floor:
            return [0 for _ in distances]
        cutoff = mean + k * std
        return [int(value > cutoff) for value in distances]

    def _doc_distances(self, sentences: list[str]) -> np.ndarray:
        matrix = extract_document(sentences)
        if len(matrix) < 2:
            return np.zeros(0, dtype=float)
        if len(matrix) == 2:
            return pairwise_euclidean(matrix)
        return pairwise_euclidean(zscore_rows(matrix, floor=self.floor))

    def fit(self, problems: Sequence[Problem]) -> Detector:
        labeled = [item for item in problems if item.changes is not None]
        if not labeled:
            self.fitted_ = True
            return self
        grid = np.linspace(0.1, 1.8, 18)
        best_k = self.k
        best_score = -1.0
        for k in grid:
            gold: list[int] = []
            pred: list[int] = []
            for problem in labeled:
                distances = self._doc_distances(problem.sentences)
                guess = self._label_distances(distances, float(k))
                if len(guess) != len(problem.changes or []):
                    continue
                gold.extend(problem.changes or [])
                pred.extend(guess)
            if not gold:
                continue
            score = macro_f1(gold, pred)
            if score > best_score:
                best_score = score
                best_k = float(k)
        self.k = best_k
        self.fitted_ = True
        return self

    def predict_document(self, sentences: list[str]) -> list[int]:
        return self._label_distances(self._doc_distances(sentences), self.k)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "k": self.k, "floor": self.floor, "fitted": self.fitted_}

    def from_dict(self, payload: dict[str, Any]) -> Detector:
        self.k = float(payload.get("k", 0.75))
        self.floor = float(payload.get("floor", 1e-6))
        self.fitted_ = bool(payload.get("fitted", False))
        return self
