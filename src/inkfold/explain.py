"""Plain-language hinge explanations for oral revision."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .detectors import Detection, EnsembleDetector, FoldScore
from .features import RegisterVector, extract_register
from .io import Problem


CHANNEL_BLURB = {
    "register_l1": "six-number register vector (exam card)",
    "function_cosine_distance": "smoothed function-word cosine distance",
    "char3_distance": "damped character 3-gram distance",
    "delta": "intra-document Burrows Delta on function words",
}


@dataclass
class HingeExplain:
    index: int
    score: float
    predicted: int
    gold: int | None
    channels: dict[str, float]
    left: RegisterVector
    right: RegisterVector
    drivers: list[str]
    verdict: str


def _drivers(left: RegisterVector, right: RegisterVector) -> list[str]:
    names = RegisterVector.NAMES
    pairs = list(zip(names, left.as_tuple(), right.as_tuple()))
    pairs.sort(key=lambda t: abs(t[1] - t[2]), reverse=True)
    out = []
    for name, a, b in pairs[:3]:
        if abs(a - b) < 0.02:
            continue
        direction = "higher on the right" if b > a else "higher on the left"
        out.append(f"{name} {direction} ({a:.3f} vs {b:.3f})")
    return out


def _verdict(pred: int, gold: int | None, expected_error: str | None) -> str:
    if gold is None:
        return "predicted fold" if pred else "predicted seam"
    if pred == gold == 1:
        return "true fold"
    if pred == gold == 0:
        return "true seam"
    if pred == 1 and gold == 0:
        return f"false fold ({expected_error or 'false_alarm'})"
    return f"missed fold ({expected_error or 'miss'})"


def explain_scores(
    units: Sequence[str],
    detection: Detection,
    gold: Sequence[int] | None = None,
    expected_error: str | None = None,
) -> list[HingeExplain]:
    rows: list[HingeExplain] = []
    for i, sc in enumerate(detection.scores):
        left = extract_register(units[: sc.index])
        right = extract_register(units[sc.index :])
        g = gold[i] if gold is not None and i < len(gold) else None
        pred = detection.changes[i] if i < len(detection.changes) else 0
        rows.append(
            HingeExplain(
                index=sc.index,
                score=sc.score,
                predicted=pred,
                gold=g,
                channels=sc.channels,
                left=left,
                right=right,
                drivers=_drivers(left, right),
                verdict=_verdict(pred, g, expected_error),
            )
        )
    return rows


def explain_document(problem: Problem, detector: EnsembleDetector | None = None) -> list[HingeExplain]:
    det = detector or EnsembleDetector()
    detection = det.detect(problem.units)
    return explain_scores(problem.units, detection, problem.truth.changes, problem.truth.expected_error)


def format_explain(problem: Problem, rows: list[HingeExplain]) -> str:
    lines = [
        f"# {problem.problem_id}",
        f"site: {problem.truth.site}",
        f"voices: {', '.join(problem.truth.voices) or '(unlisted)'}",
        f"gold authors: {problem.truth.authors}   return_author: {problem.truth.return_author}",
        f"gold changes: {problem.truth.changes}",
        f"notes: {problem.truth.notes or '—'}",
        "",
    ]
    for row in rows:
        gold = "—" if row.gold is None else str(row.gold)
        lines.append(f"## cut after unit {row.index}   score={row.score:.3f}   pred={row.predicted} gold={gold}")
        lines.append(f"verdict: {row.verdict}")
        if row.drivers:
            lines.append("drivers: " + "; ".join(row.drivers))
        for key, val in row.channels.items():
            lines.append(f"  {key:28s} {val:.3f}   {CHANNEL_BLURB[key]}")
        lines.append(
            "  left  "
            + " ".join(f"{n}={v:.3f}" for n, v in zip(RegisterVector.NAMES, row.left.as_tuple()))
        )
        lines.append(
            "  right "
            + " ".join(f"{n}={v:.3f}" for n, v in zip(RegisterVector.NAMES, row.right.as_tuple()))
        )
        lines.append("")
    return "\n".join(lines)


def strongest_fold(scores: Sequence[FoldScore]) -> FoldScore | None:
    if not scores:
        return None
    return max(scores, key=lambda s: s.score)
