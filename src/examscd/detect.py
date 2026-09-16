"""Cue-sheet detector I can defend in twenty minutes.

Adjacent short sentences share almost no character 3-grams even when
they are the same writer. The decision rule is therefore:

1. Score each unit on the closed cue sheet (slang, imperative, formal,
   notes, we-academic, one-academic, academic, personal, lab).
2. Assign a label. Stick across one-unit flickers.
3. Emit a change when the label changes.
4. Reuse an author id when a label returns.

Pair distances (character 3-grams, function-word L1, 16-D style, length)
and CUSUM on word count stay in the report so I can show *why* a cut
looks like a cut. They are not the thing that flips the bit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev

from examscd.cues import CueScore, adjacent_same, label_units, return_same
from examscd.cusum import cusum_points
from examscd.features import function_word_l1, style_l2
from examscd.ngrams import char_ngram_distance
from examscd.tokenize import split_units

ABS_MIN = 0.18
GAP_MIN = 0.07
K_SIGMA = 0.55
NGRAM_WEIGHT = 0.42
FUNC_WEIGHT = 0.28
STYLE_WEIGHT = 0.20
LENGTH_WEIGHT = 0.10


@dataclass
class PairScore:
    index: int
    left: str
    right: str
    ngram: float
    function_l1: float
    style_l2: float
    length_jump: float
    combined: float
    cusum_hit: bool
    left_label: str
    right_label: str
    change: int


@dataclass
class Detection:
    units: list[str]
    granularity: str
    labels: list[str]
    distances: list[float]
    threshold: float
    changes: list[int]
    authors: list[int]
    pairs: list[PairScore] = field(default_factory=list)
    cusum_hits: list[int] = field(default_factory=list)
    cue_rows: list[CueScore] = field(default_factory=list)

    @property
    def multi_author(self) -> bool:
        return any(self.changes)


def _length_jump(left: str, right: str) -> float:
    a = max(len(left.split()), 1)
    b = max(len(right.split()), 1)
    return abs(a - b) / max(a, b)


def pair_distance(left: str, right: str) -> dict[str, float]:
    ngram = char_ngram_distance(left, right, n=3)
    func = function_word_l1(left, right)
    func_n = min(func / 1.4, 1.2)
    style = min(style_l2(left, right) / 1.1, 1.2)
    length = _length_jump(left, right)
    combined = (
        NGRAM_WEIGHT * ngram
        + FUNC_WEIGHT * func_n
        + STYLE_WEIGHT * style
        + LENGTH_WEIGHT * length
    )
    return {
        "ngram": ngram,
        "function_l1": func,
        "style_l2": style,
        "length_jump": length,
        "combined": combined,
    }


def threshold_distances(
    distances: list[float],
    abs_min: float = ABS_MIN,
    gap_min: float = GAP_MIN,
    k_sigma: float = K_SIGMA,
) -> float:
    """Kept for the compare-table baselines. Not the cue-sheet decision."""
    if not distances:
        return abs_min
    peak = max(distances)
    if peak < abs_min:
        return abs_min
    mu = mean(distances)
    sd = pstdev(distances) if len(distances) > 1 else 0.0
    sigma_thr = max(abs_min, mu + k_sigma * sd)
    ranked = sorted(distances)
    best_gap = 0.0
    gap_thr = sigma_thr
    for lo, hi in zip(ranked, ranked[1:]):
        gap = hi - lo
        if gap > best_gap and hi >= abs_min:
            best_gap = gap
            gap_thr = (lo + hi) / 2.0
    if best_gap >= gap_min:
        return max(abs_min, min(sigma_thr, gap_thr))
    return sigma_thr


def authors_from_labels(labels: list[str]) -> list[int]:
    """Walk left to right. Compatible neighbours keep the id; returning labels reuse."""
    if not labels:
        return []
    authors = [1]
    remembered: list[tuple[str, int]] = [(labels[0], 1)]
    next_id = 2
    for label in labels[1:]:
        prev_label, prev_id = remembered[-1][0], authors[-1]
        if adjacent_same(prev_label, label):
            authors.append(prev_id)
            remembered.append((label, prev_id))
            continue
        reused = None
        for old_label, old_id in reversed(remembered):
            if return_same(old_label, label):
                reused = old_id
                break
        if reused is None:
            reused = next_id
            next_id += 1
        authors.append(reused)
        remembered.append((label, reused))
    return authors


def detect_document(
    text: str,
    granularity: str = "sentence",
    abs_min: float = ABS_MIN,
    gap_min: float = GAP_MIN,
    k_sigma: float = K_SIGMA,
) -> Detection:
    del abs_min, gap_min, k_sigma
    units = split_units(text, granularity)
    if not units:
        return Detection(
            units=[],
            granularity=granularity,
            labels=[],
            distances=[],
            threshold=0.0,
            changes=[],
            authors=[],
        )
    if len(units) == 1:
        cues = label_units(units)
        return Detection(
            units=units,
            granularity=granularity,
            labels=[cues[0].label],
            distances=[],
            threshold=0.0,
            changes=[],
            authors=[1],
            cue_rows=cues,
        )

    cues = label_units(units)
    labels = [row.label for row in cues]
    authors = authors_from_labels(labels)
    changes = [0 if authors[i] == authors[i + 1] else 1 for i in range(len(units) - 1)]

    raw_pairs = [pair_distance(units[i], units[i + 1]) for i in range(len(units) - 1)]
    distances = [p["combined"] for p in raw_pairs]
    lengths = [len(u.split()) for u in units]
    cusum_hits = cusum_points(lengths) if granularity.startswith("s") else []

    pairs = []
    for i, raw in enumerate(raw_pairs):
        pairs.append(
            PairScore(
                index=i,
                left=units[i],
                right=units[i + 1],
                ngram=raw["ngram"],
                function_l1=raw["function_l1"],
                style_l2=raw["style_l2"],
                length_jump=raw["length_jump"],
                combined=raw["combined"],
                cusum_hit=i in cusum_hits,
                left_label=labels[i],
                right_label=labels[i + 1],
                change=changes[i],
            )
        )
    return Detection(
        units=units,
        granularity=granularity,
        labels=labels,
        distances=distances,
        threshold=0.0,
        changes=changes,
        authors=authors,
        pairs=pairs,
        cusum_hits=cusum_hits,
        cue_rows=cues,
    )
