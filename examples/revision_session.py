#!/usr/bin/env python3
"""One sitting: walk a hard document, then score unsupervised vs logistic."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stylechange.detectors import LogisticDetector, UnsupervisedDetector  # noqa: E402
from stylechange.evaluate import evaluate_aligned  # noqa: E402
from stylechange.io import load_problem_dir  # noqa: E402
from stylechange.report import explain_text, write_html  # noqa: E402


def main() -> int:
    hard = load_problem_dir(ROOT / "data" / "synthetic" / "hard", require_truth=True)
    train = [item for item in load_problem_dir(ROOT / "data" / "synthetic", require_truth=True) if item.meta.get("split") == "train"]
    focus = next(item for item in hard if item.pid == "001")

    unsupervised = UnsupervisedDetector()
    logistic = LogisticDetector()
    logistic.fit(train)

    pred_u = unsupervised.predict_document(focus.sentences)
    pred_l = logistic.predict_document(focus.sentences)

    print("=== hard/problem-001 (Mira → Jules → Hale, pour-over) ===\n")
    print(explain_text(focus.sentences, gold=focus.changes, pred=pred_u, pair_limit=4))

    gold = {item.pid: item.changes or [] for item in hard}
    for name, detector in ("unsupervised", unsupervised), ("logistic", logistic):
        pred = {item.pid: detector.predict_document(item.sentences) for item in hard}
        result = evaluate_aligned(gold, pred)
        print(f"--- {name} on all hard documents ---")
        print(result)
        print()

    docs = []
    for item in hard:
        docs.append(
            {
                "pid": item.pid,
                "sentences": item.sentences,
                "gold": item.changes,
                "pred": unsupervised.predict_document(item.sentences),
                "notes": item.meta.get("topic", ""),
            }
        )
    html_path = ROOT / "reports" / "revision-hard-unsupervised.html"
    write_html(html_path, "Revision sitting · hard split · unsupervised", docs)
    print(f"HTML report: {html_path}")
    print("Compare: pred_u", pred_u, "pred_l", pred_l, "gold", focus.changes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
