"""Detectors I can defend without a GPU.

`QuoinDetector` still *computes* zlib NCD — that is the oral thesis —
but on 80-word original paragraphs the compressor saturates (NCD hangs
around 0.85 whether or not the house changed). The decision therefore
leans on a register axis plus a within-document peak: a hinge fires if
it is an obvious absolute jump, or if it is the document's loudest
hinge by a margin. Never-fire and always-fire stay in this module
because the first oral question is always "why not guess the majority
class?"
"""

from __future__ import annotations

import statistics
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
    register_l1: float
    residual: float
    pred: int


@dataclass(frozen=True)
class QuoinDetector:
    """Register-heavy blend with a peak rule for sparse documents."""

    threshold: float = 0.72
    rel_margin: float = 0.08
    floor: float = 0.40
    w_ncd: float = 0.0
    w_char: float = 0.20
    w_function: float = 0.15
    w_shape: float = 0.25
    w_register: float = 0.40

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
            + self.w_register * feats["register_l1"]
        )
        return {
            "quoin": quoin,
            "ncd": ncd_value,
            "char_cosine": feats["char_cosine"],
            "function_l1": feats["function_l1"],
            "shape_l1": feats["shape_l1"],
            "register_l1": feats["register_l1"],
        }

    def decide_scores(self, scores: list[float]) -> list[int]:
        """Absolute high jump, or the document's peak if it clears a margin."""
        if not scores:
            return []
        median = statistics.median(scores)
        loudest = max(scores)
        bits: list[int] = []
        for score in scores:
            peak = score >= loudest - 1e-12 and (score - median) >= self.rel_margin
            high = score >= self.threshold
            bits.append(1 if (high or peak) and score >= self.floor else 0)
        return bits

    def decide(self, score: float) -> int:
        return 1 if score >= self.threshold else 0

    def boundaries(self, paragraphs: list[str]) -> list[BoundaryScore]:
        vectors = [vectorize(paragraph) for paragraph in paragraphs]
        parts_list = []
        for index in range(len(paragraphs) - 1):
            parts_list.append(
                self.score_vectors(
                    paragraphs[index],
                    paragraphs[index + 1],
                    vectors[index],
                    vectors[index + 1],
                )
            )
        scores = [parts["quoin"] for parts in parts_list]
        median = statistics.median(scores) if scores else 0.0
        preds = self.decide_scores(scores)
        rows: list[BoundaryScore] = []
        for index, parts in enumerate(parts_list):
            rows.append(
                BoundaryScore(
                    index=index,
                    quoin=parts["quoin"],
                    ncd=parts["ncd"],
                    char_cosine=parts["char_cosine"],
                    function_l1=parts["function_l1"],
                    shape_l1=parts["shape_l1"],
                    register_l1=parts["register_l1"],
                    residual=parts["quoin"] - median,
                    pred=preds[index],
                )
            )
        return rows

    def predict(self, paragraphs: list[str]) -> list[int]:
        return [row.pred for row in self.boundaries(paragraphs)]


def never_fire(n_boundaries: int) -> list[int]:
    return [0] * n_boundaries


def always_fire(n_boundaries: int) -> list[int]:
    return [1] * n_boundaries
