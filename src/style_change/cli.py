"""Command-line interface for prediction, evaluation, and inspection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .detectors import DETECTORS, build_detector
from .evaluate import evaluate_changes
from .io import load_problem, load_problem_dir, load_solution_dir, write_solution
from .report import distance_table, feature_table, problem_card


def _predict(args: argparse.Namespace) -> int:
    problems = load_problem_dir(args.input_dir)
    detector = build_detector(
        args.detector,
        threshold=args.threshold,
        sensitivity=args.sensitivity,
    )
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    for problem in problems:
        pred = detector.predict(problem.paragraphs)
        dest = write_solution(args.output_dir, problem.problem_id, pred)
        print(f"{problem.problem_id}: {pred} -> {dest}")
    return 0


def _evaluate(args: argparse.Namespace) -> int:
    problems = load_problem_dir(args.gold)
    gold = {}
    for problem in problems:
        if problem.gold_changes is None:
            raise ValueError(f"no gold labels for problem {problem.problem_id}")
        gold[problem.problem_id] = problem.gold_changes
    pred = load_solution_dir(args.pred)
    result = evaluate_changes(gold, pred)
    print(f"documents          {len(result.documents)}")
    print(f"mean macro-F1      {result.mean_macro_f1:.4f}")
    print(f"pooled macro-F1    {result.pooled_macro_f1:.4f}")
    print(f"pooled TP/FP/TN/FN {result.pooled.tp}/{result.pooled.fp}/{result.pooled.tn}/{result.pooled.fn}")
    print()
    print("id            gold                 pred                 F1")
    print("-" * 68)
    for doc in result.documents:
        print(
            f"{doc.problem_id:<12} {str(doc.gold):<20} {str(doc.pred):<20} {doc.macro_f1:.4f}"
        )
    return 0


def _features(args: argparse.Namespace) -> int:
    problem = load_problem(args.path)
    detector = build_detector(args.detector)
    pred = detector.predict(problem.paragraphs)
    print(problem_card(problem, pred=pred))
    print()
    print(feature_table(problem.paragraphs))
    print()
    print(distance_table(problem.paragraphs, detector=detector))
    print()
    print(json.dumps({"changes": pred}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="style-change",
        description="Intrinsic style-change detection study toolkit.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    predict = sub.add_parser("predict", help="write solution-problem-*.json files")
    predict.add_argument("-i", "--input-dir", required=True)
    predict.add_argument("-o", "--output-dir", required=True)
    predict.add_argument(
        "--detector",
        default="ensemble",
        choices=sorted(DETECTORS),
    )
    predict.add_argument("--threshold", type=float, default=None)
    predict.add_argument("--sensitivity", type=float, default=0.42)
    predict.set_defaults(func=_predict)

    evaluate = sub.add_parser("evaluate", help="score predictions against gold")
    evaluate.add_argument("--gold", required=True, help="directory with problem + truth files")
    evaluate.add_argument("--pred", required=True, help="directory with solution files")
    evaluate.set_defaults(func=_evaluate)

    features = sub.add_parser("features", help="print profiles for one problem")
    features.add_argument("path")
    features.add_argument(
        "--detector",
        default="ensemble",
        choices=sorted(DETECTORS),
    )
    features.set_defaults(func=_features)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
