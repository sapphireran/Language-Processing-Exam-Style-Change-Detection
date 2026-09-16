# Written model answers

These are answers I would be happy to hand in. They are not
copied from a past paper. If a real paper uses different wording,
I adapt; I do not force the saw onto a question that asked for
something else.

## 1. Define style change detection and distinguish it from authorship attribution.

Style change detection is an *intrinsic* task: given one document
and no comparison texts, mark the positions where the writer
changes. Authorship attribution is *extrinsic*: given a closed or
open set of candidate authors with samples, name the writer of a
questioned text. A change vector can exist without any names. A
name can exist without any internal cut. Gift authorship and
undetected plagiarism sit on the intrinsic side; a disputed
Federalist paper sits on the extrinsic side.

## 2. Why do topical cues make the task easier, and why is that a problem?

If authors also change topic, a content model can mark the hinge
without ever seeing a function word. That inflates scores on
heterogeneous collections and collapses when a later edition holds
the topic still (PAN 2023–2025). A method that only works on the
easy band has not detected style.

## 3. Give three stylometric feature families that survive a topic swap.

Closed-class frequencies (articles, prepositions, pronouns,
deontics). Sentence and word-length geometry. Punctuation and
contraction rates. I would not list topical n-grams, named
entities, or embedding cosine on raw lexical overlap.

## 4. Write the split score and explain the size weight.

`score(k) = ||μ_left − μ_right|| · √(k(n−k)/n)`. The Euclidean
term is the kerf. The square-root term is the two-sample factor:
it down-weights a cut that peels off a single paragraph unless
that paragraph is violently unlike the rest.

## 5. Why report macro-F1 rather than accuracy?

Hinges are imbalanced. A never-change predictor can be the
accuracy winner. Macro-F1 averages the change-class and
same-class F1 and makes that predictor look like what it is.

## 6. Describe a case where a pairwise hinge score and a split score disagree.

An ABA document. Each local step can be large while each global
split is mixed. A z-scored pairwise peak may fire nothing (both
steps are "normal" for that file). A split score may fire the
better of the two cuts and then need a second rule — recursion or
an absolute adjacent floor — to recover the other.

## 7. What ethical limit do you put on a detector like this?

I will use it on text I wrote, or on a shared-task corpus with
posted terms. I will not treat a score on an unseen student's
essay as evidence of misconduct. False positives on short
functional prose are ordinary, and the cost of a false accusation
is not a metric I get to average away.
