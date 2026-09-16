"""Command-line interface.

Examples::

    stylechange detect examples/documents/easy-mixed-topics.txt --explain
    stylechange evaluate examples/documents --output /tmp/stylechange-out
    stylechange features examples/documents/medium-one-topic.txt
    stylechange generate --difficulty easy --seed 3
"""

from __future__ import annotations

import argparse
from pathlib import Path
import json
import sys

from .detector import StyleChangeDetector
from .evaluate import evaluate_dataset
from .features import extract_features
from .generate import generate_document
from .io import Solution, iter_problems, solution_path_for, write_solution
from .tokenize import split_units


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stylechange",
        description="Intrinsic style-change detection (personal exam project).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    detect = sub.add_parser("detect", help="label style-change boundaries in one file")
    detect.add_argument("path", type=Path)
    detect.add_argument("--granularity", choices=("sentence", "paragraph"), default="sentence")
    detect.add_argument("--threshold", type=float, default=None)
    detect.add_argument("--window", type=int, default=2)
    detect.add_argument("--mode", choices=("segment", "pairwise"), default="segment")
    detect.add_argument("--explain", action="store_true")
    detect.add_argument("--json", action="store_true", dest="as_json")

    features = sub.add_parser("features", help="print dense stylometric features per unit")
    features.add_argument("path", type=Path)
    features.add_argument("--granularity", choices=("sentence", "paragraph"), default="sentence")

    evaluate = sub.add_parser("evaluate", help="run the detector on a PAN-style directory")
    evaluate.add_argument("input_dir", type=Path)
    evaluate.add_argument("--output", type=Path, default=Path("output"))
    evaluate.add_argument("--granularity", choices=("sentence", "paragraph"), default="sentence")
    evaluate.add_argument("--threshold", type=float, default=None)
    evaluate.add_argument("--window", type=int, default=2)
    evaluate.add_argument("--mode", choices=("segment", "pairwise"), default="segment")

    generate = sub.add_parser("generate", help="print a synthetic labelled exam answer")
    generate.add_argument("--difficulty", choices=("easy", "medium", "hard", "single"), default="easy")
    generate.add_argument("--seed", type=int, default=1)
    generate.add_argument("--id", default="demo")

    return parser


def _detector_from_args(args: argparse.Namespace) -> StyleChangeDetector:
    kwargs: dict = {"granularity": args.granularity, "window": args.window}
    if getattr(args, "threshold", None) is not None:
        kwargs["threshold"] = args.threshold
    if getattr(args, "mode", None) is not None:
        kwargs["mode"] = args.mode
    return StyleChangeDetector(**kwargs)


def _cmd_detect(args: argparse.Namespace) -> int:
    text = args.path.read_text(encoding="utf-8")
    detector = _detector_from_args(args)
    prediction = detector.predict(text, explain=args.explain)
    if args.as_json:
        payload = prediction.as_solution_payload()
        if args.explain:
            payload["scores"] = [round(s, 4) for s in prediction.scores]
            payload["units"] = prediction.units
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    print(f"units:    {len(prediction.units)}")
    print(f"changes:  {prediction.changes}")
    print(f"authors~  {prediction.authors_estimate}")
    print(f"scores:   {[round(s, 3) for s in prediction.scores]}")
    if args.explain:
        print()
        for item in prediction.explanations:
            mark = "CHANGE" if item.change else "same  "
            print(f"[{item.index}] {mark}  score={item.score:.3f}")
            print(f"    L: {item.left_text}")
            print(f"    R: {item.right_text}")
            print(
                "    parts: "
                + ", ".join(
                    f"{k}={v:.3f}"
                    for k, v in item.parts.items()
                    if k in {"register", "function", "personal", "academic", "telegram"}
                )
            )
            if item.register_left:
                print(
                    "    axis L/R: "
                    + ", ".join(
                        f"{name} {item.register_left[name]:.2f}->{item.register_right[name]:.2f}"
                        for name in ("personal", "academic", "telegram")
                    )
                )
            tops = ", ".join(f"{name}={delta:.3f}" for name, delta in item.top_deltas[:3])
            print(f"    top Δ: {tops}")
    return 0


def _cmd_features(args: argparse.Namespace) -> int:
    text = args.path.read_text(encoding="utf-8")
    units = split_units(text, granularity=args.granularity)
    print(f"# {len(units)} {args.granularity} units from {args.path}")
    for i, unit in enumerate(units):
        vector = extract_features(unit)
        named = vector.as_named_dense()
        preview = unit if len(unit) <= 88 else unit[:85] + "..."
        print(f"\n[{i}] {preview}")
        interesting = (
            "avg_word_len",
            "type_token",
            "punct_ratio",
            "function_ratio",
            "first_person_ratio",
            "academic_ratio",
            "contraction_ratio",
        )
        bits = [f"{name}={named[name]:.3f}" for name in interesting]
        print("    " + "  ".join(bits))
    return 0


def _cmd_evaluate(args: argparse.Namespace) -> int:
    detector = _detector_from_args(args)
    args.output.mkdir(parents=True, exist_ok=True)
    problems = list(iter_problems(args.input_dir))
    if not problems:
        print(f"no problem-*.txt files in {args.input_dir}", file=sys.stderr)
        return 2
    for problem in problems:
        prediction = detector.predict(problem.text)
        write_solution(
            solution_path_for(problem, args.output),
            Solution(changes=prediction.changes, authors=prediction.authors_estimate),
        )
    print(f"wrote {len(problems)} solution files to {args.output}")
    try:
        result = evaluate_dataset(args.input_dir, args.output)
    except ValueError as exc:
        print(f"evaluation skipped: {exc}")
        return 0
    print(
        "macro-F1={macro_f1:.3f}  acc={accuracy:.3f}  "
        "P={precision:.3f}  R={recall:.3f}  pairs={pairs}  docs={documents}".format(
            **result.as_dict()
        )
    )
    if result.skipped:
        print(f"skipped {result.skipped} document(s) with length mismatch")
    return 0


def _cmd_generate(args: argparse.Namespace) -> int:
    document = generate_document(
        difficulty=args.difficulty, seed=args.seed, problem_id=args.id
    )
    print(document.text, end="")
    print("---")
    print(json.dumps(document.truth.to_json(), indent=2))
    print(f"voices: {document.authors}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    dispatch = {
        "detect": _cmd_detect,
        "features": _cmd_features,
        "evaluate": _cmd_evaluate,
        "generate": _cmd_generate,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
