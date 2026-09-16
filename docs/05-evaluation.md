# Evaluation

## Official-style metric

The headline number is **macro-F1** over the two pair classes, computed
on the **pooled** list of every predicted pair versus every gold pair.

For class \(c \in \{0, 1\}\):

\[
P_c = \frac{TP_c}{TP_c + FP_c}, \quad
R_c = \frac{TP_c}{TP_c + FN_c}, \quad
F1_c = \frac{2 P_c R_c}{P_c + R_c}
\]

with the convention \(F1_c = 0\) when the denominator is 0.
Macro-F1 is \((F1_0 + F1_1) / 2\).

Pooling matches the usual shared-task script: one long stream of pairs,
not the mean of per-document F1s. This repo reports both. They diverge
when one long document dominates the pool.

## Why not accuracy?

Suppose 90% of pairs are `0`. Always predicting `0` scores 0.90 accuracy,
\(F1_0 \approx 0.95\), \(F1_1 = 0\), macro-F1 \(\approx 0.47\). That is a
failing detector with a flattering accuracy. If your result table has
accuracy in the first column and no F1 for class `1`, you have not
evaluated the task.

## Why not micro-F1?

Micro-F1 on a binary problem with both classes present is a re-packaging
of accuracy. It re-imports the imbalance. Macro-F1 is the metric that
forces the change class to count.

## Per-document scores

Useful for debugging, dangerous for headlines. A 4-sentence document with
one switch is a coin-flip at the document level. Prefer pooling unless
the question asks whether the system is stable across documents.

`stylechange evaluate` prints:

- pooled accuracy, precision/recall/F1 per class, macro-F1
- mean per-document macro-F1
- confusion counts `tn, fp, fn, tp` with `1` as the positive change class
- length-mismatch failures (document is skipped and counted separately)

## Length mismatches

If a prediction has the wrong number of pair labels, the document is not
silently truncated. It is recorded as an I/O failure and excluded from
the pooled counts. In an exam write-up, treat I/O failures as zeros for
that document, not as “almost”.

## How to read a result on this synthetic set

The synthetic prior is richer in `1`s than a long essay would be. Numbers
here answer “do the features move when I meant them to”, not “what would
I score on a hidden shared-task test set”. Transfer claims need that
caveat in the same paragraph as the number.

A sensible revision table looks like this:

```
split     detector        acc    f1_0   f1_1   macro_f1
hard      always0         .64    .78    .00    .39
hard      unsupervised    .71    .79    .55    .67
hard      logistic        .78    .84    .66    .75
```

(The live numbers come from `examples/compare_detectors.py`; do not
memorise a stale table.)

## Statistical humility

Eight documents per split is a toy. Do not quote confidence intervals
you did not compute, and do not invent a significance test on \(n=8\).
If a question asks how you would evaluate properly, say: larger held-out
set, document-level bootstrap, and a topic-controlled hard split that
you did not tune on.
