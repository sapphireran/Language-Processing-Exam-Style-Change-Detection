"""Command-line lab interface.

Examples::

    python -m scarfjoint split examples/corpus/easy/problem-01-ferry-marsh-knit.txt
    python -m scarfjoint features examples/corpus/easy/problem-01-ferry-marsh-knit.txt
    python -m scarfjoint detect examples/corpus/easy/problem-01-ferry-marsh-knit.txt --explain
    python -m scarfjoint eval examples/corpus
    python -m scarfjoint predict-dir /tmp/in /tmp/out
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .detectors import ScarfDetector
from .evaluate import document_scores, mean_bundle
from .features import extract_features
from .io import iter_corpus, load_problem, load_truth, solution_name_for, truth_path_for, write_solution
from .report import format_detection, format_metrics, preview_paragraph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scarfjoint", description="Personal style-change exam lab")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_split = sub.add_parser("split", help="show paragraph segmentation")
    p_split.add_argument("document")

    p_feat = sub.add_parser("features", help="print a dense fingerprint per paragraph")
    p_feat.add_argument("document")

    p_det = sub.add_parser("detect", help="predict adjacent style changes")
    p_det.add_argument("document")
    p_det.add_argument("--explain", action="store_true")
    p_det.add_argument("--threshold", type=float, default=None)
    p_det.add_argument("--use-topic", action="store_true", help="let topic Jaccard vote (leakage demo)")
    p_det.add_argument("--json", action="store_true")

    p_eval = sub.add_parser("eval", help="score a labelled corpus directory")
    p_eval.add_argument("corpus")
    p_eval.add_argument("--threshold", type=float, default=None)
    p_eval.add_argument("--use-topic", action="store_true")
    p_eval.add_argument("--json", action="store_true")

    p_pred = sub.add_parser("predict-dir", help="PAN-shaped batch: problem-*.txt → solution-problem-*.json")
    p_pred.add_argument("input_dir")
    p_pred.add_argument("output_dir")
    p_pred.add_argument("--threshold", type=float, default=None)

    args = parser.parse_args(argv)
    if args.cmd == "split":
        return _cmd_split(args.document)
    if args.cmd == "features":
        return _cmd_features(args.document)
    if args.cmd == "detect":
        return _cmd_detect(args)
    if args.cmd == "eval":
        return _cmd_eval(args)
    if args.cmd == "predict-dir":
        return _cmd_predict_dir(args)
    parser.error(f"unknown command {args.cmd}")
    return 2


def _detector(args) -> ScarfDetector:
    kwargs = {}
    threshold = getattr(args, "threshold", None)
    if threshold is not None:
        kwargs["threshold"] = threshold
    if getattr(args, "use_topic", False):
        kwargs["use_topic"] = True
    return ScarfDetector(**kwargs)


def _cmd_split(document: str) -> int:
    doc = load_problem(document)
    print(f"{doc.path}  paragraphs={len(doc.paragraphs)}")
    for i, para in enumerate(doc.paragraphs, start=1):
        print(f"\n--- P{i} ({len(para.split())} words) ---")
        print(para)
    return 0


def _cmd_features(document: str) -> int:
    doc = load_problem(document)
    for i, para in enumerate(doc.paragraphs, start=1):
        feat = extract_features(para)
        print(
            json.dumps(
                {
                    "paragraph": i,
                    "n_words": feat.n_words,
                    "mean_word_len": round(feat.mean_word_len, 3),
                    "mean_sent_len": round(feat.mean_sent_len, 3),
                    "guiraud": round(feat.richness.guiraud, 3),
                    "yule_k": round(feat.richness.yule_k, 3),
                    "honore_r": round(feat.richness.honore_r, 3),
                    "contraction_rate": round(feat.contraction_rate, 4),
                    "first_person_rate": round(feat.first_person_rate, 4),
                    "second_person_rate": round(feat.second_person_rate, 4),
                    "academic_rate": round(feat.academic_rate, 4),
                    "informal_rate": round(feat.informal_rate, 4),
                    "flesch_proxy": round(feat.flesch_proxy, 2),
                    "preview": preview_paragraph(para, 72),
                },
                indent=2,
            )
        )
    return 0


def _cmd_detect(args) -> int:
    doc = load_problem(args.document)
    detection = _detector(args).detect(doc.paragraphs)
    if args.json:
        print(json.dumps({"changes": detection.changes}, indent=2))
        return 0
    gold = doc.gold_changes
    if gold is None:
        tpath = truth_path_for(doc.path)
        if tpath.exists():
            gold = [int(x) for x in load_truth(tpath).get("changes", [])]
    print(format_detection(detection, gold=gold))
    return 0


def _cmd_eval(args) -> int:
    docs = iter_corpus(args.corpus)
    if not docs:
        print(f"no problem-*.txt files under {args.corpus}", file=sys.stderr)
        return 1
    detector = _detector(args)
    bundles = []
    rows = []
    for doc in docs:
        gold = doc.gold_changes
        if gold is None:
            print(f"skip (no truth): {doc.path}", file=sys.stderr)
            continue
        pred = detector.detect(doc.paragraphs).changes
        if len(pred) != len(gold):
            print(
                f"length mismatch {doc.path}: gold={len(gold)} pred={len(pred)} paras={len(doc.paragraphs)}",
                file=sys.stderr,
            )
        bundle = document_scores(gold, pred)
        bundles.append(bundle)
        rel = str(doc.path)
        rows.append((rel, bundle, pred, gold))
        if not args.json:
            print(format_metrics(doc.path.name, bundle))
    summary = mean_bundle(bundles)
    if args.json:
        print(
            json.dumps(
                {
                    "summary": summary,
                    "documents": [
                        {
                            "path": rel,
                            "pred": pred,
                            "gold": gold,
                            "f1": bundle.f1,
                            "macro_f1": bundle.macro_f1,
                        }
                        for rel, bundle, pred, gold in rows
                    ],
                },
                indent=2,
            )
        )
    else:
        print()
        print(
            "mean over documents:  "
            f"F1={summary.get('f1', 0):.3f}  "
            f"macro-F1={summary.get('macro_f1', 0):.3f}  "
            f"acc={summary.get('accuracy', 0):.3f}  "
            f"exact={summary.get('exact_match', 0):.3f}"
        )
    return 0


def _cmd_predict_dir(args) -> int:
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    detector = _detector(args)
    problems = sorted(input_dir.glob("problem-*.txt"))
    if not problems:
        problems = sorted(input_dir.rglob("problem-*.txt"))
    if not problems:
        print(f"no problem-*.txt in {input_dir}", file=sys.stderr)
        return 1
    for path in problems:
        doc = load_problem(path)
        changes = detector.detect(doc.paragraphs).changes
        dest = output_dir / solution_name_for(path)
        write_solution(dest, changes)
        print(f"{path.name} → {dest.name}  {changes}")
    return 0
