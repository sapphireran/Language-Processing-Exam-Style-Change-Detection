"""Binary seam detectors over pairwise scores.

All detectors emit a 0/1 list of length n_units - 1. That is the PAN
`changes` array. Thresholds are teaching knobs, not fitted models.
"""

from __future__ import annotations

from dataclasses import dataclass

from .features import FeatureTable
from .pairwise import ScoreBreakdown, score_document
from .vector import mean, pop_std


def _combined(rows: list[ScoreBreakdown]) -> list[float]:
    return [row.combined for row in rows]


@dataclass
class ThresholdDetector:
    """Flag a seam when the blended score is at least `threshold`."""

    threshold: float = 0.42
    name: str = "threshold"

    def predict(self, table: FeatureTable) -> list[int]:
        return [1 if row.combined >= self.threshold else 0 for row in score_document(table)]


@dataclass
class AdaptiveDetector:
    """Document-local threshold: mean + k * std of that document's scores.

    Useful when Easy documents have huge topic jumps and Hard documents
    sit in a narrower score band. The same k cannot be perfect on both;
    that is an exam point, not a bug.
    """

    k: float = 0.85
    floor: float = 0.22
    name: str = "adaptive"

    def predict(self, table: FeatureTable) -> list[int]:
        scores = _combined(score_document(table))
        if not scores:
            return []
        cut = max(self.floor, mean(scores) + self.k * pop_std(scores))
        return [1 if s >= cut else 0 for s in scores]


@dataclass
class EnsembleDetector:
    """Average threshold and adaptive votes. Tie -> change.

    The tie-breaks toward recall because missed seams are the usual
    exam failure mode on Hard documents.
    """

    threshold: float = 0.42
    k: float = 0.85
    name: str = "ensemble"

    def predict(self, table: FeatureTable) -> list[int]:
        fixed = ThresholdDetector(self.threshold).predict(table)
        adapt = AdaptiveDetector(self.k).predict(table)
        return [1 if (a + b) >= 1 else 0 for a, b in zip(fixed, adapt)]


def available_detectors() -> dict[str, object]:
    return {
        "threshold": ThresholdDetector(),
        "adaptive": AdaptiveDetector(),
        "ensemble": EnsembleDetector(),
    }
