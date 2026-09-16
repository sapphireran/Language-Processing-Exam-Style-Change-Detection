# Calibration

A threshold is a claim about the score distribution. Treat it like
one.

## Fixed cut (default 0.42)

Pick it on a *labelled* teaching folder. Then freeze it before you
look at a held-out folder. In this repo the held-out idea is the
Hard + Control slice: tune on Easy+Medium only if you want an
honest story.

If you tune on everything, say that the number is descriptive, not
a generalisation claim.

## Adaptive cut

`mean + k · std` asks: "is this boundary tall *for this document*?"
That helps when Easy scores live around 0.5 and Hard scores live
around 0.25. It hurts when a single-author document has one
topical flourish — that flourish *is* the tallest spike.

The `floor` (0.22) stops a very flat document from flagging noise
as a seam just because *something* is slightly above the mean.

## How to choose k without lying

1. Grid `k` in `{0.4, 0.6, 0.85, 1.1, 1.4}` on Easy+Medium.
2. Record Hard and Control without touching `k`.
3. Put both columns in the paper.

`scripts/grid_thresholds.py` does the grid for the fixed cut.
`scripts/run_curriculum.py` prints all three detectors at the
defaults.

## Probability talk

These scores are not probabilities. Do not write "the model is 70%
sure". Write "the blended distance was 0.45, above the 0.42 cut."
If you ever wrap a logistic regression around the four channels,
*then* you may talk about probabilities — and you must talk about
calibration plots.

## Cost of errors

For the gift-authorship oral, a miss is worse than a false alarm.
Use the ensemble (recall bias) and say so. For a tool that would
highlight student essays, false alarms waste human time — prefer
the fixed cut and a higher threshold.

The exam is testing whether you can *name the cost*, not whether
you picked the globally best k.
