# Written model answers

These are *shapes*, not scripts to memorise. Fill every `[n]` from
a fresh `run_curriculum.py` before you submit.

## Q1. Define the task (≈150 words)

Intrinsic style-change detection asks, for each pair of consecutive
units in a single document, whether the writing style — and by
assumption the author — changes at that boundary. For \(n\) units
the system emits an array of \(n-1\) binary labels. No reference
texts are available, so the comparison is only of the document to
itself. The problem is the intrinsic counterpart of authorship
attribution and is the setting in which plagiarism detection must
operate when no source document is known. Later PAN editions mark
changes at sentence level and publish Easy / Medium / Hard splits
that vary how much topic moves with authorship. Evaluation is
macro-F1 over the stay and change classes, not accuracy, because
change pairs are the minority class.

## Q2. Describe a baseline (≈200 words)

A teaching baseline tokenises each sentence into words and
character trigrams. It builds (i) a 100-dimensional function-word
distribution, (ii) a sparse trigram distribution, (iii) a vector
of length and rate features with raw counts excluded, and (iv)
Burrows' Delta on the same function words, z-scored across the
document. Consecutive sentences receive a weighted sum of the four
distances. A sentence pair is labelled a change if that sum is at
least 0.42. Register scalars (person, contractions, sentence-initial
case) take the largest weight so that a change of subject is not
sufficient for a change label.
The baseline is deliberately unsupervised: it has no learned
parameters except the threshold, which must be chosen on labelled
teaching data and then frozen. Its expected failure modes are
short sentences (unstable rates), Hard documents where two authors
share an academic register, and single-author controls that
contain an internal topic aside.

## Q3. Why not accuracy? (≈120 words)

Stay pairs dominate. A detector that emits the all-zero vector
matches the majority class and can record accuracy equal to the
stay rate — 0.80 in a 16/4 teaching example — while scoring 0
F1 on the change class and 0.444 macro-F1. Macro-F1 averages the
two class-wise F1 scores and therefore stays low until the system
recovers seams. Any write-up that leads with accuracy is
compatible with a system that never detects a style change.

## Q4. Topic confound (≈180 words)

When authorship and subject change together, a content-word model
receives an easy cue. Easy teaching documents in this repository
are built that way: cycling in Nørrebro gives way to parchment
repair; an IKEA manual gives way to tidal locking. Hard documents
hold the subject still (two bakers on one rye loaf; two field
notes on one walk) so that only register remains. A honest
experimental table therefore reports Easy and Hard separately. If
ablating the function-word channel leaves Easy almost unchanged
and destroys Hard, the system was using topic. Diagnostics such
as content-word Jaccard versus function-word cosine are a way to
*name* that error (`topic_confound`) rather than to pretend the
model is stylometric.

## Q5. Ethics (≈120 words)

A detected seam is a pointer for a human reader. It is not
evidence of fraud, gift authorship, or plagiarism by itself.
False alarms on student work waste time and can intimidate. Misses
on a methods paragraph that suddenly changes person and hedging
can hide a real writing problem. Systems should expose the pair
and the channel breakdown, keep a human in the loop, and avoid
writing names or misconduct labels into the output JSON. Training
on public comments does not license deanonymising those speakers
in a write-up.

## Q6. One limitation of this lab (≈80 words)

Units are short. Burrows' Delta z-scores 100 bins from a handful
of sentences, TTR is biased upward, and one punctuation mark can
flip a scalar flag. The lab therefore treats CUSUM traces and
error tags as explanations, keeps the official answer in the
pairwise `changes` array, and refuses to claim that a 0.42 cut
transfers to full PAN test sets.
