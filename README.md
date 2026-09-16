# Language Processing Exam: Style Change Detection

Personal study repository for the **intrinsic multi-author writing-style analysis**
problem. The materials here are exam notes, original worked examples, and a small
Python toolkit — not a shared-task dump and not company code.

The practical question is: given one document and no reference writing samples,
can we mark the sentence boundaries where the author changes?

```
sentence_1 ──► sentence_2 ──► sentence_3 ──► sentence_4
     0              0              1
  same author   same author   author switch
```

That binary sequence is the entire prediction target. Evaluation is **macro-F1**
over the two classes `{0, 1}` so a detector that always prints `0` cannot hide
behind the fact that switches are rare.

## Why this problem is on the exam

Style-change detection is the authorship task you still have when you *do not*
have candidate authors. It is the intrinsic counterpart of attribution:

| Setting | What you are given | What you decide |
| --- | --- | --- |
| Attribution (extrinsic) | A questioned text + candidate samples | Which known author wrote it |
| Verification | A questioned text + one claimed author | Same author or not |
| **Style change (intrinsic)** | **One document only** | **Where the writer changes** |

Typical applications discussed in lectures: plagiarism with no source text,
gift authorship, collaborative drafts, and writing-support tools that flag a
sudden register shift. The exam angle is almost always the same: **topic is a
confound**. If two authors also talk about different things, a bag-of-words
classifier will look brilliant and still know nothing about style.

This repo therefore ships three original synthetic splits that isolate that
confound:

| Split | Topic | What a lazy model can exploit |
| --- | --- | --- |
| `easy` | Authors also change subject | Lexical / topical cues |
| `medium` | Same broad subject, different sub-angles | Some topic residue |
| `hard` | One subject, tightly held | Style only |

All example documents were written for this repository. They are not scraped
posts and they are not PAN evaluation data.

## Quick start

```bash
python3 -m pip install -e .
stylechange demo --split hard
stylechange evaluate --gold data/synthetic/hard --pred output/hard-unsupervised
```

Useful commands:

```bash
# Fit a logistic pairwise detector on the synthetic train problems
stylechange fit --gold data/synthetic --out models/logistic.json

# Predict PAN-style solution files
stylechange detect --input data/synthetic/hard --model models/logistic.json --out output/hard-logistic

# Score predictions against truth-problem-*.json files
stylechange evaluate --gold data/synthetic/hard --pred output/hard-logistic

# Print a sentence-by-sentence feature walkthrough
stylechange explain --input data/synthetic/hard/problem-001.txt

# Write a colour-coded HTML report
stylechange report --gold data/synthetic/hard --pred output/hard-unsupervised --html reports/hard.html
```

The same entry point is available as `python -m stylechange`.

## Repository layout

```
docs/                 exam notes, feature catalogue, pitfalls, references
data/synthetic/       original easy / medium / hard problems + truth files
examples/             scripts that walk the toolkit the way a revision session would
src/stylechange/      sentence splitter, stylometric features, detectors, CLI
scripts/              batch fit / evaluate helpers
tests/                unittest suite against the synthetic gold
```

Start with the notes, then run the examples:

1. [Problem statement](docs/01-problem-statement.md)
2. [Data format](docs/02-data-format.md)
3. [Stylometric features](docs/03-stylometric-features.md)
4. [Detectors](docs/04-detectors.md)
5. [Evaluation](docs/05-evaluation.md)
6. [Exam study notes](docs/06-exam-study-notes.md)
7. [Worked examples](docs/07-worked-examples.md)
8. [Pitfalls](docs/08-pitfalls.md)
9. [Author style cards](docs/author-styles.md)

## Toolkit in one paragraph

Each sentence is mapped to a fixed stylometric vector (length, punctuation,
pronouns, hedges, nominalizations, a cheap readability score, and similar
hand features). Consecutive sentences become a pair vector — usually the
absolute difference. A detector then labels the pair `1` if it believes the
author changed. The unsupervised detector standardizes features *inside the
document* and thresholds consecutive distance; the logistic detector learns
pair weights from the synthetic train split. Neither approach downloads a
transformer. That is deliberate: the exam wants you to reason about features,
not fine-tune `deberta-base`.

## Data format (PAN-compatible, extras allowed)

`problem-001.txt` is the document. `truth-problem-001.json` looks like:

```json
{
  "authors": 2,
  "changes": [0, 0, 1, 0, 0],
  "author_ids": ["mira", "mira", "mira", "jules", "jules", "jules"],
  "difficulty": "easy"
}
```

`changes[i]` is the label **between** sentence `i` and sentence `i+1`.
A document with `n` sentences therefore has `n-1` change labels. Predictions
are written as `solution-problem-001.json` with the same `changes` array.

The extra keys (`author_ids`, `difficulty`, topic notes) are study metadata.
The evaluator only reads `changes`.

## Detectors shipped here

| Name | Supervised? | Idea |
| --- | --- | --- |
| `always0` | no | Majority-class baseline; high accuracy, poor macro-F1 |
| `unsupervised` | no | Within-document z-scored Euclidean jump |
| `threshold` | weak | Tuned distance cutoff on labeled pairs |
| `logistic` | yes | From-scratch logistic regression on pair diffs |
| `ensemble` | mixed | Vote / average of the above |

## Evaluation

Pooled **macro-F1** on every sentence pair, plus per-document macro-F1,
accuracy, and a small confusion summary. Accuracy is reported so you can
watch it lie to you on imbalanced documents.

## Personal scope

This is a personal exam-prep repository. Documents, notes, and code were
written for revision. They are not production authorship software and they
are not affiliated with any employer.
