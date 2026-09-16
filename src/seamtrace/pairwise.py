"""Turn two unit feature rows into a single style-change score.

The score is a weighted blend:

* function-word cosine distance (topic-resistant)
* character-trigram cosine distance (orthography / punctuation)
* mean absolute difference of selected scalars
* Burrows' Delta on the same function-word space

Weights are exam-tunable. Defaults put most mass on function words
and trigrams so a topic jump without a register jump scores lower
than a register jump on the same topic.
"""

from __future__ import annotations

from dataclasses import dataclass

from .delta import burrows_delta
from .features import SCALAR_NAMES, FeatureTable, UnitFeatures
from .vector import cosine_distance, sparse_cosine_distance

# Scalars that are rates, not raw counts. Counts would dominate.
RATE_SCALARS = tuple(
    name
    for name in SCALAR_NAMES
    if name
    not in {
        "n_chars",
        "n_words",
    }
)


@dataclass(frozen=True)
class ScoreBreakdown:
    function_words: float
    trigrams: float
    scalars: float
    delta: float
    combined: float


DEFAULT_WEIGHTS = {
    "function_words": 0.40,
    "trigrams": 0.25,
    "scalars": 0.15,
    "delta": 0.20,
}


def _scalar_distance(left: UnitFeatures, right: UnitFeatures) -> float:
    diffs = [
        abs(left.scalars[name] - right.scalars[name]) for name in RATE_SCALARS
    ]
    # Bound typical rate diffs (0-1) so a single binary flag cannot explode.
    return sum(min(d, 1.0) for d in diffs) / len(diffs)


def breakdown(
    left: UnitFeatures,
    right: UnitFeatures,
    table: FeatureTable,
    weights: dict[str, float] | None = None,
) -> ScoreBreakdown:
    w = weights or DEFAULT_WEIGHTS
    fw = cosine_distance(left.function_words, right.function_words)
    tri = sparse_cosine_distance(left.trigrams, right.trigrams)
    sc = _scalar_distance(left, right)
    de = burrows_delta(left, right, table)
    combined = (
        w["function_words"] * fw
        + w["trigrams"] * tri
        + w["scalars"] * sc
        + w["delta"] * de
    )
    return ScoreBreakdown(
        function_words=fw,
        trigrams=tri,
        scalars=sc,
        delta=de,
        combined=combined,
    )


def pair_score(
    left: UnitFeatures,
    right: UnitFeatures,
    table: FeatureTable,
    weights: dict[str, float] | None = None,
) -> float:
    return breakdown(left, right, table, weights).combined


def score_document(
    table: FeatureTable, weights: dict[str, float] | None = None
) -> list[ScoreBreakdown]:
    return [
        breakdown(table.units[i], table.units[i + 1], table, weights)
        for i in range(len(table) - 1)
    ]
