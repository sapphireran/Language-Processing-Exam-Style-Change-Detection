# 8. Error analysis

This note is the companion to `examples/03_error_analysis.py`. It
lists the failure modes you should expect, how they show up in
pairwise probabilities, and what *not* to "fix" by stuffing topical
features back in.

## Anatomy of a pair error

For each pair the model stores `p = P(change)`. We look at:

| Bucket | Rule | What it usually is |
|--------|------|--------------------|
| Confident hit | truth=1, p ≥ 0.7 | Register rupture the features can see |
| Confident miss | truth=1, p ≤ 0.3 | Same-topic, same-length, mild style gap |
| False alarm | truth=0, p ≥ 0.7 | Length jump or topic drift *inside* one author |
| Near miss | |p − 0.5| < 0.15 | Features disagree with each other |

The interesting rows are confident misses on the **hard** band and
false alarms on the **easy** band. Those two tell you whether the
model learned style or topic.

## Failure mode A — topic leakage (easy-train, hard-test)

Symptoms:

- Jaccard and word-set features have large coefficients.
- Easy F1 is high; hard F1 is near the majority baseline.
- False alarms fire when one author mentions a new entity.

What to do: train with hard (or pooled) data; down-weight or drop
content overlap; inspect coefficients and confirm function-word
and contraction slots are alive.

What not to do: add BERT cosine and call the hard-band collapse
"an implementation bug".

## Failure mode B — short units

A five-word sentence cannot estimate a 50-dimensional function-word
distribution. TTR becomes 1.0 or close to it. Character n-grams
still have support; word features do not.

Symptoms: near-miss probabilities on any pair that includes an
imperative fragment ("I'm not gonna overthink dinner tonight, seriously.").
The worked example's pair (3,4) is this shape.

Mitigations (conceptual — not all implemented):

- Smooth function-word counts with a Dirichlet prior.
- Skip TTR below a token threshold (the library still emits it,
  but a linear model can learn to ignore it if length is present).
- Use character n-grams as the backbone on short units.

## Failure mode C — intra-author variation

Real (and synthetic) authors are not delta functions. A formal
writer may drop a short heading-like sentence. A casual writer may
produce one careful clause. Pairwise models see that as a change.

The generator in `scd.generate` injects a little intra-author
jitter on purpose so the baseline cannot get a perfect score by
memorising personas. If your model is perfect on train and merely
good on the same band's held-out docs, you memorised jitter
patterns. If it is perfect on *all* hard docs, the hard band is
too clean — open an issue with yourself and add noise.

## Failure mode D — change density

Documents with many authors produce many `1`s; monographs produce
almost none. A globally pooled F1 can hide that the model only
works on high-density documents. Check `mean_doc_macro_f1` and
look at errors grouped by `authors`.

## Failure mode E — splitter disagreement

If you evaluate with a different sentence splitter than the one
used to write truth, every pair index shifts and F1 becomes
fiction. This repo avoids that by storing one unit per line in
the toy corpus and using `mode="line"` when reading it.

If you switch an example to a raw paragraph, re-derive truth.
Never "fix" a length mismatch by padding zeros.

## A walk-through you should see in example 3

On `easy/problem-1` (the souffle / pizza document):

- Pair (2,3) should be a confident hit: contractions and register
  flip together.
- Pair (3,4) may be a near miss or a mild false-alarm risk because
  of the 14-vs-7 word jump, but contraction rate stays casual.

On a hard document (same topic, two polite vs two slightly more
clipped voices) the hit, if any, should ride on function-word and
punctuation slots, not on Jaccard. If example 3 shows Jaccard as
the largest contributing difference on a hard *hit*, the model
got the right label for the wrong reason. Note that in a write-up;
do not celebrate the F1.

## Coefficient reading

After training, `examples/02_train_baseline.py` prints the top
absolute logistic-regression weights. A healthy pooled model
usually ranks some of:

- `abs_contraction_rate`
- `abs_first_person_rate`
- `fw_cosine` (negative: high similarity ⇒ less change)
- `char_tri_cosine`
- `abs_exclaim` / `abs_comma`
- `abs_avg_word_len`

If the top slot is `jaccard` or `abs_digit_rate` only, the training
mix is too easy or the hard band is too small.

## Reporting errors without drowning the reader

Pick three pairs: one easy hit, one hard miss, one intra-author
false alarm. Quote the two sentences, list three feature deltas,
and say which story they support. That paragraph is worth more
than a dump of every probability.
