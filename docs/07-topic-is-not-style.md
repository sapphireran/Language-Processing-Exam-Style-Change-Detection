# Topic is not style

This is the argument the Hard split exists to make.

## The confound

Authors often change *when the subject changes*: a new contributor
writes the methods, a friend pastes a recipe, a second commenter
arrives. A detector that keys on nouns will look brilliant on those
documents and helpless on two lab notes about the same assay.

PAN's later editions built Easy / Medium / Hard so you cannot hide
in the first case.

## A concrete pair from this repo

In `problem-02-bikes-vellum.txt` the document moves from street
cycling in Nørrebro to parchment repair. Topic shift and author
shift are aligned. A content model scores a hit. A register model only scores a hit
if the voices also differ (here they do: lowercase chat vs
conservator `we`).

In `problem-14-two-bakers.txt` both writers stay on the same rye
loaf. The nouns (`rye`, `starter`, `crumb`) barely move. What moves
is person, hedging, and sentence length. If your Easy F1 is 1.00
and your Hard F1 collapses, you have measured the confound.

## How to test yourself without a leaderboard

1. Run the default threshold detector on `examples/corpus`.
2. Sort documents by Easy / Medium / Hard / Control (see the
   manifest).
3. If Easy is perfect and Hard is near the majority baseline, write
   that down as a *result*, not as a disappointment.
4. Ablate the function-word channel to 0 and watch Easy stay high.
   That is the smoking gun.

`scripts/run_curriculum.py` prints that table. Quote it in the oral.

## Content-word Jaccard as a diagnostic

`seamtrace.explain` computes a crude content-word shift
(\(1 - |A \cap B| / |A \cup B|\) on tokens longer than 3 that are
not function words). If that number is high and the function-word
cosine is low, a false alarm is labelled `topic_confound`.

That label is a teaching device. It is not proof. Two authors can
also change the nouns. But if you *only* fire when Jaccard is high,
you are not doing stylometry.

## What not to do in the written paper

Do not write "we controlled for topic by using TF-IDF". TF-IDF
still lives in the content vocabulary. Do write "we restricted the
primary vector to a closed class and used topic shift only as an
error tag."
