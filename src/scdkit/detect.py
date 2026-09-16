"""Unsupervised ensemble for paragraph-level style-change flags.

The oral-exam story:

1. Build several weakly correlated channels (Delta, char 3-grams,
   formality, sentence length, contractions, CUSUM slope).
2. Convert each adjacent score to a vote with a hard floor so a
   single-author document with one slightly longer paragraph does not
   fire just because it is the local z-score outlier.
3. Require either a strong single channel or two agreeing channels.

This is *not* how the 2023 PAN winners worked (they fine-tuned
DeBERTa). It is how you show you understand the classical pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .cusum import cusum_change_scores
from .delta import (
    char_ngram_distances,
    contraction_jumps,
    document_deltas,
    formality_jumps,
    numeric_distances,
    sentence_length_jumps,
    topic_jaccard,
)
from .features import ParagraphFeatures, extract_many
from .tokenize import split_paragraphs

# Hard floors — tuned on the bundled personal examples, not on PAN.
THRESHOLDS = {
    "delta": 0.95,
    "delta_strong": 1.45,
    "char": 0.42,
    "char_strong": 0.62,
    "formality": 0.55,
    "formality_strong": 0.90,
    "sentlen": 0.38,
    "sentlen_strong": 0.70,
    "contraction": 0.045,
    "contraction_strong": 0.09,
    "numeric": 0.55,
    "numeric_strong": 0.85,
    "cusum": 1.15,
    "cusum_strong": 2.10,
}


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
    numeric: float
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
                    "numeric": round(p.numeric, 4),
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
        "numeric": numeric_distances(features),
        "cusum": cusum_change_scores(features),
    }
    topics = topic_jaccard(features)
    pairs: list[PairScore] = []
    for i in range(n - 1):
        votes = 0
        strong = 0
        reasons: list[str] = []
        for name in ("delta", "char", "formality", "sentlen", "contraction", "numeric", "cusum"):
            v, s, reason = _channel_votes(name, channels[name][i])
            votes += v
            strong += s
            if reason:
                reasons.append(reason)
        # Two ordinary votes, or one strong channel, decide a change.
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
                numeric=channels["numeric"][i],
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
    if method == "ensemble":
        pairs = score_pairs(features)
        changes = tuple(p.change for p in pairs)
    else:
        pairs = score_pairs(features)
        key = {
            "delta": "delta",
            "char": "char",
            "formality": "formality",
            "cusum": "cusum",
            "numeric": "numeric",
        }.get(method)
        if key is None:
            raise ValueError(f"unknown method {method!r}")
        changes = []
        adjusted: list[PairScore] = []
        for pair in pairs:
            value = getattr(pair, key)
            change = 1 if value >= THRESHOLDS[key] else 0
            changes.append(change)
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
                    numeric=pair.numeric,
                    cusum=pair.cusum,
                    topic=pair.topic,
                    votes=pair.votes,
                    strong=pair.strong,
                    change=change,
                    reasons=pair.reasons,
                )
            )
        pairs = adjusted
        changes = tuple(changes)
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
