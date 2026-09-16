# Style Change Detection — Personal Exam Notes

Personal study notes, synthetic examples, and a small stylometry toolkit for
**intrinsic style-change detection**. This is coursework-style material for a
language-processing exam, not a shared-task submission and not company work.

The public research problem is: given one document, mark every place the
*writing style* (and therefore likely the author) changes. No comparison
texts are given. That is what makes the task *intrinsic*.

This repo focuses on the formulation used in recent PAN / CLEF multi-author
writing-style analysis tasks:

- split a document into units (sentences here; older editions used paragraphs)
- label each *consecutive pair* `0` (same style) or `1` (style change)
- score predictions with **macro F1** over all pairs

Three difficulty bands appear throughout the notes and the toy corpus:

| Band   | What leaks besides style                         | What you must rely on      |
|--------|--------------------------------------------------|----------------------------|
| Easy   | Topic, named entities, and style often co-change | Topic + surface style      |
| Medium | Topic variety is small                           | Style, with some topic     |
| Hard   | Topic is held nearly constant                    | Style almost alone         |

Nothing here uses real Reddit dumps or any third-party exam answers. All
example documents are **synthetic** and written for teaching.

## What is in the repo

```
docs/                 Conceptual notes and a hand-worked example
examples/             Runnable scripts + toy easy/medium/hard documents
src/scd/              Small library: I/O, features, models, evaluation
tests/                Unit and pipeline tests
```

Start with [docs/README.md](docs/README.md). Run the first example with
the commands below.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest
python examples/01_inspect_document.py
python examples/02_train_baseline.py
python examples/03_error_analysis.py
python examples/04_compare_difficulties.py
python examples/05_hand_features.py
python examples/06_write_report.py
```

The CLI mirrors the same pieces:

```bash
scd inspect examples/data/easy/problem-1.txt
scd train --data-root examples/data --out models/baseline.joblib
scd predict --model models/baseline.joblib -i examples/data/hard -o /tmp/scd-out
scd evaluate --pred /tmp/scd-out --truth examples/data/hard
scd report --problem examples/data/easy/problem-1.txt \
           --truth examples/data/easy/truth-problem-1.json \
           --out /tmp/scd-report.html
```

## Design choices (exam-relevant)

- **No transformer weights.** A logistic-regression stylometry baseline is
  enough to make the difficulty ladder visible and keeps the repo offline.
- **Pairwise features, not document clustering.** The official label is
  defined on consecutive units. Clustering can recover author *count* but
  is a different objective.
- **Synthetic authors with stable habits.** Function words, punctuation,
  contractions, and sentence length are the levers. That matches what
  classical stylometry claims is authorial rather than topical.

## License

MIT. See [LICENSE](LICENSE). Study notes are original prose with links to
the public PAN task pages. They are not a copy of any lecture PDF.
