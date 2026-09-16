"""Error taxonomy for a predicted `changes` array.

Exam answers are stronger when a miss is named. The labels are
heuristic, not a second model:

* topic_confound — large content-word shift, modest function-word shift
* short_unit_noise — one side has very few tokens
* register_only — function-word / contraction jump without a topic jump
* threshold_near_miss — score sits close to the cut
* single_author_drift — false alarm inside a no-change document
* genuine_hit / genuine_stay — agreement with gold
"""

from __future__ import annotations

from dataclasses import dataclass

from .features import FeatureTable
from .lexicon import FUNCTION_WORDS
from .pairwise import ScoreBreakdown, breakdown, window_pair, window_table
from .tokenize import words


CONTENT_HINT = frozenset(FUNCTION_WORDS)


@dataclass(frozen=True)
class PairExplanation:
    index: int
    gold: int | None
    pred: int
    score: float
    label: str
    note: str
    parts: ScoreBreakdown


def _content_shift(left: str, right: str) -> float:
    def content(text: str) -> set[str]:
        return {w for w in words(text) if w not in CONTENT_HINT and len(w) > 3}

    a, b = content(left), content(right)
    if not a or not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return 1.0 - (inter / union if union else 0.0)


def explain_pair(
    table: FeatureTable,
    index: int,
    *,
    pred: int,
    gold: int | None,
    threshold: float,
) -> PairExplanation:
    left, right = window_pair(table, index)
    parts = breakdown(left, right, window_table(table))
    topic = _content_shift(left.text, right.text)
    n_left = left.scalars["n_words"]
    n_right = right.scalars["n_words"]

    if gold is None:
        label = "unlabelled"
        note = "No gold label; score only."
    elif gold == pred == 1:
        label = "genuine_hit"
        note = "Predicted change matches gold."
    elif gold == pred == 0:
        label = "genuine_stay"
        note = "Predicted stay matches gold."
    elif gold == 0 and pred == 1:
        if topic >= 0.75 and parts.function_words < 0.45:
            label = "topic_confound"
            note = "Content nouns jumped harder than function words."
        elif min(n_left, n_right) <= 6:
            label = "short_unit_noise"
            note = "A very short unit made the distance unstable."
        else:
            label = "single_author_drift"
            note = "False alarm: score cleared the cut without a labelled seam."
    else:
        if abs(parts.combined - threshold) < 0.06:
            label = "threshold_near_miss"
            note = "Gold seam, but the blended score sat near the cut."
        elif parts.function_words >= 0.45 or parts.delta >= 0.8:
            label = "register_only"
            note = "Register moved; the blended cut still missed it."
        elif min(n_left, n_right) <= 6:
            label = "short_unit_noise"
            note = "Gold seam on a short unit; variance ate the signal."
        else:
            label = "threshold_near_miss"
            note = "Gold seam missed; inspect function-word vs topic channels."

    return PairExplanation(
        index=index,
        gold=gold,
        pred=pred,
        score=parts.combined,
        label=label,
        note=note,
        parts=parts,
    )


def explain_document(
    table: FeatureTable,
    pred: list[int],
    gold: list[int] | None,
    *,
    threshold: float,
) -> list[PairExplanation]:
    n = len(table) - 1
    rows = []
    for i in range(n):
        g = gold[i] if gold is not None else None
        rows.append(
            explain_pair(table, i, pred=pred[i], gold=g, threshold=threshold)
        )
    return rows
