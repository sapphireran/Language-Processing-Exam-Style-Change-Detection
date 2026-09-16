# Oral cards

Thirty-second answers I want in muscle memory. The longer versions live
in [written model answers](11-written-model-answers.md).

## What is the task?

Mark every paragraph hinge where the author changes. Output a binary
array of length `n-1`. It is not "who wrote this."

## Why intrinsic?

We do not get a gallery of other texts by the same people. Gift
authorship and collaborative notes look like this. Extrinsic methods
are a different exam question.

## Why not accuracy?

Most hinges are zeros. Never-fire looks accurate. PAN uses F1. I also
define F1 = 1 when both vectors are all zeros so a correct
single-author document is not punished.

## Why compression?

Same author, shared regularities, cheaper concatenation. NCD asks that
without me listing the regularities. zlib approximates Kolmogorov
complexity from above. On this bank NCD saturates around 0.85 on
80-word original paragraphs, so I keep it as the thesis and let a
register axis plus a within-document peak make the bit. Short text
and topic are the two reasons I do not use NCD alone.

## What is NCD?

`(C(xy) - min(C(x),C(y))) / max(C(x),C(y))`. Low means the compressor
reused structure. I clamp it because real compressors overshoot 1.

## Why function words?

They are frequent, half-conscious, and they do not name the topic. L1
on a closed list is the topic-light channel. Burrows' Delta is the
extrinsic cousin; I am not using Delta because I have no candidate set.

## Easy / medium / hard?

Easy lets topic leak. Hard holds topic still. I added trap files: same
voice, new topics. A content model should fail those on purpose.

## What is a quoin?

A letterpress wedge that locks type. Metaphor: do two paragraphs lock
as one voice? Also the name of the tiny detector: a register-heavy
score with a within-document peak, and NCD sitting next to it as the
method I can derive on a whiteboard even when it saturates.

## When would you use a transformer?

On a real shared-task submission, with a hard split that punishes topic
cheating, and with an error analysis I can still explain. Not as my
only oral answer.

## Ethics in one breath

A hinge is not an accusation. I will not run this on a classmate's
work to "catch" them. See the ethics page.

## Author return?

A, B, A produces two ones, not a new label C. Clustering paragraphs
is a further task. This exam asks for hinges.

## Gift authorship?

One inserted house. Mark the two hinges around it. Do not mark the
student paragraphs as different from each other just because the
abstract arrived.
