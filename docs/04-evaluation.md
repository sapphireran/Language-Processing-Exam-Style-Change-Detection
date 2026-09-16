# 04 — Evaluation

## The object that is scored

A document with `n` paragraphs produces a vector `y ∈ {0,1}^{n-1}`.
The evaluator compares your `ŷ` to gold `y` **inside that document**,
then aggregates over documents, then reports the three difficulty
bands separately.

Never concatenate every pair in the band into one giant F1 unless the
official script does that. Pair counts differ across documents.
PAN's 2023 statement is F1 per document; this lab reports both
per-document F1 and the unweighted mean over documents.

## Confusion matrix

Treat `1` (style change) as the positive class.

|  | Pred 1 | Pred 0 |
| --- | --- | --- |
| Gold 1 | TP | FN |
| Gold 0 | FP | TN |

```
precision = TP / (TP + FP)     # of your alarms, how many were real
recall    = TP / (TP + FN)     # of the real joins, how many you caught
F1        = 2PR / (P + R)
accuracy  = (TP + TN) / (TP + FP + TN + FN)
```

If a class has no predicted positives, precision is defined here as 0
(the lab does not invent a 1.0 for an empty prediction). That choice
matches "you predicted nothing, you get no credit for the positive
class", which is the conservative exam default. State it if asked.

## Why accuracy lies

A six-paragraph single-author document has gold `[0, 0, 0, 0, 0]`.
Predicting all zeros scores accuracy 1.0 and positive-class F1 0.0
(no positive class to hit, and if there *were* none, some scripts
skip the document). A detector that never predicts a change looks
brilliant on single-author pages and dies on multi-author pages.

Always report **positive-class F1** and **macro-F1**.

## Macro-F1

```
macro-F1 = (F1_{class=1} + F1_{class=0}) / 2
```

Class 0's F1 uses TN as its "true positives". Macro-F1 punishes a
system that only predicts zeros *and* a system that only predicts
ones. It is the number you quote when an examiner says "the labels
are imbalanced".

Micro-F1 on concatenated pairs is dominated by whichever documents
are longest. Do not confuse the two.

## Exact match

A document is exact if `ŷ = y` as vectors. Exact match is a harsh
teaching diagnostic; it is not the official PAN number. The lab
prints it so you can see whether errors are one-off or structural.

## Worked confusion matrix

Gold `y = [0, 1, 0, 1]`, prediction `ŷ = [0, 1, 1, 1]`.

- TP = 2 (positions 2 and 4)
- FP = 1 (position 3)
- TN = 1 (position 1)
- FN = 0

```
P = 2/3 ≈ 0.667
R = 2/2 = 1.0
F1 = 2 · 0.667 · 1 / 1.667 = 0.8
accuracy = 3/4 = 0.75
F1_{class=0}: TP0=TN=1, FP0=FN=0, FN0=FP=1
  P0 = 1/(1+0) = 1.0
  R0 = 1/(1+1) = 0.5
  F10 = 2·1·0.5 / 1.5 = 2/3 ≈ 0.667
macro-F1 = (0.8 + 0.667) / 2 ≈ 0.733
```

`scarfjoint.evaluate.document_scores` reproduces these figures. The
unit test in `tests/test_evaluate.py` locks them.

## What not to claim

The mean F1 on `examples/corpus` is a **collection score on original
teaching prose, with a threshold fit on the same prose**. It is not a
PAN result. Writing it on an exam as if it were would be a
methodology error, which is itself a style of mistake this course
likes to catch.
