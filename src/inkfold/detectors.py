"""Fold scorers: prefix-suffix, local window, threshold, adaptive, ensemble."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .distance import score_cut
from .features import extract_register


@dataclass
class FoldScore:
    index: int  # boundary after unit ``index`` (1-based unit on the left)
    score: float
    channels: dict[str, float]
    mode: str


@dataclass
class Detection:
    changes: list[int]
    scores: list[FoldScore]
    authors: int
    threshold: float
    detector: str

    def as_truth(self) -> dict:
        return {
            "authors": self.authors,
            "changes": self.changes,
            "detector": self.detector,
            "threshold": self.threshold,
        }


def prefix_suffix_scores(units: Sequence[str]) -> list[FoldScore]:
    """Compare the whole left prefix to the right suffix at each cut.

    Useful as a picture for a *single* hinge. Misleading on a return
    author, where both sides of a true fold are mixed.
    """
    scores: list[FoldScore] = []
    n = len(units)
    for i in range(1, n):
        score, channels = score_cut(units[:i], units[i:])
        scores.append(FoldScore(index=i, score=score, channels=channels, mode="prefix_suffix"))
    return scores


def adjacent_scores(units: Sequence[str]) -> list[FoldScore]:
    """Pencil method: compare the unit on the left of the cut to the unit on the right."""
    scores: list[FoldScore] = []
    n = len(units)
    for i in range(1, n):
        score, channels = score_cut([units[i - 1]], [units[i]])
        scores.append(FoldScore(index=i, score=score, channels=channels, mode="adjacent"))
    return scores


def local_window_scores(units: Sequence[str], width: int = 2) -> list[FoldScore]:
    """Compare a left window to a right window around each cut."""
    scores: list[FoldScore] = []
    n = len(units)
    for i in range(1, n):
        left = units[max(0, i - width) : i]
        right = units[i : min(n, i + width)]
        score, channels = score_cut(left, right)
        scores.append(FoldScore(index=i, score=score, channels=channels, mode="local"))
    return scores


def hinge_scores(units: Sequence[str]) -> list[FoldScore]:
    """Default teaching score: 0.65 adjacent + 0.35 window-2.

    Adjacent is what you can count on paper. The two-unit window steadies
    a one-line chat fragment without turning into prefix-suffix.
    """
    adj = adjacent_scores(units)
    win = local_window_scores(units, width=2)
    out: list[FoldScore] = []
    for a, w in zip(adj, win):
        score = 0.65 * a.score + 0.35 * w.score
        channels = {k: 0.65 * a.channels[k] + 0.35 * w.channels[k] for k in a.channels}
        out.append(FoldScore(index=a.index, score=score, channels=channels, mode="hinge"))
    return out


def peak_picks(scores: Sequence[FoldScore], threshold: float, sure: float = 0.45) -> list[int]:
    """Fire a cut if it is a local max above ``threshold``, or simply loud.

    The sure-fold branch is what lets a three-voice collage fire every
    hinge even when the middle score is a little lower than its neighbours.
    Oral card: *a fold is a peak, unless the score is already undeniable.*
    """
    values = [s.score for s in scores]
    n = len(values)
    fires: list[int] = []
    for i, v in enumerate(values):
        if v < threshold:
            fires.append(0)
            continue
        if v >= sure:
            fires.append(1)
            continue
        left = values[i - 1] if i else v
        right = values[i + 1] if i + 1 < n else v
        fires.append(1 if v >= left and v >= right else 0)
    return fires


def _authors_from_changes(changes: Sequence[int], units: Sequence[str]) -> int:
    """Naive author count: 1 + number of folds.

    This *over-counts* a return author. That is intentional: the kiln-return
    document exists so the oral can ask why the formula is wrong.
    """
    if not units:
        return 0
    return 1 + sum(1 for c in changes if c)


def _apply_threshold(scores: Sequence[FoldScore], threshold: float) -> list[int]:
    return [1 if s.score >= threshold else 0 for s in scores]


class ThresholdDetector:
    """Fold if the blended prefix-suffix score is at least ``threshold``."""

    name = "threshold"

    def __init__(self, threshold: float = 0.30):
        self.threshold = threshold

    def detect(self, units: Sequence[str]) -> Detection:
        scores = hinge_scores(units)
        changes = peak_picks(scores, self.threshold)
        return Detection(
            changes=changes,
            scores=scores,
            authors=_authors_from_changes(changes, units),
            threshold=self.threshold,
            detector=self.name,
        )


class AdaptiveDetector:
    """Fold if score > median + k * MAD of the document's own scores."""

    name = "adaptive"

    def __init__(self, k: float = 0.85, floor: float = 0.22):
        self.k = k
        self.floor = floor

    def detect(self, units: Sequence[str]) -> Detection:
        scores = hinge_scores(units)
        values = [s.score for s in scores]
        thr = max(self.floor, _median(values) + self.k * _mad(values))
        changes = peak_picks(scores, thr)
        return Detection(
            changes=changes,
            scores=scores,
            authors=_authors_from_changes(changes, units),
            threshold=thr,
            detector=self.name,
        )


