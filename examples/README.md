# Examples

All documents under `data/` are original. They follow the PAN-style
layout (`problem-*.txt` + `truth-problem-*.json`) so the same commands
work on every split.

```
data/
  easy/      topic *and* register jump (teaching set)
  medium/    one situation, two registers
  hard/      one topic, close registers + one single-author hard control
  control/   single-author, used to measure false positives
```

## Commands

From the repo root:

```bash
PYTHONPATH=src python3 -m stylechange.cli inspect examples/data/easy/problem-001.txt
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/easy
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/hard
PYTHONPATH=src python3 -m stylechange.cli detect examples/data/easy -o /tmp/easy-out
```

Or run every split at once:

```bash
PYTHONPATH=src python3 scripts/run_curriculum.py
```

## What each walkthrough is for

| File | Point |
| --- | --- |
| [walkthrough_easy.md](walkthrough_easy.md) | Style and topic agree; read the feature flip |
| [walkthrough_medium.md](walkthrough_medium.md) | Same topic (coffee / dough / canal), alternating voices |
| [walkthrough_hard.md](walkthrough_hard.md) | Where the baseline still works, and where it lies |
| [topic_confound.md](topic_confound.md) | Content-word cosine vs style distance |
| [false_friends.md](false_friends.md) | Single-author drift that looks like a change |
| [hand_calculation.md](hand_calculation.md) | TTR and function-word cosine you can do on paper |

## Live scores (fixed threshold 0.33)

Recorded from `stylechange.cli eval` in this revision:

| Split | macro-F1 | micro-F1 | Note |
| --- | --- | --- | --- |
| Easy | 1.000 | 1.000 | 6 TP, 0 FP |
| Medium | 1.000 | 1.000 | 7 TP, 0 FP |
| Hard | 0.333 | 0.400 | 1 TP, 2 FP, 1 FN |
| Control | 0.000 | 0.000 | 2 FP on 4 boundaries |

If you retune `--threshold`, update this table. The numbers are the
lesson, not a leaderboard claim.
