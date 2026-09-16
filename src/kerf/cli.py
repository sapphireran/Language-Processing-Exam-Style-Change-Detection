"""Command line for the personal exam lab."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .detect import detect_path
from .io import write_prediction
from .report import directory_report, document_report, feature_table


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="kerf",
        description="Saw a document at a stylometric change-point.",
    )
    parser.add_argument("--version", action="version", version=f"kerf {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ins = sub.add_parser("inspect", help="print hinge table for one problem file")
    p_ins.add_argument("path")

    p_pred = sub.add_parser("predict", help="write a PAN-shaped prediction JSON")
    p_pred.add_argument("path")
    p_pred.add_argument("-o", "--out", required=True)

    p_feat = sub.add_parser("features", help="top weighted features for a paragraph file")
    p_feat.add_argument("path")
    p_feat.add_argument("--paragraph", type=int, default=0)

    p_score = sub.add_parser("score", help="score a directory of problem/truth pairs")
    p_score.add_argument("directory")

    args = parser.parse_args(argv)
    if args.cmd == "inspect":
        sys.stdout.write(document_report(args.path))
        return 0
    if args.cmd == "predict":
        det = detect_path(args.path)
        write_prediction(args.out, det.changes, authors=det.authors_guess)
        return 0
    if args.cmd == "features":
        text = Path(args.path).read_text(encoding="utf-8")
        from .text import split_paragraphs

        paras = split_paragraphs(text)
        if args.paragraph < 0 or args.paragraph >= len(paras):
            sys.stderr.write(f"paragraph {args.paragraph} out of range 0..{len(paras) - 1}\n")
            return 2
        sys.stdout.write(feature_table(paras[args.paragraph]))
        return 0
    if args.cmd == "score":
        sys.stdout.write(directory_report(args.directory))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
