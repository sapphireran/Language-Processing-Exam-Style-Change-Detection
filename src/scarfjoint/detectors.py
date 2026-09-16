"""Pairwise and sequential detectors. Tuned on the bundled teaching corpus."""

from __future__ import annotations

from dataclasses import dataclass, field

from .distances import (
    burrows_delta,
    compression_ncd,
    cosine_distance,
    euclidean,
    jensen_shannon,
    topic_distance,
    zscore_rows,
)
from .features import ParagraphFeatures, extract_features

# Weights and threshold were chosen by sweeping this lab's twelve documents.
# They are not a claim about PAN test data.
DEFAULT_WEIGHTS = {
    "function_cosine": 0.28,
    "char_cosine": 0.22,
    "dense_euclidean": 0.18,
    "function_js": 0.14,
    "delta": 0.10,
    "ncd": 0.08,
}
DEFAULT_THRESHOLD = 0.42


@dataclass(frozen=True)
class ChannelScores:
    function_cosine: float
    char_cosine: float
    dense_euclidean: float
    function_js: float
    delta: float
    ncd: float
    topic: float
    combined: float


@dataclass(frozen=True)
class DetectedBoundary:
    index: int  # boundary after paragraph index (0-based left paragraph)
    scores: ChannelScores
    predicted: int
    reasons: tuple[str, ...]


@dataclass
class Detection:
    paragraphs: tuple[str, ...]
    features: list[ParagraphFeatures]
    boundaries: list[DetectedBoundary]
    changes: list[int]
    threshold: float
    notes: list[str] = field(default_factory=list)

    @property
    def n_authors_estimate(self) -> int:
        return 1 + sum(self.changes)


class ScarfDetector:
    """Intrinsic style-change detector: adjacent paragraphs only.

    The topic channel is computed and returned for teaching, but it does
    not vote. Easy PAN documents leak topic; hard ones do not. An oral
    answer that cannot say which channel is which is incomplete.
    """

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        weights: dict[str, float] | None = None,
        use_topic: bool = False,
        topic_weight: float = 0.25,
    ) -> None:
        self.threshold = threshold
        self.weights = dict(weights or DEFAULT_WEIGHTS)
        self.use_topic = use_topic
        self.topic_weight = topic_weight

    def featurize(self, paragraphs: list[str] | tuple[str, ...]) -> list[ParagraphFeatures]:
        return [extract_features(p) for p in paragraphs]

    def pair_scores(
        self,
        left: ParagraphFeatures,
        right: ParagraphFeatures,
        dense_left: tuple[float, ...],
        dense_right: tuple[float, ...],
        fw_scales: tuple[float, ...] | None,
    ) -> ChannelScores:
        function_cosine = cosine_distance(left.function_word_rel, right.function_word_rel)
        char_cosine = cosine_distance(left.char_trigrams, right.char_trigrams)
        dense_euclidean = euclidean(dense_left, dense_right)
        function_js = jensen_shannon(left.function_word_rel, right.function_word_rel)
        delta = burrows_delta(left.function_word_rel, right.function_word_rel, fw_scales)
        ncd = compression_ncd(left.text, right.text)
        topic = topic_distance(left, right)
        combined = (
            self.weights["function_cosine"] * function_cosine
            + self.weights["char_cosine"] * char_cosine
            + self.weights["dense_euclidean"] * min(dense_euclidean / 8.0, 1.5)
            + self.weights["function_js"] * min(function_js * 4.0, 1.5)
            + self.weights["delta"] * min(delta * 8.0, 1.5)
            + self.weights["ncd"] * ncd
        )
        if self.use_topic:
            combined += self.topic_weight * topic
        return ChannelScores(
            function_cosine=function_cosine,
            char_cosine=char_cosine,
            dense_euclidean=dense_euclidean,
            function_js=function_js,
            delta=delta,
            ncd=ncd,
            topic=topic,
            combined=combined,
        )

    def detect(self, paragraphs: list[str] | tuple[str, ...]) -> Detection:
        paras = tuple(p for p in paragraphs if p.strip())
        if len(paras) < 2:
            feats = self.featurize(paras)
            return Detection(
                paragraphs=paras,
                features=feats,
                boundaries=[],
                changes=[],
                threshold=self.threshold,
                notes=["fewer than two paragraphs; nothing to decide"],
            )
        feats = self.featurize(paras)
        dense_z = zscore_rows([f.dense for f in feats])
        fw_scales = _column_stds([f.function_word_rel for f in feats])
        boundaries: list[DetectedBoundary] = []
        changes: list[int] = []
        for i in range(len(feats) - 1):
            scores = self.pair_scores(
                feats[i],
                feats[i + 1],
                dense_z[i],
                dense_z[i + 1],
                fw_scales,
            )
            predicted = 1 if scores.combined >= self.threshold else 0
            reasons = _reasons(scores, self.threshold, predicted)
            boundaries.append(
                DetectedBoundary(
                    index=i,
                    scores=scores,
                    predicted=predicted,
                    reasons=reasons,
                )
            )
            changes.append(predicted)
        notes = [
            f"threshold={self.threshold:.3f}",
            "topic channel is diagnostic only" if not self.use_topic else "topic channel is voting (leakage mode)",
        ]
        return Detection(
            paragraphs=paras,
            features=feats,
            boundaries=boundaries,
            changes=changes,
            threshold=self.threshold,
            notes=notes,
        )


def _column_stds(rows: list[tuple[float, ...]]) -> tuple[float, ...]:
    if not rows:
        return ()
    dim = len(rows[0])
    n = len(rows)
    out = []
    for j in range(dim):
        col = [row[j] for row in rows]
        mean = sum(col) / n
        var = sum((x - mean) ** 2 for x in col) / n
        out.append(var**0.5 if var > 1e-12 else 1.0)
    return tuple(out)


def _reasons(scores: ChannelScores, threshold: float, predicted: int) -> tuple[str, ...]:
    ranked = sorted(
        [
            ("function-word cosine", scores.function_cosine),
            ("char 3-gram cosine", scores.char_cosine),
            ("dense euclidean", min(scores.dense_euclidean / 8.0, 1.5)),
            ("function-word JS", min(scores.function_js * 4.0, 1.5)),
            ("Burrows delta", min(scores.delta * 8.0, 1.5)),
            ("NCD", scores.ncd),
        ],
        key=lambda kv: kv[1],
        reverse=True,
    )
    head = [f"{name}={value:.3f}" for name, value in ranked[:3]]
    decision = "CHANGE" if predicted else "same-author"
    head.append(f"combined={scores.combined:.3f} vs {threshold:.3f} → {decision}")
    head.append(f"topic-distance={scores.topic:.3f} (not a vote)")
    return tuple(head)
