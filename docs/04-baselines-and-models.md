# 4. Baselines and models

A style-change paper or exam answer that only reports one number is
incomplete. You need to say *compared to what*. This note lists the
baselines implemented in `scd.models` and the modelling choices that
usually show up in the literature.

## Trivial baselines

### Always-same (`majority_0`)

Predict `0` for every pair. On real and synthetic data, most neighbouring
units share an author, so accuracy looks respectable and **macro F1
collapses** because the positive class is never predicted.

This is the first number to put in a table. If your clever model cannot
beat it on macro F1, you have not solved the task.

### Always-change (`majority_1`)

Predict `1` everywhere. Rarely strong. Useful only as a symmetry check.

### Random

Predict 1 with probability `p`, usually the training-set positive rate.
Expected macro F1 sits near 0.5 on a balanced problem and lower when
the labels are skewed. Report it so "0.62 F1" is interpretable.

### Length-threshold

Predict 1 if the absolute word-count difference exceeds a threshold
tuned on training data. This catches some formal-vs-casual switches
and fails when two authors write similar-length sentences about the
same thing (the hard band).

## Classical pairwise classifier (what this repo trains)

Pipeline:

1. Split each document into units.
2. Extract unit features and pairwise features (see note 3).
3. Stack every pair from the training documents.
4. Fit `sklearn.linear_model.LogisticRegression` with class weighting.
5. Threshold at 0.5, or tune the threshold on a validation split.

Class weighting matters. If 80% of pairs are `0`, an unweighted log-loss
will happily ignore changes. `class_weight="balanced"` is the default
in `scd.models.PairwiseLogReg`.

Why logistic regression rather than a random forest?

- Coefficients are readable. You can say "contraction-rate gap" and
  "function-word cosine" in an error analysis.
- It is stable on a few dozen toy documents.
- It is the honest version of "a linear combination of stylometric
  cues", which is what most exam answers describe.

A random forest would probably score higher on the toy set and tell
you less. The point of this repo is the *ladder* easy > medium > hard,
not a leaderboard.

## Other classical options you should be able to name

| Method | Idea | Weakness |
|--------|------|----------|
| Cosine on TF-IDF word vectors | Low similarity => change | Topic detector |
| Burrows' Delta on function words | Z-scored closed-class distance | Needs a comparison corpus; originally for long texts |
| Clustering (k-means on unit vectors) | Recover author blocks | Must pick k; metric is still pairwise |
| Threshold on char-n-gram cosine | Keyboard-habit change | Unstable on 5-word sentences |
| SVM on the same pairwise features | Non-linear margin | Extra hyperparameters, same features |

## Neural pair classifiers (not shipped here)

The usual 2024–2025 approach is: encode `(sentence_i, sentence_i+1)`
with a pretrained transformer (RoBERTa, DeBERTa) and train a sigmoid
head with binary cross-entropy. That is the right tool if you are
entering a shared task. It is the wrong first tool if you are trying
to *understand* the exam problem, because:

- Pretraining already encodes topic.
- You cannot read the features.
- You cannot run it offline in this environment without fetching
  weights.

If an exam question is "why might a transformer beat stylometry on the
easy set and tie it on the hard set?", the answer is topic leakage plus
short-sentence noise.

## Training protocol used by the examples

`examples/02_train_baseline.py` trains **one** model on all three bands
pooled, then reports macro F1 per band. That is deliberate. A model
trained only on easy data will overweight Jaccard and content-ish
cues and then fall over on hard. Pooling forces the linear model to
keep some style weights.

A second run in `examples/04_compare_difficulties.py` trains *separate*
models on each band and evaluates them cross-band. The expected
pattern:

- Train easy, test hard: large drop.
- Train hard, test easy: smaller drop (style still works when topic
  also moves).
- Train pooled, test each: in between.

That 2×2 is a better exam figure than a single F1.

## Thresholding and calibration

Logistic regression outputs probabilities. The default cut is 0.5.
On imbalanced data you may want a lower threshold to recall more
changes, then watch precision. Macro F1 will tell you if the trade
is worth it. The library exposes `predict_proba` so example 3 can
show near-miss pairs (probability 0.4–0.6) separately from confident
errors.

## Output contract

Whatever `g` you train, wrap it so that:

- a 1-unit document yields `[]` (no pairs)
- a 2-unit document yields a single bit
- empty input is an error, not a silent `[]`

`scd.models.StyleChangeModel.predict_document` implements that.
