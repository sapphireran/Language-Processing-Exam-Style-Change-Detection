"""Command-line entry points for the personal exam toolkit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .calibrate import format_sweep, sweep_thresholds
from .cusum import ascii_sparkline, paragraph_feature_trace, sentence_length_trace
from .detect import detect_text
from .evaluate import collection_report, format_score, score_document
from .features import extract_document, feature_table
from .generate import make_split
from .io import (
    load_collection,
    load_problem,
    load_solutions,
    load_truth,
    write_problem,
    write_solution,
    write_truth,
)
from .report import html_report, text_report, write_html


def _add_detect_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("text", type=Path, help="UTF-8 document with blank-line paragraphs")
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument(
        "--method",
        default="relative",
        choices=("relative", "ensemble", "features", "delta", "ngram", "cusum", "adaptive"),
    )
    parser.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="splicefind",
        description="Personal style-change exam toolkit (PAN-format I/O, no corpus download).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    detect = sub.add_parser("detect", help="score paragraph boundaries in one document")
    _add_detect_args(detect)

    features = sub.add_parser("features", help="print a per-paragraph feature table")
    features.add_argument("text", type=Path)

    cusum = sub.add_parser("cusum", help="print a CUSUM sparkline")
    cusum.add_argument("text", type=Path)
    cusum.add_argument("--feature", default="avg_sent_len")

    report = sub.add_parser("report", help="write a text or HTML walkthrough")
    report.add_argument("text", type=Path)
    report.add_argument("--truth", type=Path)
    report.add_argument("--html", type=Path)
    report.add_argument("--threshold", type=float, default=0.55)
    report.add_argument("--method", default="relative")
    report.add_argument("--title", default="style-change report")

    batch = sub.add_parser("detect-dir", help="PAN-style directory in, solutions out")
    batch.add_argument("-i", "--input-dir", type=Path, required=True)
    batch.add_argument("-o", "--output-dir", type=Path, required=True)
    batch.add_argument("--threshold", type=float, default=0.55)
    batch.add_argument("--method", default="relative")

    evaluate = sub.add_parser("evaluate", help="score solution JSON against truth JSON")
    evaluate.add_argument("--pred", type=Path, required=True)
    evaluate.add_argument("--gold", type=Path, required=True)

    score = sub.add_parser("score-corpus", help="run the detector on a labelled collection")
    score.add_argument("root", type=Path)
    score.add_argument("--threshold", type=float, default=0.55)
    score.add_argument("--method", default="relative")

    calibrate = sub.add_parser("calibrate", help="sweep thresholds on a labelled collection")
    calibrate.add_argument("root", type=Path)
    calibrate.add_argument("--method", default="relative")

    generate = sub.add_parser("generate", help="write a tiny synthetic PAN-format split")
    generate.add_argument("-o", "--output-dir", type=Path, required=True)
    generate.add_argument("--easy", type=int, default=4)
    generate.add_argument("--medium", type=int, default=4)
    generate.add_argument("--hard", type=int, default=4)
    generate.add_argument("--seed", type=int, default=23)
    return parser


def _print_detection(detection, as_json: bool) -> int:
    if as_json:
        print(json.dumps({"changes": detection.changes}, indent=2))
        return 0
    print(json.dumps({"changes": detection.changes}))
    for boundary in detection.boundaries:
        flag = "CHANGE" if boundary.decision else "same"
        print(
            f"  [{boundary.index}] {flag:6}  ens={boundary.ensemble:.3f}  "
            f"Δ={boundary.delta:.3f}  3g={boundary.ngram_distance:.3f}"
        )
        print(f"       L: {boundary.left_preview}")
        print(f"       R: {boundary.right_preview}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "detect":
        text = args.text.read_text(encoding="utf-8")
        detection = detect_text(text, threshold=args.threshold, method=args.method)
        return _print_detection(detection, args.json)

    if args.command == "features":
        text = args.text.read_text(encoding="utf-8")
        doc = extract_document(text)
        table = feature_table(doc.vectors)
        for i, row in enumerate(table, start=1):
            print(f"# paragraph {i}")
            for key in (
                "avg_sent_len",
                "avg_word_len",
                "type_token_ratio",
                "first_person_rate",
                "second_person_rate",
                "contraction_rate",
                "hedge_rate",
                "flesch_like",
            ):
                print(f"  {key:20} {row[key]:8.3f}")
            print()
        return 0

    if args.command == "cusum":
        text = args.text.read_text(encoding="utf-8")
        if args.feature == "sentence_length":
            trace = sentence_length_trace(text)
        else:
            doc = extract_document(text)
            trace = paragraph_feature_trace(doc.vectors, args.feature)
        print(f"mean={trace.mean:.3f}")
        print("values ", ascii_sparkline(trace.values))
        print("cusum  ", ascii_sparkline(trace.cusum))
        if trace.labels:
            print("labels ", " ".join(trace.labels))
        return 0

    if args.command == "report":
        text = args.text.read_text(encoding="utf-8")
        doc = extract_document(text)
        detection = detect_text(text, threshold=args.threshold, method=args.method)
        score = None
        if args.truth:
            truth = load_truth(args.truth)
            score = score_document(truth.changes, detection.changes, truth.problem_id)
        print(text_report(doc, detection, score, title=args.title))
        if args.html:
            write_html(args.html, html_report(doc, detection, score, title=args.title))
            print(f"wrote {args.html}", file=sys.stderr)
        return 0

    if args.command == "detect-dir":
        collection = load_collection(args.input_dir)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for problem, _ in collection.pairs():
            detection = detect_text(
                problem.text, threshold=args.threshold, method=args.method
            )
            write_solution(
                args.output_dir / f"solution-problem-{problem.problem_id}.json",
                detection.changes,
            )
        print(f"wrote {len(collection)} solutions to {args.output_dir}")
        return 0

    if args.command == "evaluate":
        gold_root = args.gold
        pred_root = args.pred
        if gold_root.is_file() and pred_root.is_file():
            gold = load_truth(gold_root)
            pred = json.loads(pred_root.read_text(encoding="utf-8"))["changes"]
            print(format_score(score_document(gold.changes, pred, gold.problem_id)))
            return 0
        collection = load_collection(gold_root)
        solutions = load_solutions(pred_root)
        scores = []
        for problem, truth in collection.pairs():
            if truth is None or problem.problem_id not in solutions:
                continue
            scores.append(
                score_document(truth.changes, solutions[problem.problem_id], problem.problem_id)
            )
        for score in scores:
            print(format_score(score))
        summary = collection_report(scores)
        print(
            f"macro F1={summary['macro_f1']:.3f}  micro F1={summary['micro_f1']:.3f}  "
            f"docs={int(summary['n_docs'])}"
        )
        return 0

    if args.command == "score-corpus":
        collection = load_collection(args.root)
        scores = []
        for problem, truth in collection.pairs():
            detection = detect_text(
                problem.text, threshold=args.threshold, method=args.method
            )
            if truth is None:
                print(f"{problem.problem_id}: changes={detection.changes}")
                continue
            score = score_document(truth.changes, detection.changes, problem.problem_id)
            scores.append(score)
            print(format_score(score))
        if scores:
            summary = collection_report(scores)
            print(
                f"macro F1={summary['macro_f1']:.3f}  micro F1={summary['micro_f1']:.3f}  "
                f"accuracy={summary['mean_accuracy']:.3f}"
            )
        return 0

    if args.command == "calibrate":
        collection = load_collection(args.root)
        points = sweep_thresholds(collection, method=args.method)
        print(format_sweep(points))
        return 0

    if args.command == "generate":
        docs = make_split(
            n_easy=args.easy,
            n_medium=args.medium,
            n_hard=args.hard,
            seed=args.seed,
        )
        out = args.output_dir
        out.mkdir(parents=True, exist_ok=True)
        truth_dir = out / "truth"
        truth_dir.mkdir(exist_ok=True)
        for doc in docs:
            write_problem(out / f"problem-{doc.problem.problem_id}.txt", doc.problem.text)
            write_truth(truth_dir / f"truth-problem-{doc.problem.problem_id}.json", doc.truth)
        print(f"wrote {len(docs)} synthetic problems to {out}")
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
