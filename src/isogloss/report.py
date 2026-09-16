"""Human-readable inspect and score tables for the oral."""

from __future__ import annotations

from .detect import Detection
from .evaluate import always_fire, confusion, macro_f1, never_fire, score_changes
from .io import Problem


def _bar(value: float, width: int = 12) -> str:
    n = max(0, min(width, int(round(abs(value) * 2))))
    return "#" * n


def render_inspect(detection: Detection, gold: list[int] | None = None) -> str:
    lines = [
        f"units={len(detection.units)} hinges={len(detection.changes)} "
        f"zeta={detection.zeta:.2f} rho={detection.rho:.2f} k={detection.min_votes}",
        "",
        f"{'i':>3} {'votes':>5} {'max|z|':>7} {'pred':>7} {'gold':>6}  top channels",
        "-" * 72,
    ]
    for view in detection.hinges:
        pred = "CHANGE" if view.fires else "same"
        truth = ""
        if gold is not None and view.index < len(gold):
            truth = "CHANGE" if gold[view.index] else "same"
        tops = ", ".join(
            f"{m.name}={m.z:+.2f}{'*' if m.marked else ''}"
            for m in view.top_channels(4)
        )
        lines.append(
            f"{view.index:3d} {view.votes:5d} {view.max_abs_z:7.2f} {pred:>7} {truth:>6}  {tops}"
        )
    if gold is not None and len(gold) == len(detection.changes):
        scored = score_changes(gold, detection.changes)
        lines.append("")
        lines.append(
            f"macro-F1={scored['macro_f1']:.3f}  acc={scored['accuracy']:.3f}  "
            f"tp={scored['tp']} fp={scored['fp']} fn={scored['fn']} tn={scored['tn']}"
        )
    return "\n".join(lines) + "\n"


def render_feature_table(detection: Detection) -> str:
    names = [row[:18] for row in (
        "i_rate",
        "we_rate",
        "you_rate",
        "contraction_rate",
        "deontic_rate",
        "hedge_rate",
        "formal_rate",
        "digit_rate",
        "n_words",
    )]
    header = f"{'unit':>4} " + " ".join(f"{n:>10}" for n in names)
    lines = [header, "-" * len(header)]
    for i, feat in enumerate(detection.features):
        data = feat.as_dict()
        cells = " ".join(f"{data[n.strip()]:10.3f}" if n.strip() != "n_words" else f"{data['n_words']:10.1f}" for n in names)
        lines.append(f"{i:4d} {cells}")
    return "\n".join(lines) + "\n"


def render_score_table(
    rows: list[tuple[str, list[int], list[int]]],
) -> str:
    """rows: (name, gold, pred) including optional liar predictors."""
    lines = [
        f"{'predictor':<14} {'macro-F1':>9} {'acc':>8} {'tp':>4} {'fp':>4} {'fn':>4} {'tn':>4}",
        "-" * 52,
    ]
    for name, gold, pred in rows:
        s = score_changes(gold, pred)
        lines.append(
            f"{name:<14} {s['macro_f1']:9.3f} {s['accuracy']:8.3f} "
            f"{s['tp']:4d} {s['fp']:4d} {s['fn']:4d} {s['tn']:4d}"
        )
    return "\n".join(lines) + "\n"


def corpus_score_payload(
    gold: list[int], pred: list[int]
) -> dict[str, float | int]:
    return score_changes(gold, pred)


def liar_rows(gold: list[int], pred: list[int]) -> list[tuple[str, list[int], list[int]]]:
    n = len(gold)
    return [
        ("never-fire", gold, never_fire(n)),
        ("always-fire", gold, always_fire(n)),
        ("isogloss", gold, pred),
    ]


def problem_line(problem: Problem, pred: list[int]) -> str:
    gold = problem.gold
    extra = ""
    if gold is not None:
        extra = f"  F1={macro_f1(gold, pred):.3f}"
        table = confusion(gold, pred)
        extra += f"  fp={table.fp} fn={table.fn}"
    return (
        f"problem-{problem.ident} units={problem.n_units} "
        f"pred={pred}{extra}"
    )
