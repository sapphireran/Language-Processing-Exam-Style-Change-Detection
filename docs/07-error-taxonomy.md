# 07 — Error taxonomy

The detector is supposed to fail in boring, nameable ways. If it
fails in a way you cannot name, that is a different problem.

## False positives (predict 1, gold 0)

**Length shock.** A two-sentence aside in the same voice as a long
paragraph next to it. Sentence-length and Flesch proxies jump; the
function-word profile usually does not. Look at whether *only* the
dense Euclidean moved.

**Quoted or instructional fragment.** A same-author paragraph that
switches into a list of imperatives ("measure, wait, record") can
look like a new instructor. Imperative-rate is the tell.

**Z-score fragility.** With four paragraphs, a within-document
z-score has almost no sample. One slightly longer paragraph becomes
an outlier in every scaled dense dimension. This is why hard
single-digit paragraph counts are nasty.

## False negatives (predict 0, gold 1)

**Close register, shared topic.** The hard band by construction. Two
careful first-person photographers talking about fixer trays will
share `the`, `and`, `in`, sentence length, and character 3-grams like
`ing` / `the`. You need a cue they do not share: contraction rate,
hedges, or a rare punctuation habit.

**Short paragraphs.** A 28-word join does not estimate Yule's K.
Cosine on function words is high-variance. Character 3-grams overfit
the few content stems that happened to appear.

**Returning author with a topic shift in between.** Pairwise tagging
does not remember author 1. That is not a false negative of the
*stated* task — the bits can still be right — but a clustering
head-film will trick you into expecting `[1, 0]` when gold is `[1, 1]`.

## Leakage that looks like success

On easy documents, topic Jaccard spikes at the gold joins. If you
let it vote, easy F1 becomes a topic-segmentation score. That is a
bad oral. Always compare `--use-topic` against the default on easy
*and* hard. The gap should shrink on hard. If it does not, your
"topic" channel is still picking up style (or your hard documents
are not actually same-topic).

## Systematic bias of this ensemble

Weights put 0.50 of the mass on function-word and character n-gram
cosine. Documents whose authors differ mainly in *punctuation
choreography* but share a closed-class profile will be under-flagged.
Documents whose authors differ in genre will be over-flagged. That
bias is acceptable for a teaching baseline and unacceptable as a
silent assumption in a shared-task write-up.

## What to write in an error analysis paragraph

For each miss, name:

1. the gold bit and the predicted bit;
2. the channel with the largest score;
3. a human-readable cause (length shock / close register / topic
   leak / too short);
4. one feature you would add or one sequential trick you would try.

Do not write "the model failed because style change is hard".
