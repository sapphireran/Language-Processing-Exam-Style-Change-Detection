# Task 4: How to score the three questions

A detector that always predicts "single author, no boundaries, one
cluster" is not a detector. The metrics have to punish that behaviour
on mixed documents and also punish a trigger-happy system on
single-author documents.

This repo scores one document at a time. Macro-averaging across a
corpus is the obvious next sentence in an exam answer.

## Task 1: document-level mixture

Treat `multi_author` as a single binary prediction.

```
accuracy = (TP + TN) / N
precision = TP / (TP + FP)
recall = TP / (TP + FN)
F1 = 2PR / (P + R)
```

On one document these numbers are 0 or 1. They become meaningful after
you average over a folder of files. `examples/run_demo.py` prints the
per-document bit so you can see which study text is misclassified.

If both gold and prediction are "single author" (no positive class),
precision/recall/F1 of the *positive* class are undefined. This toolkit
treats that vacuous case as 1.0 — you correctly predicted the absence
of a mixture — rather than as 0.0. Say which convention you used if
you write your own scorer.

Always state the prevalence. If 80% of the collection is mixed, a
constant "yes" has accuracy 0.80 and is still useless.

## Task 2: boundary F1

Each gap between consecutive scored paragraphs is one binary item.
Gold can come from an explicit `changes` array or be derived from
author ids: a change exists wherever `author[i] != author[i+1]`.

Boundary F1 is stricter than Task 1. You can know that a document is
mixed and still put the cut one paragraph too late. Off-by-one errors
are common because style often eases in (an editor's sentence, a
transitional paragraph). Some shared-task write-ups allow a window of
one paragraph; this toolkit does not. If you loosen the matching rule
in an exam, say so explicitly.

Precision and recall are not interchangeable here:

- high precision, low recall: conservative threshold, missed cuts
- low precision, high recall: the floor was too low, false cuts on
  single-author variation

## Task 3: clustering agreement

Author ids are arbitrary, so you cannot compute accuracy against gold
ids. Two standard answers:

### Adjusted Rand Index (ARI)

The Rand index is the fraction of paragraph-pairs on which the
prediction and the gold agree (same cluster vs different cluster). ARI
subtracts the agreement expected by chance and rescales:

```
ARI = (RI − E[RI]) / (max(RI) − E[RI])
```

ARI is 1 for a perfect match, around 0 for a random labelling, and
negative if you do worse than chance. It is the number to quote if you
only have room for one clustering metric.

The implementation is the contingency-table form in
`adjusted_rand_index` — no `sklearn` dependency.

### BCubed precision, recall, F1

For each paragraph `x`:

- BCubed precision is the fraction of `x`'s predicted cluster that
  shares `x`'s gold author
- BCubed recall is the fraction of `x`'s gold author that sits in
  `x`'s predicted cluster

Average over paragraphs, then take the harmonic mean. BCubed is easier
to explain in words than ARI and decomposes into precision/recall, so
it is a good oral-exam metric.

Purity and inverse purity are cousins. Pair them with ARI if a
question asks for "two clustering measures".

## What not to report

- Raw author-id accuracy (`pred[i] == gold[i]`). The labels are not
  aligned.
- Token-level F1. The unit is the paragraph.
- A single accuracy number that mixes Task 1 and Task 2. They answer
  different questions.

## Micro versus macro

If you evaluate a corpus:

- **micro:** pool every boundary (or every document bit) then compute
  F1. Large documents dominate.
- **macro:** compute F1 per document, then average. Each document
  votes equally.

Shared-task leaderboards specify one. In an exam, naming both and
picking one with a reason is enough.

## A checklist before you trust a number

1. Did short paragraphs get dropped, and did you drop the matching gold
   labels?
2. Are single-author documents in the average, or only mixed ones?
3. Is Task 1 majority-class trivial?
4. For Task 3, did you use a permutation-invariant metric?
5. Did you look at at least one error by hand (see
   `examples/inspect_features.py`)?

The last item is not optional. A distance spike caused by a heading is
not a modelling success even if F1 moves.
