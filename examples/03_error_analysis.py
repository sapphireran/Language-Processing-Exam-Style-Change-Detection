#!/usr/bin/env python3
"""Walk hits, misses, and near-misses after the pooled baseline is trained.

Companion to docs/08-error-analysis.md. For each selected pair we print
the two sentences and the stylometric deltas that should (or should not)
explain the decision.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.features import pairwise_feature_map
from scd.generate import TRAIN_ID_MAX
from scd.io import list_problems, problem_id, read_problem, read_truth
from scd.models import train_logreg
from scd.sentences import split_units

DATA = ROOT / "examples" / "data"
BANDS = ("easy", "medium", "hard")
HOLD_MIN = TRAIN_ID_MAX + 1
CUES = (
    "abs_contraction_rate",
    "abs_first_person_rate",
    "abs_exclaim",
    "fw_cosine",
    "char_tri_cosine",
    "jaccard",
    "length_ratio",
    "abs_n_words",
)


@dataclass
class PairRow:
    band: str
    pid: str
    index: int
    left: str
    right: str
    y: int
    p: float
    cues: dict[str, float]

    @property
    def kind(self) -> str:
        if self.y == 1 and self.p >= 0.7:
            return "confident-hit"
        if self.y == 1 and self.p <= 0.3:
            return "confident-miss"
        if self.y == 0 and self.p >= 0.7:
            return "false-alarm"
        if abs(self.p - 0.5) < 0.15:
            return "near-miss"
        if self.y == 1:
            return "soft-hit"
        return "soft-correct"


def collect_rows() -> list[PairRow]:
    model = train_logreg(DATA, seed=0, id_min=1, id_max=TRAIN_ID_MAX)
    rows: list[PairRow] = []
    for band in BANDS:
        for problem in list_problems(DATA / band):
            pid = problem_id(problem)
            if not pid.isdigit() or int(pid) < HOLD_MIN:
                continue
            units = split_units(read_problem(problem), mode="line")
            truth = read_truth(DATA / band / f"truth-problem-{problem_id(problem)}.json")
            proba = model.predict_proba_units(units)
            for i, (left, right, y, p) in enumerate(
                zip(units, units[1:], truth.changes, proba)
            ):
                cues = pairwise_feature_map(left, right)
                rows.append(
                    PairRow(
                        band=band,
                        pid=problem_id(problem),
                        index=i,
                        left=left,
                        right=right,
                        y=y,
                        p=float(p),
                        cues={name: cues[name] for name in CUES},
                    )
                )
    return rows


def pick(rows: list[PairRow], kind: str, band: str | None = None) -> PairRow | None:
    matches = [row for row in rows if row.kind == kind and (band is None or row.band == band)]
    if not matches:
        return None
    prefer_high = kind in {"confident-hit", "false-alarm", "soft-hit"}
    matches.sort(key=lambda row: -row.p if prefer_high else row.p)
    return matches[0]


def show(title: str, row: PairRow | None) -> None:
    print("=" * 72)
    print(title)
    if row is None:
        print("  (no pair in this bucket on the toy corpus)")
        return
    print(f"  {row.band}/problem-{row.pid}  pair {row.index + 1}-{row.index + 2}")
    print(f"  truth={row.y}  p(change)={row.p:.3f}  bucket={row.kind}")
    print(f"  L: {row.left}")
    print(f"  R: {row.right}")
    print("  cues:")
    for name, value in row.cues.items():
        print(f"    {name:<24} {value:7.3f}")


def main() -> int:
    rows = collect_rows()
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.kind] = counts.get(row.kind, 0) + 1
    print("pair buckets (pooled model, all bands)")
    for key in sorted(counts):
        print(f"  {key:<16} {counts[key]:3d}")
    print()

    show("Easy register rupture — should be a confident hit", pick(rows, "confident-hit", "easy"))
    print()
    hard_miss = pick(rows, "confident-miss", "hard") or pick(rows, "confident-miss")
    title = (
        "Hard miss — same topic, weak closed-class gap"
        if hard_miss and hard_miss.band == "hard"
        else "Holdout miss — the model did not see this splice"
    )
    show(title, hard_miss)
    print()
    show("False alarm — length or topic drift inside one author", pick(rows, "false-alarm"))
    print()
    show("Near miss — features disagree with each other", pick(rows, "near-miss"))
    print()
    print("Quote three of these pairs in a write-up; do not dump every probability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
