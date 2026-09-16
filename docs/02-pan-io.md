# PAN-shaped I/O

I keep the shared-task file shape so an examiner can recognise the
task in ten seconds. I do not keep their data.

## Problem file

A UTF-8 text file. Paragraphs are separated by a blank line. The
filename is `problem-<code>-<slug>.txt`. The slug is for me; the
detector only reads the text.

```
The stilling well was opened at 06:40. …

The intake strainer was lifted at 07:05. …
```

Sentence-level editions of the task exist. This lab stays at
paragraph level because that is the unit I can write by hand without
lying about sentence boundaries.

## Truth file

`truth-problem-<code>.json`:

```json
{
  "changes": [0, 1, 0],
  "authors": 2,
  "houses": ["caliper", "placard"],
  "band": "easy",
  "holdout": false
}
```

`changes` has length `n_paragraphs - 1`. A `1` means the author
changed between paragraph *i* and paragraph *i+1*. `authors` is the
number of distinct houses, not `1 + sum(changes)` — those differ on
an ABA return.

`houses` and `band` are study metadata. The detector never reads them.

## Prediction file

The CLI writes the same `changes` list, plus a naive
`authors = 1 + sum(changes)`. That naive count is wrong on returns
and I say so. See the oral card on author counting.

## Pairing rule

`kerf.io.paired_files` matches `problem-05-….txt` to
`truth-problem-05.json` by the numeric code. The slug can change
without breaking the score script.
