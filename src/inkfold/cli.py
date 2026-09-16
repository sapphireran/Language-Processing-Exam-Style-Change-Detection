"""Command line for the personal exam lab."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .corpus import iter_problems, validate_corpus
from .cusum import contraction_rate, first_person_rate, formal_rate, format_cusum
from .detectors import AdaptiveDetector, EnsembleDetector, ThresholdDetector
from .evaluate import score_document, score_folder
from .explain import explain_document, explain_scores, format_explain
from .handcalc import format_table
from .io import read_problem, read_problem_text
from .report import format_scoreboard, write_html_reports, write_markdown_explain


def _detector(name: str, threshold: float) -> ThresholdDetector | AdaptiveDetector | EnsembleDetector:
    if name == "threshold":
        return ThresholdDetector(threshold)
    if name == "adaptive":
        return AdaptiveDetector()
    if name == "ensemble":
        return EnsembleDetector(threshold=threshold)
    raise SystemExit(f"unknown detector: {name}")


def cmd_detect(args: argparse.Namespace) -> int:
    units = read_problem_text(args.problem)
    det = _detector(args.detector, args.threshold).detect(units)
    payload = det.as_truth()
    payload["scores"] = [round(s.score, 4) for s in det.scores]
    print(json.dumps(payload, indent=2))
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    if args.truth:
        problem = read_problem(args.problem, args.truth)
        rows = explain_document(problem, EnsembleDetector(threshold=args.threshold))
        print(format_explain(problem, rows))
        return 0
    # Problem without truth: still explain scores.
    from .io import Problem, Truth

    units = read_problem_text(args.problem)
    dummy = Problem(
        path=Path(args.problem),
        problem_id=Path(args.problem).stem,
        units=units,
        truth=Truth(authors=0, changes=[]),
    )
    detection = EnsembleDetector(threshold=args.threshold).detect(units)
    rows = explain_scores(units, detection)
    print(format_explain(dummy, rows))
    return 0


def cmd_hand(args: argparse.Namespace) -> int:
    units = read_problem_text(args.problem)
    print(format_table(units))
    return 0


def cmd_cusum(args: argparse.Namespace) -> int:
    units = read_problem_text(args.problem)
    rate = {
        "first_person": first_person_rate,
        "contraction": contraction_rate,
        "formal": formal_rate,
    }[args.rate]
    print(format_cusum(units, rate, args.rate))
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    problems = iter_problems(args.corpus)
    folder = score_folder(problems, EnsembleDetector(threshold=args.threshold))
    print(format_scoreboard(folder), end="")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    problems = iter_problems(args.corpus)
    det = EnsembleDetector(threshold=args.threshold)
    items = []
    walk = Path(args.walkthroughs) if args.walkthroughs else None
    for problem in problems:
        detection = det.detect(problem.units)
        doc = score_document(problem, detection)
        rows = explain_document(problem, det)
        items.append((problem, rows, doc))
        if walk:
            write_markdown_explain(walk / f"{problem.problem_id}.md", problem, rows)
    write_html_reports(Path(args.out), items)
    folder = score_folder(problems, det)
    print(format_scoreboard(folder), end="")
    print(f"wrote {len(items)} html reports under {args.out}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_corpus(args.corpus)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    n = len(iter_problems(args.corpus))
    print(f"ok: {n} problems, contract holds")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="inkfold", description="Fold a document at style-change hinges.")
    p.add_argument("--threshold", type=float, default=0.30)
    p.add_argument("--detector", choices=("threshold", "adaptive", "ensemble"), default="ensemble")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("detect", help="print predicted folds as JSON")
    d.add_argument("problem")
    d.set_defaults(func=cmd_detect)

    e = sub.add_parser("explain", help="print per-hinge drivers")
    e.add_argument("problem")
    e.add_argument("--truth", default=None)
    e.set_defaults(func=cmd_explain)

    h = sub.add_parser("hand", help="pencil-and-paper count table")
    h.add_argument("problem")
    h.set_defaults(func=cmd_hand)

    c = sub.add_parser("cusum", help="CUSUM on one register rate")
    c.add_argument("problem")
    c.add_argument("--rate", choices=("first_person", "contraction", "formal"), default="first_person")
    c.set_defaults(func=cmd_cusum)

    s = sub.add_parser("score", help="score the teaching corpus")
    s.add_argument("--corpus", default=None)
    s.set_defaults(func=cmd_score)

    r = sub.add_parser("report", help="write HTML reports (+ optional walkthroughs)")
    r.add_argument("--corpus", default=None)
    r.add_argument("--out", default="examples/reports")
    r.add_argument("--walkthroughs", default=None)
    r.set_defaults(func=cmd_report)

    v = sub.add_parser("validate", help="check PAN-style contract on the corpus")
    v.add_argument("--corpus", default=None)
    v.set_defaults(func=cmd_validate)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