class EnsembleDetector:
    """Agree if threshold *or* adaptive fires, but require a register hint.

    The register hint (L1 >= ``register_floor``) is what keeps the river-style
    topic control quiet: function-word cosine can twitch when the topic
    changes, but the six-number vector should not.
    """

    name = "ensemble"

    def __init__(
        self,
        threshold: float = 0.30,
        k: float = 0.85,
        floor: float = 0.22,
        register_floor: float = 0.18,
    ):
        self.threshold = threshold
        self.k = k
        self.floor = floor
        self.register_floor = register_floor

    def detect(self, units: Sequence[str]) -> Detection:
        scores = hinge_scores(units)
        fixed = peak_picks(scores, self.threshold)
        values = [s.score for s in scores]
        adapt_thr = max(self.floor, _median(values) + self.k * _mad(values))
        adapt = peak_picks(scores, adapt_thr)
        changes = []
        for a, b, sc in zip(fixed, adapt, scores):
            register_ok = sc.channels.get("register_l1", 0.0) >= self.register_floor
            fire = (a or b) and register_ok
            changes.append(1 if fire else 0)
        return Detection(
            changes=changes,
            scores=scores,
            authors=_authors_from_changes(changes, units),
            threshold=self.threshold,
            detector=self.name,
        )


def default_detector() -> EnsembleDetector:
    return EnsembleDetector()


def _median(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    n = len(ys)
    mid = n // 2
    if n % 2:
        return ys[mid]
    return 0.5 * (ys[mid - 1] + ys[mid])


def _mad(xs: Sequence[float]) -> float:
    if not xs:
        return 0.0
    med = _median(xs)
    return _median([abs(x - med) for x in xs])


def never_fire(units: Sequence[str]) -> Detection:
    n = max(len(units) - 1, 0)
    scores = prefix_suffix_scores(units) if units else []
    return Detection(changes=[0] * n, scores=scores, authors=1 if units else 0, threshold=1.0, detector="never")


def always_fire(units: Sequence[str]) -> Detection:
    n = max(len(units) - 1, 0)
    scores = prefix_suffix_scores(units) if units else []
    return Detection(changes=[1] * n, scores=scores, authors=n + 1 if units else 0, threshold=0.0, detector="always")


def register_jump(units: Sequence[str]) -> list[float]:
    """Per-unit first-person rate, handy for a CUSUM sketch on the oral."""
    return [extract_register([u]).first_person for u in units]


@dataclass
class DetectorGrid:
    """Tiny grid used by scripts/grid_thresholds.py."""

    thresholds: list[float] = field(default_factory=lambda: [0.20, 0.25, 0.30, 0.35, 0.40])
