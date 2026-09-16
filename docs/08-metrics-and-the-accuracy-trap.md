# Metrics and the accuracy trap

This corpus has 117 inter-unit boundaries and 27 gold folds. A
predictor that never fires is right on 90 / 117 ≈ **0.77** of the
cuts. That number will be on the board if you lead with accuracy.

## What to report instead

For each boundary, the label is fold (`1`) or seam (`0`). Report:

- precision / recall / F1 on the **fold** class
- the same on the **seam** class
- **macro-F1** = mean of those two F1s
- exact-match on the whole `changes` list, per document
- author-count agreement, with the return trap named

`inkfold score` prints all of this. `scripts/run_curriculum.py` also
prints the never-fire row next to the detector row.

## A document with no seams

`problem-23-four-voice-collage` is three folds and no seams. Exact
match can be perfect while per-document macro-F1 is 0.5, because the
seam F1 is 0/0. Pooled over the collage site (which includes
problem-26, which has seams) the macro-F1 comes back. If you quote a
per-document macro-F1, glance at the support.

## Document-level "was there a change?"

A different task. Always-yes is strong on a corpus that is mostly
multi-author teaching documents. Do not mix that number with boundary
F1.

## Why we also print mean macro-F1

Pooled F1 hides a hard site that is all misses. Mean of per-document
macro-F1 on this revision is lower than pooled macro-F1 because every
hard document contributes a ~0.44. That is the honest headline for
the oral: **loud registers we get; same-register pairs we do not.**
