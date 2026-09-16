"""Human-readable detection dumps for lab sessions."""

from __future__ import annotations

from .detectors import Detection
from .evaluate import MetricBundle


def preview_paragraph(text: str, width: int = 88) -> str:
    compact = " ".join(text.split())
    if len(compact) <= width:
        return compact
    return compact[: width - 1] + "…"


def format_detection(detection: Detection, gold: list[int] | None = None) -> str:
    lines = []
    lines.append(f"paragraphs: {len(detection.paragraphs)}")
    lines.append(f"predicted changes: {detection.changes}")
    if gold is not None:
        lines.append(f"gold changes:      {gold}")
    lines.extend(detection.notes)
    lines.append("")
    for i, para in enumerate(detection.paragraphs):
        feat = detection.features[i]
        lines.append(
            f"[P{i + 1}] words={feat.n_words}  "
            f"1st={feat.first_person_rate:.2f}  "
            f"2nd={feat.second_person_rate:.2f}  "
            f"academic={feat.academic_rate:.2f}  "
            f"informal={feat.informal_rate:.2f}  "
            f"Guiraud={feat.richness.guiraud:.2f}"
        )
        lines.append(f"     {preview_paragraph(para)}")
        if i < len(detection.boundaries):
            b = detection.boundaries[i]
            mark = "CHANGE" if b.predicted else "same  "
            gold_bit = ""
            if gold is not None and i < len(gold):
                gold_bit = "  gold=" + ("CHANGE" if gold[i] else "same")
                if gold[i] != b.predicted:
                    gold_bit += "  ← mismatch"
            lines.append(f"  -- {mark}  combined={b.scores.combined:.3f}{gold_bit}")
            for reason in b.reasons:
                lines.append(f"     {reason}")
    return "\n".join(lines)


def format_metrics(name: str, bundle: MetricBundle) -> str:
    exact = "exact" if bundle.exact else "errors"
    return (
        f"{name:28s}  pairs={bundle.n_pairs:2d}  "
        f"F1={bundle.f1:.3f}  macro-F1={bundle.macro_f1:.3f}  "
        f"acc={bundle.accuracy:.3f}  {exact}"
    )
