"""Intrinsic style-change detector.

Short sentences have unstable n-gram profiles, so the default model does
**not** classify every adjacent pair independently. Exam answers (and the
PAN-style problems they imitate) are written in contiguous author blocks.
The detector therefore:

1. extracts a stylometric vector for every sentence or paragraph
2. projects each span onto personal / academic / telegram register axes
3. searches for the most surprising cut in a span (binary segmentation)
4. recurses on each side while the best cut stays above a threshold

``mode="pairwise"`` keeps the older windowed threshold rule around for
ablations and the calibration demo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Sequence

from .features import FeatureVector, extract_many, iter_named_deltas, merge_span
from .register import mean_span_distance, register_axes, span_distance
from .tokenize import Granularity, split_units

DEFAULT_THRESHOLD = 0.36
DEFAULT_WINDOW = 2
Mode = Literal["segment", "pairwise"]


@dataclass(frozen=True)
class BoundaryExplanation:
    index: int
    left_text: str
    right_text: str
    score: float
    change: int
    parts: dict[str, float]
    top_deltas: list[tuple[str, float]]
    register_left: dict[str, float]
    register_right: dict[str, float]


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
    """Register-axis change-point detector."""

    def __init__(
        self,
        *,
        granularity: Granularity = "sentence",
        threshold: float = DEFAULT_THRESHOLD,
        window: int = DEFAULT_WINDOW,
        mode: Mode = "segment",
        min_span: int | None = None,
        dense_weight: float = 0.45,
        function_weight: float = 0.30,
        char_weight: float = 0.25,
    ) -> None:
        if window < 1:
            raise ValueError("window must be >= 1")
        if mode not in {"segment", "pairwise"}:
            raise ValueError(f"unknown mode: {mode}")
        self.granularity = granularity
        self.threshold = threshold
        self.window = window
        self.mode = mode
        if min_span is None:
            min_span = 1 if granularity == "paragraph" else 2
        if min_span < 1:
            raise ValueError("min_span must be >= 1")
        self.min_span = min_span
        # Short children are almost always one author block in this task.
        # Recursing into a 3–4 sentence notes dump overfits punctuation.
        self.min_child_span = 6 if granularity == "sentence" else 2
        # Kept so older call sites / CLI experiments still construct cleanly.
        total = dense_weight + function_weight + char_weight
        self.dense_weight = dense_weight / total if total else 0.0
        self.function_weight = function_weight / total if total else 0.0
        self.char_weight = char_weight / total if total else 0.0

    def split(self, text: str) -> list[str]:
        return split_units(text, granularity=self.granularity)

    def score_spans(
        self, left: FeatureVector, right: FeatureVector
    ) -> tuple[float, dict[str, float]]:
        return span_distance(left, right)

    def score_boundary(
        self, vectors: Sequence[FeatureVector], index: int
    ) -> tuple[float, dict[str, float], FeatureVector, FeatureVector]:
        """Score the boundary between ``vectors[index]`` and ``vectors[index+1]``."""
        left_start = max(0, index - self.window + 1)
        right_end = min(len(vectors), index + 1 + self.window)
        left = merge_span(vectors, left_start, index + 1)
        right = merge_span(vectors, index + 1, right_end)
        score, parts = self.score_spans(left, right)
        return score, parts, left, right

    def _best_cut(
        self, vectors: Sequence[FeatureVector], lo: int, hi: int
    ) -> tuple[int, float, dict[str, float]] | None:
        """Return the highest-scoring split inside ``[lo, hi)``."""
        span = hi - lo
        if span < 2 * self.min_span:
            return None
        best_i = -1
        best_score = -1.0
        best_parts: dict[str, float] = {}
        start = lo + self.min_span - 1
        stop = hi - self.min_span
        for index in range(start, stop):
            left = merge_span(vectors, lo, index + 1)
            right = merge_span(vectors, index + 1, hi)
            score, parts = mean_span_distance(
                vectors[lo : index + 1],
                vectors[index + 1 : hi],
                left,
                right,
            )
            if score > best_score:
                best_i = index
                best_score = score
                best_parts = parts
        if best_i < 0:
            return None
        return best_i, best_score, best_parts

    def _segment(self, vectors: Sequence[FeatureVector]) -> list[int]:
        changes = [0] * (len(vectors) - 1)

        def recurse(lo: int, hi: int, depth: int) -> None:
            if depth > 0 and (hi - lo) < self.min_child_span:
                return
            cut = self._best_cut(vectors, lo, hi)
            if cut is None:
                return
            index, score, _ = cut
            if score < self.threshold:
                return
            changes[index] = 1
            recurse(lo, index + 1, depth + 1)
            recurse(index + 1, hi, depth + 1)

        recurse(0, len(vectors), 0)
        return changes

    def _pairwise(self, vectors: Sequence[FeatureVector]) -> tuple[list[float], list[int]]:
        scores: list[float] = []
        changes: list[int] = []
        for index in range(len(vectors) - 1):
            score, _, _, _ = self.score_boundary(vectors, index)
            scores.append(score)
            changes.append(1 if score >= self.threshold else 0)
        return scores, changes

    def _cut_quality(self, vectors: Sequence[FeatureVector]) -> list[float]:
        """How good a *global* prefix/suffix cut would be at each boundary."""
        scores: list[float] = []
        n = len(vectors)
        for index in range(n - 1):
            if index + 1 < self.min_span or (n - index - 1) < self.min_span:
                score, _, _, _ = self.score_boundary(vectors, index)
            else:
                left = merge_span(vectors, 0, index + 1)
                right = merge_span(vectors, index + 1, n)
                score, _ = mean_span_distance(
                    vectors[: index + 1], vectors[index + 1 :], left, right
                )
            scores.append(score)
        return scores

    def predict(self, text: str, *, explain: bool = False) -> StyleChangePrediction:
        units = self.split(text)
        if len(units) < 2:
            return StyleChangePrediction(units=units, scores=[], changes=[])

        vectors = extract_many(units)
        if self.mode == "pairwise":
            scores, changes = self._pairwise(vectors)
        else:
            changes = self._segment(vectors)
            scores = self._cut_quality(vectors)

        explanations: list[BoundaryExplanation] = []
        if explain:
            for index, (score, label) in enumerate(zip(scores, changes)):
                _, parts, left, right = self.score_boundary(vectors, index)
                parts = dict(parts)
                parts["cut"] = score
                deltas = sorted(
                    iter_named_deltas(left, right),
                    key=lambda item: item[1],
                    reverse=True,
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
                        register_left=register_axes(left),
                        register_right=register_axes(right),
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
            # Stay near the default. A tiny synthetic split will happily
            # drive the threshold to 0.2 and start splitting single-author
            # textbooks in half.
            grid = [round(0.28 + 0.02 * i, 2) for i in range(15)]

        best_threshold = self.threshold
        best_f1 = -1.0
        original = self.threshold
        for candidate in grid:
            self.threshold = candidate
            predictions = [self.predict_changes(document) for document in documents]
            f1 = evaluate_changes(gold, predictions).macro_f1
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = candidate
        self.threshold = best_threshold if best_f1 >= 0 else original
        return self.threshold
