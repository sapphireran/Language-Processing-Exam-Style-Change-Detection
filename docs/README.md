# Study notes index

These notes are a personal reconstruction of the **intrinsic style-change
detection** problem as it is usually set on a language-processing exam:
definition, data format, features, baselines, evaluation, and failure modes.

Read them in order the first time. After that, jump via the table.

| # | Note | What it is for |
|---|------|----------------|
| 1 | [Task definition](01-task-definition.md) | Intrinsic vs extrinsic; units; three difficulties |
| 2 | [Data format](02-data-format.md) | `problem-X.txt`, truth JSON, solution JSON |
| 3 | [Stylometric features](03-stylometric-features.md) | What to measure and why |
| 4 | [Baselines and models](04-baselines-and-models.md) | From "always 0" to pairwise classifiers |
| 5 | [Evaluation](05-evaluation.md) | Macro F1, imbalance, per-document scores |
| 6 | [Worked example](06-worked-example.md) | One document, features computed by hand |
| 7 | [Exam study notes](07-exam-study-notes.md) | Short answers and contrast questions |
| 8 | [Error analysis](08-error-analysis.md) | Topic leakage, short units, mixed signals |
| 9 | [Reproducibility](09-reproducibility.md) | How the toy corpus and baseline are generated |

Runnable companions live in [`examples/`](../examples/README.md).

## One-paragraph recap

A system receives a single English document and must emit a binary vector
one shorter than the number of units. Index `i` answers: "did the author
change between unit `i` and unit `i+1`?" Easy data lets topic shifts
stand in for author shifts. Hard data removes that crutch. Macro F1
punishes a classifier that only predicts the majority class (usually
"no change").

## What this is not

- Not a PAN software submission (no TIRA wrapper, no official datasets).
- Not authorship *attribution* (no candidate author set).
- Not plagiarism detection against a reference collection.
- Not company code and not trained on scraped user posts.
