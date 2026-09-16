# Walkthrough: run the toolkit on the sample documents

This is the path I actually run after a fresh checkout. Commands assume
the repository root and use `PYTHONPATH` so the package does not have to
be installed.

## 1. Inspect one easy document

```bash
PYTHONPATH=src python3 -m style_change features \
  examples/sample_problems/easy/problem-001.txt
```

You should see five paragraphs, gold `[0, 1, 0, 1]`, a feature table,
and ensemble distances for the four boundaries. The two large distances
should sit on the author changes (P2–P3 and P4–P5), not on the
same-author pairs.

A slower, script-shaped version of the same view:

```bash
python3 examples/inspect_features.py \
  examples/sample_problems/easy/problem-001.txt
```

Read `examples/annotated/easy-001.md` next to the table. The annotation
says which columns ought to move.

## 2. Predict a whole split

```bash
PYTHONPATH=src python3 -m style_change predict \
  -i examples/sample_problems/easy \
  -o /tmp/style-easy
```

That writes `solution-problem-001.json` and `solution-problem-002.json`.
Open one: it must contain only a `changes` array.

## 3. Score against gold

```bash
PYTHONPATH=src python3 -m style_change evaluate \
  --gold examples/sample_problems/easy \
  --pred /tmp/style-easy
```

The table lists each document's gold, prediction, and macro-F1, then a
split-level mean and a pooled score.

Repeat for `medium`, `hard`, and `single_author`. The control split is
the one that should stay near 1.0 if adaptive thresholding is doing its
job. If it collapses, the detector is firing on ordinary paragraph
variation.

## 4. Compare detectors

```bash
python3 examples/compare_baselines.py
```

Columns:

- `mean F1` — average of per-document macro-F1
- `pooled F1` — one confusion matrix for the split
- `n` — documents in the split

`ensemble` is the default CLI detector. `stylometric`, `char3`, and
`function_word` are the pieces. On `easy` they should mostly agree. On
`hard` they will disagree; that disagreement is the lesson.

Optional: pin a global threshold instead of the adaptive cut.

```bash
PYTHONPATH=src python3 -m style_change predict \
  -i examples/sample_problems/hard \
  -o /tmp/style-hard-fixed \
  --detector ensemble \
  --threshold 0.35
```

If the fixed cut is too low, `single_author` will start emitting ones.
That is the demonstration that adaptive thresholding is not a flourish.

## 5. Unit tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Tests cover paragraph splitting, feature finiteness, the toy confusion
example from `docs/03-evaluation.md`, I/O round-trips, and the claim
that the ensemble finds the obvious change in `easy/problem-001`.

## Expected shape of a healthy run

I do not freeze exact F1 numbers in this note because the adaptive cut
is a heuristic. Qualitatively:

- `easy/problem-001` should recover `[0, 1, 0, 1]` or something one
  flip away.
- `single_author/*` should be all zeros, or at most one spurious one.
- `medium` should beat a coin flip without using a topic change.
- `hard` may be incomplete. That is acceptable teaching data: the
  documents exist to show the remaining gap, not to claim a solved task.

On the current ensemble those bullets look like this: easy 1.00, medium
1.00, single-author 1.00, hard about 0.17. `compare_baselines.py` also
shows why not to celebrate a hard-only score: `char3` and
`function_word` can look perfect on hard while shredding the
single-author control. The ensemble is the compromise that keeps the
control intact.

If `easy` is already near chance, start with `inspect_features.py` and
check that paragraph segmentation produced the number of blocks the gold
file expects. Almost every surprising score I have seen began as a
splitter that treated the whole file as one paragraph.
