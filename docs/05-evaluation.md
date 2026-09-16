# 5. Evaluation

## Official-style metric: macro F1 over pairs

Treat every consecutive pair in the evaluation set as one binary
example. Compute precision and recall **per class** (`0` and `1`) and
average them:

```
F1_c = 2 * P_c * R_c / (P_c + R_c)     for c in {0, 1}
macro-F1 = (F1_0 + F1_1) / 2
```

`scd.evaluate.macro_f1` is a thin wrapper around
`sklearn.metrics.f1_score(..., average="macro", zero_division=0)`.

Why not accuracy? Because a majority-0 classifier can score 0.8
accuracy on a corpus where authors switch rarely, and that number
does not mean the system found any boundaries.

Why not F1 of the positive class only? Because a system that over-
predicts changes should be punished on class `0` as well. Macro
average makes both mistakes visible.

Why `zero_division=0`? If a classifier never predicts class `1`,
precision for that class is undefined. Scoring it as 0 is the
honest choice and matches "you did not find any changes".

## What is pooled

Two legitimate pooling choices exist. Do not mix them in one table
without saying so.

**Micro / global pool (used here as the headline number).** Concatenate
every pair from every document, then compute one macro F1. Long
documents weigh more, which is fine if you care about "a random pair
in this corpus".

**Mean of per-document macro F1.** Compute macro F1 inside each
document, then average documents. Short documents weigh as much as
long ones. Older PAN write-ups sometimes reported a per-document
aggregation.

`scd.evaluate.evaluate_directory` reports both:

- `macro_f1` — global pool
- `mean_doc_macro_f1` — unweighted mean over documents that have at
  least one pair. A document that only contains class `0` (or only
  class `1`) still has both classes forced, so a perfect single-author
  document scores 0.5, not 1.0. That is why the two headline numbers
  can diverge even when every pair is correct.
- `n_pairs`, `n_docs`, `positive_rate`

If those two F1s disagree a lot, a few long documents are dominating.

## Length of the `changes` vector

For document `d` with `n_d` units:

```
len(y_d) == n_d - 1
```

The evaluator checks this against the units produced by the same
splitter the model used. A length mismatch is a hard error. It is
never silently padded. Silent padding is how off-by-one bugs become
fake F1.

## Class imbalance

Synthetic and real style-change data are imbalanced toward `0`.
Report the positive rate next to F1 so a reader can see the base
rate. On this repo's toy hard band the positive rate is lower than
on easy, because hard documents stay with one author longer (style
cues need room). That is a generation choice, documented in note 9.

## Confidence intervals (what to say in an exam)

With a few dozen documents, a 0.03 F1 gap is often noise. The honest
sentence is: "I would bootstrap documents, not pairs, because pairs
inside one document are dependent." This repo does not bootstrap by
default; `scd.evaluate.bootstrap_doc_f1` exists for the write-up
example and resamples *documents*.

## What not to optimise

- Do not tune on the test band.
- Do not report only the easy band.
- Do not average easy/medium/hard F1 and hide a hard-band collapse.
- Do not use pair-level accuracy as the headline.

The comparison script writes a 3×3 train-band × test-band table on
purpose. That table *is* the result.

## Worked numeric example

Suppose one document has truth `[0, 0, 1, 0]` and a model predicts
`[0, 1, 1, 0]`.

Confusion:

|  | pred 0 | pred 1 |
|--|--------|--------|
| true 0 | 2 | 1 |
| true 1 | 0 | 1 |

```
P_0 = 2/2 = 1.00    R_0 = 2/3 ≈ 0.667    F1_0 ≈ 0.800
P_1 = 1/2 = 0.50    R_1 = 1/1 = 1.00     F1_1 ≈ 0.667
macro-F1 ≈ 0.733
```

Accuracy would be 0.75 and would not tell you the false alarm on the
second pair. Macro F1 does.

The same numbers are locked in `tests/test_evaluate.py`.
