from __future__ import annotations

from typing import Any

import numpy as np

from .base import Detector


class AlwaysZeroDetector(Detector):
    """Majority-class baseline: never declare a style change."""

    name = "always0"

    def predict_document(self, sentences: list[str]) -> list[int]:
        return [0] * max(0, len(sentences) - 1)

    def predict_proba_document(self, sentences: list[str]) -> list[float]:
        return [0.0] * max(0, len(sentences) - 1)


class RandomDetector(Detector):
    """Bernoulli(p) control. Not a serious system; useful for smoke tests."""

    name = "random"

    def __init__(self, p: float = 0.3, seed: int = 0) -> None:
        self.p = float(p)
        self.seed = int(seed)

    def predict_document(self, sentences: list[str]) -> list[int]:
        n = max(0, len(sentences) - 1)
        rng = np.random.default_rng(self.seed + n)
        return [int(x) for x in rng.random(n) < self.p]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "p": self.p, "seed": self.seed}

    def from_dict(self, payload: dict[str, Any]) -> Detector:
        self.p = float(payload.get("p", 0.3))
        self.seed = int(payload.get("seed", 0))
        return self
