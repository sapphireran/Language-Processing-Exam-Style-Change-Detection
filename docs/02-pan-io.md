# PAN IO contract

I treat the on-disk format as part of the exam, not as plumbing. A
wrong-length `changes` array is a zero even if the ideas were good.

## Problem

A UTF-8 text file. Paragraphs are separated by one or more blank lines.
Leading and trailing whitespace on a paragraph does not count. A file
with one paragraph has **zero** hinges.

```
paragraph one, which may wrap
across lines if it wants.

paragraph two.

paragraph three.
```

`quoin.tokenize.paragraphs` is the splitter I would write on a
whiteboard: split on `\n\s*\n+`, strip, drop empties.

## Solution

```json
{
  "changes": [0, 1]
}
```

Rules I have on a card:

- `len(changes) == n_paragraphs - 1`
- every bit is `0` or `1`
- a `1` at index `i` means "author changed between paragraph `i` and
  `i+1`" (zero-based)

My truth files also carry `authors`, `band`, `title`, `note`. Those are
teaching fields. A submission that included them would not be wrong; a
submission that omitted `changes` would be.

## Validator, in prose

For every problem file:

1. split paragraphs
2. read the matching `truth-*.json`
3. refuse the pair if the bit-vector is the wrong length
4. refuse the pair if any bit is not in `{0,1}`
5. if `authors` is present, refuse if that list is not length `n`

`quoin.io.validate_pair` is that list as code.

## Why I bother with a CLI `predict`

The oral can ask me to show a solution file. `python -m quoin predict
path/to.txt` prints the JSON. `--out` writes it. That is the entire
submission story for a single document. The shared task used TIRA; I am
not pretending this lab deploys there.

## A mistake I made once and wrote down

I counted hinges as `n` instead of `n-1` and then padded with a trailing
zero "for the last paragraph." That is not what the format wants. The
last paragraph does not have a right-hand neighbour. There is no bit
for it.
