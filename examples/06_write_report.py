#!/usr/bin/env python3
"""Write HTML walk-throughs for the pinned easy document and one hard holdout.

The reports colour author-runs from the truth vector and print the same
pairwise cues as the worked example. Open the HTML in a browser; no
network is required.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scd.generate import TRAIN_ID_MAX
from scd.io import problem_id, read_problem, read_truth
from scd.models import train_logreg
from scd.report import render_report, write_report
from scd.sentences import split_units

DATA = ROOT / "examples" / "data"
OUT = ROOT / "models" / "reports"


def _write(problem: Path, dest: Path, model) -> None:
    units = split_units(read_problem(problem), mode="line")
    truth = read_truth(problem.with_name(f"truth-problem-{problem_id(problem)}.json"))
    pred = model.predict_units(units)
    proba = model.predict_proba_units(units).tolist()
    html = render_report(
        units,
        truth=truth.changes,
        pred=pred,
        proba=proba,
        title=f"{problem.parent.name} / {problem.name}",
    )
    write_report(dest, html)
    print(f"wrote {dest.relative_to(ROOT)}")


def main() -> int:
    model = train_logreg(DATA, seed=0, id_min=1, id_max=TRAIN_ID_MAX)
    OUT.mkdir(parents=True, exist_ok=True)
    _write(DATA / "easy" / "problem-1.txt", OUT / "easy-problem-1.html", model)
    _write(DATA / "hard" / "problem-14.txt", OUT / "hard-problem-14.html", model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
