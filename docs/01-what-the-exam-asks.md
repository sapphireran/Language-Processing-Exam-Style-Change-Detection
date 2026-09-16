# What the exam asks

Style-change detection is the *intrinsic* half of authorship analysis. You are given one document and no comparison texts. The question is not "who wrote this?" It is "where, if anywhere, did the writer change?"

A useful picture: the document is a chain of units (sentences in this lab, paragraphs in some shared-task years). Every pair of neighbours is a **hinge**. The hinge either holds (same writer) or snaps (style change). The official answer is a binary array, one bit per hinge.

```
units:     u0    u1    u2    u3
hinges:      h0    h1    h2
changes:     0     1     0
```

If `changes = [0, 1, 0]` the writers are something like A A B B. That is the only thing the array can say. It cannot say that A came back later. See problem-22.

## Why the task exists

- Plagiarism when you have no source text to compare against.
- Gift authorship: a polished abstract pasted under a student paragraph.
- Shared accounts and compromised voices.
- Writing-support tools that flag a sudden register jump.

None of those jobs are solved by topic keywords. A single writer can change subject. Two writers can share a subject. The exam will try to make you forget that.

## Shared-task memory (for the oral)

Rough shape, not a chronology you must recite:

- Early editions asked "single vs multi-author" and then "how many authors."
- Later editions asked for paragraph-level change points, then sentence-level ones.
- Datasets that mix topic with authorship let a bag-of-words model cheat. Later editions try to hold topic still.

This repo does not ship shared-task files. The teaching stand-in is `examples/corpus/`: easy files let topic and register move together, medium files hold the topic, hard files hold the topic *and* keep the two voices close.

## What a good short answer sounds like

> I treat every consecutive pair as a hinge. I score the hinge with closed-class and register features, not with the nouns. I cut the score with a threshold I can defend, and I report macro-F1 because holds dominate. If a writer returns, the binary array under-counts authors.

That is the whole lab in four sentences. The rest of the notes unpack it.
