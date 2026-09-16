"""Adjacent-unit detector I can defend in twenty minutes.

The pair score is a weighted mix of three families:

1. character 3-gram cosine distance (morphology + punctuation)
2. function-word L1 (Mosteller–Wallace closed class)
3. a 16-D stylometric L2 (length, pronouns, hedges, imperatives)

CUSUM slope reversals on sentence length get a small bonus so a clean
short→long cut is not missed when n-grams are still mixed. The threshold
is a gap heuristic with an absolute floor: if the largest pair is still
quiet, the document is single-author.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev

from examscd.cusum import cusum_points, sentence_lengths
from examscd.features import function_word_l1, style_l2, style_vector
from examscd.ngrams import char_ngram_distance
from examscd.tokenize import split_units

ABS_MIN = 0.18
GAP_MIN = 0.07
K_SIGMA = 0.55
NGRAM_WEIGHT = 0.42
FUNC_WEIGHT = 0.28
STYLE_WEIGHT = 0.20
LENGTH_WEIGHT = 0.10
CUSUM_BONUS = 0.06
RETURN_MATCH = 0.16


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
    change: int


@dataclass
class Detection:
    units: list[str]
    granularity: str
    distances: list[float]
    threshold: float
    changes: list[int]
    authors: list[int]
    pairs: list[PairScore] = field(default_factory=list)
    cusum_hits: list[int] = field(default_factory=list)

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
    # function-word L1 lives in [0, 2]; compress toward [0, 1].
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
    """Return a cut threshold. Values below ``abs_min`` never fire."""
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


def assign_authors(units: list[str], changes: list[int]) -> list[int]:
    """Sequential author ids with a cheap return-author check.

    When a change fires, compare the new unit to each previous author
    centroid in the 16-D style space. If it is close enough, reuse that
    id; otherwise mint a new one. This is Task-2 flavoured, not a
    clustering paper.
    """
    if not units:
        return []
    authors = [1]
    centroids = {1: style_vector(units[0])}
    counts = {1: 1}
    next_id = 2
    for idx, unit in enumerate(units[1:], start=1):
        changed = changes[idx - 1] if idx - 1 < len(changes) else 0
        vec = style_vector(unit)
        if not changed:
            aid = authors[-1]
            authors.append(aid)
        else:
            best_id = None
            best_dist = None
            for aid, centroid in centroids.items():
                dist = sum((a - b) ** 2 for a, b in zip(vec, centroid, strict=True)) ** 0.5
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_id = aid
            if best_id is not None and best_dist is not None and best_dist <= RETURN_MATCH:
                authors.append(best_id)
            else:
                authors.append(next_id)
                next_id += 1
                aid = authors[-1]
        aid = authors[-1]
        old = centroids.get(aid, [0.0] * len(vec))
        n = counts.get(aid, 0)
        centroids[aid] = [(old_i * n + new_i) / (n + 1) for old_i, new_i in zip(old, vec, strict=True)]
        counts[aid] = n + 1
    return authors


def detect_document(
    text: str,
    granularity: str = "sentence",
    abs_min: float = ABS_MIN,
    gap_min: float = GAP_MIN,
    k_sigma: float = K_SIGMA,
) -> Detection:
    units = split_units(text, granularity)
    if len(units) < 2:
        return Detection(
            units=units,
            granularity=granularity,
            distances=[],
            threshold=abs_min,
            changes=[],
            authors=[1] if units else [],
            pairs=[],
            cusum_hits=[],
        )

    raw_pairs = [pair_distance(units[i], units[i + 1]) for i in range(len(units) - 1)]
    distances = [p["combined"] for p in raw_pairs]

    cusum_hits: list[int] = []
    if granularity.startswith("s"):
        lengths = sentence_lengths("\n".join(units) if all("\n" not in u for u in units) else " ".join(units))
        if len(lengths) != len(units):
            lengths = [len(u.split()) for u in units]
        cusum_hits = cusum_points(lengths)

    boosted = list(distances)
    for hit in cusum_hits:
        if 0 <= hit < len(boosted):
            boosted[hit] = boosted[hit] + CUSUM_BONUS

    threshold = threshold_distances(boosted, abs_min=abs_min, gap_min=gap_min, k_sigma=k_sigma)
    changes = [1 if d >= threshold else 0 for d in boosted]
    authors = assign_authors(units, changes)

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
                combined=boosted[i],
                cusum_hit=i in cusum_hits,
                change=changes[i],
            )
        )
    return Detection(
        units=units,
        granularity=granularity,
        distances=boosted,
        threshold=threshold,
        changes=changes,
        authors=authors,
        pairs=pairs,
        cusum_hits=cusum_hits,
    )
