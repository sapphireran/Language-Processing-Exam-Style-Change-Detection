# Metrics and dummy baselines

PAN 2023 scores **F1 on the `changes` vector**. That is a binary
classification metric on paragraph *boundaries*, not on paragraphs.

For gold \(g\) and prediction \(p\):

- TP: both 1
- FP: gold 0, pred 1
- FN: gold 1, pred 0
- TN: both 0

\[
P = \frac{TP}{TP+FP}, \quad
R = \frac{TP}{TP+FN}, \quad
F_1 = \frac{2PR}{P+R}
\]

Accuracy \((TP+TN)/N\) is reported in this kit because students ask
for it. It is the wrong headline. Most boundaries in a short document
are 0.

## Dummy baselines you should quote

| Baseline        | Prediction      | Typical behaviour                      |
|-----------------|-----------------|----------------------------------------|
| Always same     | all 0           | High accuracy, zero recall, F1 = 0     |
| Always change   | all 1           | High recall, miserable precision       |
| Coin flip       | Bern(0.5)       | Honest chaos                           |
| Length jump     | 1 if \|Δ words\| is huge | Fires on lists and quotes      |

If your model cannot beat "always same" on **F1**, it is not a style
detector. It is a prior.

## Macro vs micro

- **Macro F1**: unweighted mean of per-document F1. A four-paragraph
  gift-authorship case counts as much as an eight-paragraph collage.
- **Micro F1**: pool TP/FP/FN across the collection, then compute F1.

PAN's official script evaluates per dataset; this kit prints both so
you can say which one you are looking at. Oral preference: lead with
macro F1, then mention that a single missed cut in a short document
hurts more under macro than under micro.

## Length of the vector

A document with \(k\) paragraphs has \(k-1\) boundaries. If your
solution file has the wrong length, the scorer should refuse to play.
`splicefind.evaluate.confusion` raises `ValueError` on purpose. That
is a better failure than silently padding.

## Why F1 and not accuracy, again

Suppose gold is `[0, 0, 1, 0, 0]`. Predicting all zeros is 80%
accurate and useless. Predicting the single 1 and nothing else is the
actual scientific claim. F1 makes you pay for that claim.
