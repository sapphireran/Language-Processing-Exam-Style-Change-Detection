"""Unsupervised ensemble for paragraph-level style-change flags.

The oral-exam story:

1. Build several weakly correlated *register* channels (formality,
   contractions, pronoun person, closed-class Delta).
2. Treat character n-grams as a weak extra vote only after subtracting
   the distance you already expect from short, different-content
   paragraphs. They leak topic.
3. Require either a strong single channel or two agreeing channels.
   Hard floors exist so a single-author letter with one slightly
   longer paragraph does not fire just because it is the local
   z-score outlier.

This is *not* how the 2023 PAN winners worked (they fine-tuned
DeBERTa). It is how you show you understand the classical pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .cusum import cusum_change_scores
from .delta import (
    char_ngram_distances,
    contraction_jumps,
    document_deltas,
    formality_jumps,
    marker_jumps,
    person_flag_jumps,
    pronoun_jumps,
    register_jumps,
    sentence_length_jumps,
    topic_jaccard,
)
from .features import ParagraphFeatures, extract_many
from .tokenize import split_paragraphs

# Hard floors — tuned on the bundled personal examples, not on PAN.
# Character n-gram floors sit high because short paragraphs about
# different *nouns* already have cosine distance ~0.6.
THRESHOLDS = {
    "formality": 0.22,
    "formality_strong": 0.40,
    "contraction": 0.050,
    "contraction_strong": 0.085,
    "person": 1.00,
    "person_strong": 2.00,
    "pronoun": 0.090,
    "pronoun_strong": 0.150,
    "register": 0.26,
    "register_strong": 0.46,
    "marker": 0.030,
    "marker_strong": 0.050,
    "delta": 0.90,
    "delta_strong": 1.40,
    "char": 0.82,
    "char_strong": 0.90,
    "sentlen": 0.80,
    "sentlen_strong": 1.10,
    "cusum": 1.80,
    "cusum_strong": 2.80,
}

VOTE_CHANNELS = (
    "formality",
    "contraction",
    "person",
    "pronoun",
    "register",
    "marker",
    "delta",
    "char",
    "sentlen",
    "cusum",
)


@dataclass(frozen=True)
class PairScore:
    index: int
    left_preview: str
    right_preview: str
    delta: float
    char: float
    formality: float
    sentlen: float
    contraction: float
    pronoun: float
    person: float
    register: float
    marker: float
    cusum: float
    topic: float
    votes: int
    strong: int
    change: int
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Detection:
    paragraphs: tuple[str, ...]
    features: tuple[ParagraphFeatures, ...]
    pairs: tuple[PairScore, ...]
    changes: tuple[int, ...]
    method: str = "ensemble"

    def as_dict(self) -> dict:
        return {
            "changes": list(self.changes),
            "method": self.method,
            "n_paragraphs": len(self.paragraphs),
            "pairs": [
                {
                    "index": p.index,
                    "change": p.change,
                    "votes": p.votes,
                    "strong": p.strong,
                    "delta": round(p.delta, 4),
                    "char": round(p.char, 4),
                    "formality": round(p.formality, 4),
                    "sentlen": round(p.sentlen, 4),
                    "contraction": round(p.contraction, 4),
                    "pronoun": round(p.pronoun, 4),
                    "person": round(p.person, 4),
                    "register": round(p.register, 4),
                    "marker": round(p.marker, 4),
                    "cusum": round(p.cusum, 4),
                    "topic": round(p.topic, 4),
                    "reasons": list(p.reasons),
                }
                for p in self.pairs
            ],
        }


def _preview(text: str, width: int = 72) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def _channel_votes(name: str, value: float) -> tuple[int, int, str | None]:
    floor = THRESHOLDS[name]
    strong = THRESHOLDS[f"{name}_strong"]
    if value >= strong:
        return 1, 1, f"{name}={value:.2f}≥{strong:.2f} (strong)"
    if value >= floor:
        return 1, 0, f"{name}={value:.2f}≥{floor:.2f}"
    return 0, 0, None


def score_pairs(features: Sequence[ParagraphFeatures]) -> list[PairScore]:
    n = len(features)
    if n < 2:
        return []
    channels = {
        "delta": document_deltas(features),
        "char": char_ngram_distances(features),
        "formality": formality_jumps(features),
        "sentlen": sentence_length_jumps(features),
        "contraction": contraction_jumps(features),
        "pronoun": pronoun_jumps(features),
        "person": person_flag_jumps(features),
        "register": register_jumps(features),
        "marker": marker_jumps(features),
        "cusum": cusum_change_scores(features),
    }
    topics = topic_jaccard(features)
    pairs: list[PairScore] = []
    for i in range(n - 1):
        votes = 0
        strong = 0
        reasons: list[str] = []
        for name in VOTE_CHANNELS:
            v, s, reason = _channel_votes(name, channels[name][i])
            votes += v
            strong += s
            if reason:
                reasons.append(reason)
        change = 1 if (strong >= 1 or votes >= 2) else 0
        pairs.append(
            PairScore(
                index=i,
                left_preview=_preview(features[i].text),
                right_preview=_preview(features[i + 1].text),
                delta=channels["delta"][i],
                char=channels["char"][i],
                formality=channels["formality"][i],
                sentlen=channels["sentlen"][i],
                contraction=channels["contraction"][i],
                pronoun=channels["pronoun"][i],
                person=channels["person"][i],
                register=channels["register"][i],
                marker=channels["marker"][i],
                cusum=channels["cusum"][i],
                topic=topics[i],
                votes=votes,
                strong=strong,
                change=change,
                reasons=tuple(reasons),
            )
        )
    return pairs


def detect_from_features(
    paragraphs: Sequence[str],
    features: Sequence[ParagraphFeatures],
    method: str = "ensemble",
) -> Detection:
    pairs = score_pairs(features)
    if method == "ensemble":
        changes = tuple(p.change for p in pairs)
    else:
        key = {
            "delta": "delta",
            "char": "char",
            "formality": "formality",
            "cusum": "cusum",
            "register": "register",
            "pronoun": "pronoun",
            "person": "person",
        }.get(method)
        if key is None:
            raise ValueError(f"unknown method {method!r}")
        adjusted: list[PairScore] = []
        changes_list: list[int] = []
        for pair in pairs:
            value = getattr(pair, key)
            change = 1 if value >= THRESHOLDS[key] else 0
            changes_list.append(change)
            adjusted.append(
                PairScore(
                    index=pair.index,
                    left_preview=pair.left_preview,
                    right_preview=pair.right_preview,
                    delta=pair.delta,
                    char=pair.char,
                    formality=pair.formality,
                    sentlen=pair.sentlen,
                    contraction=pair.contraction,
                    pronoun=pair.pronoun,
                    person=pair.person,
                    register=pair.register,
                    marker=pair.marker,
                    cusum=pair.cusum,
                    topic=pair.topic,
                    votes=pair.votes,
                    strong=pair.strong,
                    change=change,
                    reasons=pair.reasons,
                )
            )
        pairs = adjusted
        changes = tuple(changes_list)
    return Detection(
        paragraphs=tuple(paragraphs),
        features=tuple(features),
        pairs=tuple(pairs),
        changes=changes,
        method=method,
    )


def detect_changes(
    text: str,
    method: str = "ensemble",
) -> list[int]:
    detection = explain_document(text, method=method)
    return list(detection.changes)


def explain_document(text: str, method: str = "ensemble") -> Detection:
    paragraphs = split_paragraphs(text)
    features = extract_many(paragraphs)
    return detect_from_features(paragraphs, features, method=method)


def detect_many(
    texts: Iterable[str],
    method: str = "ensemble",
) -> list[list[int]]:
    return [detect_changes(text, method=method) for text in texts]
