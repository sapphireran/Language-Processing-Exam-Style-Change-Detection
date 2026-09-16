"""Human-readable hinge table for one document."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .cusum import cusum_trace
from .detectors import DEFAULT_THRESHOLD, DetectorResult, threshold_detect
from .evaluate import BinaryReport, score_pairs
from .pairwise import Hinge, score_unit_hinges
from .tokenize import Mode, split_units


@dataclass(frozen=True)
class Explanation:
    units: tuple[str, ...]
    hinges: tuple[Hinge, ...]
    result: DetectorResult
    gold: tuple[int, ...] | None
    report: BinaryReport | None
    cusum_peak: int
    returning_author_note: str | None


def explain_document(
    text: str,
    *,
    mode: Mode = "lines",
    threshold: float = DEFAULT_THRESHOLD,
    gold: Sequence[int] | None = None,
    authors: Sequence[int] | None = None,
) -> Explanation:
    units = tuple(split_units(text, mode=mode))
    hinges = tuple(score_unit_hinges(units))
    result = threshold_detect(hinges, threshold=threshold)
    report = score_pairs(gold, result.changes) if gold is not None else None
    trace = cusum_trace(result.scores)
    note = None
    if authors is not None:
        n_from_changes = 1 + sum(gold or result.changes)
        n_ids = len(set(authors))
        if n_ids != n_from_changes:
            note = (
                f"authors={n_ids} but 1+sum(changes)={n_from_changes}: "
                "a writer came back. Binary hinges cannot name who."
            )
    return Explanation(
        units=units,
        hinges=hinges,
        result=result,
        gold=tuple(gold) if gold is not None else None,
        report=report,
        cusum_peak=trace.peak_index,
        returning_author_note=note,
    )


def format_explanation(exp: Explanation, *, width: int = 72) -> str:
    lines = [
        f"units={len(exp.units)} hinges={len(exp.hinges)} "
        f"detector={exp.result.name} cut={exp.result.threshold:.3f}",
        f"pred={list(exp.result.changes)}",
    ]
    if exp.gold is not None:
        lines.append(f"gold={list(exp.gold)}")
    if exp.report is not None:
        r = exp.report
        lines.append(
            f"accuracy={r.accuracy:.3f} macro-F1={r.macro_f1:.3f} "
            f"change-F1={r.change.f1:.3f} (tp={r.tp} fp={r.fp} fn={r.fn} tn={r.tn})"
        )
    lines.append(f"cusum peak hinge={exp.cusum_peak}")
    if exp.returning_author_note:
        lines.append(exp.returning_author_note)
    lines.append("")
    for h, pred in zip(exp.hinges, exp.result.changes):
        gold = exp.gold[h.index] if exp.gold is not None else None
        mark = "SNAP" if pred else "hold"
        gold_s = "" if gold is None else ("  gold=1" if gold else "  gold=0")
        miss = ""
        if gold is not None and gold != pred:
            miss = "  MISS" if gold == 1 else "  FALSE ALARM"
        lines.append(
            f"[{h.index}] {mark}  blend={h.blend:.3f}  "
            f"reg={h.register_gap:.3f}  fw={h.fw_distance:.3f}  "
            f"char={h.char_distance:.3f}  d={h.delta:.3f}{gold_s}{miss}"
        )
        if h.drivers:
            lines.append("     drivers: " + ", ".join(h.drivers))
        left = _clip(h.left, width)
        right = _clip(h.right, width)
        lines.append(f"     L: {left}")
        lines.append(f"     R: {right}")
    return "\n".join(lines)


def _clip(text: str, width: int) -> str:
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."
