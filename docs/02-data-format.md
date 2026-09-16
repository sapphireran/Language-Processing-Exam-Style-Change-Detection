# 2. Data format

The on-disk format used here copies the *public* PAN problem/truth/solution
convention so exam answers and scripts stay aligned. Official corpora are
not included.

## Directory layout

```
<split-or-band>/
  problem-1.txt
  truth-problem-1.json
  problem-2.txt
  truth-problem-2.json
  ...
```

A test-style directory may omit the `truth-*.json` files. Predictions are
written elsewhere as `solution-problem-X.json`.

This repo's toy files live under [`examples/data/`](../examples/data) in
three bands: `easy/`, `medium/`, `hard/`.

## Input document: `problem-X.txt`

Plain UTF-8 text. The shared-task note is to open files with
`newline=""` in Python so `\r\n` is not rewritten. The library does that
in `scd.io.read_problem`.

How you recover units from the file matters:

| Mode | Rule used in this repo |
|------|------------------------|
| `sentence` (default) | Regex splitter on `.?!` plus paragraph breaks |
| `paragraph` | Split on blank lines (`\n\s*\n`) |
| `pre-tokenized` | One unit per line, if the file was written that way |

Official 2025-style code often calls `nltk.sent_tokenize`. For the
synthetic corpus we keep units unambiguous: most `.txt` files are
**one sentence per line**. That makes the worked examples inspectable
without arguing about whether "Dr. Smith went." is one sentence or two.

If you add your own documents, prefer one unit per line. The inspector
prints both the raw text and the recovered list so you can see drift.

## Ground truth: `truth-problem-X.json`

```json
{
  "authors": 2,
  "changes": [0, 0, 1, 0, 1, 0]
}
```

| Field | Meaning |
|-------|---------|
| `authors` | Number of distinct authors in the document |
| `changes` | Length `n-1` binary vector; `1` means a style change after that unit |

`authors` is extra supervision. The official *prediction* file does not
require it. It is useful for sanity checks: if you reconstruct runs from
`changes` and get a different author count, the file is inconsistent.

Consistency rules the loader enforces:

1. `changes` is a list of `0`/`1` (ints or bools).
2. `len(changes) == n_units - 1` when units are known.
3. `authors >= 1`.
4. If `authors == 1`, every entry of `changes` must be `0`.
5. If `authors >= 2`, at least one entry must be `1`.

## Prediction: `solution-problem-X.json`

```json
{
  "changes": [0, 0, 1, 0, 1, 0]
}
```

Same length and alphabet as the truth `changes` array. No `authors` key
is required. A missing solution for a problem is an evaluation error, not
a silent zero vector — the CLI fails loud so you notice.

## Pairing files

IDs are taken from the filename, not from directory order:

```
problem-12.txt          <->  truth-problem-12.json
                            solution-problem-12.json
```

`scd.io.problem_id("problem-12.txt")` returns `"12"`. IDs are strings, not
ints, because official sets sometimes use zero-padded or alphanumeric
tokens.

## Command-line shape (shared-task style)

A submission-style program is expected to look like:

```
mySoftware -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY
```

`INPUT-DIRECTORY` contains only `problem-*.txt` at test time.
`OUTPUT-DIRECTORY` must receive one `solution-problem-*.json` per input.

This repo's CLI is slightly more explicit (`scd predict -i … -o …`) so
the same binary can also inspect and evaluate. The I/O contract is the
same.

## A complete toy instance

`examples/data/easy/problem-1.txt` (one sentence per line):

```
The souffle requires a precise fold of the egg whites into the batter.
Oven temperature should remain stable so the structure can set.
Yeah I'm just gonna chuck the frozen pizza in and hope for the best.
I'm not gonna overthink dinner tonight, seriously.
```

`examples/data/easy/truth-problem-1.json`:

```json
{
  "authors": 2,
  "changes": [0, 1, 0]
}
```

Four units, three pairwise labels. The switch sits between the careful
baking voice and the casual dinner voice. Topic also changes (technique
vs frozen pizza), which is why this pair is *easy*.

## Common format bugs

- Splitting on `'. '` and then wondering why `"e.g. this"` became two
  units. Prefer a real sentence segmenter, or write one unit per line.
- Off-by-one: emitting `n` labels for `n` units. The last unit has no
  successor.
- Writing `"0"`/`"1"` strings. The evaluator accepts them, but official
  validators have historically wanted integers.
- Windows newlines changing unit counts if you split on `'\n'` only.
  Use `newline=""` plus a split that treats `\r\n` as one break.
- Evaluating predictions against a *different* splitter than the one
  used to create truth. Truth is defined on a specific segmentation.

The tests in `tests/test_io.py` lock the pairing rules and the
consistency checks so the examples cannot silently rot.
