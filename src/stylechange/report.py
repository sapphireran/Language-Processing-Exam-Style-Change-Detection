"""Human-readable dumps for exam walkthroughs."""

from __future__ import annotations

from stylechange.detectors import Detection
from stylechange.evaluate import Score
from stylechange.features import SCALAR_NAMES, StyleProfile
from stylechange.topic import topic_distance


def _fmt(value: float) -> str:
    return f"{value:0.3f}"


def format_scalars(profile: StyleProfile, names: tuple[str, ...] | None = None) -> str:
    chosen = names or SCALAR_NAMES
    width = max(len(name) for name in chosen)
    lines = [f"{name:<{width}}  {_fmt(profile.scalars[name])}" for name in chosen]
    return "\n".join(lines)


def format_top_function_words(profile: StyleProfile, k: int = 8) -> str:
    ranked = sorted(profile.function_words.items(), key=lambda kv: kv[1], reverse=True)
    ranked = [(word, rate) for word, rate in ranked if rate > 0][:k]
    if not ranked:
        return "(no function words)"
    return ", ".join(f"{word}={rate:0.3f}" for word, rate in ranked)


def format_detection(detection: Detection, paragraphs: list[str] | None = None) -> str:
    lines = [f"threshold = {detection.threshold:0.3f}", ""]
    for i, dist in enumerate(detection.distances):
        flag = "CHANGE" if detection.changes[i] else "same  "
        parts = detection.components[i]
        preview = ""
        if paragraphs is not None:
            left = paragraphs[i][:48].replace("\n", " ")
            right = paragraphs[i + 1][:48].replace("\n", " ")
            preview = f"\n    {left!r} …\n    {right!r} …"
        lines.append(
            f"boundary {i + 1:>2}  {flag}  combined={dist:0.3f}  "
            f"scalar={parts['scalar']:0.3f}  "
            f"fw={parts['function_words']:0.3f}  "
            f"3gram={parts['trigram']:0.3f}  "
            f"punct={parts['punct']:0.3f}"
            f"{preview}"
        )
        if paragraphs is not None:
            lines.append(
                f"    topic-cosine-distance = "
                f"{topic_distance(paragraphs[i], paragraphs[i + 1]):0.3f}"
            )
    return "\n".join(lines)


def format_score(score: Score, title: str = "score") -> str:
    return (
        f"{title}: F1={score.f1:0.3f}  P={score.precision:0.3f}  "
        f"R={score.recall:0.3f}  acc={score.accuracy:0.3f}  "
        f"tp={score.true_positives} fp={score.false_positives} "
        f"fn={score.false_negatives} tn={score.true_negatives}"
    )
