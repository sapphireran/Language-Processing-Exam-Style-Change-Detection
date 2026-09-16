# Written model answers

Short paper-shaped answers. Numbers from this revision; refresh `docs/15-live-results.md` if you retune.

## Q1. Define style-change detection and name one official output format.

Style-change detection is the intrinsic task of marking positions in a single document where writing style changes. A common output is a JSON object `{"changes": [0,1,0,…]}` with one bit per pair of consecutive units. 1 means a change between unit *i* and unit *i+1*. The array does not identify writers.

## Q2. Why is accuracy a bad headline metric?

Because the hold class dominates. A never-fire detector on 16 holds and 4 changes scores accuracy 0.800 and macro-F1 0.444. Macro-F1 (or change-class F1) makes that visible.

## Q3. Distinguish intrinsic and extrinsic authorship.

Extrinsic tasks compare a questioned text to named candidates. Intrinsic tasks see only the questioned text. Style-change detection is intrinsic: same-or-different at each hinge, no names.

## Q4. Give an example where topic and authorship disagree.

In problem-19 one writer changes topic three times; gold `changes` is all zeros. In problem-08 two writers stay on quince paste; gold has a single 1. A topic model gets both files backwards.

## Q5. What does `1 + sum(changes)` assume?

That each snap introduces a *new* writer. If a previous writer returns, the sum over-counts. Problem-22 has two writers and two snaps, so the sum is 3.

## Q6. Sketch a feature set that is not a topic detector.

Function-word rates, person pronouns, contraction marks, hedge adverbs, `shall`/`must`, vocatives, question/exclaim rates, digit and semicolon rates. Exclude nouns and named entities from the change score.

## Q7. Why smooth function-word cosine on this corpus?

Units are one sentence. Two same-author lines can share no closed-class word by chance. Unsmoothed cosine then reports distance 1. Additive smoothing keeps that pair near the prior.

## Q8. When would you use CUSUM?

On a long document with a persistent new writer, as a picture of slope change. Not as the only cut on a six-hinge teaching file.

## Q9. Interpret a miss on problem-13.

The two spans share topic and most register flags. Leftover signal is a handful of function words (*towards/toward*, *whilst/while*). The default blender scores the gold hinge below 0.30. Class: `same_register_miss`. Accuracy on the file is still high because holds dominate.

## Q10. How would you choose a threshold in a real submission?

Reserve a development split. Grid-search macro-F1, not accuracy. Report leave-one-group-out or a frozen test set. Do not tune on the file you quote.
