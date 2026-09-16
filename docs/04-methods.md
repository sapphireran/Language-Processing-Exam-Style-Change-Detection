# Methods

Style change detection is pairwise binary classification on boundaries.
Every method in this note is a way to turn two adjacent paragraphs into
a score, then cut that score.

## 1. Fixed-threshold stylometry (the repo baseline)

```
for each boundary (p_i, p_{i+1}):
    d_i = combined_distance(profile(p_i), profile(p_{i+1}))
    c_i = 1 if d_i > t else 0
```

Default \(t = 0.33\) was chosen on the Easy and Medium teaching documents
in this repo. It is **not** a universal constant. On a real validation
split you would sweep \(t\).

**Say in an exam:** unsupervised, cheap, transparent, brittle under
length imbalance and under register drift inside one author.

## 2. Adaptive (document-relative) threshold

A global \(t\) assumes every document lives on the same distance scale.
Hard documents compress that scale: every pair is “quite similar”, and
the true change is only *relatively* large.

```
t_doc = max(floor, mean(d) + k * std(d))
```

Defaults: \(k = 0.65\), \(\text{floor} = 0.30\).

This is the stylometric cousin of z-scoring. It helps when a document is
uniformly formal. It **hurts** when every boundary is a true change
(Easy problem 002): the mean is already high, so an adaptive cut can
call every jump “normal”. Always report both.

## 3. Smoothing

Isolated `1`s in a sea of `0`s are sometimes noise. A majority vote over
a window of radius 1 is an optional post-process (`smooth_changes`).
Do **not** enable it by default: a single real change in a four-paragraph
document is exactly an isolated 1, and smoothing will delete the answer.

## 4. Unsupervised clustering of paragraphs

Embed each paragraph as a style vector and cluster (2-means, agglomerative,
or “number of authors unknown”). Then label a boundary as a change when
the two paragraphs fall in different clusters.

This solves a *stronger* problem (a partition into author IDs) and
projects it down to the change array. It can capture non-adjacent
repeats of an author (A B A), which pairwise thresholds treat as two
independent jumps — correctly, because both jumps *are* changes.

**Exam contrast:** clustering needs a guess for \(k\) or a model-selection
hack (silhouette). Pairwise thresholding does not.

## 5. Supervised classical models

If you have labelled boundaries, you can train a classifier on the
*concatenation or difference* of two profiles:

\[
x_i = [S(p_i);\; S(p_{i+1});\; |S(p_i)-S(p_{i+1})|]
\]

Logistic regression or a linear SVM is the honest exam baseline. It
learns the threshold and the feature weights together. It also learns
dataset artefacts (Easy topic leak) unless you regularise or ablate
content features.

## 6. Neural pair classifiers

Fine-tune a pair encoder (two sentences / two paragraphs → `[CLS]` →
sigmoid). This is what recent PAN winners do (RoBERTa, DeBERTa, and
friends). It works. It also needs a GPU, a labelled split, and an
explicit story about topic leakage: a pretrained transformer is a
superb topic model.

If the exam asks “why might BERT be unfairly strong on Easy?”, the
answer is: masked-language pretraining encodes topical neighbourhoods;
Easy authorship changes are correlated with those neighbourhoods.

## 7. Topic-only straw man

Drop function words, keep content words of length ≥ 4, take cosine
distance. That is `stylechange.topic.topic_distance`. On Easy problem
001 the cooking→planning boundary is 1.000 (no shared content types).
On Hard problem 001 the true style boundary is *not* the largest topic
jump. That plot is the whole point of the difficulty split. See
[../examples/topic_confound.md](../examples/topic_confound.md).

## What to write if the question is “propose a system”

A full-mark sketch:

1. Segment on blank lines.
2. Extract function-word rates + a short register vector (no content
   TF–IDF).
3. Train a logistic regressor on pair differences if labels exist;
   otherwise sweep a threshold on validation F1.
4. Report Easy / Medium / Hard separately.
5. Ablate the content-word straw man to prove you did not cheat on Easy.
6. Error analysis: short paragraphs, single-author controls,
   author-revisiting patterns (A B A).

That is a method, not a leaderboard entry.
