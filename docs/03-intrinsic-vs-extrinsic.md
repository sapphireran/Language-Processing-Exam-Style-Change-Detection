# Intrinsic vs extrinsic authorship

Write this distinction down before you open a notebook.

## Extrinsic

You have a questioned document **and** a set of candidate authors with
known texts. You build a profile for each candidate (function-word
rates, Delta, a classifier) and ask who the questioned text is closest
to. That is authorship *attribution* or *verification*.

## Intrinsic

You have only the questioned document. You ask where it stops being
self-similar. That is style-change detection, and it is the only
authorship problem you can still pose when there is no comparison
corpus — which is exactly the plagiarism case the shared-task text
keeps repeating.

## Why intrinsic is harder

A two-author document with a single late seam looks, locally, like
one author who got tired. Short units have unstable rates. Topic
shifts imitate register shifts. Returning authors break the "new
author at every 1" story.

Extrinsic methods leak into exam answers as wishful thinking:
"we would just cluster the paragraphs and match them to authors."
Without profiles, clustering still needs a distance that is about
style. You have only moved the same problem into an unsupervised
box.

## Gift authorship and the exam story

A common oral prompt: a paper lists four authors; the abstract sounds
like one lab's house style; the methods paragraph suddenly uses
contractions and second person. Intrinsic detection is a *hypothesis
generator* ("something changed here"), not a legal finding. See
[problem-11](../examples/corpus/problem-11-gift-authorship.txt) and
the ethics note in the failure gallery.

## What to say if they ask for transformers

A sentence encoder can be an intrinsic detector: embed two windows,
take cosine distance, threshold. That is still intrinsic. It becomes
extrinsic only if you compare those embeddings to stored author
vectors. The exam risk is not "neural vs classical". The risk is
**topic leakage** — contextual embeddings are very good at topic.
On Hard documents that is a bug.
