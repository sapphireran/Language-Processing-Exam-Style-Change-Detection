"""Pairwise / windowed style-change detector.

The default model is intrinsic and unsupervised:

1. extract a stylometric vector for every sentence (or paragraph)
2. compare a *left window* against a *right window* at each boundary
3. mix dense cosine distance, function-word cosine distance, and
   character 3-gram cosine distance
4. mark a change when the mixed score exceeds a threshold

A small window (default 2) is important. Single-sentence profiles are noisy —
especially for one- or two-word units — so the detector asks “does the writing
immediately before this point look unlike the writing immediately after it?”
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .features import (
    FeatureVector,
    cosine,
    cosine_maps,
    extract_many,
    iter_named_deltas,
    merge_span,
)
from .tokenize import Granularity, split_units

DEFAULT_THRESHOLD = 0.34
DEFAULT_WINDOW = 2


@dataclass(frozen=True)
class BoundaryExplanation:
    index: int
    left_text: str
    right_text: str
    score: float
    change: int
    parts: dict[str, float]
    top_deltas: list[tuple[str, float]]


@dataclass
class StyleChangePrediction:
    units: list[str]
    scores: list[float]
    changes: list[int]
    explanations: list[BoundaryExplanation] = field(default_factory=list)

    @property
    def authors_estimate(self) -> int:
        return 1 + sum(self.changes)

    def as_solution_payload(self) -> dict:
        return {
            "changes": [int(c) for c in self.changes],
            "authors": self.authors_estimate,
        }


class StyleChangeDetector:
    """Thresholded stylometric change detector."""

    def __init__(
        self,
        *,
        granularity: Granularity = "sentence",
        threshold: float = DEFAULT_THRESHOLD,
        window: int = DEFAULT_WINDOW,
        dense_weight: float = 0.45,
        function_weight: float = 0.30,
        char_weight: float = 0.25,
    ) -> None:
        if window < 1:
            raise ValueError("window must be >= 1")
        total = dense_weight + function_weight + char_weight
        if total <= 0:
            raise ValueError("at least one weight must be positive")
        self.granularity = granularity
        self.threshold = threshold
        self.window = window
        self.dense_weight = dense_weight / total
        self.function_weight = function_weight / total
        self.char_weight = char_weight / total

    def split(self, text: str) -> list[str]:
        return split_units(text, granularity=self.granularity)

    def score_boundary(
        self, vectors: Sequence[FeatureVector], index: int
    ) -> tuple[float, dict[str, float], FeatureVector, FeatureVector]:
        """Score the boundary between ``vectors[index]`` and ``vectors[index+1]``."""
        left_start = max(0, index - self.window + 1)
        right_end = min(len(vectors), index + 1 + self.window)
        left = merge_span(vectors, left_start, index + 1)
        right = merge_span(vectors, index + 1, right_end)

        dense = 1.0 - cosine(left.dense, right.dense)
        function = 1.0 - cosine(left.function_distribution(), right.function_distribution())
        char = 1.0 - cosine_maps(left.char_distribution(), right.char_distribution())
        # Empty profiles (punctuation-only fragments) should not scream “change”.
        if left.n_words == 0 or right.n_words == 0:
            mixed = 0.15 * dense + 0.85 * char
        else:
            mixed = (
                self.dense_weight * dense
                + self.function_weight * function
                + self.char_weight * char
            )
        parts = {
            "dense": dense,
            "function": function,
            "char": char,
            "mixed": mixed,
        }
        return mixed, parts, left, right

    def predict(
        self, text: str, *, explain: bool = False
    ) -> StyleChangePrediction:
        units = self.split(text)
        if len(units) < 2:
            return StyleChangePrediction(units=units, scores=[], changes=[])

        vectors = extract_many(units)
        scores: list[float] = []
        changes: list[int] = []
        explanations: list[BoundaryExplanation] = []

        for index in range(len(units) - 1):
            score, parts, left, right = self.score_boundary(vectors, index)
            label = 1 if score >= self.threshold else 0
            scores.append(score)
            changes.append(label)
            if explain:
                deltas = sorted(
                    iter_named_deltas(left, right), key=lambda item: item[1], reverse=True
                )
                explanations.append(
                    BoundaryExplanation(
                        index=index,
                        left_text=units[index],
                        right_text=units[index + 1],
                        score=score,
                        change=label,
                        parts=parts,
                        top_deltas=deltas[:5],
                    )
                )

        return StyleChangePrediction(
            units=units,
            scores=scores,
            changes=changes,
            explanations=explanations,
        )

    def predict_changes(self, text: str) -> list[int]:
        return self.predict(text).changes

    def calibrate(
        self,
        documents: Sequence[str],
        gold: Sequence[Sequence[int]],
        *,
        grid: Sequence[float] | None = None,
    ) -> float:
        """Pick the threshold that maximises macro-F1 on labelled documents."""
        from .evaluate import evaluate_changes

        if grid is None:
            grid = [round(0.18 + 0.02 * i, 2) for i in range(22)]

        scored: list[list[float]] = []
        for document in documents:
            scored.append(self.predict(document).scores)

        best_threshold = self.threshold
        best_f1 = -1.0
        for candidate in grid:
            predictions = [
                [1 if score >= candidate else 0 for score in scores] for scores in scored
            ]
            f1 = evaluate_changes(gold, predictions).macro_f1
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = candidate
        self.threshold = best_threshold
        return best_threshold
