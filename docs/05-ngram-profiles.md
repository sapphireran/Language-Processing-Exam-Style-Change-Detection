# 05 — Character n-gram profiles

If I am allowed one representation, I take character 3-grams.

## Construction

1. Lowercase the unit.
2. Pad with a single space on each side so the first and last letters
   have context.
3. Count every overlapping window of length `n=3`.
4. Treat the counts as a sparse vector.
5. Distance between units A and B is `1 − cosine(A, B)`.

Example, tiny on purpose:

```
A: "Add salt."
B: "The reaction proceeds slowly."
```

A produces grams such as ` ad`, `add`, `dd `, ` sa`, `sal`, `alt`.
B produces ` th`, `the`, `he `, ` re`, `rea`, `eac`, … They share
almost nothing. Cosine is near 0, distance near 1. That is an easy
pair.

Two academic sentences on the same topic share `the`, `ion`, `ing`,
` to`. Distance shrinks. That is the hard pair.

## Why I prefer characters to words on exam snippets

Word unigrams on a six-word SMS are a six-dimensional one-hot.
Character 3-grams still see `n't`, `!!`, `lol`, and the shape of
`gonna`. They also survive a spelling that a word tokenizer would
split.

Koppel-style authorship work used character n-grams as a workhorse
for exactly this reason. I do not need the rest of unmasking for the
exam. The profile-plus-cosine piece is enough.

## Unmasking, in one paragraph, if they ask

Koppel and Schler drop the features that most distinguish two texts
and ask whether the texts remain separable. If they do, the difference
was probably content. If they collapse, the difference was a thin
stylistic crust. I will not implement unmasking in thirty minutes. I
will say why the idea exists: **to stop topic pretending to be style**.

## Smoothing and empty units

A one-token unit has almost no 3-grams. Cosine against a long unit
is then noisy, not informative. The detector's absolute floor is there
so a quiet pair cannot win just because both sides are short and
unstable.

Add-λ on KL (see the window walkthrough) is the same anxiety in
probability language: never let a missing gram send `log(0)` through
the desk.

## What I say if they want "deep" features

A sentence transformer cosine is a character n-gram profile trained
on the internet. It works. It also encodes topic extremely well, which
is why it shines on the easy split and lies on the hard split. I will
use it in a project. I will not use it as my only exam answer.
