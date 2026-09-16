"""Unsupervised detectors for the three classic style-change subtasks.

Task 1: is the document multi-authored?
Task 2: which paragraph boundaries are style changes?
Task 3: assign a latent author id to each paragraph.

Distances are computed in a 4-D style space (formality, address,
rhythm, procedure). A high-dimensional z-scored cosine on the full
feature vector is the wrong geometry for a handful of exam paragraphs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Callable, Sequence

import numpy as np

from style_change.features import FeatureExtractor, FeatureTable, style_axes
from style_change.tokenize import Document, split_paragraphs


def cosine_distance(left: np.ndarray, right: np.ndarray) -> float:
    norm_l = float(np.linalg.norm(left))
    norm_r = float(np.linalg.norm(right))
    if norm_l == 0.0 or norm_r == 0.0:
        return 1.0
    similarity = float(np.dot(left, right) / (norm_l * norm_r))
    similarity = max(-1.0, min(1.0, similarity))
    return 1.0 - similarity


def euclidean_distance(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right))


def adjacent_distances(
    matrix: np.ndarray,
    metric: Callable[[np.ndarray, np.ndarray], float] = cosine_distance,
) -> np.ndarray:
    if matrix.shape[0] < 2:
        return np.zeros(0, dtype=np.float64)
    return np.asarray(
        [metric(matrix[i], matrix[i + 1]) for i in range(matrix.shape[0] - 1)],
        dtype=np.float64,
    )


def mad_threshold(values: np.ndarray, k: float, floor: float) -> float:
    """Robust peak threshold: median + k * MAD, never below ``floor``."""
    if values.size == 0:
        return floor
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    scaled = 1.4826 * mad
    if scaled < 1e-6:
        return max(floor, median + 0.05)
    return max(floor, median + k * scaled)


def knee_threshold(values: np.ndarray, floor: float, min_gap: float = 0.45) -> float:
    """Raise the floor into the first small-vs-large gap, if one exists.

    Only the jump that leaves the below-floor cluster is used. A later
    giant gap (one author pair much farther than another) is ignored, so
    a three-author document does not lose its weaker cut.
    """
    if values.size == 0:
        return floor
    order = np.sort(values.astype(float))
    if order.size == 1:
        return floor
    gaps = np.diff(order)
    for i, gap in enumerate(gaps):
        low = float(order[i])
        high = float(order[i + 1])
        if gap >= min_gap and low < floor <= high:
            return max(floor, 0.5 * (low + high))
    return floor


def agglomerative_labels(
    matrix: np.ndarray,
    threshold: float,
    metric: Callable[[np.ndarray, np.ndarray], float] = cosine_distance,
) -> list[int]:
    """Average-linkage clustering, cut at ``threshold``."""
    n = matrix.shape[0]
    if n == 0:
        return []
    if n == 1:
        return [0]

    clusters: list[list[int]] = [[i] for i in range(n)]

    def average_distance(a: Sequence[int], b: Sequence[int]) -> float:
        total = 0.0
        count = 0
        for i in a:
            for j in b:
                total += metric(matrix[i], matrix[j])
                count += 1
        return total / count if count else 1.0

    active = list(range(n))
    while len(active) > 1:
        best = float("inf")
        pair = (-1, -1)
        for i, ci in enumerate(active):
            for cj in active[i + 1 :]:
                dist = average_distance(clusters[ci], clusters[cj])
                if dist < best:
                    best = dist
                    pair = (ci, cj)
        if best > threshold:
            break
        left, right = pair
        clusters[left] = clusters[left] + clusters[right]
        clusters[right] = []
        active.remove(right)

    labels = [0] * n
    for new_id, cluster_id in enumerate(active):
        for index in clusters[cluster_id]:
            labels[index] = new_id
    return labels


@dataclass
class DetectionResult:
    """Predictions for the three style-change subtasks."""

    multi_author: bool
    changes: list[bool]
    authors: list[int]
    distances: list[float]
    threshold: float
    paragraph_indices: list[int]
    notes: list[str] = field(default_factory=list)
    axes: list[list[float]] = field(default_factory=list)

    @property
    def change_positions(self) -> list[int]:
        """Paragraph index *after* which a change is predicted (0-based)."""
        return [i for i, flag in enumerate(self.changes) if flag]

    def as_dict(self) -> dict[str, object]:
        return {
            "multi_author": self.multi_author,
            "changes": self.changes,
            "authors": self.authors,
            "distances": self.distances,
            "threshold": self.threshold,
            "paragraph_indices": self.paragraph_indices,
            "change_positions": self.change_positions,
            "notes": self.notes,
            "axes": self.axes,
        }


class StyleChangeDetector:
    """Detect changes as jumps in a 4-D style space."""

    def __init__(
        self,
        extractor: FeatureExtractor | None = None,
        distance_floor: float = 0.75,
        mad_k: float = 1.6,
        min_words: int = 8,
        min_gap: float = 0.45,
    ) -> None:
        self.extractor = extractor or FeatureExtractor(min_words=min_words)
        self.distance_floor = distance_floor
        self.mad_k = mad_k
        self.min_gap = min_gap

    def detect_table(self, table: FeatureTable) -> DetectionResult:
        notes: list[str] = []
        n = table.matrix.shape[0]
        indices = list(table.paragraph_indices)
        if n == 0:
            return DetectionResult(False, [], [], [], self.distance_floor, [], ["empty document"])
        if n == 1:
            return DetectionResult(False, [], [0], [], self.distance_floor, indices, ["single paragraph"])

        axes = style_axes(table)
        notes.append("distance computed in 4-D style space (formality, address, rhythm, procedure)")
        distances = adjacent_distances(axes, metric=euclidean_distance)
        threshold = knee_threshold(distances, self.distance_floor, min_gap=self.min_gap)
        changes = [float(dist) >= threshold for dist in distances]

        block_authors = [0]
        next_id = 0
        for changed in changes:
            if changed:
                next_id += 1
            block_authors.append(next_id)

        cluster_authors = agglomerative_labels(axes, threshold, metric=euclidean_distance)
        n_blocks = len(set(block_authors))
        n_clusters = len(set(cluster_authors))
        if any(changes) and 1 < n_clusters < n_blocks:
            authors = cluster_authors
            notes.append("clustering reused an earlier author id (returning style)")
        elif any(changes):
            authors = block_authors
        elif n_clusters > 1:
            authors = cluster_authors
            notes.append("clustering split authors without an adjacent peak")
        else:
            authors = block_authors
        multi = any(changes) or len(set(authors)) > 1
        if any(changes) and len(set(authors)) == 1:
            notes.append("adjacent peak present but clustering collapsed to one author")
            authors = block_authors
            multi = True

        return DetectionResult(
            multi_author=multi,
            changes=changes,
            authors=authors,
            distances=[float(x) for x in distances],
            threshold=threshold,
            paragraph_indices=indices,
            notes=notes,
            axes=[[float(x) for x in row] for row in axes],
        )

    def detect_document(self, document: Document) -> tuple[FeatureTable, DetectionResult]:
        table = self.extractor.extract_document(document)
        return table, self.detect_table(table)

    def detect_text(self, text: str, source: str | None = None) -> tuple[Document, FeatureTable, DetectionResult]:
        document = split_paragraphs(text, source=source)
        table, result = self.detect_document(document)
        return document, table, result


def detect_style_changes(text: str, **kwargs: object) -> DetectionResult:
    """Convenience wrapper around :class:`StyleChangeDetector`."""
    detector_keys = {"distance_floor", "mad_k", "min_words", "min_gap"}
    detector_kwargs = {key: kwargs[key] for key in detector_keys if key in kwargs}
    detector = StyleChangeDetector(**detector_kwargs)  # type: ignore[arg-type]
    _document, _table, result = detector.detect_text(text)
    return result
