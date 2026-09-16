# Data format

The on-disk layout follows the shared-task convention so exam answers can
talk about `problem-X.txt` / `truth-problem-X.json` / `solution-problem-X.json`
without inventing a private schema. The *text* is original to this repo.

## Directory layout

```
data/synthetic/
  manifest.json
  easy/
    problem-001.txt
    truth-problem-001.json
    ...
  medium/
    ...
  hard/
    ...
```

`manifest.json` records split (`train` / `val` / `test`), difficulty, and a
short topic note. Training scripts should honour the split field rather
than reshuffling, so published numbers stay comparable.

## Problem file

A problem file is UTF-8 text. Two encodings are accepted by
`stylechange.io.load_document`:

1. **One sentence per line** (used throughout the synthetic set). This
   removes splitter ambiguity during revision.
2. **Running prose.** The sentence splitter in `stylechange.sentences` is
   applied. Abbreviations such as `Dr.`, `e.g.`, and `U.S.` are protected
   before the terminal-punctuation split.

When you write a new problem by hand, prefer one sentence per line. When
you discuss a shared-task dump in an exam essay, assume running prose and
mention splitter error as a source of label noise.

Always open files with `newline=""` in Python if you need byte-identical
behaviour with the shared-task validators. This toolkit does that in
`stylechange.io`.

## Truth file

```json
{
  "authors": 3,
  "changes": [0, 1, 0, 0, 1, 0],
  "author_ids": ["mira", "mira", "hale", "hale", "hale", "nell", "nell"],
  "difficulty": "hard",
  "topic": "pour-over coffee",
  "notes": "switches after sentence 2 and sentence 5"
}
```

Rules:

- `len(changes) == len(sentences) - 1`
- `len(author_ids) == len(sentences)` when the key is present
- `changes[i] == 1` iff `author_ids[i] != author_ids[i+1]`
- `authors` is the number of *distinct* IDs, not the number of switches

The last point is a common exam trick. Three blocks `A A | B | A A` is
**two authors** and **two changes**: `[0, 1, 1, 0]`.

## Solution file

```json
{ "changes": [0, 1, 0, 0, 1, 0] }
```

Only `changes` is required. Extra keys are ignored by the evaluator.

## Pair indexing

Sentences are 1-based in prose (“the change between sentence 3 and 4”) and
0-based in arrays (`changes[2] == 1`). Worked examples in this repo always
print both so the off-by-one cannot hide.

```
sentences:  s0    s1    s2    s3    s4
pairs:         y0    y1    y2    y3
```

## Filename contract used by the CLI

| Input | Output |
| --- | --- |
| `problem-012.txt` | `solution-problem-012.json` |
| `truth-problem-012.json` | compared against the solution of the same id |

IDs are the digit run after `problem-`. They are zero-padded in this repo
(`001`) but the loader accepts `problem-12.txt` as well.

## Synthetic-set sizes

See `data/synthetic/manifest.json` for the live inventory. The design
target is:

- eight documents per difficulty
- 7–12 sentences each
- roughly 25–40% of pairs labeled `1`, higher than a typical shared-task
  prior, so a revision laptop can see both classes without a huge corpus

That prior is *not* realistic for long multi-author essays. Say so if an
exam question asks whether your validation numbers would transfer.
