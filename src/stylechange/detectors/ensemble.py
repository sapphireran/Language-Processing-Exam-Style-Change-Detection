from __future__ import annotations

from typing import Any, Sequence

from ..io import Problem
from .base import Detector
from .logistic import LogisticDetector
from .unsupervised import UnsupervisedDetector


class EnsembleDetector(Detector):
    """Average unsupervised and logistic probabilities when both exist."""

    name = "ensemble"

    def __init__(self) -> None:
        self.unsupervised = UnsupervisedDetector()
        self.logistic = LogisticDetector()
        self.has_logistic = False

    def fit(self, problems: Sequence[Problem]) -> Detector:
        self.unsupervised.fit(problems)
        try:
            self.logistic.fit(problems)
            self.has_logistic = True
        except ValueError:
            self.has_logistic = False
        return self

    def predict_proba_document(self, sentences: list[str]) -> list[float]:
        u = self.unsupervised.predict_proba_document(sentences)
        if not self.has_logistic:
            return u
        try:
            v = self.logistic.predict_proba_document(sentences)
        except RuntimeError:
            return u
        return [0.5 * a + 0.5 * b for a, b in zip(u, v)]

    def predict_document(self, sentences: list[str]) -> list[int]:
        return [int(p >= 0.5) for p in self.predict_proba_document(sentences)]

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "unsupervised": self.unsupervised.to_dict(),
            "has_logistic": self.has_logistic,
        }
        if self.has_logistic and self.logistic.weights_ is not None:
            payload["logistic"] = self.logistic.to_dict()
        return payload

    def from_dict(self, payload: dict[str, Any]) -> Detector:
        self.unsupervised.from_dict(payload.get("unsupervised", {"name": "unsupervised"}))
        self.has_logistic = bool(payload.get("has_logistic"))
        if self.has_logistic and "logistic" in payload:
            self.logistic.from_dict(payload["logistic"])
        return self
