# Folds and the PAN-flavoured contract

Teaching files look like a miniature PAN problem.

```
examples/corpus/problem-01-kiln-then-notice.txt
examples/corpus/truth/truth-problem-01-kiln-then-notice.json
```

The problem file is **one sentence per line**. That sentence is a
teaching unit. We do not sentence-split again.

The truth file is JSON:

```json
{
  "authors": 2,
  "changes": [0, 0, 1, 0, 0],
  "site": "easy",
  "return_author": false
}
```

## Invariants

Let `n` be the number of non-empty lines.

- `len(changes) == n - 1`
- each change is `0` (seam) or `1` (fold)
- if `return_author` is false, `authors == 1 + sum(changes)`
- if `return_author` is true, that equality is **supposed to fail**

`inkfold validate` checks this for the whole folder.

## The return trap

`problem-22-kiln-return` is stall, notice, stall:

```
changes = [0, 1, 0, 1, 0]
authors = 2
1 + sum(changes) = 3
```

Two faces, two folds, three *segments*. A segment is not an author.
Say that sentence in the oral.

## Why one sentence per line

So a hand count and the program see the same units. If you let a
tokenizer invent boundaries, you cannot mark a script against a gold
list. The exam will either give you the units or tell you to treat
paragraphs as units. Ask which.

## Writing a prediction

```bash
PYTHONPATH=src python3 -m inkfold detect examples/corpus/problem-01-kiln-then-notice.txt
```

prints `authors`, `changes`, the detector name, and the raw scores.
That is all a shared-task run would have uploaded. We also keep the
scores so the oral can point at a peak.
