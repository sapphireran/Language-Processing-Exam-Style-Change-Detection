# Detectors

Every detector in this repo implements the same contract:

```python
class Detector:
    name: str
    def fit(self, documents, labels) -> None: ...
    def predict_document(self, sentences: list[str]) -> list[int]: ...
```

`labels` is a list of `changes` arrays, one per document. Detectors that
do not train implement `fit` as a no-op.

## Majority baseline (`always0`)

Predict `0` for every pair. This is the score you must beat.

- Accuracy is high whenever switches are rare.
- Macro-F1 collapses because class `1` has precision/recall zero.
- On the synthetic set the prior is intentionally less skewed, so the
  baseline is weak but still the first row of any result table.

Write this baseline down even if it feels insulting. Markers look for it.

## Unsupervised z-score jump (`unsupervised`)

1. Embed every sentence.
2. Standardize each feature with the **document** mean and standard
   deviation (a floor of \(10^{-6}\) avoids divide-by-zero).
3. Compute Euclidean distance between consecutive standardized vectors.
4. Label \(y_i = 1\) iff \(d_i > \mu_d + k \sigma_d\), with default
   \(k = 0.75\).

Why within-document standardization? Because Mira’s “short” sentence is
still longer than Hale’s “long” sentence. Corpus-level z-scores would
compare Hale to Mira instead of Hale to the Hale-ish block he is sitting
in. Change-point detection cares about *local* jumps.

Failure modes:

- A single-author document with one unusually short sentence (a title, a
  fragment) produces a spurious peak.
- Two similar authors in a short document produce a flat distance series;
  the threshold then fires on noise or never fires.
- \(k\) is a knob. The default was chosen on the synthetic train split,
  which is circular if you treat this as a blind test. Say so.

## Tuned threshold (`threshold`)

Same distance as above, but \(k\) (or an absolute cutoff on raw pairwise
L1) is chosen to maximise macro-F1 on labeled training pairs. This is the
smallest *supervised* model. It has one parameter and is easy to plot.

## Logistic pairwise classifier (`logistic`)

Reduce the document to labeled pairs \((d_i, y_i)\), then fit

\[
p(y=1 \mid d) = \sigma(w^\top d + b)
\]

by batch gradient descent with L2 penalty. Implementation notes you can
quote:

- Features are z-scored with **training-pair** mean/variance, stored in
  the model JSON, and reused at test time. Do not re-fit the scaler on
  the test document.
- Class weights inverse to frequency so the rare `1` is not ignored.
- Default pair map is `absdiff`. `stack` overfits the tiny synthetic set.
- Threshold on \(p\) defaults to \(0.5\) and can be swept on the val split.

This is not sklearn. The point of the from-scratch fit is that an exam
answer can write the update rule:

\[
w \leftarrow w - \eta \left( \frac{1}{N}\sum_i (p_i - y_i)\, d_i + \lambda w \right)
\]

## Ensemble (`ensemble`)

Average the *probabilities* of `unsupervised` (sigmoid of a z-scored
distance) and `logistic` when both exist; otherwise vote. Ensembles are
not magic on eight-document splits. They are included so you can discuss
error complementarity: the unsupervised detector catches large register
jumps the logistic model under-weighted, and vice versa.

## How to choose in an exam booklet

| If the question gives you… | Prefer |
| --- | --- |
| No labeled training data | `unsupervised` |
| A tiny labeled set and a need for a graph | `threshold` |
| Labeled pairs and a request for a model | `logistic` |
| “Compare two approaches” | `always0` vs any of the above |
| Hard / topic-controlled data | any style-only model; say why BoW fails |

## What a detector must never do

- Peek at `truth-problem-*.json` at test time.
- Use future sentences in a way you do not declare. (Looking at the whole
  document for z-scores is declared and fine; looking at gold labels is
  not.)
- Emit the wrong-length `changes` array. That is an I/O zero, not a
  modelling near-miss.
