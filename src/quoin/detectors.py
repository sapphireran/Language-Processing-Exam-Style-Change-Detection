"""Detectors I can defend without a GPU.

`QuoinDetector` blends four distances. The weights are not magic: they are
the ones that survived the calibration lab on this toy bank. I keep the
never-fire and always-fire baselines in the same module because the first
oral question is always "why not just guess the majority class?"
"""

from __future__ import annotations

from dataclasses import dataclass

from .features import FeatureVector, pairwise_feature_distance, vectorize
from .ncd import ncd


@dataclass(frozen=True)
class BoundaryScore:
    index: int
    quoin: float
    ncd: float
    char_cosine: float
    function_l1: float
    shape_l1: float
    pred: int


@dataclass(frozen=True)
class QuoinDetector:
    """Weighted blend of compression distance and closed-class stylometry."""

    threshold: float = 0.34
    w_ncd: float = 0.22
    w_char: float = 0.38
    w_function: float = 0.25
    w_shape: float = 0.15

    def score_pair(self, left: str, right: str) -> dict[str, float]:
        left_vec = vectorize(left)
        right_vec = vectorize(right)
        return self.score_vectors(left, right, left_vec, right_vec)

    def score_vectors(
        self,
        left: str,
        right: str,
        left_vec: FeatureVector,
        right_vec: FeatureVector,
    ) -> dict[str, float]:
        feats = pairwise_feature_distance(left_vec, right_vec)
        ncd_value = ncd(left, right)
        quoin = (
            self.w_ncd * ncd_value
            + self.w_char * feats["char_cosine"]
            + self.w_function * feats["function_l1"]
            + self.w_shape * feats["shape_l1"]
        )
        return {
            "quoin": quoin,
            "ncd": ncd_value,
            "char_cosine": feats["char_cosine"],
            "function_l1": feats["function_l1"],
            "shape_l1": feats["shape_l1"],
        }

    def decide(self, score: float) -> int:
        return 1 if score >= self.threshold else 0

    def boundaries(self, paragraphs: list[str]) -> list[BoundaryScore]:
        vectors = [vectorize(paragraph) for paragraph in paragraphs]
        rows: list[BoundaryScore] = []
        for index in range(len(paragraphs) - 1):
            parts = self.score_vectors(
                paragraphs[index],
                paragraphs[index + 1],
                vectors[index],
                vectors[index + 1],
            )
            rows.append(
                BoundaryScore(
                    index=index,
                    quoin=parts["quoin"],
                    ncd=parts["ncd"],
                    char_cosine=parts["char_cosine"],
                    function_l1=parts["function_l1"],
                    shape_l1=parts["shape_l1"],
                    pred=self.decide(parts["quoin"]),
                )
            )
        return rows

    def predict(self, paragraphs: list[str]) -> list[int]:
        return [row.pred for row in self.boundaries(paragraphs)]


def never_fire(n_boundaries: int) -> list[int]:
    return [0] * n_boundaries


def always_fire(n_boundaries: int) -> list[int]:
    return [1] * n_boundaries
