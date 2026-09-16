# A saw, not a classifier

The exam question is usually written as classification: given two
neighbouring paragraphs, is there a style change between them? That
wording is a trap. It invites a pairwise model — extract features from
each side, score the pair, threshold.

Kerf refuses that framing. A document is a *walk* on a small
closed-class space. A style change is a *change-point* in that walk.
The object I defend is a **saw**: I ask, for each place I could cut,
how cleanly the two sides pull apart.

## Why the wording matters

Pairwise classification treats hinge *i* as if hinges *i-1* and *i+1*
did not exist. That is fine when a document is AAAAABBBBB. It is
clumsy when the document is ABA, or when one paragraph is short, or
when two houses share a topic and the local step is modest.

A split score uses every paragraph to the left and every paragraph to
the right. One quiet paragraph cannot hide a house that occupies half
the file. One loud paragraph cannot fake a house unless I refuse to
pay a penalty for a tiny side.

## What I will say in the oral

> I do not classify neighbours. I saw the document. The kerf is the
> gap the blade leaves. If the best kerf is narrower than the blade,
> I do not cut.

That is the whole thesis. Features, I/O, and F1 are how I keep the
thesis from becoming a metaphor.

## What this repo is not

- Not a PAN 2024/2025 submission.
- Not trained on Reddit, news, or anyone else's homework.
- Not company code and not a workplace corpus.
- Not an authorship *attribution* system. I never name an author. I
  only mark where the hand changes.

The twenty-eight documents in `examples/corpus/` exist so I can show
the saw working, and so I can show the one place it does not.
