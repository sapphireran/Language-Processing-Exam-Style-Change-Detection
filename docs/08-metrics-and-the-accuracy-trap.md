# Metrics and the accuracy trap

Holds dominate. A detector that never fires looks competent on accuracy.

## The 16/4 hand calculation

Gold: sixteen 0s and four 1s. Pred: twenty 0s.

|  | pred 0 | pred 1 |
| --- | --- | --- |
| gold 0 | TN = 16 | FP = 0 |
| gold 1 | FN = 4 | TP = 0 |

- Accuracy = 16/20 = **0.800**
- Change precision = 0 / (0+0) = 0, recall = 0/4 = 0, F1 = **0**
- Hold precision = 16/20 = 0.800, recall = 16/16 = 1, F1 = 2·0.8·1 / 1.8 = **0.889**
- Macro-F1 = (0 + 0.889) / 2 = **0.444**

`hingemark trap` and `scripts/check_hand_calculation.py` lock these numbers.

## What to report

- **Macro-F1** of the two classes (change vs hold). This is what the notes compare across files.
- **Change-class F1** when you care about finding seams.
- **Accuracy** only as a warning light.

Per-document macro-F1 on a 5-hinge file is jumpy. The live table therefore also prints micro-F1 over all 140 hinges.

## Baselines you must beat in words, not just numbers

- `never`: all zeros. Wins accuracy, loses change-F1.
- `always`: all ones. Wins recall, floods false alarms.
- A topic detector: wins easy, loses controls.

The default threshold detector is a register blender. On this revision it beats `never` on macro-F1 and loses to `never` on some hard files. That loss is documented in `15-live-results.md`.
