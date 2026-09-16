"""Command-line entry point for inspect / detect / eval."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from stylechange.detectors import AdaptiveDetector, ThresholdDetector
from stylechange.evaluate import score_changes, score_corpus
from stylechange.features import CORE_SCALAR_NAMES, extract_profile
from stylechange.io import iter_problems, load_problem, load_split, write_solution
from stylechange.report import (
    format_detection,
    format_scalars,
    format_score,
    format_top_function_words,
)


def _build_detector(args: argparse.Namespace) -> ThresholdDetector | AdaptiveDetector:
    if args.adaptive:
        return AdaptiveDetector(k=args.k, floor=args.floor)
    return ThresholdDetector(threshold=args.threshold)


def cmd_inspect(args: argparse.Namespace) -> int:
    problem = load_problem(args.path)
    print(f"problem {problem.problem_id}: {len(problem.paragraphs)} paragraphs\n")
    for i, paragraph in enumerate(problem.paragraphs, start=1):
        profile = extract_profile(paragraph)
        print(f"--- paragraph {i} ({profile.n_tokens} tokens) ---")
        print(paragraph)
        print()
        print(format_scalars(profile, CORE_SCALAR_NAMES))
        print("function words:", format_top_function_words(profile))
        print()
    if len(problem.paragraphs) >= 2:
        detector = _build_detector(args)
        detection = detector.predict_paragraphs(problem.paragraphs)
        print(format_detection(detection, problem.paragraphs))
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    detector = _build_detector(args)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for problem in iter_problems(args.input):
        detection = detector.predict_paragraphs(problem.paragraphs)
        dest = out_dir / f"solution-problem-{problem.problem_id}.json"
        write_solution(dest, detection.changes)
        count += 1
        print(f"{problem.problem_id}: {detection.changes}  (t={detection.threshold:0.3f})")
    print(f"wrote {count} solution files to {out_dir}")
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    detector = _build_detector(args)
    rows = load_split(args.input)
    if not rows:
        print(f"no problem-*.txt files in {args.input}", file=sys.stderr)
        return 2

    triples: list[tuple[str, list[int], list[int]]] = []
    for problem, truth in rows:
        if truth is None:
            print(f"missing truth for {problem.problem_id}", file=sys.stderr)
            return 2
        if args.predictions:
            pred_path = Path(args.predictions) / f"solution-problem-{problem.problem_id}.json"
            predicted = json.loads(pred_path.read_text(encoding="utf-8"))["changes"]
        else:
            predicted = detector.predict_paragraphs(problem.paragraphs).changes
        if args.output:
            write_solution(
                Path(args.output) / f"solution-problem-{problem.problem_id}.json",
                list(predicted),
            )
        score = score_changes(truth.changes, predicted)
        print(
            f"{problem.problem_id:8} truth={truth.changes} pred={list(predicted)}  "
            f"{format_score(score, title='doc')}"
        )
        triples.append((problem.problem_id, truth.changes, list(predicted)))

    summary = score_corpus(triples)
    micro = summary["micro"]
    print()
    print(f"macro-F1 = {summary['macro_f1']:0.3f}")
    print(format_score(micro, title="micro"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stylechange",
        description="Inspect, detect, and evaluate paragraph-level style changes.",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--threshold", type=float, default=0.33, help="fixed distance cut-off")
    common.add_argument("--adaptive", action="store_true", help="use mean + k*std threshold")
    common.add_argument("--k", type=float, default=0.65, help="adaptive std multiplier")
    common.add_argument("--floor", type=float, default=0.30, help="adaptive minimum threshold")

    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser("inspect", parents=[common], help="print features for one problem")
    inspect.add_argument("path", help="path to problem-*.txt")
    inspect.set_defaults(func=cmd_inspect)

    detect = sub.add_parser("detect", parents=[common], help="write solution JSON files")
    detect.add_argument("input", help="directory of problem-*.txt files")
    detect.add_argument("-o", "--output", required=True, help="output directory")
    detect.set_defaults(func=cmd_detect)

    evaluate = sub.add_parser("eval", parents=[common], help="score against truth files")
    evaluate.add_argument("input", help="directory with problem and truth files")
    evaluate.add_argument("--predictions", help="optional directory of solution-*.json")
    evaluate.add_argument("-o", "--output", help="optional directory to write solutions")
    evaluate.set_defaults(func=cmd_eval)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
