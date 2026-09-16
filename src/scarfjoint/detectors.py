"""Pairwise detectors. Tuned on the bundled teaching corpus."""

from __future__ import annotations

from dataclasses import dataclass, field

from .distances import compression_ncd, cosine_distance, jensen_shannon, topic_distance
from .features import ParagraphFeatures, extract_features

# Weights and threshold were chosen by sweeping this lab's twelve documents.
# They are not a claim about PAN test data.
DEFAULT_WEIGHTS = {
    "function_cosine": 0.30,
    "formality": 0.35,
    "char_cosine": 0.15,
    "sentence": 0.10,
    "person": 0.10,
}
DEFAULT_THRESHOLD = 0.345


@dataclass(frozen=True)
class ChannelScores:
    function_cosine: float
    char_cosine: float
    formality_jump: float
    person_jump: float
    sentence_jump: float
    function_js: float
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

    def pair_scores(self, left: ParagraphFeatures, right: ParagraphFeatures) -> ChannelScores:
        function_cosine = cosine_distance(left.function_word_rel, right.function_word_rel)
        char_cosine = cosine_distance(left.char_trigrams, right.char_trigrams)
        formality_jump = abs(left.formality - right.formality)
        person_jump = abs(left.first_person_rate - right.first_person_rate) + abs(
            left.second_person_rate - right.second_person_rate
        )
        sentence_jump = abs(left.mean_sent_len - right.mean_sent_len) / 25.0
        function_js = jensen_shannon(left.function_word_rel, right.function_word_rel)
        ncd = compression_ncd(left.text, right.text)
        topic = topic_distance(left, right)
        combined = (
            self.weights["function_cosine"] * function_cosine
            + self.weights["formality"] * min(formality_jump, 1.5) / 1.5
            + self.weights["char_cosine"] * char_cosine
            + self.weights["sentence"] * min(sentence_jump, 1.0)
            + self.weights["person"] * min(person_jump * 5.0, 1.5) / 1.5
        )
        if self.use_topic:
            combined += self.topic_weight * topic
        return ChannelScores(
            function_cosine=function_cosine,
            char_cosine=char_cosine,
            formality_jump=formality_jump,
            person_jump=person_jump,
            sentence_jump=sentence_jump,
            function_js=function_js,
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
        boundaries: list[DetectedBoundary] = []
        changes: list[int] = []
        for i in range(len(feats) - 1):
            scores = self.pair_scores(feats[i], feats[i + 1])
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
            "topic channel is diagnostic only"
            if not self.use_topic
            else "topic channel is voting (leakage mode)",
        ]
        return Detection(
            paragraphs=paras,
            features=feats,
            boundaries=boundaries,
            changes=changes,
            threshold=self.threshold,
            notes=notes,
        )


def _reasons(scores: ChannelScores, threshold: float, predicted: int) -> tuple[str, ...]:
    ranked = sorted(
        [
            ("function-word cosine", scores.function_cosine),
            ("formality jump", min(scores.formality_jump, 1.5) / 1.5),
            ("char 3-gram cosine", scores.char_cosine),
            ("sentence-length jump", min(scores.sentence_jump, 1.0)),
            ("person jump", min(scores.person_jump * 5.0, 1.5) / 1.5),
        ],
        key=lambda kv: kv[1],
        reverse=True,
    )
    head = [f"{name}={value:.3f}" for name, value in ranked[:3]]
    decision = "CHANGE" if predicted else "same-author"
    head.append(f"combined={scores.combined:.3f} vs {threshold:.3f} → {decision}")
    head.append(f"topic-distance={scores.topic:.3f} (not a vote)")
    return tuple(head)
