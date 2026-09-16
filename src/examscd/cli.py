"""Command line for the personal exam study kit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from examscd import __version__
from examscd.compare import compare_methods, format_table
from examscd.cusum import ascii_cusum, cusum_points, cusum_series, sentence_lengths
from examscd.detect import detect_document
from examscd.evaluate import adjusted_rand_index, boundary_report
from examscd.features import style_dict
from examscd.io import read_text, read_truth, write_solution
from examscd.render import cusum_svg
from examscd.tokenize import split_units


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("document", type=Path, help="UTF-8 text file")
    parser.add_argument(
        "-g",
        "--granularity",
        default="sentence",
        choices=("sentence", "paragraph"),
        help="unit to score (default: sentence)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="examscd",
        description="Personal exam study kit for intrinsic style-change detection.",
    )
    parser.add_argument("--version", action="version", version=f"examscd {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_detect = sub.add_parser("detect", help="score adjacent units and emit changes")
    _add_common(p_detect)
    p_detect.add_argument("--explain", action="store_true", help="print each pair")
    p_detect.add_argument("-o", "--output", type=Path, help="write PAN-shaped JSON")

    p_eval = sub.add_parser("evaluate", help="score a document against a truth file")
    _add_common(p_eval)
    p_eval.add_argument("truth", type=Path, help="JSON with a changes array")

    p_feat = sub.add_parser("features", help="dump the closed stylometric vector")
    _add_common(p_feat)

    p_cusum = sub.add_parser("cusum", help="print / draw a CUSUM of unit length")
    _add_common(p_cusum)
    p_cusum.add_argument("--svg", type=Path, help="write an SVG figure")

    p_cmp = sub.add_parser("compare", help="table of exam-explainable baselines")
    _add_common(p_cmp)
    p_cmp.add_argument("truth", type=Path, help="JSON with a changes array")

    return parser


def _print_detect(doc: Path, granularity: str, explain: bool) -> int:
    text = read_text(doc)
    result = detect_document(text, granularity=granularity)
    print(f"file:         {doc}")
    print(f"granularity:  {granularity}")
    print(f"units:        {len(result.units)}")
    print(f"labels:       {result.labels}")
    print(f"changes:      {result.changes}")
    print(f"authors:      {result.authors}")
    print(f"cusum hits:   {result.cusum_hits}")
    print(f"multi-author: {result.multi_author}")
    if explain:
        print()
        for pair in result.pairs:
            mark = "CHANGE" if pair.change else "same  "
            cue = "  +cusum" if pair.cusum_hit else ""
            print(
                f"[{pair.index:02d}] {mark}  {pair.left_label} → {pair.right_label}  "
                f"d={pair.combined:.3f}  ng={pair.ngram:.3f}  "
                f"fw={pair.function_l1:.3f}  st={pair.style_l2:.3f}  "
                f"len={pair.length_jump:.3f}{cue}"
            )
            left = pair.left.replace("\n", " ")
            right = pair.right.replace("\n", " ")
            print(f"     L: {left[:96]}")
            print(f"     R: {right[:96]}")
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    text = read_text(args.document)
    result = detect_document(text, granularity=args.granularity)
    if args.output:
        write_solution(
            args.output,
            result.changes,
            authors=result.authors,
            extra={"labels": result.labels, "cusum_hits": result.cusum_hits},
        )
        print(f"wrote {args.output}")
    return _print_detect(args.document, args.granularity, args.explain)


def _cmd_evaluate(args: argparse.Namespace) -> int:
    text = read_text(args.document)
    truth = read_truth(args.truth)
    granularity = truth.granularity or args.granularity
    result = detect_document(text, granularity=granularity)
    if len(result.changes) != len(truth.changes):
        print(
            f"pair-count mismatch: pred={len(result.changes)} gold={len(truth.changes)}",
            file=sys.stderr,
        )
        return 2
    report = boundary_report(truth.changes, result.changes)
    print(f"file:         {args.document}")
    print(f"truth:        {args.truth}")
    print(f"gold:         {truth.changes}")
    print(f"pred:         {result.changes}")
    print(f"macro-F1:     {report.macro_f1:.3f}")
    print(f"F1-change:    {report.f1_1:.3f}")
    print(f"F1-same:      {report.f1_0:.3f}")
    print(f"accuracy:     {report.accuracy:.3f}")
    if truth.authors and result.authors:
        print(f"gold authors: {truth.authors}")
        print(f"pred authors: {result.authors}")
        print(f"ARI:          {adjusted_rand_index(truth.authors, result.authors):.3f}")
    return 0


def _cmd_features(args: argparse.Namespace) -> int:
    text = read_text(args.document)
    units = split_units(text, args.granularity)
    print(f"file: {args.document}  units: {len(units)}  granularity: {args.granularity}")
    for i, unit in enumerate(units):
        vec = style_dict(unit)
        preview = unit.replace("\n", " ")[:72]
        print(f"\n[{i}] {preview}")
        for key, value in vec.items():
            print(f"    {key:<18} {value:.4f}")
    return 0


def _cmd_cusum(args: argparse.Namespace) -> int:
    text = read_text(args.document)
    units = split_units(text, args.granularity)
    values = [len(u.split()) for u in units]
    if args.granularity == "sentence" and not values:
        values = sentence_lengths(text)
    series = cusum_series(values)
    hits = cusum_points(values)
    print(f"file:    {args.document}")
    print(f"lengths: {values}")
    print(f"cusum:   {[round(x, 2) for x in series]}")
    print(f"hits:    {hits}")
    print()
    print(ascii_cusum(values))
    if args.svg:
        cusum_svg(values, args.svg, change_slots=hits, title=f"CUSUM — {args.document.name}")
        print(f"\nwrote {args.svg}")
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    text = read_text(args.document)
    truth = read_truth(args.truth)
    granularity = truth.granularity or args.granularity
    rows = compare_methods(text, truth.changes, granularity=granularity)
    print(f"file:  {args.document}")
    print(f"gold:  {truth.changes}")
    print()
    print(format_table(rows))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "detect": _cmd_detect,
        "evaluate": _cmd_evaluate,
        "features": _cmd_features,
        "cusum": _cmd_cusum,
        "compare": _cmd_compare,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
