# Evaluation

The prediction for a document is a binary vector, one label per
paragraph boundary. Scoring treats those labels as a two-class problem
and reports **macro-averaged F1**.

Macro-F1 is the unweighted mean of F1(class 0) and F1(class 1). It does
not let the majority class hide a dead minority class. That matters
because “no change” is usually more common than “change”, especially in
the single-author controls.

## Per-class arithmetic

From the confusion counts:

|  | Predicted 1 | Predicted 0 |
| --- | ---: | ---: |
| Gold 1 | TP | FN |
| Gold 0 | FP | TN |

```text
precision_1 = TP / (TP + FP)
recall_1    = TP / (TP + FN)
F1_1        = 2 * precision_1 * recall_1 / (precision_1 + recall_1)

precision_0 = TN / (TN + FN)
recall_0    = TN / (TN + FP)
F1_0        = 2 * precision_0 * recall_0 / (precision_0 + recall_0)

macro-F1    = (F1_0 + F1_1) / 2
```

Undefined ratios (zero denominator) are treated as 0. An empty vector
(a one-paragraph document) scores 1: there was nothing to get wrong.

## Document mean vs pooled

`style-change evaluate` prints both:

- **mean macro-F1** — macro-F1 on each document, then average. A failure
  on a short document hurts as much as a failure on a long one.
- **pooled macro-F1** — concatenate every gold/pred pair in the split,
  then compute one macro-F1. Longer documents weigh more.

Shared-task writeups often pick one and stick to it. This repo prints
both so the walkthrough can show they are not the same number when
document lengths differ.

## Worked toy

Gold: `[0, 0, 1, 0]`
Pred: `[0, 1, 1, 0]`

- TP = 1, FP = 1, TN = 2, FN = 0
- F1_1 = 2 * (1/2) * (1/1) / (0.5 + 1) = 2/3
- F1_0 = 2 * (2/2) * (2/3) / (1 + 2/3) = 0.8
- macro-F1 = (0.8 + 0.666...) / 2 ≈ 0.733

The detector found the real change and invented one extra change. Accuracy
would still be 0.75; macro-F1 records the false positive on class 1.

## Baselines the metric should punish

| Baseline | What it does | Why it is in the notes |
| --- | --- | --- |
| All zeros | Never predict a change | Looks strong on single-author; dies on easy-002 |
| All ones | Always predict a change | Inverse problem |
| Coin flip | Independent 50/50 | Sanity floor |
| Topic only | Fire when lexical overlap is low | Cheats on easy, fails medium/hard |

`examples/compare_baselines.py` scores the actual detectors, not these
jokes, on every synthetic split. After you run it, check that
`single_author` stays high: that is the control that all-ones cannot pass.

## Protocol used here

1. Gold lives next to the problem file as `truth-problem-<id>.json`.
2. Predictions are `solution-problem-<id>.json` in a separate directory.
3. IDs must match exactly. Extra or missing files are errors, not
   silently skipped.
4. Label length must equal `n_paragraphs - 1` at load time.

That last check belongs in I/O, not in the metric. If the lengths are
wrong, the run should refuse to score rather than invent a confusion
matrix.

## What I would write in an exam booklet

> Evaluate paragraph-boundary labels with macro-F1 so that the majority
> “no change” class cannot dominate. Report a document-averaged score
> and, if lengths vary, a pooled score. Include a single-author control
> so a detector that always fires is exposed.
