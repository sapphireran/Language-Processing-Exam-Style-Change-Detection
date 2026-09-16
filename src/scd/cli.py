"""Command-line interface for the personal SCD study toolkit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scd.evaluate import bootstrap_doc_f1, evaluate_directory
from scd.features import pairwise_feature_map, unit_feature_map
from scd.generate import DEFAULT_SEED, write_corpus
from scd.io import (
    check_alignment,
    problem_id,
    read_problem,
    read_truth,
    reconstruct_authors,
)
from scd.models import predict_directory, train_logreg
from scd.report import render_report, write_report
from scd.sentences import split_units


def _print_units(units: list[str], changes: list[int] | None = None) -> None:
    runs = reconstruct_authors(changes) if changes is not None else [None] * len(units)
    for i, unit in enumerate(units, start=1):
        tag = f"  run={runs[i - 1]}" if runs[i - 1] is not None else ""
        print(f"{i:2d}.{tag}  {unit}")
        if changes is not None and i <= len(changes):
            mark = "CHANGE" if changes[i - 1] else "same"
            print(f"     -- {mark} --")


def cmd_inspect(args: argparse.Namespace) -> int:
    text = read_problem(args.problem)
    units = split_units(text, mode=args.mode)
    print(f"{args.problem}: {len(units)} units (mode={args.mode})")
    changes = None
    if args.truth:
        truth = read_truth(args.truth)
        check_alignment(len(units), truth.changes, path=args.truth)
        changes = truth.changes
        print(f"authors={truth.authors}  changes={truth.changes}")
    else:
        sibling = Path(args.problem).with_name(
            f"truth-problem-{problem_id(args.problem)}.json"
        )
        if sibling.exists():
            truth = read_truth(sibling)
            check_alignment(len(units), truth.changes, path=sibling)
            changes = truth.changes
            print(f"authors={truth.authors}  changes={truth.changes}  (from {sibling.name})")
    _print_units(units, changes)
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    units = split_units(read_problem(args.problem), mode=args.mode)
    for i, unit in enumerate(units, start=1):
        feats = unit_feature_map(unit)
        preview = {
            key: round(feats[key], 4)
            for key in (
                "n_words",
                "avg_word_len",
                "contraction_rate",
                "first_person_rate",
                "function_word_rate",
                "exclaim",
            )
        }
        print(f"unit {i}: {preview}")
    print("--- pairs ---")
    for i in range(len(units) - 1):
        pair = pairwise_feature_map(units[i], units[i + 1])
        preview = {
            key: round(pair[key], 4)
            for key in (
                "abs_contraction_rate",
                "abs_first_person_rate",
                "fw_cosine",
                "char_tri_cosine",
                "jaccard",
                "length_ratio",
            )
        }
        print(f"pair {i + 1}-{i + 2}: {preview}")
    return 0


def cmd_train(args: argparse.Namespace) -> int:
    bands = args.bands.split(",") if args.bands else None
    model = train_logreg(args.data_root, mode=args.mode, bands=bands, seed=args.seed)
    model.save(args.out)
    print(f"saved {args.out}")
    print("top weights:")
    for name, weight in model.fitted.top_weights(args.top):
        print(f"  {weight:+.3f}  {name}")
    return 0


def cmd_predict(args: argparse.Namespace) -> int:
    from scd.models import StyleChangeModel

    model = StyleChangeModel.load(args.model)
    written = predict_directory(model, args.input, args.output)
    print(f"wrote {written} solution files to {args.output}")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    scores = evaluate_directory(args.pred, args.truth, mode=args.mode)
    payload = scores.as_dict()
    if args.bootstrap:
        lo, hi = bootstrap_doc_f1(scores, n_boot=args.bootstrap, seed=args.seed)
        payload["bootstrap_f1_2.5"] = lo
        payload["bootstrap_f1_97.5"] = hi
    print(json.dumps(payload, indent=2))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    units = split_units(read_problem(args.problem), mode=args.mode)
    truth = read_truth(args.truth).changes if args.truth else None
    if truth is None:
        sibling = Path(args.problem).with_name(
            f"truth-problem-{problem_id(args.problem)}.json"
        )
        if sibling.exists():
            truth = read_truth(sibling).changes
            check_alignment(len(units), truth, path=sibling)
    pred = None
    proba = None
    if args.model:
        from scd.models import StyleChangeModel

        model = StyleChangeModel.load(args.model)
        pred = model.predict_units(units)
        proba = model.predict_proba_units(units).tolist()
    html = render_report(
        units,
        truth=truth,
        pred=pred,
        proba=proba,
        title=args.title or f"Report · {Path(args.problem).name}",
    )
    dest = write_report(args.out, html)
    print(f"wrote {dest}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    counts = write_corpus(args.out, seed=args.seed)
    print(f"wrote {counts} under {args.out} (seed={args.seed})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scd", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    inspect = sub.add_parser("inspect", help="Print units and optional truth cuts.")
    inspect.add_argument("problem")
    inspect.add_argument("--truth")
    inspect.add_argument("--mode", default="line")
    inspect.set_defaults(func=cmd_inspect)

    feats = sub.add_parser("features", help="Print a few unit and pair features.")
    feats.add_argument("problem")
    feats.add_argument("--mode", default="line")
    feats.set_defaults(func=cmd_features)

    train = sub.add_parser("train", help="Train the pairwise logistic baseline.")
    train.add_argument("--data-root", required=True)
    train.add_argument("--out", required=True)
    train.add_argument("--mode", default="line")
    train.add_argument("--bands", default="")
    train.add_argument("--seed", type=int, default=0)
    train.add_argument("--top", type=int, default=10)
    train.set_defaults(func=cmd_train)

    predict = sub.add_parser("predict", help="Write solution-problem-*.json files.")
    predict.add_argument("--model", required=True)
    predict.add_argument("-i", "--input", required=True)
    predict.add_argument("-o", "--output", required=True)
    predict.set_defaults(func=cmd_predict)

    ev = sub.add_parser("evaluate", help="Score a prediction directory.")
    ev.add_argument("--pred", required=True)
    ev.add_argument("--truth", required=True)
    ev.add_argument("--mode", default="line")
    ev.add_argument("--bootstrap", type=int, default=0)
    ev.add_argument("--seed", type=int, default=0)
    ev.set_defaults(func=cmd_evaluate)

    report = sub.add_parser("report", help="Write an HTML walk-through.")
    report.add_argument("--problem", required=True)
    report.add_argument("--truth")
    report.add_argument("--model")
    report.add_argument("--out", required=True)
    report.add_argument("--mode", default="line")
    report.add_argument("--title", default="")
    report.set_defaults(func=cmd_report)

    gen = sub.add_parser("generate", help="Regenerate the synthetic toy corpus.")
    gen.add_argument("--out", required=True)
    gen.add_argument("--seed", type=int, default=DEFAULT_SEED)
    gen.set_defaults(func=cmd_generate)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
