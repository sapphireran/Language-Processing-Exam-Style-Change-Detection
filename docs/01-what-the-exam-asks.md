# What the exam asks

The shared-task sentence I am rehearsing is this:

> Given a document, mark every paragraph boundary where the author
> changes.

That is *style-change detection*, sometimes sold under the longer PAN
name **multi-author writing style analysis**. It is not "who wrote this?"
It is "where did the writer stop being the same person?"

I care about the difference because the first question is *authorship
attribution* (a closed or open set of candidates, a pile of comparison
texts). The second question is what you still have when you do **not**
have that pile. Gift authorship, collaborative notes, a pasted exam
answer, a paragraph a supervisor "helped" with: those are style-change
problems long before they are attribution problems.

## The unit is the hinge

A document of `n` paragraphs has `n-1` hinges. Each hinge is a binary
question:

- `0` — the two paragraphs are still the same author
- `1` — they are not

The output is a JSON array of those bits. Nothing else is required for
the official format. I also store optional `authors` labels in my truth
files so I can talk about an author *returning* (A, B, A) without
pretending the third paragraph is a new person.

## Intrinsic, on purpose

The exam adjective is **intrinsic**. I am not allowed, in the story of
the task, to retrieve other documents by the same people and build a
nice author profile. I have to work from the document in front of me.
That constraint is what makes compression interesting: a compressor does
not need a gallery of candidates. It only needs two strings and a
question about shared structure.

Extrinsic methods (a trained verifier, a closed-set classifier, a
retrieval index) are allowed in the real world. I would use them if I
had the data. I would also have to say, in the oral, that they are a
different task.

## Three difficulties I must be able to name

PAN 2023/2024 controlled *topic* as a leak:

- **easy** — paragraphs wander across topics, so a content model can
  masquerade as a style model
- **medium** — less topical variety; style has to do more of the work
- **hard** — one topic all the way down

My toy bank copies the idea, not the Reddit data. I added two extra
bands the oral likes: **trap** (same voice, new topics — a detector
should stay quiet) and **return** (A leaves and comes back).

## What I will say if they ask "is this plagiarism detection?"

It is a neighbour, not the same house. Intrinsic plagiarism detection
asks whether a document contains a borrowed *passage* when you do not
have the source. Style-change is the hinge version of that question. I
will not claim that a `1` on a hinge is proof of theft. It is a flag
that two neighbouring paragraphs do not lock.
