# Language Processing exam: style-change detection

Personal study kit for an intrinsic **style-change detection** exam
(PAN 2023 multi-author writing-style analysis contract: paragraph
pairs, binary `changes`, F1). The repository is original notes,
original example documents, and a small dependency-free detector. It
does **not** include PAN data, Reddit dumps, or any company code.

If you only open one folder, open [`docs/`](docs/README.md). If you
only run one command, run the corpus scorer.

## Quick start

```bash
python3 -m pip install -e .[ ]  # or just keep src/ on PYTHONPATH
PYTHONPATH=src python3 -m splicefind score-corpus examples/corpus
PYTHONPATH=src python3 -m pytest -q
```

Useful one-document commands:

```bash
PYTHONPATH=src python3 -m splicefind detect examples/corpus/problem-14-grandma-and-landlord.txt
PYTHONPATH=src python3 -m splicefind features examples/corpus/problem-14-grandma-and-landlord.txt
PYTHONPATH=src python3 -m splicefind report examples/corpus/problem-14-grandma-and-landlord.txt \
  --truth examples/corpus/truth/truth-problem-14-grandma-and-landlord.json
PYTHONPATH=src python3 -m splicefind calibrate examples/corpus
```

PAN-shaped batch I/O (TIRA-like `-i` / `-o`):

```bash
PYTHONPATH=src python3 -m splicefind detect-dir -i examples/corpus -o /tmp/scd-out
```

## What is in here

| Path | Role |
|------|------|
| [`docs/`](docs/README.md) | Exam handbook: task, features, Delta, CUSUM, topic, metrics, oral cards, written answers |
| [`examples/corpus/`](examples/corpus/README.md) | 18 original labelled documents |
| [`examples/`](examples/README.md) | Labs 00–10: tables, ablation, confound, PAN roundtrip |
| [`src/splicefind/`](src/splicefind) | Detector, evaluation, synthetic voices, CLI |

The detector blends a bounded register gap (pronouns, contractions,
sentence length), Burrows-like function-word Delta, character 3-gram
excess, and a weak CUSUM hint, then marks intra-document outliers. It
is a baseline you can explain, not a competition entry.

## Task in one paragraph

Given one English document and no candidate authors, mark every
boundary between consecutive paragraphs with `0` (same author) or `1`
(author change). Easy documents are allowed to change topic when they
change author; hard documents hold topic still so that noun-heavy
models starve. Score F1 on the binary vector. Accuracy is the wrong
headline because most boundaries are `0`.

## Designed documents

- `01` single gardener (false-alarm trap)
- `04` two lecturers on tidally locked climates (hard)
- `07` allotment committee, author A returns
- `14` same leak, letter to grandmother then notice to landlord
- `16` same diarist, tomato then train (topic-confound control)

Walkthrough: [`docs/10-worked-walkthrough.md`](docs/10-worked-walkthrough.md).

## Licence

MIT (see `LICENSE`). Notes and example prose are personal exam
material written for this repository.
