"""Command-line entry point: `python -m quoin ...`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .calibrate import best_threshold, grid_search_threshold
from .corpus import load_corpus
from .detectors import QuoinDetector
from .explain import explain_document
from .features import vectorize
from .io import read_problem, write_solution, solution_from_changes
from .ncd import compressed_len, cross_gain, ncd
from .report import render_baselines, render_markdown, render_table, score_corpus
from .tokenize import paragraphs as split_paragraphs
from .tokenize import word_count


def _detector_from_args(args: argparse.Namespace) -> QuoinDetector:
    return QuoinDetector(threshold=args.threshold)


def cmd_score(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.corpus)
    detector = _detector_from_args(args)
    rows = score_corpus(corpus, detector)
    bands = {item.name: item.band for item in corpus}
    print(render_table(rows, bands))
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    problem = read_problem(args.path)
    print(explain_document(problem, _detector_from_args(args)))
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    problem = read_problem(args.path)
    print(f"# {problem.path.name}")
    print(f"{'i':>3} {'words':>6} {'sent':>6} {'ttr':>6} {'contr':>7} {'form':>7} {'inform':>7} {'C':>6}")
    for index, paragraph in enumerate(problem.paragraphs):
        vec = vectorize(paragraph)
        print(
            f"{index:3d} {vec.n_words:6d} {vec.shape['mean_sentence']:6.1f} "
            f"{vec.shape['ttr']:6.3f} {vec.shape['contraction']:7.3f} "
            f"{vec.shape['formal']:7.3f} {vec.shape['informal']:7.3f} "
            f"{compressed_len(paragraph):6d}"
        )
    print()
    detector = _detector_from_args(args)
    print(f"{'b':>3} {'quoin':>7} {'ncd':>7} {'char':>7} {'func':>7} {'shape':>7} {'reg':>7} {'res':>7} pred")
    for row in detector.boundaries(problem.paragraphs):
        print(
            f"{row.index:3d} {row.quoin:7.3f} {row.ncd:7.3f} {row.char_cosine:7.3f} "
            f"{row.function_l1:7.3f} {row.shape_l1:7.3f} {row.register_l1:7.3f} "
            f"{row.residual:7.3f} {row.pred:4d}"
        )
    return 0


def cmd_calibrate(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.corpus)
    detector = _detector_from_args(args)
    documents = []
    for item in corpus:
        scores = [row.quoin for row in detector.boundaries(item.problem.paragraphs)]
        documents.append((item.truth.changes, scores))
    rows = grid_search_threshold(documents, start=args.start, stop=args.stop, step=args.step)
    winner = best_threshold(rows)
    print(f"{'t':>6} {'macro-F1':>9} {'micro-F1':>9} {'n_pred':>7}")
    print("-" * 36)
    for row in rows:
        mark = "  <--" if row.threshold == winner.threshold else ""
        print(f"{row.threshold:6.2f} {row.macro_f1:9.3f} {row.micro_f1:9.3f} {row.n_pred:7d}{mark}")
    print()
    print(f"best threshold on this bank: {winner.threshold:.2f}  (macro-F1 {winner.macro_f1:.3f})")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.corpus)
    detector = _detector_from_args(args)
    text = render_markdown(corpus, detector)
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        path = out / "live-results.md"
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path}")
    else:
        print(text)
    return 0


def cmd_baselines(args: argparse.Namespace) -> int:
    corpus = load_corpus(args.corpus)
    print(render_baselines(corpus, _detector_from_args(args)))
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    problem = read_problem(args.path)
    detector = _detector_from_args(args)
    changes = detector.predict(problem.paragraphs)
    solution = solution_from_changes(changes)
    if args.out:
        write_solution(args.out, solution)
        print(f"wrote {args.out}")
    else:
        print(json.dumps(solution.as_json(), indent=2))
    return 0


def cmd_ncd(args: argparse.Namespace) -> int:
    left = Path(args.left).read_text(encoding="utf-8") if args.files else args.left
    right = Path(args.right).read_text(encoding="utf-8") if args.files else args.right
    if args.files:
        left_paras = split_paragraphs(left)
        right_paras = split_paragraphs(right)
        left = left_paras[0] if left_paras else left
        right = right_paras[0] if right_paras else right
    print(f"words: {word_count(left)} / {word_count(right)}")
    print(f"C(left)  {compressed_len(left)}")
    print(f"C(right) {compressed_len(right)}")
    print(f"C(both)  {compressed_len(left + chr(10) + right)}")
    print(f"NCD      {ncd(left, right):.4f}")
    print(f"gain     {cross_gain(left, right):.4f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quoin",
        description="Personal exam lab for intrinsic style-change detection.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.72,
        help="Absolute high-jump cutoff (peak rule still applies below this)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    score = sub.add_parser("score", help="Score the example corpus")
    score.add_argument("corpus", nargs="?", default=None)
    score.set_defaults(func=cmd_score)

    explain = sub.add_parser("explain", help="Explain one document's boundaries")
    explain.add_argument("path")
    explain.set_defaults(func=cmd_explain)

    features = sub.add_parser("features", help="Print a per-paragraph feature table")
    features.add_argument("path")
    features.set_defaults(func=cmd_features)

    calibrate = sub.add_parser("calibrate", help="Grid-search a threshold on the corpus")
    calibrate.add_argument("corpus", nargs="?", default=None)
    calibrate.add_argument("--start", type=float, default=0.16)
    calibrate.add_argument("--stop", type=float, default=0.60)
    calibrate.add_argument("--step", type=float, default=0.02)
    calibrate.set_defaults(func=cmd_calibrate)

    report = sub.add_parser("report", help="Write a markdown results report")
    report.add_argument("corpus", nargs="?", default=None)
    report.add_argument("--out", default=None)
    report.set_defaults(func=cmd_report)

    baselines = sub.add_parser("baselines", help="Compare never-fire / always-fire / quoin")
    baselines.add_argument("corpus", nargs="?", default=None)
    baselines.set_defaults(func=cmd_baselines)

    predict = sub.add_parser("predict", help="Emit a PAN solution JSON for one document")
    predict.add_argument("path")
    predict.add_argument("--out", default=None)
    predict.set_defaults(func=cmd_predict)

    ncd_cmd = sub.add_parser("ncd", help="Compute NCD of two strings or files")
    ncd_cmd.add_argument("left")
    ncd_cmd.add_argument("right")
    ncd_cmd.add_argument("--files", action="store_true", help="Treat arguments as file paths")
    ncd_cmd.set_defaults(func=cmd_ncd)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001 — CLI should print a short error
        print(f"quoin: {exc}", file=sys.stderr)
        return 1
