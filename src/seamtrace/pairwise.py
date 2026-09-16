"""Turn two unit feature rows into a single style-change score.

The score is a weighted blend:

* function-word cosine distance (topic-resistant)
* character-trigram cosine distance (orthography / punctuation)
* mean absolute difference of selected scalars
* Burrows' Delta on the same function-word space

Weights are exam-tunable. Defaults put most mass on a small register
vector (person, contractions, sentence-initial case) plus function
words, so a topic jump without a register jump is not an automatic hit.
"""

from __future__ import annotations

from dataclasses import dataclass

from .delta import burrows_delta
from .features import FeatureTable, UnitFeatures, extract_unit_features
from .vector import cosine_distance, sparse_cosine_distance

# Style-leaning rates. TTR / hapax / digits are stored but not blended:
# they mostly measure length and topic, not register.
STYLE_SCALARS = (
    "first_person_rate",
    "second_person_rate",
    "contraction_rate",
    "hedge_rate",
    "modal_rate",
    "starts_lower",
    "long_word_rate",
    "avg_word_len",
)


@dataclass(frozen=True)
class ScoreBreakdown:
    function_words: float
    trigrams: float
    scalars: float
    delta: float
    combined: float


DEFAULT_WEIGHTS = {
    "function_words": 0.35,
    "trigrams": 0.10,
    "scalars": 0.40,
    "delta": 0.15,
}

# Consecutive units are short. Score the boundary using a left/right window
# so function-word estimates stop looking orthogonal by accident.
DEFAULT_WINDOW = 1


def _join_window(units: list[UnitFeatures], start: int, end: int) -> UnitFeatures:
    text = " ".join(unit.text for unit in units[start:end])
    return extract_unit_features(text)


def window_pair(table: FeatureTable, index: int, window: int = DEFAULT_WINDOW) -> tuple[UnitFeatures, UnitFeatures]:
    left_start = max(0, index - window + 1)
    right_end = min(len(table), index + 1 + window)
    left = _join_window(table.units, left_start, index + 1)
    right = _join_window(table.units, index + 1, right_end)
    return left, right


def _scalar_distance(left: UnitFeatures, right: UnitFeatures) -> float:
    diffs = []
    for name in STYLE_SCALARS:
        a = left.scalars[name]
        b = right.scalars[name]
        if name == "avg_word_len":
            diffs.append(min(abs(a - b) / 8.0, 1.0))
        else:
            diffs.append(min(abs(a - b), 1.0))
    return sum(diffs) / len(diffs)


def window_table(table: FeatureTable, window: int = DEFAULT_WINDOW) -> FeatureTable:
    sides: list[UnitFeatures] = []
    for i in range(max(0, len(table) - 1)):
        left, right = window_pair(table, i, window)
        sides.extend([left, right])
    return FeatureTable(sides) if sides else table


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
    raw_delta = burrows_delta(left, right, table)
    de = raw_delta / (1.0 + raw_delta)
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
    table: FeatureTable,
    weights: dict[str, float] | None = None,
    window: int = DEFAULT_WINDOW,
) -> list[ScoreBreakdown]:
    if len(table) < 2:
        return []
    ref = window_table(table, window)
    rows = []
    for i in range(len(table) - 1):
        left, right = window_pair(table, i, window)
        rows.append(breakdown(left, right, ref, weights))
    return rows
