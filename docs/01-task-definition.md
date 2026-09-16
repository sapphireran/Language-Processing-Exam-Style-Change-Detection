# 1. Task definition

## The question the exam is actually asking

You are given **one document** and no other texts. Several people may have
written it. Your job is to mark the *boundaries* where the writer changes,
using only evidence inside that document.

That problem is called **intrinsic style-change detection** (also
"multi-author writing-style analysis"). It is intrinsic because the
system never sees a gallery of known authors and never searches a
plagiarism corpus. The only signal is variation *inside* the text.

If you can do this reliably, you have a building block for:

- plagiarism detection when the source is not in any index
- spotting gift authorship or uncredited splices
- writing-support tools that warn "this paragraph does not sound like you"
- preprocessing for authorship attribution (first find the segments)

## Three neighbouring tasks (do not mix them up)

| Task | Input | Output |
|------|--------|--------|
| Authorship attribution | A disputed text + a closed set of candidates | Which candidate wrote it |
| Authorship verification | A disputed text + one claimed author (with samples) | Same author or not |
| Style-change detection | One document, no candidates | Positions of switches |

Attribution and verification are *extrinsic*: they need comparison texts.
Style change is *intrinsic*. An exam question that says "no reference
documents are provided" is pointing at the intrinsic setting.

A related but weaker question is **single- vs multi-author classification**:
is this document homogeneous? That is PAN 2018-style. Later editions ask
for the *locations* of changes, which is strictly more informative.

## Units and pairwise labels

The document is cut into ordered units `u[1] … u[n]`. Recent shared tasks
use **sentences**. Earlier ones used **paragraphs**. The label is not
"who wrote unit i". It is:

```
y[i] = 1  if author(u[i]) != author(u[i+1])
y[i] = 0  otherwise
```

So `y` has length `n-1`. A six-sentence document with a single switch
after sentence 3 is `[0, 0, 1, 0, 0]`.

This design has consequences:

1. **A one-unit document is unanswerable.** There is no pair.
2. **Author identity is only recovered up to segmentation.** The labels
   do not name authors A/B/C; they only cut the text into same-author
   runs. Reconstructing an author *index* from `y` is easy (start at 1,
   increment on every 1) but the numbers are arbitrary.
3. **Clustering the units into k authors is a different objective.**
   It can agree with `y` after the fact, but the official metric scores
   the pairwise cuts, not the cluster IDs.
4. **Changes are assumed not to occur inside a unit.** If the unit is a
   sentence, a sentence is treated as single-authored. That is a
   modelling assumption, not a linguistic truth.

Paragraph-level units are longer, so each pair has more style evidence
and the task is easier. Sentence-level units are short, noisy, and closer
to how people actually splice text. If an exam question asks why sentence
level is harder, "less signal per pair, more pairs, more class imbalance"
is the short answer.

## Intrinsic signal vs topic leakage

The scientific claim of stylometry is that some habits are **authorial**:
function-word rates, punctuation, contractions, preferred syntactic
shapes, average word length. Other habits are **topical**: named
entities, content nouns, domain jargon.

If authors also change topic when they change turns — "Alice writes about
baking, Bob writes about GPUs" — a bag-of-words model looks brilliant
and has learned the wrong thing. Shared-task organizers therefore publish
three bands:

**Easy.** Units wander across topics. A topical change is a cheap proxy
for an author change. Lexical overlap features will look strong.

**Medium.** Topic variety is reduced. Content words still help a little,
but function-word and punctuation features start to matter.

**Hard.** Units stay on one topic. Content overlap between neighbouring
sentences is high even when the author changes. Systems that only
compare "aboutness" collapse.

A clean experimental question, and a common exam essay prompt, is:
*does your method still work when topic is controlled?* If the answer
is no, you built a topic-segmentation system and labelled it stylometry.

## What a system is allowed to use

Typical exam / shared-task rules:

- You may use any features computed from the input document.
- You may train on the provided training split (and, if the rules allow,
  on extra public data you also release).
- You may not look at the hidden test labels.
- You must emit one solution file per problem file, even if you abstain
  (guessing `0` everywhere is still a legal output).

This repo's toy corpus follows the same *shape* of those rules. It does
not include official data.

## A minimal formalisation

Let a document be a sequence of units. Let `f(u)` be a feature vector
for a unit (length, function-word histogram, punctuation rates, …).
A pairwise classifier is any function

```
g(f(u[i]), f(u[i+1])) -> {0, 1}
```

or a score in `[0, 1]` that is later thresholded. Everything in
`src/scd` is an instance of that template: extract `f`, concatenate
absolute differences and similarities, train a linear model for `g`.

You can replace `g` with a transformer that reads the raw pair. The
*task* does not change. The *inductive bias* does: a pretrained language
model has seen a lot of topic structure, so it is even more tempted to
use aboutness unless the training data punishes that.

## History in one page (for timeline questions)

Approximate public progression of the PAN-style problem:

- 2018: is the document multi-author?
- 2019: how many authors?
- 2020–2021: style change between consecutive *paragraphs*
- 2022: also locate changes, including some sentence-level work
- 2023–2024: paragraph-level changes, with topic explicitly controlled
  across easy / medium / hard
- 2025–2026: sentence-level changes, same three-band idea

You do not need the year list in an exam unless the question asks for
it. What you do need is the *why* of each step: first detect
heterogeneity, then count authors, then locate cuts, then shrink the
unit, then stop topic from leaking the answer.

## Assumptions this repo makes on purpose

- English only.
- Units are sentences unless a file is explicitly paragraph-split.
- A sentence has one author.
- Style habits are stable enough *inside* a short synthetic document
  that a linear model can see them.
- We evaluate on pairwise macro F1, not on author-ID accuracy.

If a short-answer question is "list three assumptions of the pairwise
sentence-level setup", those first three bullets are a complete answer.
