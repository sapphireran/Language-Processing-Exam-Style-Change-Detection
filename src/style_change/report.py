"""Human-readable feature tables and score cards."""

from __future__ import annotations

from .detectors import EnsembleDetector, StyleChangeDetector
from .features import StylometricProfile, extract_profile
from .io import Problem


def _fmt(value: float) -> str:
    return f"{value:8.4f}"


def feature_table(paragraphs: list[str]) -> str:
    profiles = [extract_profile(p) for p in paragraphs]
    names = StylometricProfile.names()
    header = ["feature"] + [f"p{i+1}" for i in range(len(paragraphs))]
    width = max(len("feature"), max(len(n) for n in names))
    lines = [
        f"{'feature':<{width}}  " + "  ".join(f"{col:>8}" for col in header[1:])
    ]
    lines.append("-" * len(lines[0]))
    for name in names:
        cells = [_fmt(getattr(profile, name)) for profile in profiles]
        lines.append(f"{name:<{width}}  " + "  ".join(cells))
    return "\n".join(lines)


def distance_table(paragraphs: list[str], detector: StyleChangeDetector | None = None) -> str:
    detector = detector or EnsembleDetector()
    scores = detector.distances(paragraphs)
    if not scores:
        return "no paragraph boundaries"
    lines = ["pair     distance"]
    lines.append("----------------")
    for i, score in enumerate(scores, start=1):
        lines.append(f"p{i}-p{i+1}   {score:8.4f}")
    return "\n".join(lines)


def problem_card(problem: Problem, pred: list[int] | None = None) -> str:
    lines = [
        f"problem {problem.problem_id}",
        f"paragraphs: {len(problem.paragraphs)}",
        f"authors (gold): {problem.authors}",
        f"gold changes: {problem.gold_changes}",
    ]
    if pred is not None:
        lines.append(f"pred changes: {pred}")
    lines.append("")
    for i, para in enumerate(problem.paragraphs, start=1):
        preview = para if len(para) <= 160 else para[:157] + "..."
        lines.append(f"[{i}] {preview}")
    return "\n".join(lines)
