# PAN I/O contract

The teaching files mimic the shared-task filenames so an exam answer
can talk about software without inventing a private format.

## Input

```
problem-12.txt          # the document
truth-problem-12.json   # gold, training/validation only
```

Read the text with `open(path, "r", newline="")` (or the equivalent in
`seamtrace.io.load_problem`). That keeps `\r` from being silently
eaten — a real source of off-by-one unit counts.

This repo's teaching documents use **one sentence per non-empty line**.
`seamtrace` treats that as the unit list. Running prose without line
breaks is split on `.?!` with a short abbreviation list. Blank lines
are never units.

## Gold JSON

```json
{
  "authors": 2,
  "changes": [0, 0, 1, 0, 0]
}
```

`changes[i] == 1` means a style/author change between sentence `i` and
sentence `i+1`. For six sentences there are five labels.

`authors` is metadata for humans. The official scorer cares about
`changes`. Do not emit author IDs unless a later edition of the task
asks for clustering.

## Output

For each `problem-X.txt` write `solution-problem-X.json`:

```json
{
  "changes": [0, 0, 1, 0, 0]
}
```

Same length as gold. Values must be 0 or 1. Extra keys are ignored by
a strict scorer and are a good way to fail a home-grown validator, so
the CLI does not write them.

## Command-line shape

Shared-task software is expected to look like:

```
mySoftware -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY
```

Seamtrace mirrors that with:

```
python -m seamtrace solve -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY
```

Inside the input directory you only see `problem-*.txt` at test time.
Do not assume truth files exist. `inspect` and `score` look for them;
`solve` does not.

## Length mismatches

If you emit four bits for a five-boundary document, the scorer cannot
save you. The usual causes in this lab:

1. You dropped a one-word sentence (`Yes.`).
2. You split on `.` inside `e.g.` or `Dr.`.
3. You read the file with a newline translation that merged two lines.

`tests/test_corpus_contract.py` checks every teaching file: `len(changes)
== n_units - 1`.
