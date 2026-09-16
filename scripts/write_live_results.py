#!/usr/bin/env python3
"""Rewrite docs/15-live-results.md from the current detector."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hingemark.calibrate import grid_thresholds
from hingemark.corpus import list_corpus
from hingemark.detectors import DEFAULT_THRESHOLD, always_change, never_change, threshold_detect
from hingemark.evaluate import accuracy_trap, score_corpus, score_pairs
from hingemark.pairwise import score_unit_hinges
from hingemark.report import detect_item, evaluate_items, format_corpus_table


def main() -> int:
    items = list_corpus()
    scored = evaluate_items(items)
    never = score_corpus(
        (
            it.name,
            it.truth.changes,
            never_change(score_unit_hinges(it.problem.units)).changes,
        )
        for it in items
    )
    always = score_corpus(
        (
            it.name,
            it.truth.changes,
            always_change(score_unit_hinges(it.problem.units)).changes,
        )
        for it in items
    )
    trap = accuracy_trap()
    grid = grid_thresholds(items)[:5]
    splits: dict[str, list[float]] = {}
    named = []
    for item in items:
        pred = detect_item(item).changes
        report = score_pairs(item.truth.changes, pred)
        splits.setdefault(item.split, []).append(report.macro_f1)
        named.append((item, pred, report))

    split_lines = ["| split | n | mean macro-F1 |", "| --- | ---: | ---: |"]
    for split, vals in splits.items():
        split_lines.append(f"| {split} | {len(vals)} | {sum(vals)/len(vals):.3f} |")

    grid_lines = ["| τ | mean macro-F1 | micro macro-F1 | mean acc |", "| ---: | ---: | ---: | ---: |"]
    for row in grid:
        grid_lines.append(
            f"| {row.threshold:.2f} | {row.mean_macro_f1:.3f} | {row.micro_macro_f1:.3f} | {row.mean_accuracy:.3f} |"
        )

    spotlight = []
    want = (
        "canal-then-lot",
        "quince-batch-then-letter",
        "two-mycologists",
        "river-three-topics",
        "spark-three-chats",
        "canal-return",
        "tidepool-gift-abstract",
        "exam-two-answers",
    )
    for item, pred, report in named:
        if not any(s in item.name for s in want):
            continue
        spotlight.append(
            f"- `{item.name}` ({item.split}): gold `{''.join(map(str, item.truth.changes))}` "
            f"pred `{''.join(map(str, pred))}` macro-F1 {report.macro_f1:.3f}"
        )

    table = format_corpus_table(items, scored, DEFAULT_THRESHOLD)
    body = f"""# Live results

Numbers from `scripts/write_live_results.py` on this revision. Teaching scores, not a leaderboard.

## Headlines

- Default cut **{DEFAULT_THRESHOLD:.2f}**
- Documents {scored.documents}, hinges {scored.hinges}
- Mean per-document macro-F1 **{scored.mean_macro_f1:.3f}**
- Mean accuracy {scored.mean_accuracy:.3f} (do not quote this first)
- Micro macro-F1 {scored.micro.macro_f1:.3f}
- Never-fire mean macro-F1 {never.mean_macro_f1:.3f}
- Always-fire mean macro-F1 {always.mean_macro_f1:.3f}
- Hand-calculation trap: accuracy {trap.accuracy:.3f}, macro-F1 {trap.macro_f1:.3f}

## By split

{chr(10).join(split_lines)}

Hard is supposed to look worse than medium. If it does not, the blender is cheating with topic.

## Spotlight

{chr(10).join(spotlight)}

## Top of the threshold grid

{chr(10).join(grid_lines)}

## Full table

```
{table}
```

Regenerate:

```bash
PYTHONPATH=src python3 scripts/write_live_results.py
```
"""
    dest = ROOT / "docs/15-live-results.md"
    dest.write_text(body, encoding="utf-8")
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
