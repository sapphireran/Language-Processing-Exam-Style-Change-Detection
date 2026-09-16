"""Command-line entry for inspect / score / report / solve."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .detectors import AdaptiveDetector, EnsembleDetector, ThresholdDetector
from .evaluate import score_pairs
from .explain import explain_document
from .features import FeatureTable
from .io import guess_truth_path, iter_problems, load_problem, load_truth, write_solution
from .pairwise import score_document
from .report import format_metrics, format_pair_table, html_report, write_html


def _detector(name: str, threshold: float, k: float):
    if name == "threshold":
        return ThresholdDetector(threshold=threshold)
    if name == "adaptive":
        return AdaptiveDetector(k=k)
    if name == "ensemble":
        return EnsembleDetector(threshold=threshold, k=k)
    raise SystemExit(f"unknown detector: {name}")


def _load_gold(problem_path: Path, n_pairs: int) -> list[int] | None:
    truth = guess_truth_path(problem_path)
    if truth is None:
        return None
    changes = load_truth(truth)["changes"]
    if len(changes) != n_pairs:
        raise SystemExit(
            f"{truth} has {len(changes)} labels; document has {n_pairs} pairs"
        )
    return changes


def cmd_inspect(args: argparse.Namespace) -> int:
    problem = load_problem(args.path)
    table = FeatureTable.from_units(problem.units)
    detector = _detector(args.detector, args.threshold, args.k)
    pred = detector.predict(table)
    gold = _load_gold(problem.path, problem.n_pairs)
    rows = score_document(table)
    exps = explain_document(table, pred, gold, threshold=args.threshold)
    print(f"{problem.path}  units={len(problem.units)}  pairs={problem.n_pairs}")
    if gold is not None:
        print(format_metrics(detector.name, score_pairs(gold, pred)))
    print(format_pair_table(problem.units, rows, exps))
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    root = Path(args.path)
    detector = _detector(args.detector, args.threshold, args.k)
    print(f"# {detector.name}  threshold={args.threshold}  k={args.k}")
    labelled = 0
    gold_all: list[int] = []
    pred_all: list[int] = []
    for path in iter_problems(root):
        problem = load_problem(path)
        table = FeatureTable.from_units(problem.units)
        pred = detector.predict(table)
        gold = _load_gold(path, problem.n_pairs)
        if gold is None:
            print(f"{path.name}: unlabelled  pred={pred}")
            continue
        labelled += 1
        gold_all.extend(gold)
        pred_all.extend(pred)
        metrics = score_pairs(gold, pred)
        print(f"{path.name}: {format_metrics('', metrics)}")
    if labelled:
        print(format_metrics("TOTAL", score_pairs(gold_all, pred_all)))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    detector = _detector(args.detector, args.threshold, args.k)
    index_rows = []
    for path in iter_problems(args.path):
        problem = load_problem(path)
        table = FeatureTable.from_units(problem.units)
        pred = detector.predict(table)
        gold = _load_gold(path, problem.n_pairs)
        metrics = score_pairs(gold, pred) if gold is not None else None
        exps = explain_document(table, pred, gold, threshold=args.threshold)
        html = html_report(path.stem, problem.units, table, exps, metrics)
        dest = out / f"{path.stem}.html"
        write_html(dest, html)
        f1 = f"{metrics.macro_f1:.3f}" if metrics else "—"
        index_rows.append(f'<li><a href="{dest.name}">{path.stem}</a> — macro-F1 {f1}</li>')
    index = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Seamtrace reports</title></head>"
        "<body><h1>Seamtrace reports</h1><ul>"
        + "".join(index_rows)
        + "</ul></body></html>\n"
    )
    write_html(out / "index.html", index)
    print(f"wrote {len(index_rows)} reports to {out}")
    return 0


def cmd_solve(args: argparse.Namespace) -> int:
    inp = Path(args.input)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    detector = _detector(args.detector, args.threshold, args.k)
    for path in iter_problems(inp):
        problem = load_problem(path)
        table = FeatureTable.from_units(problem.units)
        pred = detector.predict(table)
        # PAN wants solution-problem-X.json; stem already includes "problem-X".
        dest = out / f"solution-{path.name.replace('.txt', '.json')}"
        write_solution(dest, pred)
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    problem = load_problem(args.path)
    table = FeatureTable.from_units(problem.units)
    payload = []
    for i, unit in enumerate(table.units):
        payload.append(
            {
                "index": i,
                "text": unit.text,
                "scalars": unit.scalars,
            }
        )
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="seamtrace", description="Personal style-change exam lab")
    p.add_argument("--detector", default="threshold", choices=["threshold", "adaptive", "ensemble"])
    p.add_argument("--threshold", type=float, default=0.42)
    p.add_argument("--k", type=float, default=0.85)
    sub = p.add_subparsers(dest="cmd", required=True)

    inspect = sub.add_parser("inspect", help="print pair table for one document")
    inspect.add_argument("path")
    inspect.set_defaults(func=cmd_inspect)

    score = sub.add_parser("score", help="score every problem-*.txt in a folder")
    score.add_argument("path")
    score.set_defaults(func=cmd_score)

    report = sub.add_parser("report", help="write HTML pair reports")
    report.add_argument("path")
    report.add_argument("--out", default="examples/reports")
    report.set_defaults(func=cmd_report)

    solve = sub.add_parser("solve", help="write PAN solution-problem-X.json files")
    solve.add_argument("-i", "--input", required=True)
    solve.add_argument("-o", "--output", required=True)
    solve.set_defaults(func=cmd_solve)

    feats = sub.add_parser("features", help="dump per-unit scalars as JSON")
    feats.add_argument("path")
    feats.set_defaults(func=cmd_features)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
