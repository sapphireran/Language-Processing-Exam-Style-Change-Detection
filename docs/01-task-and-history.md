# Task definition and a short history

## The question you are actually answering

Given one English document, mark every paragraph boundary where the
*author* changes. You do not get a list of candidate authors. You do
not get other documents by those authors. You only get the text itself.
That is why the task is called **intrinsic**.

For a document of `n` paragraphs the system emits a binary vector of
length `n - 1`:

```
changes[i] = 1  if paragraph i and paragraph i+1 have different authors
changes[i] = 0  otherwise
```

Three assumptions are part of the task, not implementation details:

1. Style changes occur only at paragraph boundaries.
2. A paragraph has exactly one author.
3. A document may have two to four authors (PAN 2023), and an author
   may return later. The official label is still just the adjacent
   change vector, so A-B-A and A-B-C look the same at the first two
   boundaries.

If an examiner asks "could we do this at sentence level?", the honest
answer is yes — PAN 2022 did — and it is harder because sentences are
short and the style estimate is noisy.

## Why the task exists

Intrinsic style-change detection is what you still have when there is
no reference corpus. That is the situation in:

- intrinsic plagiarism (a ghost-written passage inside a thesis)
- gift authorship (a polished abstract stapled onto student methods)
- collaborative documents where the edit history was stripped
- writing-support tools that flag an inconsistent voice

It is *not* authorship attribution. Attribution says "this looks like
Austen". Style-change detection says "paragraph 4 is not the same
person as paragraph 3".

## How PAN moved the goalposts

A compact timeline you can recite:

| year | what you had to do |
| --- | --- |
| 2016 | segment and cluster by author |
| 2017 | multi-author? if yes, mark the positions |
| 2018 | binary: single- vs multi-author document |
| 2019 | also guess the *number* of authors |
| 2020 | paragraph-level change flags |
| 2021 | multi-author flag + paragraph changes + author labels |
| 2022 | sentence-level changes as well |
| 2023 | paragraph changes again, but **topic is controlled** |

2023 is the edition this kit studies. The organisers built three
English Reddit-derived sets (easy / medium / hard) that differ in how
much topical variety you are allowed to exploit. All documents have
two to four authors. Evaluation is **macro-averaged F1** of the
per-document binary vectors.

## Input / output you should memorise

```
problem-42.txt          plain text, paragraphs separated by newlines
truth-problem-42.json   {"changes": [0, 1, 0, 1]}
```

This kit also stores optional `authors` and `paragraph_authors` so the
labs can talk about returning authors. A real PAN evaluator ignores
those keys.

## What a 2023 winner looked like

The competitive systems were not CUSUM charts. They were fine-tuned
DeBERTa-style encoders, often with contrastive losses or an NLI
prompt: "do these two paragraphs share an author?". You should be able
to say that in one sentence, then add: *classical stylometry is still
the right oral-exam story, because you can derive it on paper and you
can see where topic leaks in.*
