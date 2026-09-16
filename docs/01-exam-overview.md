# Exam overview

These notes are personal study material for a language-processing exam built
around **intrinsic style change detection**. The practical object is the
paragraph-level PAN task: given one document, decide for every pair of
consecutive paragraphs whether the author changed.

Nothing here is a shared-task submission and nothing is scraped from a
competition corpus. The `examples/data/` documents are original. The small
Python package in `src/stylechange/` is a from-scratch baseline so the
formulas in these notes can be executed, not just memorised.

## What the exam is actually testing

A good answer does four things:

1. **Define the prediction problem** without smuggling in extra tasks
   (author count, author IDs, plagiarism source retrieval).
2. **Separate style from topic.** Easy documents leak topic. Hard documents
   do not. If your method is secretly a topic segmenter, say so and say
   why that fails on Hard.
3. **Choose features that are habitual, not topical.** Function words,
   punctuation, sentence length, contractions, pronoun rates.
4. **Evaluate with a metric that survives class imbalance.** Most
   boundaries are *not* changes. Accuracy of a constant-0 predictor is a
   trap; F1 is the exam-safe default.

## Map of this folder

| File | Use it for |
| --- | --- |
| [02-task-definition.md](02-task-definition.md) | Formal I/O, legal change sites, Easy / Medium / Hard |
| [03-stylometry-features.md](03-stylometry-features.md) | What to measure and why it is (or is not) “style” |
| [04-methods.md](04-methods.md) | Threshold, adaptive, clustering, neural options |
| [05-evaluation.md](05-evaluation.md) | Precision, recall, F1, macro vs micro |
| [06-worked-exam-questions.md](06-worked-exam-questions.md) | Practice questions with full solutions |
| [07-limitations-and-ethics.md](07-limitations-and-ethics.md) | Confounds, forensic misuse, gift authorship |
| [references.md](references.md) | Short reading list |

Worked files that you can run live sit under [`../examples/`](../examples/README.md).

## One-sentence theory

Authorship is a **habit distribution** over low-content choices (the, of,
I, you, ;, it's). A style change is a statistically unusual jump in that
habit between two adjacent spans, **not** a jump in what the spans are
about.

## Recommended 90-minute revision order

1. Write the task on a blank page: input, output array length, legal
   change sites (15 min).
2. Compute TTR and a 3-word function-word cosine by hand
   ([question 3 and 4](06-worked-exam-questions.md)) (20 min).
3. Explain why Easy can be solved with content words and Hard cannot
   (15 min).
4. Run `python -m stylechange.cli eval examples/data/easy` and read the
   printed F1 (15 min).
5. Contrast that run with `examples/data/hard` and write three sentences
   about the drop (15 min).
6. Skim ethics: what this method cannot prove in a forensic setting
   (10 min).
