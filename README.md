# Language-Processing-Exam-Style-Change-Detection

Personal exam lab for **intrinsic, paragraph-level style-change
detection** — the PAN multi-author writing-style analysis task, in
the form you can still derive on paper.

This repository is study material. It is not a PAN submission, not a
course official, and not company code. The fourteen bundled documents
are hand-written. Thresholds were set on those documents. Do not quote
the collection score as a shared-task result.

## What the task is

Given one English document, emit a bit for every pair of neighbouring
paragraphs: did the author change? No candidate-author gallery is
provided. PAN 2023 scores **macro-F1** on that binary vector and
splits the data into easy / medium / hard by how much topical variety
you are allowed to lean on.

```
P1  I lock the bike in the basement…
P2  Helmet's on the hook…
P3  Conservation of medieval bindings, however…
P4  The vellum's response to relative humidity…

changes = [0, 1, 0]
```

Notes and a question bank live in [`docs/`](docs/README.md). Runnable
walks live in [`examples/`](examples/README.md).

## Install

Python 3.10+. No runtime dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Or just keep `src/` on `PYTHONPATH` (the lab scripts do this).

## Thirty-second demo

```bash
python -m scdkit detect examples/documents/02_easy_bikes_then_vellum.txt --explain --preview
python -m scdkit eval examples/documents --truth examples/documents/truth
python examples/run_all.py
```

`scdkit` is an alias for `python -m scdkit` after an editable install.

## How the baseline decides

1. Split on blank lines (or one paragraph per line).
2. Fingerprint each paragraph: function-word frequencies, character
   3-grams, sentence / word length, contractions, pronoun person,
   formal vs casual markers.
3. Score every adjacent pair with Burrows's Delta, cosine, formality
   jump, CUSUM slope, and a dense z-scored vector.
4. Flag a change if one channel is strong or two channels agree.

Content-word Jaccard is computed as a **topic channel** and is *not*
allowed to vote. Lab 07 exists so you can see it leak on the easy
document and stay uninformative on the circadian hard document.

Transformers win the real shared task. This kit exists so you can
explain why, and what they still get from topic.

## Repository map

```
src/scdkit/          tokenise, features, Delta, CUSUM, ensemble, CLI
docs/                exam notes, formulae, oral script, 30 questions
examples/documents/  14 labelled study texts
examples/authors/    restackable voice cards
examples/lab*.py     one sitting, from split to ablation
tests/               unit tests plus locked gold labels
```

## Commands

| command | purpose |
| --- | --- |
| `scdkit detect FILE --explain` | print adjacent votes |
| `scdkit features FILE` | fingerprint table |
| `scdkit eval DIR --truth DIR` | collection macro-F1 |
| `scdkit compare DIR --truth DIR` | F1 by method |
| `scdkit report FILE --truth FILE --out report.html` | HTML walkthrough |
| `scdkit mix examples/authors ABA` | stitch a new drill |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Licence

MIT (see `LICENSE`). Copyright on the original empty repo remains
with the 2023 commit. New notes and examples are personal study
material.
