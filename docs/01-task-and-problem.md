# Task 1: What style change detection actually asks

Style change detection (SCD) is not authorship attribution and it is not
topic segmentation, although exam questions like to put the three in a
line and ask you to separate them.

- **Authorship attribution** starts with a closed set of candidate
  writers and a pile of labelled text for each. The job is
  classification: given a new document, name the author.
- **Authorship verification** is a pairwise yes/no: are these two
  documents (or a document and a profile) by the same person?
- **Style change detection** starts with *one* document and no named
  authors. The job is to decide whether the writing style is
  homogeneous and, if not, where it shifts and how the pieces group.

The usual exam decomposition, inherited from the PAN shared tasks, is
three nested questions.

## Three nested questions

1. **Mixture.** Is the document multi-authored? This is a document-level
   binary label. A system that always answers "yes" can look strong on a
   collection that happens to be mostly mixed. Always report the class
   balance.
2. **Boundaries.** Between which consecutive paragraphs does the style
   change? This is a sequence of binary labels, one per inter-paragraph
   gap. The unit is almost always the paragraph because sentence-level
   labels are unstable and word-level labels are not a realistic exam
   setting.
3. **Authors.** Assign a latent author id to each paragraph. The ids
   have no external meaning. Getting `{0,0,1,1}` when the gold is
   `{7,7,3,3}` is a perfect score. That is why accuracy on raw ids is
   the wrong metric; see [04-evaluation.md](04-evaluation.md).

The third question is strictly harder than the second. Adjacent
boundaries give you *contiguous blocks*. Recovering a writer who leaves
and later returns requires comparing non-adjacent paragraphs, which is a
clustering problem.

## What "style" means here

Style, in this project, is a habit of *choice under weak constraint*.
Topic often forces nouns (`enzyme`, `sonata`, `invoice`). It rarely
forces whether you write `however` or `but`, whether you contract
`do not`, or whether your sentences run 12 words or 28. Those leftover
choices are the stylometric signal.

That definition has consequences:

- Content words are usually the wrong features for SCD. They track
  topic, and a single author can change topic without changing style.
- Function words, punctuation, and a few morphological habits are the
  right first inventory. They are frequent, closed-class, and only
  loosely tied to subject matter.
- The signal is statistical, not legal. One paragraph of quoted speech
  can look like a second author. A heading can look like a third.
  Exam answers should mention these confounds before claiming the
  method is robust.

## Why the paragraph is the unit

A paragraph is long enough for frequencies to be estimated and short
enough to localise a change. Shared-task datasets typically put one
paragraph on each line; prose notes often separate paragraphs with a
blank line. The tokenizer in this repo accepts both.

If a paragraph is very short (a one-word reply, a list item, a
caption), every rate feature becomes a coin flip. The detector therefore
exposes `min_words` and skips units below that floor. On an exam, say
that you would either merge short paragraphs into their neighbour or
refuse to score them.

## Single-author variation is not a change point

Even a single writer varies. Openings are denser than conclusions.
Examples are more informal than definitions. Dialogue is not the
narrator. A competent answer distinguishes:

- **Register shift inside one author** (a quotation, a bullet list, an
  equation block)
- **Authorial style change** (a second person takes over the keyboard)

Distance methods cannot see the difference. They only see that the
vector moved. That is a limitation you should be willing to write down
in a short-answer question.

## What this repository implements

A closed stylometric vector per paragraph, a 4-D projection you can
name out loud, adjacent Euclidean distances, a floor-plus-gap
threshold, and average-linkage clustering for returning authors. It is
a baseline you can run, inspect, and criticise. It is not a claim
about the state of the art.

The example documents are original study texts written so that the
formal / casual / procedural contrast is obvious in the features
students are expected to name.
