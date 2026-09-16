# The task, in exam language

Style-change detection is an *intrinsic* authorship problem.

You are given **one document** and no candidate authors, no comparison
corpus, and no "this paragraph was copied from Wikipedia" pointer. The
only question you can ask is:

> Does the writing immediately before this point look unlike the writing
> immediately after it?

That is also the only setting in which style-change detection can stand
in for plagiarism detection, gift authorship, or "someone else finished
question 3 of the take-home". Extrinsic authorship attribution (Given
texts by A, B, and C, who wrote this?) is a different exam topic.

## What you have to emit

The layout copies the PAN multi-author writing-style analysis shared
task, because that is the format an examiner will recognise.

For a document `problem-X.txt` with *n* comparison units you emit
`solution-problem-X.json`:

```json
{ "changes": [0, 0, 1, 0] }
```

The array is length *n − 1*. Label `i` is the join between unit `i` and
unit `i + 1`. `0` means same author / same style; `1` means a cut.

Units are **sentences** in the later PAN editions and in most of the
bundled files (one sentence per line). They are **paragraphs** in PAN
2023 and in `problem-paragraph-gift.txt` (blank-line separated). A
single unit is assumed to be one author; you never cut *inside* a unit.

## Difficulty is about topic, not about vocabulary size

PAN editions after ~2022 go out of their way to stop you from cheating
with topic drift:

| name | what is allowed to change with the author |
| --- | --- |
| easy | topic *and* register |
| medium | mostly register; the topic stays close |
| hard | register only; the topic is held fixed |

A detector that lights up whenever the document starts talking about
cooking instead of syntax will ace the easy split and die on the hard
split. That is the point of the three names, and it is the first thing
to say in an oral exam if someone asks "why not just TF–IDF?"

## Why adjacent-sentence n-grams are a bad answer

Character 3-grams are a classic stylometric representation. They are a
bad *pairwise* representation of two isolated sentences:

- two sentences from the same person barely share 3-grams
- so the cosine at every boundary looks like a change
- so you predict `1` everywhere and the majority-class F1 collapses

The baseline in this repo therefore compares **blocks** (voice runs, or
mean register flags on each side of a cut), not raw 3-gram bags of two
lonely sentences. See [baseline.md](baseline.md).

## What this repository is not

The files under `examples/documents/` are **made-up exam answers**. They
are not the PAN Reddit dumps, they are not a claim about shared-task
numbers, and they are not company code. A collection macro-F1 of 1.0 on
eight hand-written stories means the baseline recovers the stories it
was designed around.
