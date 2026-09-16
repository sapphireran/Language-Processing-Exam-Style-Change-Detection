# Oral cards

Short answers I can say without looking at the repo. If I cannot
say them, I have not revised.

## What is the task?

Given a document, mark every paragraph hinge where the author
changes. Intrinsic: no comparison texts. Not attribution: I do
not name anyone.

## Why not pairwise?

Neighbours lie on short paragraphs, on ABA returns, and on topic
jumps. A left/right split asks whether this is the best place to
saw the file.

## What is in the vector?

Closed-class rates and sentence geometry. No nouns. The saw uses
a short fingerprint: person, deontics, contractions, hedges,
dashes, questions, a little *the*/*was*/digits.

## What is the penalty?

Blade width. First cut 0.22, recursion 0.40, adjacent floor 0.40.
Set on in-band files. Holdout is a quote.

## Why is accuracy a liar?

Most hinges are zeros. Never-fire looks accurate. I lead with
macro-F1 on both classes.

## Easy / medium / hard?

Easy: topic and house jump. Medium: house jumps, topic stays.
Hard: house jumps, topic stays, houses share a register. Trap:
topic jumps, house stays.

## How many authors?

The change vector does not say. ABA has two authors and two
changes. `1 + sum(changes)` over-counts. I would cluster after
cutting. I did not, because the exam I am revising is the vector.

## Failure I will volunteer

Document 27, last hinge, Seminar → Pocket on the same well. Both
are first-person-ish (`we` vs `I`). The adjacent step sits inside
the same-house cloud. Catching it would cut a true same-house
hinge elsewhere. I left it.

## Ethics in two sentences

Style change is used for plagiarism and gift authorship. A toy
detector on original text is revision. Running it on a student's
unseen essay as evidence is a different act and I will not blur
them.

## NCD in one sentence

Normalized compression distance is a lovely oral object (same
author, cheaper concatenation) and a poor tool on 80–120 word
paragraphs: zlib saturates. I did not make it the saw.
