"""High-level detector: binary segmentation, then a cautious adjacent peak."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .changepoint import (
    DEFAULT_ADJ_ABS,
    DEFAULT_PENALTY,
    DEFAULT_RECURSE_PENALTY,
    adjacent_absolute,
    adjacent_scores,
    binary_segment,
    inspect_splits,
)
from .features import FeatureVector, extract_many
from .io import Problem, read_problem


@dataclass
class Detection:
    paragraphs: list[str]
    features: list[FeatureVector]
    changes: list[int]
    split_scores: list[float]
    adjacent: list[float]
    cut_reason: list[str] = field(default_factory=list)
    penalty: float = DEFAULT_PENALTY

    @property
    def authors_guess(self) -> int:
        return 1 + sum(self.changes)

    def label_at(self, hinge: int) -> str:
        if hinge < 0 or hinge >= len(self.changes):
            raise IndexError(hinge)
        return "CHANGE" if self.changes[hinge] else "same"


def detect_paragraphs(
    paragraphs: list[str],
    penalty: float = DEFAULT_PENALTY,
    recurse_penalty: float = DEFAULT_RECURSE_PENALTY,
    adj_abs: float = DEFAULT_ADJ_ABS,
    use_adjacent: bool = True,
) -> Detection:
    features = extract_many(paragraphs)
    n = len(paragraphs)
    changes = [0] * max(0, n - 1)
    reasons = [""] * max(0, n - 1)
    view = inspect_splits(features)
    cuts = set(
        binary_segment(features, penalty=penalty, recurse_penalty=recurse_penalty)
    )
    for i in cuts:
        if 0 <= i < len(changes):
            changes[i] = 1
            reasons[i] = "split"
    if use_adjacent:
        for i in adjacent_absolute(features, floor=adj_abs):
            if 0 <= i < len(changes) and not changes[i]:
                changes[i] = 1
                reasons[i] = "adjacent-floor"
    return Detection(
        paragraphs=list(paragraphs),
        features=features,
        changes=changes,
        split_scores=view.scores,
        adjacent=view.adjacent or adjacent_scores(features),
        cut_reason=reasons,
        penalty=penalty,
    )


def detect_document(text: str, **kwargs) -> Detection:
    from .text import split_paragraphs

    return detect_paragraphs(split_paragraphs(text), **kwargs)


def detect_path(path: str | Path, **kwargs) -> Detection:
    problem = read_problem(path)
    return detect_problem(problem, **kwargs)


def detect_problem(problem: Problem, **kwargs) -> Detection:
    return detect_paragraphs(problem.paragraphs, **kwargs)
