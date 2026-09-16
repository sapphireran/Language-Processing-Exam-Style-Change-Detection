"""Command line for the oral: inspect, score, predict, features."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .detect import DEFAULT_K, DEFAULT_RHO, DEFAULT_ZETA, detect_problem
from .evaluate import always_fire, macro_f1, never_fire, score_changes
from .io import iter_problems, read_problem, solution_name, write_solution
from .report import liar_rows, render_feature_table, render_inspect, render_score_table


def _add_thresholds(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--zeta", type=float, default=DEFAULT_ZETA, help="absolute |z| floor")
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO, help="fraction of per-channel peak")
    parser.add_argument("-k", "--min-votes", type=int, default=DEFAULT_K, dest="min_votes")


def cmd_inspect(args: argparse.Namespace) -> int:
    problem = read_problem(args.path)
    detection = detect_problem(
        problem, zeta=args.zeta, rho=args.rho, min_votes=args.min_votes
    )
    sys.stdout.write(render_inspect(detection, gold=problem.gold))
    if args.features:
        sys.stdout.write("\n")
        sys.stdout.write(render_feature_table(detection))
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    problem = read_problem(args.path)
    detection = detect_problem(problem)
    sys.stdout.write(render_feature_table(detection))
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    folder = Path(args.folder)
    gold_all: list[int] = []
    pred_all: list[int] = []
    per: list[dict] = []
    for problem in iter_problems(folder):
        if problem.gold is None:
            print(f"skip problem-{problem.ident}: no truth", file=sys.stderr)
            continue
        detection = detect_problem(
            problem, zeta=args.zeta, rho=args.rho, min_votes=args.min_votes
        )
        gold_all.extend(problem.gold)
        pred_all.extend(detection.changes)
        scored = score_changes(problem.gold, detection.changes)
        per.append(
            {
                "id": problem.ident,
                "path": problem.path.name,
                "pred": detection.changes,
                "gold": problem.gold,
                **scored,
            }
        )
        if args.verbose:
            print(
                f"problem-{problem.ident} pred={detection.changes} "
                f"gold={problem.gold} macro-F1={scored['macro_f1']:.3f}"
            )
    if not gold_all:
        print("no scored problems", file=sys.stderr)
        return 1
    print(render_score_table(liar_rows(gold_all, pred_all)).rstrip())
    print(f"hinges={len(gold_all)} documents={len(per)}")
    if args.json:
        payload = {
            "overall": score_changes(gold_all, pred_all),
            "liars": {
                "never_fire": score_changes(gold_all, never_fire(len(gold_all))),
                "always_fire": score_changes(gold_all, always_fire(len(gold_all))),
            },
            "documents": per,
        }
        Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    incoming = Path(args.input)
    outgoing = Path(args.output)
    outgoing.mkdir(parents=True, exist_ok=True)
    count = 0
    for problem in iter_problems(incoming):
        detection = detect_problem(
            problem, zeta=args.zeta, rho=args.rho, min_votes=args.min_votes
        )
        write_solution(outgoing / solution_name(problem.ident), detection.changes)
        count += 1
    print(f"wrote {count} solutions to {outgoing}")
    return 0


def cmd_holdout(args: argparse.Namespace) -> int:
    keep = {x.strip().lstrip("0") or "0" for x in args.ids.split(",") if x.strip()}
    gold_all: list[int] = []
    pred_all: list[int] = []
    used = []
    for problem in iter_problems(args.folder):
        ident = problem.ident.lstrip("0") or "0"
        if ident not in keep:
            continue
        if problem.gold is None:
            continue
        detection = detect_problem(
            problem, zeta=args.zeta, rho=args.rho, min_votes=args.min_votes
        )
        gold_all.extend(problem.gold)
        pred_all.extend(detection.changes)
        used.append(problem.ident)
    if not gold_all:
        print("holdout empty", file=sys.stderr)
        return 1
    print("holdout documents: " + ", ".join(used))
    print(render_score_table(liar_rows(gold_all, pred_all)).rstrip())
    print(f"macro-F1={macro_f1(gold_all, pred_all):.3f} hinges={len(gold_all)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="isogloss",
        description="Style change as a bundle of closed-class isoglosses.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    inspect = sub.add_parser("inspect", help="print votes and top channels for one file")
    inspect.add_argument("path")
    inspect.add_argument("--features", action="store_true")
    _add_thresholds(inspect)
    inspect.set_defaults(func=cmd_inspect)

    features = sub.add_parser("features", help="print the closed-class table")
    features.add_argument("path")
    features.set_defaults(func=cmd_features)

    score = sub.add_parser("score", help="macro-F1 against a folder of problems")
    score.add_argument("folder")
    score.add_argument("-v", "--verbose", action="store_true")
    score.add_argument("--json", help="write a JSON dump")
    _add_thresholds(score)
    score.set_defaults(func=cmd_score)

    predict = sub.add_parser("predict", help="PAN-shaped -i / -o prediction")
    predict.add_argument("-i", "--input", required=True)
    predict.add_argument("-o", "--output", required=True)
    _add_thresholds(predict)
    predict.set_defaults(func=cmd_predict)

    holdout = sub.add_parser("holdout", help="score a comma-separated id list")
    holdout.add_argument("folder")
    holdout.add_argument("--ids", required=True, help="comma-separated problem ids")
    _add_thresholds(holdout)
    holdout.set_defaults(func=cmd_holdout)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
