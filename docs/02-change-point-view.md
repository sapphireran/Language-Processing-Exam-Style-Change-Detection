# 02 — A change-point view

Authorship *attribution* is a gallery problem: here are texts by A,
B, and C; whose is this anonymous page? Style-change detection is a
*segmentation* problem: here is one page; where does the writer
change?

Those two problems share features and almost nothing else in the
decision rule.

## The hidden sequence

Let paragraphs be `x_1, …, x_n` and let `z_i` be the author of
paragraph `i`. The task does not ask for `z`. It asks for

```
y_i = 1[z_i ≠ z_{i+1}],   i = 1 … n-1
```

If authors never return, `y` determines `z` up to a permutation of
labels. If authors *do* return, `y` is strictly poorer than `z`.
PAN 2023 asked for `y`.

## Why pairwise is already a model

The lab detector scores each adjacent pair independently:

```
score(x_i, x_{i+1})  ≷  threshold
```

That is a noisy independent classifier. It ignores:

- the length of the current run ("we have been in this voice for four
  paragraphs, so a small blip is probably still the same person");
- returning authors;
- document-level base rate (some documents are single-author, so the
  prior on `y_i = 1` should shrink).

A sequential model — HMM, CUSUM on a one-dimensional style
coordinate, Bayesian change-point — can use those facts. Transformers
that read the whole document do it implicitly. On an exam you should
be able to *name* the independence assumption and say what it costs.

## CUSUM in one paragraph of algebra

Map each paragraph to a scalar `s_i` (for example first-person rate
minus academic-marker rate). Let `μ` be the mean of the current
putative segment. The CUSUM statistic

```
S_0 = 0
S_t = max(0, S_{t-1} + (s_t - μ) - k)
```

alarms when `S_t > h`. After an alarm you restart the segment. This
is how quality-control charts find a mean shift. It is a legitimate
style-change detector and it is easy to draw on a whiteboard.

`scarfjoint` does **not** ship CUSUM as the primary decision rule. It
ships pairwise scores so you can see each channel. The independence
assumption is therefore explicit, which is the point of a lab.

## Intrinsic vs extrinsic, restated

| | Intrinsic SCD | Extrinsic attribution |
| --- | --- | --- |
| Comparison texts | none | a gallery |
| Output | boundaries | a name or a ranking |
| Topic risk | topic change looks like author change | topic can still leak into the representation |
| Typical exam trap | using content words as style | using the same document as train and test |

If the question is "how would you detect gift authorship on a thesis
chapter with no writing sample from the alleged gift author?", the
answer is intrinsic SCD, not a closed-set SVM.

## What "style" is allowed to be

Anything that varies with *how* something is written rather than
*what* it is about:

- closed-class frequencies (function words);
- character n-grams (affixes, punctuation habits, spelling);
- sentence and word length, punctuation choreography;
- lexical richness;
- pronoun person, contractions, hedges, boosters.

Anything that varies with *what* it is about is a confound:

- content-word TF-IDF;
- named entities;
- sentence embeddings from a model that was trained to represent
  meaning.

The lab still computes a content-word Jaccard distance. It is labelled
`topic` in the explain output. It does not vote unless you pass
`--use-topic`, which exists so you can watch easy documents get
easier and hard documents get no help.
