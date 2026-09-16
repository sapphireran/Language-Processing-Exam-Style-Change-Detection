# Burrows' Delta and closed-class lists

## The one-paragraph version

Burrows (2002) takes the relative frequencies of a fixed list of
function words, z-scores each word across the texts in the
comparison, and defines Delta as the mean absolute difference of
those z-scores. Large Delta: unlike. Small Delta: alike.

It is a distance between **profiles**, not a neural embedding. The
whole point is that the coordinates are interpretable (`of` is
elevated, `you` is absent).

## What Seamtrace actually computes

For a pair \((u, v)\) inside a document, each function-word bin is
z-scored using **all units in that document** as the sample. Delta
is then

\[
\Delta(u,v) = \frac{1}{M} \sum_{j=1}^{M} |z_j(u) - z_j(v)|
\]

with \(M = 100\) in this lab.

That is a local, exam-sized Delta. Classic papers compare whole
novels against a corpus of novels. We do not have novels. We have
sentences. So the z-score sample is small and the estimate is
noisy. Say that out loud.

## Why z-score at all?

Raw frequencies make `the` dominate `however`. Z-scoring asks
whether *this unit* uses `however` more than *this document*
usually does. Two units can both use `the` a lot and still differ
on the rarer closed-class items.

If the document is three sentences long, the z-score sample is
three points. Delta then becomes a fancy restatement of the raw
difference. That is why Hard documents with short units are where
Delta looks least magical.

## Closed-class vs content

A content word that appears once (`vellum`) has a huge relative
frequency in an eight-word sentence and zero next door. Delta on
content words is a topic detector. The exam phrase is:

> I keep the list closed so a change of subject is not automatically
> a change of author.

## What to do if they ask for variations

- **Quadratic Delta / Eder's Delta.** Weight rarer items more, or
  raise frequencies to a power. Mention it; do not implement it
  unless you have time to re-tune the blend.
- **Cosine Delta.** Use cosine on the z-scored vector instead of
  mean absolute difference. Related, not identical.
- **Different M.** 50–200 function words is the usual teaching
  range. Adding content adjectives is how people accidentally
  cheat on Easy.

## Implementation note

`the` at the start of a sentence is still `the`. Do not drop it
because a tokenizer lowercased it. Do drop `The` as a separate
type — that is case leakage, not style.
