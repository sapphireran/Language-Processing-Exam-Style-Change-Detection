from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from ..features import FEATURE_NAMES, extract_document
from ..io import Problem
from ..pairwise import PairMode, pair_matrix
from .base import Detector


def _sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-z))


class LogisticDetector(Detector):
    """From-scratch logistic regression on pairwise feature diffs."""

    name = "logistic"

    def __init__(
        self,
        pair_mode: PairMode = "absdiff",
        lr: float = 0.15,
        epochs: int = 700,
        l2: float = 1e-2,
        threshold: float = 0.5,
        seed: int = 0,
    ) -> None:
        self.pair_mode: PairMode = pair_mode
        self.lr = float(lr)
        self.epochs = int(epochs)
        self.l2 = float(l2)
        self.threshold = float(threshold)
        self.seed = int(seed)
        self.weights_: np.ndarray | None = None
        self.bias_: float = 0.0
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None

    def _pairs_from_sentences(self, sentences: list[str]) -> np.ndarray:
        vectors = extract_document(sentences)
        return pair_matrix(vectors, self.pair_mode)

    def _collect(self, problems: Sequence[Problem]) -> tuple[np.ndarray, np.ndarray]:
        rows: list[np.ndarray] = []
        labels: list[int] = []
        for problem in problems:
            if problem.changes is None:
                continue
            pairs = self._pairs_from_sentences(problem.sentences)
            if len(pairs) != len(problem.changes):
                continue
            rows.append(pairs)
            labels.extend(problem.changes)
        if not rows:
            raise ValueError("logistic fit needs labeled problems with aligned pairs")
        return np.vstack(rows), np.asarray(labels, dtype=float)

    def fit(self, problems: Sequence[Problem]) -> Detector:
        x_raw, y = self._collect(problems)
        self.mean_ = x_raw.mean(axis=0)
        std = x_raw.std(axis=0)
        self.std_ = np.where(std < 1e-6, 1.0, std)
        x = (x_raw - self.mean_) / self.std_
        n, dim = x.shape
        rng = np.random.default_rng(self.seed)
        weights = rng.normal(0.0, 0.01, size=dim)
        bias = 0.0
        n1 = float(y.sum())
        n0 = float(n - n1)
        class_weight = np.where(y >= 0.5, n / (2.0 * max(n1, 1.0)), n / (2.0 * max(n0, 1.0)))
        for _ in range(self.epochs):
            probs = _sigmoid(x @ weights + bias)
            err = (probs - y) * class_weight
            weights -= self.lr * (x.T @ err / n + self.l2 * weights)
            bias -= self.lr * float(err.mean())
        self.weights_ = weights
        self.bias_ = float(bias)
        return self

    def _transform(self, pairs: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("logistic detector has not been fit")
        return (pairs - self.mean_) / self.std_

    def predict_proba_document(self, sentences: list[str]) -> list[float]:
        if self.weights_ is None:
            raise RuntimeError("logistic detector has not been fit")
        pairs = self._pairs_from_sentences(sentences)
        if len(pairs) == 0:
            return []
        x = self._transform(pairs)
        return [float(p) for p in _sigmoid(x @ self.weights_ + self.bias_)]

    def predict_document(self, sentences: list[str]) -> list[int]:
        return [int(p >= self.threshold) for p in self.predict_proba_document(sentences)]

    def to_dict(self) -> dict[str, Any]:
        if self.weights_ is None or self.mean_ is None or self.std_ is None:
            raise RuntimeError("refusing to serialise an unfitted logistic detector")
        return {
            "name": self.name,
            "pair_mode": self.pair_mode,
            "lr": self.lr,
            "epochs": self.epochs,
            "l2": self.l2,
            "threshold": self.threshold,
            "seed": self.seed,
            "weights": self.weights_.tolist(),
            "bias": self.bias_,
            "mean": self.mean_.tolist(),
            "std": self.std_.tolist(),
            "feature_names": list(FEATURE_NAMES),
        }

    def from_dict(self, payload: dict[str, Any]) -> Detector:
        self.pair_mode = payload.get("pair_mode", "absdiff")
        self.lr = float(payload.get("lr", self.lr))
        self.epochs = int(payload.get("epochs", self.epochs))
        self.l2 = float(payload.get("l2", self.l2))
        self.threshold = float(payload.get("threshold", self.threshold))
        self.seed = int(payload.get("seed", self.seed))
        self.weights_ = np.asarray(payload["weights"], dtype=float)
        self.bias_ = float(payload.get("bias", 0.0))
        self.mean_ = np.asarray(payload["mean"], dtype=float)
        self.std_ = np.asarray(payload["std"], dtype=float)
        return self
