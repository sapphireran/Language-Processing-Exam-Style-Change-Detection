# 07 — Metrics

I will be asked to compute a number. This page is the number.

## Pairwise macro-F1 (the one that matters)

Gold and prediction are binary vectors of length `n_units - 1`.

For each class `c ∈ {0, 1}`:

```
P_c = TP_c / (TP_c + FP_c)
R_c = TP_c / (TP_c + FN_c)
F1_c = 2 P_c R_c / (P_c + R_c)
```

Macro-F1 is `(F1_0 + F1_1) / 2`.

I do **not** average F1 per document and then talk as if that were the
official sentence-level score. Current write-ups average over pairs.
If a question says "macro-F1 across documents", I follow that wording
and say so.

### Empty-class convention

A single-author gold vector is all zeros. Class `1` has `TP=0`,
`FP=0`, `FN=0` if I also predict all zeros.

I take `P=1` and `R=1` when the denominator is zero. Then both class
F1s are 1 and macro-F1 is 1. That matches the intuition "I did not
invent a writer".

If I instead define `0/0 = 0`, an all-zero document scores 0.5 even
when I was perfect. I will mention the convention before I write the
number.

### Worked example

Gold:    `0 0 1 0 0`
Pred:    `0 1 1 0 0`

Class 1 (change): `TP=1`, `FP=1`, `FN=0` → `P=1/2`, `R=1`, `F1=2/3`

Class 0 (same):   `TP=3`, `FP=0`, `FN=1` → `P=1`, `R=3/4`, `F1=6/7 ≈ 0.857`

Macro-F1 ≈ `(0.667 + 0.857) / 2 = 0.762`

`examples/walkthrough_f1.py` prints the same arithmetic.

## Accuracy is a trap

If 90% of pairs are `0`, always predicting `0` looks accurate and
scores a miserable class-1 F1. I will not lead with accuracy.

## Task 1 (single cut) is almost accuracy on a one-hot

If every document has exactly one `1`, macro-F1 and "did you hit the
cut" tell a similar story. I still compute F1 so I can reuse the
script.

## Author ids: adjusted Rand index

Task 2 emits a label per unit. The labels are arbitrary. `1,1,2,2`
and `7,7,3,3` are the same clustering.

ARI asks: of all pairs of units, how often do gold and pred agree on
"same author" versus "different author", adjusted for chance.

```
ARI = (Index − Expected) / (Max − Expected)
```

I implement it from the contingency table in `examscd.evaluate`. I do
not need sklearn in the exam. A perfect return-author labelling on
`04_minutes_return` (`1,1,1,1,2,2,2,2,1,1,1,1`) should score 1.0
against a permutation of itself.

If I refuse to detect returns and mint a new id every cut, ARI drops
even when every boundary was right. That is the sentence I need: **F1
on `changes` can be 1.0 while ARI is not.**

## Other names I should recognise

- **DER / JER** — diarization / Jaccard error, used as secondary
  measures in some older task-2 write-ups. Lower is better. I will not
  compute them unless asked.
- **BCubed** — another clustering F-score. Same job as ARI, different
  formula.
- **WindowDiff / Pk** — text-segmentation metrics. They punish near
  misses less than exact-pair F1. Mention them if the question is
  about segmentation rather than authorship.

## What I put on the board

```
pairs     → macro-F1 (class 0 and class 1)
authors   → ARI (label permutation invariant)
claim     → never from easy-split accuracy alone
```
