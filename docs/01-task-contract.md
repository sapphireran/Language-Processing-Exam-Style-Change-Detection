# 01 — Task contract

## One sentence

Given a single English document, emit a bit for every pair of
neighbouring paragraphs: did the author change between them?

No candidate-author gallery is provided. You do not name the authors.
You do not count them except as a side-effect of the bit vector.
You do not look outside the document. That is what **intrinsic**
means.

```
P1  I lock the bike under the stairs and hope the tide has not
    soaked the bottom of the basket again.
P2  Helmet's on the hook. Lights still work. Fine.
P3  Conservation of nineteenth-century ledgers, however, is
    governed by the interaction of iron-gall ink with residual
    sizing in the paper support.
P4  Relative humidity above sixty percent accelerates that
    corrosion; below forty percent the sheets cockle.

changes = [0, 1, 0]
```

The `1` sits on the *boundary after P2*. Length of `changes` is always
`n_paragraphs - 1`.

## What PAN asked in 2023

The 2023 multi-author writing style analysis task (PAN @ CLEF) is the
template this lab copies:

- **Input:** one document per problem, paragraphs separated by a blank
  line. Read files with `open(path, "r", newline="")` so a Windows
  `\\r\\n` does not get rewritten before you split.
- **Output:** `solution-problem-X.json` containing `{"changes": [0, 1, ...]}`.
- **Positive class:** a style change (`1`).
- **Evaluation:** F1 on those bits, reported separately on three
  difficulty bands.
- **Submission shape:** a CLI that takes an input directory and an
  empty output directory.

This repository does not contain PAN/Reddit data. The contract is
copied; the documents are original teaching prose.

## Difficulty is about topic, not about author distance

| Band | Topic structure | What a lazy system will do |
| --- | --- | --- |
| Easy | Neighbouring paragraphs often change topic when they change author | Classify topic and call it style |
| Medium | Topical variety is small but not zero | Mix of leakage and actual style |
| Hard | All paragraphs share a topic | Topic features go quiet; style has to work |

An oral answer that says "hard means the authors are more similar" is
half-wrong. Authors *may* also be closer, but the official knob is
topic control. If you cannot say that sentence, you do not yet have
the task.

## Constraints you will be asked to recite

1. Style changes occur **only between paragraphs**. A paragraph is
   single-author by construction.
2. The number of authors is arbitrary. It is not a classification
   into "one vs two".
3. Documents are English.
4. You may use extra training data in the real shared task; this lab
   does not, because the point is to see the features.
5. Intrinsic: no comparison texts for the candidate authors.

## Adjacent-pair tagging is not clustering

You could cluster paragraphs in style space and then cut whenever the
cluster id changes. That is a legal method. The required *output* is
still a sequence of adjacent bits, not a partition. Two non-adjacent
paragraphs by the same author with a stranger in between should
produce `changes = [1, 1]`, not "there are two authors so maybe [1, 0]".
The task does not ask you to re-identify returning authors. It asks
whether *this* boundary is a join.

That is why the scarf-joint metaphor: you inspect the splice in front
of you. You do not inventory the whole timber stack.

## File names

For a problem `problem-12.txt` the gold file is `truth-problem-12.json`
and your prediction is `solution-problem-12.json`.

```json
{
  "authors": 3,
  "changes": [0, 1, 0, 1]
}
```

`authors` is teaching metadata in this lab. PAN's required key is
`changes`. `scarfjoint` writes only `changes` when it predicts a
directory, because that is what an evaluator will read.
