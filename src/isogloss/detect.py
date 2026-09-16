"""Bundle detector: a hinge fires when several feature-maps agree.

For each closed-class channel f we draw the adjacent jump

    z_{i,f} = (x_{i,f} - x_{i+1,f}) / (s_f + ε)

and mark an isogloss at i when |z_{i,f}| is both loud in absolute
terms and near the loudest jump that channel makes in this file:

    mark_{i,f} = 1[ |z_{i,f}| ≥ max(ζ, ρ · max_j |z_{j,f}| ) ]

The hinge fires when at least k channels mark it. A single screaming
feature (digits, one hedge) is a wrinkle. A bundle is a change of hand.

Nouns never enter x. Window is 1: this is a local dialect boundary,
not a global mean-shift saw.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from statistics import pstdev
from typing import Iterable

from .features import CHANNELS, FeatureRow, extract_many, matrix
from .io import Problem, read_problem
from .text import split_units

DEFAULT_ZETA = 0.90
DEFAULT_RHO = 0.70
DEFAULT_K = 3
EPS = 1e-6


@dataclass(frozen=True)
class ChannelMark:
    name: str
    z: float
    marked: bool


@dataclass
class HingeView:
    index: int
    votes: int
    max_abs_z: float
    marks: list[ChannelMark]
    fires: bool
    reason: str

    def top_channels(self, n: int = 4) -> list[ChannelMark]:
        return sorted(self.marks, key=lambda m: abs(m.z), reverse=True)[:n]


@dataclass
class Detection:
    units: list[str]
    features: list[FeatureRow]
    changes: list[int]
    hinges: list[HingeView]
    zeta: float = DEFAULT_ZETA
    rho: float = DEFAULT_RHO
    min_votes: int = DEFAULT_K

    @property
    def authors_guess(self) -> int:
        return 1 + sum(self.changes)

    def label_at(self, hinge: int) -> str:
        if hinge < 0 or hinge >= len(self.changes):
            raise IndexError(hinge)
        return "CHANGE" if self.changes[hinge] else "same"


def _column_stds(rows: list[list[float]]) -> list[float]:
    if not rows:
        return []
    d = len(rows[0])
    stds: list[float] = []
    for j in range(d):
        col = [row[j] for row in rows]
        stds.append(pstdev(col) if len(col) > 1 else 0.0)
    return stds


def _adjacent_z(rows: list[list[float]]) -> list[list[float]]:
    """z-jumps between consecutive units. Shape: (n-1) x d."""
    if len(rows) < 2:
        return []
    stds = _column_stds(rows)
    out: list[list[float]] = []
    for i in range(len(rows) - 1):
        jump = []
        for j, (a, b) in enumerate(zip(rows[i], rows[i + 1], strict=True)):
            jump.append((a - b) / (stds[j] + EPS))
        out.append(jump)
    return out


def _peak_abs(column: Iterable[float]) -> float:
    values = [abs(x) for x in column]
    return max(values) if values else 0.0


def _reason(votes: int, max_abs: float, min_votes: int, zeta: float) -> str:
    if votes >= min_votes and max_abs >= zeta:
        return "bundle"
    if votes >= min_votes:
        return "bundle-quiet"
    return ""


def inspect_hinges(
    features: list[FeatureRow],
    zeta: float = DEFAULT_ZETA,
    rho: float = DEFAULT_RHO,
    min_votes: int = DEFAULT_K,
) -> list[HingeView]:
    rows = matrix(features)
    z = _adjacent_z(rows)
    if not z:
        return []
    d = len(CHANNELS)
    peaks = [_peak_abs(col[j] for col in z) for j in range(d)]
    views: list[HingeView] = []
    for i, jump in enumerate(z):
        marks: list[ChannelMark] = []
        votes = 0
        for j, name in enumerate(CHANNELS):
            abs_z = abs(jump[j])
            threshold = max(zeta, rho * peaks[j])
            marked = abs_z >= threshold and abs_z >= zeta
            marks.append(ChannelMark(name=name, z=jump[j], marked=marked))
            if marked:
                votes += 1
        max_abs = max(abs(v) for v in jump)
        fires = votes >= min_votes
        views.append(
            HingeView(
                index=i,
                votes=votes,
                max_abs_z=max_abs,
                marks=marks,
                fires=fires,
                reason=_reason(votes, max_abs, min_votes, zeta),
            )
        )
    return views


def detect_paragraphs(
    units: list[str],
    zeta: float = DEFAULT_ZETA,
    rho: float = DEFAULT_RHO,
    min_votes: int = DEFAULT_K,
) -> Detection:
    features = extract_many(units)
    hinges = inspect_hinges(features, zeta=zeta, rho=rho, min_votes=min_votes)
    changes = [1 if view.fires else 0 for view in hinges]
    return Detection(
        units=list(units),
        features=features,
        changes=changes,
        hinges=hinges,
        zeta=zeta,
        rho=rho,
        min_votes=min_votes,
    )


def detect_text(
    text: str,
    zeta: float = DEFAULT_ZETA,
    rho: float = DEFAULT_RHO,
    min_votes: int = DEFAULT_K,
) -> Detection:
    return detect_paragraphs(split_units(text), zeta=zeta, rho=rho, min_votes=min_votes)


def detect_problem(
    problem: Problem | Path | str,
    zeta: float = DEFAULT_ZETA,
    rho: float = DEFAULT_RHO,
    min_votes: int = DEFAULT_K,
) -> Detection:
    if not isinstance(problem, Problem):
        problem = read_problem(problem)
    return detect_paragraphs(problem.units, zeta=zeta, rho=rho, min_votes=min_votes)
