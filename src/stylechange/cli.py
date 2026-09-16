"""Command-line entry point: ``stylechange`` or ``python -m stylechange``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .detector import debug_scores, detect, explain_lines
from .evaluate import evaluate_collection, format_collection
from .features import extract
from .io import load_problem, solution_path, write_solution
from .tokenize import Granularity
from .voices import voice_scores


def _granularity(value: str) -> Granularity:
    if value not in {"auto", "sentence", "paragraph"}:
        raise argparse.ArgumentTypeError(value)
    return value  # type: ignore[return-value]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stylechange",
        description="Intrinsic style-change detection for a personal NLP exam project.",
    )
    parser.add_argument("--version", action="version", version=f"stylechange {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    detect_p = sub.add_parser("detect", help="mark change boundaries in one document")
    detect_p.add_argument("document", type=Path)
    detect_p.add_argument(
        "--granularity",
        default="auto",
        type=_granularity,
        help="auto (default), sentence, or paragraph",
    )
    detect_p.add_argument("--threshold", type=float, default=1.00)
    detect_p.add_argument("--explain", action="store_true")
    detect_p.add_argument("--debug-voices", action="store_true")
    detect_p.add_argument("--json", action="store_true", help="print the solution object only")
    detect_p.add_argument("-o", "--output", type=Path, help="write solution-problem-*.json here")

    eval_p = sub.add_parser("evaluate", help="score a folder of problem-*.txt + truth-*.json")
    eval_p.add_argument("directory", type=Path)
    eval_p.add_argument("--granularity", default="auto", type=_granularity)
    eval_p.add_argument("--threshold", type=float, default=1.00)
    eval_p.add_argument("-o", "--output", type=Path, help="write solution-*.json into this folder")

    feat_p = sub.add_parser("features", help="print the stylometric profile of each unit")
    feat_p.add_argument("document", type=Path)
    feat_p.add_argument("--granularity", default="auto", type=_granularity)

    voice_p = sub.add_parser("voices", help="print voice scores for each unit")
    voice_p.add_argument("document", type=Path)
    voice_p.add_argument("--granularity", default="auto", type=_granularity)

    return parser


def _detect_command(args: argparse.Namespace) -> int:
    text = load_problem(args.document)
    detection = detect(text, granularity=args.granularity, threshold=args.threshold)
    if args.output is not None:
        dest = args.output
        if dest.is_dir() or dest.suffix != ".json":
            dest = solution_path(args.document, dest)
        write_solution(dest, detection.changes)
    if args.json:
        print(json.dumps(detection.as_solution(), indent=2))
        return 0
    if args.debug_voices:
        print("\n".join(debug_scores(detection)))
        print()
    if args.explain:
        print("\n".join(explain_lines(detection)))
        return 0
    print(f"units:    {len(detection.units)}")
    print(f"changes:  {detection.changes}")
    print(f"authors~  {detection.n_authors}")
    return 0


def _evaluate_command(args: argparse.Namespace) -> int:
    score = evaluate_collection(
        args.directory,
        output_dir=args.output,
        granularity=args.granularity,
        threshold=args.threshold,
    )
    print(format_collection(score))
    return 0


def _features_command(args: argparse.Namespace) -> int:
    detection = detect(load_problem(args.document), granularity=args.granularity)
    for index, (unit, vector) in enumerate(zip(detection.units, detection.features)):
        preview = unit.replace("\n", " ")[:64]
        print(f"## {index}  {preview}")
        for name, value in vector.named_values().items():
            print(f"  {name:<22} {value:.4f}")
        print()
    return 0


def _voices_command(args: argparse.Namespace) -> int:
    detection = detect(load_problem(args.document), granularity=args.granularity)
    for index, (unit, vector, raw, voice) in enumerate(
        zip(detection.units, detection.features, detection.raw_voices, detection.voices)
    ):
        scores = voice_scores(vector)
        packed = "  ".join(f"{name}={scores[name]:+.2f}" for name in ("chat", "student", "textbook", "notes"))
        preview = unit.replace("\n", " ")[:72]
        print(f"{index:2d}  {raw:<8}->{voice:<8}  {packed}")
        print(f"    {preview}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    commands = {
        "detect": _detect_command,
        "evaluate": _evaluate_command,
        "features": _features_command,
        "voices": _voices_command,
    }
    try:
        return commands[args.command](args)
    except Exception as exc:  # noqa: BLE001 — CLI prints a short error
        print(f"stylechange: {exc}", file=sys.stderr)
        return 2
