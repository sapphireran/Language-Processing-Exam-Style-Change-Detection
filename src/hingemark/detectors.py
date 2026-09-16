"""Binary decisions on a hinge-score series."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .pairwise import Hinge

# Default cut is a study-set number, not a PAN claim. Recalibrate with
# `hingemark calibrate` after you add documents.
DEFAULT_THRESHOLD = 0.30
DEFAULT_ADAPTIVE_K = 0.75
DEFAULT_ADAPTIVE_FLOOR = 0.22
DEFAULT_MAD_FLOOR = 0.05


@dataclass(frozen=True)
class DetectorResult:
    name: str
    changes: tuple[int, ...]
    scores: tuple[float, ...]
    threshold: float | None = None


def threshold_detect(
    hinges: Sequence[Hinge],
    threshold: float = DEFAULT_THRESHOLD,
) -> DetectorResult:
    scores = tuple(h.blend for h in hinges)
    changes = tuple(1 if s >= threshold else 0 for s in scores)
    return DetectorResult(
        name="threshold",
        changes=changes,
        scores=scores,
        threshold=threshold,
    )


def adaptive_detect(
    hinges: Sequence[Hinge],
    k: float = DEFAULT_ADAPTIVE_K,
) -> DetectorResult:
    """Fire when a hinge sits above median + k * MAD and an absolute floor.

    A single-author control has a tight score cloud, so the adaptive cut
    stays quiet. A two-author document with one loud hinge pulls the
    median down and the loud hinge over the cut.
    """
    scores = tuple(h.blend for h in hinges)
    if not scores:
        return DetectorResult(name="adaptive", changes=(), scores=())
    ordered = sorted(scores)
    mid = _median(ordered)
    mad = _median([abs(s - mid) for s in ordered])
    cut = max(DEFAULT_ADAPTIVE_FLOOR, mid + k * max(mad, DEFAULT_MAD_FLOOR))
    changes = tuple(1 if s >= cut else 0 for s in scores)
    return DetectorResult(
        name="adaptive",
        changes=changes,
        scores=scores,
        threshold=cut,
    )


def ensemble_detect(
    hinges: Sequence[Hinge],
    threshold: float = DEFAULT_THRESHOLD,
    k: float = DEFAULT_ADAPTIVE_K,
) -> DetectorResult:
    """Union of threshold and adaptive: recall-leaning study detector."""
    fixed = threshold_detect(hinges, threshold=threshold)
    adapt = adaptive_detect(hinges, k=k)
    changes = tuple(1 if a or b else 0 for a, b in zip(fixed.changes, adapt.changes))
    return DetectorResult(
        name="ensemble",
        changes=changes,
        scores=fixed.scores,
        threshold=threshold,
    )


def never_change(hinges: Sequence[Hinge]) -> DetectorResult:
    scores = tuple(h.blend for h in hinges)
    return DetectorResult(name="never", changes=tuple(0 for _ in scores), scores=scores)


def always_change(hinges: Sequence[Hinge]) -> DetectorResult:
    scores = tuple(h.blend for h in hinges)
    return DetectorResult(name="always", changes=tuple(1 for _ in scores), scores=scores)


def _median(ordered: Sequence[float]) -> float:
    n = len(ordered)
    if n == 0:
        return 0.0
    if n % 2:
        return ordered[n // 2]
    return 0.5 * (ordered[n // 2 - 1] + ordered[n // 2])
