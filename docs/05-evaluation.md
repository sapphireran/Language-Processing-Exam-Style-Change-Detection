# Evaluation

## Per document, then macro

For one document, treat `changes` as a binary classification over
boundaries. Compute precision, recall, F1. Then **average the document
F1s**. That is PAN's macro-F1.

Consequences you should mention:

- A two-paragraph document (one bit) counts as much as a
  twelve-paragraph collage.
- Pooling every boundary and computing one F1 is *micro* and is a
  different number. `scdkit eval` prints both.
- A single-author document whose gold is all zeros and whose
  prediction is all zeros is a perfect document (F1 = 1), even though
  there is no positive class. Several student write-ups adopt that
  convention; this kit does too. Say it, do not hide it.

## Worked numbers

See `examples/walkthrough_f1.py` and [the worked example](07-worked-example.md).

Gold `[1, 0, 1]`, pred `[1, 1, 0]`:

- TP=1, FP=1, FN=1, TN=0
- P=0.5, R=0.5, F1=0.5

All-zero prediction on that gold: P=1 (no false positives), R=0,
F1=0 under the usual formula — and this kit does *not* special-case
that, only the all-zero / all-zero document.

## What not to optimise

Do not tune thresholds on the official test set. TIRA exists so you
cannot. Tuning on the fourteen bundled texts is fine for a study kit
and forbidden as a claim about PAN. The README says that twice
because it is the mistake an examiner will look for.

## Other metrics, if asked

- **Accuracy** is a bad headline on a mostly-zero `changes` vector.
- **Windowed boundary** scores (a hit within ±1 paragraph) appear in
  older segmentation papers. PAN 2023 is exact.
- **Author-ID clustering** metrics (ARI, BCubed) belong to the 2021
  flavour of the task, not 2023.

## Difficulty splits

Easy / medium / hard are evaluated **independently**. A system that
is secretly a topic model will look strong on easy and collapse on
hard. Always report the three numbers, not a pool.
