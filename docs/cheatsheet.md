# Exam cheatsheet

One page. Expand from the longer notes if a question goes deep.

## Task

- Input: paragraphs \(p_1\ldots p_n\), one author each.
- Output: \(c_i \in \{0,1\}\) for \(i=1\ldots n-1\).
- Intrinsic: no candidate authors, no comparison corpus.
- Change sites are paragraph boundaries only.
- Easy / Medium / Hard = topic control, **not** author count.

## Features that are allowed to be called “style”

Function words, punctuation, contractions, pronoun rates, hedges,
nominalizations, sentence / word length. Not: content TF–IDF, named
entities, raw embeddings, TTR on mismatched lengths.

## Distance

Relative difference \(|a-b|/(|a|+|b|)\). Cosine distance \(1-\cos\).
Default blend 0.55 scalar + 0.25 function words + 0.10 3-grams + 0.10
punct. Default cut \(t=0.33\) (this repo only).

## F1 conventions

Empty predicted-positive ⇒ P=1. Empty true-positive ⇒ R=1. All-zero
on `[0,0,1,0,0]` ⇒ acc=0.8, F1=0. Always quote F1. Macro = mean of
docs. Score Easy / Medium / Hard separately.

## Arguments that score marks

- A–B–A still yields `[1,1]`. Returning is a change.
- Topic straw man wins Easy, loses Hard (Hard 001: biggest topic jump
  is *not* the author change).
- Short paragraphs make function-word cosine noisy (Hard 002, Control).
- Adaptive thresholds help uniform Hard docs and hurt 2-boundary
  controls.
- A distance is a shift in habit, not a name. Do not accuse.

## Commands

```bash
PYTHONPATH=src python3 -m stylechange.cli inspect examples/data/easy/problem-001.txt
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/hard
PYTHONPATH=src python3 scripts/check_hand_calculation.py
```
