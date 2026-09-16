# Overview

This folder is the written half of a personal language-processing exam revision
set. The code in `src/stylechange` exists so the notes are executable, not the
other way around.

## The claim you should be able to defend

Style is a *distributional habit* of a writer: preferred sentence length,
punctuation rhythm, pronoun stance, hedging, nominalization, and a handful of
closed-class words. Those habits are stable enough, on average, that a sudden
jump in the feature space is evidence of a new author. They are *not* stable
enough that a two-sentence window is a fingerprint. Every detector in this repo
is therefore a **change-point** model, not an identification model.

## What you must be able to do on paper

1. Define intrinsic vs extrinsic authorship analysis in one sentence each.
2. Write the input/output contract: `n` sentences → `n-1` binary labels.
3. Explain why macro-F1 is the exam metric and accuracy is not.
4. Name at least four feature families that survive a topic-controlled split.
5. Show how a within-document z-score removes corpus-level scale.
6. Sketch the pairwise learning reduction (sentence → vector → abs-diff → label).
7. List the failure modes: topic leakage, sentence-splitter errors, class
   imbalance, register change by one author, quoted speech.

If you can do those seven without looking at the code, the toolkit is only a
calculator. If you cannot, start at [01-problem-statement.md](01-problem-statement.md)
and work forward; do not jump to the logistic regressor.

## Reading order for a short revision session

| Time-box | Read | Then run |
| --- | --- | --- |
| 15 min | Problem statement + data format | `stylechange explain --input data/synthetic/easy/problem-001.txt` |
| 20 min | Feature catalogue + author cards | `python examples/feature_walkthrough.py` |
| 20 min | Detectors + evaluation | `python examples/compare_detectors.py` |
| 20 min | Study notes + pitfalls | `stylechange demo --split hard` |
| leftover | Worked examples | recompute one pair by hand |

## What is intentionally missing

- No transformer fine-tunes.
- No scraped social-media dumps.
- No hidden test set from a shared task.
- No company or production pipeline.

Those omissions keep the repo inside personal exam scope and keep the maths
visible.
