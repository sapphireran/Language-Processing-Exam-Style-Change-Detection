"""Command-line entry point: detect, features, evaluate, plot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from style_change.detectors import StyleChangeDetector
from style_change.evaluate import evaluate_document
from style_change.features import FeatureExtractor, describe_features
from style_change.io import load_document, load_labels
from style_change.visualize import format_report, plot_distances


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="style-change",
        description="Stylometric style-change detection for exam study.",
    )
    parser.add_argument("--min-words", type=int, default=8, help="skip shorter paragraphs")
    parser.add_argument("--distance-floor", type=float, default=0.75)
    parser.add_argument("--mad-k", type=float, default=1.6)
    parser.add_argument("--min-gap", type=float, default=0.45, help="minimum knee gap to call a document mixed")
    sub = parser.add_subparsers(dest="command", required=True)

    detect = sub.add_parser("detect", help="run Tasks 1–3 on a document")
    detect.add_argument("document", type=Path)
    detect.add_argument("--json", action="store_true", help="print machine-readable output")

    feats = sub.add_parser("features", help="print headline stylometric features")
    feats.add_argument("document", type=Path)

    ev = sub.add_parser("evaluate", help="score a prediction against gold labels")
    ev.add_argument("document", type=Path)
    ev.add_argument("labels", type=Path)

    plot = sub.add_parser("plot", help="write an adjacent-distance figure")
    plot.add_argument("document", type=Path)
    plot.add_argument("-o", "--output", type=Path, default=Path("distance.png"))
    return parser


def _detector(args: argparse.Namespace) -> StyleChangeDetector:
    return StyleChangeDetector(
        extractor=FeatureExtractor(min_words=args.min_words),
        distance_floor=args.distance_floor,
        mad_k=args.mad_k,
        min_words=args.min_words,
        min_gap=args.min_gap,
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    document = load_document(args.document)
    detector = _detector(args)
    table, result = detector.detect_document(document)

    if args.command == "detect":
        if args.json:
            print(json.dumps(result.as_dict(), indent=2))
        else:
            print(format_report(document, table, result))
        return 0

    if args.command == "features":
        print(describe_features(table))
        print()
        print(f"{len(table.names)} features, {table.matrix.shape[0]} paragraphs")
        return 0

    if args.command == "evaluate":
        labels = load_labels(args.labels)
        authors = labels.get("authors")
        if authors is None:
            parser.error("label file must include an 'authors' list")
        report = evaluate_document(
            result,
            gold_authors=authors,
            gold_multi=labels.get("multi_author"),
            gold_changes=labels.get("changes"),
        )
        print(format_report(document, table, result))
        print()
        print(report.summary())
        return 0

    if args.command == "plot":
        path = plot_distances(result, args.output)
        print(f"wrote {path}")
        return 0

    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
