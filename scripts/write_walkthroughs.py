#!/usr/bin/env python3
"""Write pair walkthroughs that quote the live detector, not remembered numbers."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seamtrace.corpus import load_teaching_corpus
from seamtrace.detectors import ThresholdDetector
from seamtrace.evaluate import score_pairs
from seamtrace.explain import explain_document
from seamtrace.pairwise import score_document

OUT = ROOT / "examples" / "walkthroughs"
PICKS = {
    "easy": "problem-02-bikes-vellum",
    "medium": "problem-10-committee-slack",
    "hard": "problem-14-two-bakers",
    "control": "problem-20-campus-return",
}


def render(doc, detector: ThresholdDetector) -> str:
    table = doc.table()
    pred = detector.predict(table)
    metrics = score_pairs(doc.changes, pred)
    rows = score_document(table)
    exps = explain_document(table, pred, doc.changes, threshold=detector.threshold)
    lines = [
        f"# Walkthrough — {doc.title}",
        "",
        f"File: `{doc.problem_path.name}`  ·  tier: **{doc.tier}**  ·  "
        f"voices: {', '.join(doc.voices)}",
        "",
        f"Default threshold detector (τ = {detector.threshold:.2f}): "
        f"macro-F1 {metrics.macro_f1:.3f}, change-F1 {metrics.f1_1:.3f}, "
        f"stay-F1 {metrics.f1_0:.3f}. Cells: tp={metrics.tp} fp={metrics.fp} "
        f"fn={metrics.fn} tn={metrics.tn}.",
        "",
        "Numbers come from `seamtrace` on this revision. Re-run "
        "`scripts/write_walkthroughs.py` if you move the cut.",
        "",
        "| i | gold | pred | score | fw | tri | Δ | label |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for exp, row in zip(exps, rows):
        lines.append(
            f"| {exp.index} | {exp.gold} | {exp.pred} | {exp.score:.3f} | "
            f"{row.function_words:.2f} | {row.trigrams:.2f} | {row.delta:.2f} | "
            f"{exp.label} |"
        )
    lines.extend(["", "## Boundaries", ""])
    for exp in exps:
        left = doc.units[exp.index]
        right = doc.units[exp.index + 1]
        lines.append(f"### Pair {exp.index} — `{exp.label}`")
        lines.append("")
        lines.append(f"- Score {exp.score:.3f} ({exp.note})")
        lines.append(f"- Left: {left}")
        lines.append(f"- Right: {right}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    docs = {doc.stem: doc for doc in load_teaching_corpus()}
    detector = ThresholdDetector()
    index = ["# Walkthroughs", "", "Generated from the live detector.", ""]
    for tier, stem in PICKS.items():
        text = render(docs[stem], detector)
        dest = OUT / f"{tier}.md"
        dest.write_text(text + "\n", encoding="utf-8")
        index.append(f"- [{tier}]({dest.name}) — {docs[stem].title}")
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"wrote {len(PICKS)} walkthroughs to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
