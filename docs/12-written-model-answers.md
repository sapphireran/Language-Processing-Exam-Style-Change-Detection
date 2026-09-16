# Written model answers

These are the length of a decent exam paragraph, not a tweet. Steal
the structure, not the jokes.

## 1. Define style-change detection and distinguish it from topic segmentation.

Style-change detection is an intrinsic authorship problem: given a
single document and no gallery of known writers, decide whether more
than one author contributed and mark the boundaries at which the
writing habits change. The habits that matter are closed-class —
pronoun choice, contraction, formal modals, hedges — because those
rates can stay put while the subject matter moves. Topic segmentation
asks a different question and lights up when the content words
change. A teaching document in this lab that discusses dumpling
skins, a night bus, and a cat, all in the same first-person
contracted English, has three topics and no style change. A detector
that fires there is a topic model, however it was advertised.

## 2. Why is accuracy a poor metric for boundary labelling?

Inter-sentential gold labels are dominated by seams. On the
twenty-six-document teaching folder there are 117 boundaries and 27
folds. The constant-negative predictor is therefore correct on
roughly 77% of cuts and has a fold-class F1 of zero. Macro-F1, which
averages the fold F1 with the seam F1, exposes that cheat. Exact
match on the full change-list is stricter still and is what the
easy/medium sites in this lab are checked against.

## 3. Explain the return-author trap.

A naive conversion `authors = 1 + number of predicted folds` counts
*segments*, not people. If author A writes, then B, then A again,
there are two folds and two authors but three segments. The kiln
return document in this folder is labelled `authors = 2` with
`return_author = true` precisely so that `1 + sum(changes)` is 3. A
system that only marks folds has not clustered the first and last
spans, and should not pretend it has counted writers.

## 4. Describe a method you could compute in an exam hall.

Tokenise each provided unit. Count six rates against published
closed-class lists: I, you, contraction, formal, hedge, we. At each
cut compute the L1 distance between the unit on the left and the unit
on the right. Mark a fold if that score is a local maximum above a
stated threshold, or if it exceeds a higher "sure-fold" cutoff.
Report the binary list. State that same-register specialists will be
missed and that very short chat units may false-alarm.

## 5. What would you change before running on a real shared-task collection?

Freeze the feature definition. Fit the two cutoffs on the official
training split, maximising boundary macro-F1 subject to a low false
fold rate on single-author documents. Replace naive author count with
a clustering step on the spans between folds. Do not tune on the test
zip. Do not treat character n-grams as style on paragraph-length
units without checking a topic control.
