# Language-Processing-Exam-Style-Change-Detection

Personal exam lab for **intrinsic, paragraph-level style-change
detection** — the PAN multi-author writing-style analysis task, in
the form you can still derive on paper.

This repository is study material. It is not a PAN submission, not a
course official, and not company code. The twelve bundled documents
are hand-written. Thresholds were set on those documents. Do not quote
the collection score as a shared-task result.

## What the task is

Given one English document, emit a bit for every pair of neighbouring
paragraphs: did the author change? No candidate-author gallery is
provided. PAN 2023 scores F1 on that binary vector and splits the
data into easy / medium / hard by how much topical variety you are
allowed to lean on.

```
P1  I lock the bike under the stairs…
P2  Helmet's on the hook…
P3  Conservation of nineteenth-century ledgers, however…
P4  Relative humidity above sixty percent…

changes = [0, 1, 0]
```

Notes live in [`docs/`](docs/README.md). Runnable walks live in
[`examples/`](examples/README.md). The labelled pages live in
[`examples/corpus/`](examples/corpus/README.md).

## Install

Python 3.10+. No runtime dependencies.

```bash
export PYTHONPATH=src
# or: pip install -e .
```

## Thirty-second demo

```bash
python3 -m scarfjoint detect examples/corpus/easy/problem-01-ferry-marsh-knit.txt --explain
python3 -m scarfjoint eval examples/corpus
python3 examples/walk_worked_example.py
python3 examples/compare_channels.py
python3 examples/run_lab.py
python3 -m unittest discover -s tests -v
```

`scarfjoint` is also an alias for `python3 -m scarfjoint` after an
editable install.

## How the baseline decides

1. Split on blank lines (PAN's paragraph boundary; open files with
   `newline=""`).
2. Fingerprint each paragraph: function-word frequencies, character
   3-grams, a signed **formality** coordinate (academic/policy up;
   first person, contractions, imperatives down), sentence length,
   pronoun person.
3. Score every adjacent pair with a weighted sum of those jumps.
4. Flag a change if the combined score is at least **0.345**.

Content-word Jaccard and zlib NCD are computed for the explain dump
and are **not** allowed to vote. On these short teaching paragraphs
Jaccard is saturated even inside a single author — which is itself an
exam point about needing enough text, or a better topic model, before
you accuse topic of helping.

Transformers win the real shared task. This kit exists so you can
explain why, and what they still get from register.

## What the collection currently does

On the twelve original pages, with a threshold fit on those pages:

- **Easy:** all three documents exact.
- **Medium:** the casual→formal join is caught; the closer second
  join is not always.
- **Hard:** the pairwise threshold under-fires. That is the point of
  the hard pages, not a surprise to be patched away.
- **Single-author:** all quiet.

Mean F1 over documents is a lab number. Read the per-document flags
before you believe it. See `python3 examples/run_lab.py`.

## Repository map

```
src/scarfjoint/     split, features, formality, detector, CLI
docs/               contract, formulae, orals, worked cosine / Yule K
examples/corpus/    12 labelled study texts
examples/annotated/ boundary notes for four of them
examples/*.py       lab session scripts
tests/              unit tests plus locked gold behaviour
```
