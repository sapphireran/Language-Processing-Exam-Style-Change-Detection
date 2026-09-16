"""Command-line entry point: `hingemark` or `python -m hingemark`."""

from __future__ import annotations

import argparse
from pathlib import Path

from .calibrate import grid_thresholds, leave_one_out
from .corpus import DEFAULT_CORPUS, list_corpus
from .detectors import DEFAULT_THRESHOLD
from .evaluate import accuracy_trap
from .explain import explain_document, format_explanation
from .io import read_problem, read_truth, truth_path_for, write_solution
from .report import evaluate_items, format_corpus_table, write_html_report
from .tokenize import Mode


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hingemark",
        description="Personal exam lab for sentence-level style-change detection.",
    )
    parser.add_argument("--mode", default="lines", choices=("lines", "paragraphs", "sentences"))
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("split", help="print units")
    p.add_argument("file")
    p.set_defaults(func=cmd_split)

    p = sub.add_parser("detect", help="print a changes array")
    p.add_argument("file")
    p.add_argument("--out", type=Path, default=None)
    p.set_defaults(func=cmd_detect)

    p = sub.add_parser("explain", help="hinge table for one document")
    p.add_argument("file")
    p.add_argument("--truth", type=Path, default=None)
    p.set_defaults(func=cmd_explain)

    p = sub.add_parser("eval", help="score a corpus directory")
    p.add_argument("corpus", nargs="?", default=str(DEFAULT_CORPUS))
    p.add_argument("--split", action="append", dest="splits")
    p.set_defaults(func=cmd_eval)

    p = sub.add_parser("calibrate", help="grid-search a threshold")
    p.add_argument("corpus", nargs="?", default=str(DEFAULT_CORPUS))
    p.add_argument("--loo", action="store_true")
    p.set_defaults(func=cmd_calibrate)

    p = sub.add_parser("report", help="write HTML reports")
    p.add_argument("corpus", nargs="?", default=str(DEFAULT_CORPUS))
    p.add_argument("--out", type=Path, default=Path("examples/reports"))
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("trap", help="print the 16/4 accuracy trap")
    p.set_defaults(func=cmd_trap)

    p = sub.add_parser("demo", help="explain one spotlight document")
    p.add_argument("--name", default="problem-14-two-mycologists")
    p.set_defaults(func=cmd_demo)
    return parser


def _mode(args: argparse.Namespace) -> Mode:
    return args.mode  # type: ignore[return-value]


def cmd_split(args: argparse.Namespace) -> int:
    problem = read_problem(args.file, mode=_mode(args))
    for i, unit in enumerate(problem.units):
        print(f"{i:02d}  {unit}")
    print(f"# {len(problem.units)} units, {problem.n_hinges} hinges")
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    from .detectors import threshold_detect
    from .pairwise import score_unit_hinges

    problem = read_problem(args.file, mode=_mode(args))
    result = threshold_detect(score_unit_hinges(problem.units), threshold=args.threshold)
    print(list(result.changes))
    if args.out:
        write_solution(args.out, result.changes)
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    problem = read_problem(args.file, mode=_mode(args))
    gold = authors = None
    truth_path = args.truth or truth_path_for(problem.path)
    if Path(truth_path).exists():
        truth = read_truth(truth_path)
        gold = truth.changes
        authors = truth.authors
    exp = explain_document(
        problem.text,
        mode=_mode(args),
        threshold=args.threshold,
        gold=gold,
        authors=authors,
    )
    print(format_explanation(exp))
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    splits = tuple(args.splits) if args.splits else None
    items = list_corpus(args.corpus, mode=_mode(args), splits=splits)
    scored = evaluate_items(items, threshold=args.threshold)
    print(format_corpus_table(items, scored, args.threshold))
    return 0


def cmd_calibrate(args: argparse.Namespace) -> int:
    items = list_corpus(args.corpus, mode=_mode(args))
    if args.loo:
        rows = leave_one_out(items)
        print(f"{'held-out':<42} {'tau':>6} {'held F1':>8} {'train F1':>8}")
        for row in rows:
            print(
                f"{row.held_out:<42} {row.best_threshold:6.2f} "
                f"{row.held_out_macro_f1:8.3f} {row.train_macro_f1:8.3f}"
            )
        if rows:
            mean = sum(r.held_out_macro_f1 for r in rows) / len(rows)
            print(f"# mean held-out macro-F1={mean:.3f}")
        return 0
    rows = grid_thresholds(items)
    print(f"{'tau':>6} {'mean F1':>8} {'micro F1':>8} {'acc':>6}")
    for row in rows[:12]:
        print(
            f"{row.threshold:6.2f} {row.mean_macro_f1:8.3f} "
            f"{row.micro_macro_f1:8.3f} {row.mean_accuracy:6.3f}"
        )
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    items = list_corpus(args.corpus, mode=_mode(args))
    args.out.mkdir(parents=True, exist_ok=True)
    for item in items:
        write_html_report(item, args.out / f"{item.name}.html", threshold=args.threshold)
    print(f"wrote {len(items)} reports under {args.out}")
    return 0


def cmd_trap(args: argparse.Namespace) -> int:
    trap = accuracy_trap()
    print(f"gold={list(trap.gold)}")
    print(f"pred={list(trap.pred)}")
    print(f"accuracy={trap.accuracy:.3f}")
    print(f"macro-F1={trap.macro_f1:.3f}")
    print(trap.note)
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    items = list_corpus(mode=_mode(args))
    match = next((it for it in items if args.name in it.name), None)
    if match is None:
        print(f"no document matching {args.name!r}")
        return 1
    args.file = str(match.problem.path)
    args.truth = match.truth.path
    return cmd_explain(args)
