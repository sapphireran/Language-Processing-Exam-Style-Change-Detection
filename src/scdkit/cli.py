"""Command-line surface for the personal exam lab."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .detect import explain_document
from .evaluate import evaluate_collection, format_table
from .features import extract_features
from .generate import load_author_bank, write_mix
from .io import load_document, load_truth, write_prediction
from .report import render_collection_html, render_document_html, write_html
from .tokenize import split_paragraphs


def _add_method(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--method",
        default="ensemble",
        choices=("ensemble", "delta", "char", "formality", "cusum", "register", "pronoun", "person"),
        help="detector channel (default: ensemble)",
    )


def cmd_detect(args: argparse.Namespace) -> int:
    text = load_document(args.document) if args.document != "-" else sys.stdin.read()
    detection = explain_document(text, method=args.method)
    if args.explain:
        print(f"# {Path(args.document).name if args.document != '-' else 'stdin'}")
        print(f"paragraphs\t{len(detection.paragraphs)}")
        print(f"changes\t{list(detection.changes)}")
        for pair in detection.pairs:
            flag = "CHANGE" if pair.change else "same  "
            print(
                f"{pair.index + 1}->{pair.index + 2}\t{flag}\t"
                f"Δ={pair.delta:.2f} char={pair.char:.2f} "
                f"form={pair.formality:.2f} reg={pair.register:.2f} "
                f"person={pair.person:.0f} pron={pair.pronoun:.2f} "
                f"topic={pair.topic:.2f}"
            )
            if pair.reasons:
                print("    " + "; ".join(pair.reasons))
            if args.preview:
                print(f"    L: {pair.left_preview}")
                print(f"    R: {pair.right_preview}")
    else:
        print(json.dumps({"changes": list(detection.changes)}, indent=2))
    if args.out:
        write_prediction(args.out, detection.changes)
    return 0


def cmd_features(args: argparse.Namespace) -> int:
    text = load_document(args.document)
    for i, para in enumerate(split_paragraphs(text), start=1):
        feat = extract_features(para)
        row = {"paragraph": i, **feat.as_dict()}
        if args.json:
            print(json.dumps(row, ensure_ascii=True))
        else:
            print(
                f"P{i}\twords={feat.n_words}\tsent={feat.mean_sent_len:.1f}\t"
                f"ttr={feat.ttr:.2f}\tcontr={feat.contraction_rate:.2f}\t"
                f"form={feat.formality:.2f}\tI={feat.pronoun_i:.2f}\t"
                f"you={feat.pronoun_you:.2f}\tone={feat.pronoun_one:.2f}"
            )
    return 0


def cmd_eval(args: argparse.Namespace) -> int:
    score = evaluate_collection(args.documents, args.truth, method=args.method)
    print(format_table(score))
    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(score.as_dict(), indent=2) + "\n", encoding="utf-8"
        )
    if args.html_out:
        write_html(args.html_out, render_collection_html(score))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    text = load_document(args.document)
    detection = explain_document(text, method=args.method)
    gold = list(load_truth(args.truth).changes) if args.truth else None
    title = args.title or Path(args.document).stem
    write_html(args.out, render_document_html(detection, title=title, gold=gold))
    print(args.out)
    return 0


def cmd_mix(args: argparse.Namespace) -> int:
    cards = load_author_bank(args.authors)
    doc, gold = write_mix(cards, args.pattern, args.out_dir, args.stem, seed=args.seed)
    print(doc)
    print(gold)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    methods = args.methods or ["ensemble", "delta", "char", "formality", "cusum"]
    print("method      macro-F1  micro-F1")
    print("---------   --------  --------")
    for method in methods:
        score = evaluate_collection(args.documents, args.truth, method=method)
        print(f"{method:<10}  {score.macro_f1:8.3f}  {score.micro.f1:8.3f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scdkit",
        description="Personal exam lab for intrinsic style-change detection.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_det = sub.add_parser("detect", help="flag adjacent style changes")
    p_det.add_argument("document")
    p_det.add_argument("--explain", action="store_true")
    p_det.add_argument("--preview", action="store_true")
    p_det.add_argument("--out")
    _add_method(p_det)
    p_det.set_defaults(func=cmd_detect)

    p_feat = sub.add_parser("features", help="print paragraph fingerprints")
    p_feat.add_argument("document")
    p_feat.add_argument("--json", action="store_true")
    p_feat.set_defaults(func=cmd_features)

    p_eval = sub.add_parser("eval", help="score a gold collection")
    p_eval.add_argument("documents")
    p_eval.add_argument("--truth")
    p_eval.add_argument("--json-out")
    p_eval.add_argument("--html-out")
    _add_method(p_eval)
    p_eval.set_defaults(func=cmd_eval)

    p_rep = sub.add_parser("report", help="write an HTML walkthrough")
    p_rep.add_argument("document")
    p_rep.add_argument("--truth")
    p_rep.add_argument("--out", default="report.html")
    p_rep.add_argument("--title")
    _add_method(p_rep)
    p_rep.set_defaults(func=cmd_report)

    p_mix = sub.add_parser("mix", help="stack author cards into a new document")
    p_mix.add_argument("authors", help="directory of author JSON cards")
    p_mix.add_argument("pattern", help="e.g. AABBA or ABA")
    p_mix.add_argument("--out-dir", default="examples/generated")
    p_mix.add_argument("--stem", default="mixed")
    p_mix.add_argument("--seed", type=int, default=0)
    p_mix.set_defaults(func=cmd_mix)

    p_cmp = sub.add_parser("compare", help="macro-F1 by method on a collection")
    p_cmp.add_argument("documents")
    p_cmp.add_argument("--truth")
    p_cmp.add_argument("--methods", nargs="+")
    p_cmp.set_defaults(func=cmd_compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
