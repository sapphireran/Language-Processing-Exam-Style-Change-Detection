# Intrinsic vs extrinsic authorship

Keep the three neighbouring problems separate. Examiners like it when
you can draw the Venn diagram on a whiteboard.

## Extrinsic attribution

You have a questioned document *and* writing samples from candidate
authors. The system says "this is closer to author A than to author B".
That is nearest-neighbour classification in stylometric space. Burrows'
Delta was built for this setting.

## Verification

You have a questioned document and *one* claimed author. The system
says "same person" or "not". The score needs a threshold, and the
threshold needs calibration, because the class prior is a policy
choice (court vs inbox filter).

## Intrinsic style change

You have only the questioned document. No candidates, no claimed
author. You look for **seams**: places where the local writing habit
stops matching the local context. That is this exam.

Intrinsic methods are what you use when:

- a paper may contain a gift-authored abstract
- a student answer may switch from notes to a memorised paragraph
- a leaked document may be a collage of emails
- you suspect plagiarism but have no source to align against

They are also strictly harder. Every feature you compute has to be
estimated from a few dozen words. Variance is the enemy. That is why
this kit reports rates, not raw counts, and why it z-scores inside the
document before comparing neighbours.

## Closed class vs open class

Open-class words (nouns, verbs, adjectives) carry topic. Closed-class
words (articles, prepositions, pronouns, auxiliaries) carry habit.
Mosteller and Wallace's work on the Federalist Papers is the usual
citation: the rates of *upon*, *while*, and *whilst* separated Hamilton
from Madison better than the political nouns did.

A sentence you can say out loud:

> I trust function-word rates and character n-grams first because they
> are frequent, weakly referential, and reusable across topics. I treat
> rare content words as a topic alarm, not as a style proof.

## Single-author documents are part of the task

A document with gold `changes = [0, 0, 0]` is not a trick. A system
that cannot keep its hands off the "change" button will bleed
precision on the single-author items and the easy "same author, new
example" spans. The dummy baseline "always 0" exists so you can show
that your F1 is not an accuracy costume.
