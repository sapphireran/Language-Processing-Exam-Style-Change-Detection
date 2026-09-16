from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from ..io import Problem


class Detector(ABC):
    name: str = "base"

    def fit(self, problems: Sequence[Problem]) -> "Detector":
        return self

    @abstractmethod
    def predict_document(self, sentences: list[str]) -> list[int]:
        raise NotImplementedError

    def predict_proba_document(self, sentences: list[str]) -> list[float]:
        return [float(label) for label in self.predict_document(sentences)]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name}

    def from_dict(self, payload: dict[str, Any]) -> "Detector":
        return self
