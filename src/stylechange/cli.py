"""Command-line interface for the personal style-change toolkit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .detectors import build, load_model, save_model
from .evaluate import evaluate_dirs
from .features import FEATURE_NAMES, as_dict, extract_sentence
from .io import load_document, load_problem_dir, solution_path, write_solution
from .report import explain_text, pair_table, write_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="stylechange",
        description="Intrinsic sentence-level style-change detection (personal exam toolkit).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fit = sub.add_parser("fit", help="fit a supervised detector on labeled problems")
    p_fit.add_argument("--gold", required=True, help="directory of problem/truth files")
    p_fit.add_argument("--out", required=True, help="path to write model JSON")
    p_fit.add_argument("--detector", default="logistic", choices=["logistic", "threshold", "ensemble"])
    p_fit.add_argument("--split", default="train", help="manifest split to train on")
    p_fit.add_argument("--difficulty", default=None)

    p_det = sub.add_parser("detect", help="write solution-problem-*.json files")
    p_det.add_argument("--input", required=True, help="directory of problem-*.txt files")
    p_det.add_argument("--out", required=True, help="empty-ish output directory")
    p_det.add_argument("--model", default=None, help="fitted model JSON")
    p_det.add_argument("--detector", default="unsupervised", help="used when --model is omitted")

    p_ev = sub.add_parser("evaluate", help="score solution files against truth files")
    p_ev.add_argument("--gold", required=True)
    p_ev.add_argument("--pred", required=True)

    p_ex = sub.add_parser("explain", help="print a feature walkthrough for one document")
    p_ex.add_argument("--input", required=True, help="problem-*.txt or any text file")
    p_ex.add_argument("--gold", default=None, help="optional truth JSON")
    p_ex.add_argument("--model", default=None)
    p_ex.add_argument("--detector", default="unsupervised")
    p_ex.add_argument("--pairs", default=None, help="how many pairs to print, e.g. 4")

    p_rep = sub.add_parser("report", help="write an HTML colour-coded report")
    p_rep.add_argument("--gold", required=True)
    p_rep.add_argument("--pred", required=True)
    p_rep.add_argument("--html", required=True)
    p_rep.add_argument("--title", default="Style-change report")

    p_demo = sub.add_parser("demo", help="run the unsupervised detector on a synthetic split")
    p_demo.add_argument("--split", default="hard", choices=["easy", "medium", "hard"])
    p_demo.add_argument("--root", default="data/synthetic")

    p_feat = sub.add_parser("features", help="print the feature vector of a sentence")
    p_feat.add_argument("--text", required=True)

    args = parser.parse_args(argv)
    handlers = {
        "fit": _cmd_fit,
        "detect": _cmd_detect,
        "evaluate": _cmd_evaluate,
        "explain": _cmd_explain,
        "report": _cmd_report,
        "demo": _cmd_demo,
        "features": _cmd_features,
    }
    return handlers[args.cmd](args)


def _select_problems(gold: str, split: str | None, difficulty: str | None, require_truth: bool):
    problems = load_problem_dir(gold, require_truth=require_truth, split=split, difficulty=difficulty)
    if split:
        filtered = [p for p in problems if p.meta.get("split") == split]
        if filtered:
            problems = filtered
    return problems


def _cmd_fit(args: argparse.Namespace) -> int:
    problems = _select_problems(args.gold, args.split, args.difficulty, require_truth=True)
    if not problems:
        print(f"no labeled problems under {args.gold}", file=sys.stderr)
        return 2
    detector = build(args.detector)
    detector.fit(problems)
    save_model(detector, args.out)
    print(f"fitted {detector.name} on {len(problems)} documents → {args.out}")
    return 0


def _resolve_detector(args: argparse.Namespace):
    if getattr(args, "model", None):
        return load_model(args.model)
    return build(args.detector)


def _cmd_detect(args: argparse.Namespace) -> int:
    detector = _resolve_detector(args)
    problems = load_problem_dir(args.input, require_truth=False)
    if not problems:
        print(f"no problem-*.txt files under {args.input}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for problem in problems:
        pred = detector.predict_document(problem.sentences)
        write_solution(solution_path(out, problem.pid), pred)
    print(f"wrote {len(problems)} solutions to {out}")
    return 0


def _cmd_evaluate(args: argparse.Namespace) -> int:
    result = evaluate_dirs(args.gold, args.pred)
    print(result)
    return 0


def _cmd_explain(args: argparse.Namespace) -> int:
    sentences = load_document(args.input)
    gold = None
    gold_path = args.gold
    if gold_path is None:
        candidate = Path(args.input).with_name(f"truth-problem-{Path(args.input).name.split('-')[-1].replace('.txt', '')}.json")
        if candidate.is_file():
            gold_path = str(candidate)
    if gold_path:
        gold = json.loads(Path(gold_path).read_text(encoding="utf-8")).get("changes")
    detector = _resolve_detector(args)
    try:
        pred = detector.predict_document(sentences)
    except RuntimeError:
        pred = None
    limit = int(args.pairs) if args.pairs else None
    print(
        explain_text(sentences, gold=gold, pred=pred, pair_limit=limit)
    )
    if pred is not None:
        print(pair_table(sentences, gold, pred))
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    problems = load_problem_dir(args.gold, require_truth=True)
    pred_dir = Path(args.pred)
    docs = []
    for problem in problems:
        sol = pred_dir / f"solution-problem-{problem.pid}.json"
        pred = json.loads(sol.read_text(encoding="utf-8"))["changes"] if sol.is_file() else []
        docs.append(
            {
                "pid": problem.pid,
                "sentences": problem.sentences,
                "gold": problem.changes,
                "pred": pred,
                "notes": problem.meta.get("topic") or problem.meta.get("notes") or "",
            }
        )
    path = write_html(args.html, args.title, docs)
    print(f"wrote {path}")
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    root = Path(args.root) / args.split
    if not root.is_dir():
        print(f"missing {root}", file=sys.stderr)
        return 2
    out = Path("output") / f"{args.split}-unsupervised"
    detect_ns = argparse.Namespace(input=str(root), out=str(out), model=None, detector="unsupervised")
    _cmd_detect(detect_ns)
    ev = argparse.Namespace(gold=str(root), pred=str(out))
    print(f"--- unsupervised on {args.split} ---")
    _cmd_evaluate(ev)
    html_path = Path("reports") / f"{args.split}-unsupervised.html"
    _cmd_report(
        argparse.Namespace(
            gold=str(root),
            pred=str(out),
            html=str(html_path),
            title=f"Unsupervised detector · {args.split} split",
        )
    )
    return 0


def _cmd_features(args: argparse.Namespace) -> int:
    vector = extract_sentence(args.text)
    mapping = as_dict(vector)
    width = max(len(name) for name in FEATURE_NAMES)
    for name in FEATURE_NAMES:
        print(f"{name:<{width}}  {mapping[name]:.4f}")
    return 0
