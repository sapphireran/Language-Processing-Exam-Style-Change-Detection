# Pairwise scores, windows, and CUSUM

## The default object

For units \(u_i, u_{i+1}\) Seamtrace computes four distances and
blends them:

| Channel | Default weight | Role |
| --- | --- | --- |
| Function-word cosine distance | 0.35 | Closed class |
| Character-trigram cosine distance | 0.10 | Orthography |
| Register scalars (person, contractions, case) | 0.40 | Speech vs memo |
| Bounded Burrows' Delta | 0.15 | Closed-class, z-scored |

The blend is the **pair score**. A detector turns scores into bits.

The weights are a teaching choice. If you raise the scalar weight, Easy
documents get easier (length and `!` fire) and Hard documents get
noisier. If you zero the function-word channel, you have mostly built
a topic-plus-punctuation detector.

## Why not classify one sentence?

A single sentence does not have a stable TTR. Pairwise comparison
asks a better question: *is this sentence unlike its neighbour?*
That matches the gold format and keeps the label local.

The default detector uses a window of **one** unit on each side so
the gold seam stays local. Windows of 2–3 units trade locality for
stability. They help when a writer inserts one short acknowledgement
(`Thanks.`) inside an otherwise consistent block. They hurt when the
seam is a clean block change — the neighbouring pairs become mixed
author bags and the labelled boundary is no longer the tallest spike.

## Detectors

**Threshold.** `score >= 0.42` → 1. Simple, comparable across
documents, better on Medium register shifts than on Easy topic
jumps, and still capable of false alarms on Controls.

**Adaptive.** `score >= max(0.22, mean + 0.85 · std)` inside *this*
document. A Hard document with a low, tight score band can still
surface its tallest spike. A Control document with one topical
aside can still false-alarm on that aside.

**Ensemble.** A change if either voter fires. That is a recall bias.
The oral line: "I would rather over-flag and inspect than miss the
only seam in a gift-authorship abstract."

## CUSUM as an explanation, not a scorer

`seamtrace.cusum` walks the document, scores each unit against a
short left context, subtracts the document mean, and accumulates.
A late author who is consistently unlike the opening will produce a
long climb. A single weird sentence produces a spike that falls
back.

Use the trace in HTML reports to *talk* about structure. Do not
treat a homemade CUSUM peak list as the official `changes` array
unless you have validated it — the default exam detector is still
the pairwise cut.

## Hand-size example

Take three toy sentences:

1. `I think we should probably go.`
2. `I guess we should maybe stay.`
3. `One might argue that remaining is preferable.`

1 vs 2 share first person, `should`, and hedges. 2 vs 3 loses
contractions and first person and gains `one` / `that` / `is`.
The second boundary should outscore the first. If your implementation
disagrees, you have a normalisation bug, not a new scientific
result.
