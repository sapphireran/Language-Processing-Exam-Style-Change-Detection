"""Run several exam-explainable baselines on the same document.

The table is the point: I want to see which signal actually carries the
cut. A method that scores 1.0 on a toy file is not a PAN result.
"""

from __future__ import annotations

from dataclasses import dataclass

from examscd.cusum import cusum_points
from examscd.detect import ABS_MIN, detect_document, pair_distance, threshold_distances
from examscd.evaluate import boundary_report
from examscd.tokenize import split_units


@dataclass(frozen=True)
class MethodResult:
    name: str
    pred: list[int]
    macro_f1: float
    f1_change: float
    accuracy: float


def _from_scores(scores: list[float], gold: list[int], abs_min: float = ABS_MIN) -> list[int]:
    thr = threshold_distances(scores, abs_min=abs_min)
    if scores and max(scores) < abs_min:
        return [0] * len(scores)
    return [1 if s >= thr else 0 for s in scores]


def compare_methods(text: str, gold: list[int], granularity: str = "sentence") -> list[MethodResult]:
    units = split_units(text, granularity)
    n_pairs = max(len(units) - 1, 0)
    if len(gold) != n_pairs:
        raise ValueError(f"gold has {len(gold)} pairs but document has {n_pairs}")

    ngram = []
    func = []
    style = []
    length = []
    combined = []
    for i in range(n_pairs):
        raw = pair_distance(units[i], units[i + 1])
        ngram.append(raw["ngram"])
        func.append(min(raw["function_l1"] / 1.4, 1.2))
        style.append(raw["style_l2"])
        length.append(raw["length_jump"])
        combined.append(raw["combined"])

    lengths = [len(u.split()) for u in units]
    cusum_hits = set(cusum_points(lengths))
    cusum_pred = [1 if i in cusum_hits else 0 for i in range(n_pairs)]

    methods = {
        "always-0 (single)": [0] * n_pairs,
        "always-1 (every pair)": [1] * n_pairs,
        "sentence-length jump": _from_scores(length, gold, abs_min=0.35),
        "function-word L1": _from_scores(func, gold, abs_min=0.16),
        "char-3gram cosine": _from_scores(ngram, gold, abs_min=0.22),
        "16-D style L2": _from_scores(style, gold, abs_min=0.18),
        "CUSUM slope reverse": cusum_pred,
        "cue-sheet (examscd)": detect_document(text, granularity=granularity).changes,
    }

    rows: list[MethodResult] = []
    for name, pred in methods.items():
        report = boundary_report(gold, pred)
        rows.append(
            MethodResult(
                name=name,
                pred=pred,
                macro_f1=report.macro_f1,
                f1_change=report.f1_1,
                accuracy=report.accuracy,
            )
        )
    return rows


def format_table(rows: list[MethodResult]) -> str:
    header = f"{'method':<24} {'macro-F1':>9} {'F1-change':>10} {'acc':>7}  prediction"
    lines = [header, "-" * len(header)]
    for row in rows:
        pred = "".join(str(x) for x in row.pred) if row.pred else "∅"
        lines.append(
            f"{row.name:<24} {row.macro_f1:>9.3f} {row.f1_change:>10.3f} {row.accuracy:>7.3f}  {pred}"
        )
    return "\n".join(lines)
