# From distances to a `changes` vector

## The decision the shared task wants

You do **not** have to recover author IDs. You have to emit a bit for
each adjacent pair. Clustering (A-B-A) is a harder problem that this
kit only discusses, via `paragraph_authors` in the gold files.

## Ensemble used here

For each adjacent pair we compute seven scores:

- Burrows Delta on function words
- character 3-gram cosine distance
- absolute formality jump
- relative sentence-length jump
- contraction-rate jump
- cosine on the dense z-scored vector
- mean adjacent |ΔCUSUM| on three channels

Each score has a *floor* and a *strong* threshold (see
`scdkit.detect.THRESHOLDS`). A pair is flagged if

- at least one channel is strong, or
- at least two channels clear their floor.

That rule is the entire "model". There is no logistic regression.

## Why not a pure z-score of distances?

If a single-author document has four paragraphs and one of them is
slightly longer, that pair is the local maximum. A z-score rule will
invent a change. Hard floors stop that. You trade some recall on the
hard circadian document for fewer false alarms on the landlord letter.
That trade-off is the exam answer; the numbers are just one setting.

## Other algorithms you should be able to sketch

**Thresholded pairwise.** What we do.

**Sliding-window comparison.** Compare paragraph \(i\) to the
concatenation of \(i-k \ldots i-1\). More stable, blurs short
authors.

**Agglomerative clustering.** Distance matrix over all paragraph
pairs, cut the dendrogram, then read adjacent label changes. This
*can* recover A-B-A. PAN 2023 does not require it.

**Neural pairwise classifier.** Encode \((p_i, p_{i+1})\) with a
transformer, train on gold bits. Best numbers on the shared task.
You must then explain leakage (topic, subreddit jargon) and why the
hard split still hurts.

**Change-point statistics.** PELT, Bayesian online change-point, HMM
with author states. Mention them; do not pretend this repo implements
them.

## Returning authors

Gold file `07_return_ferry.json` is `paragraph_authors = [1, 2, 1]`
and `changes = [1, 1]`. Any system that only emits `changes` has
already thrown away the identity of paragraph 3. If the oral goes
there, say: *binary adjacent labels are a detection task;
re-identifying a returning author is clustering / attribution.*
