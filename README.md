# Language Processing Exam: Style Change Detection

Personal study code for an intrinsic **writing-style change detection**
task: given one document and no comparison texts, mark the sentence (or
paragraph) joins where the author — or at least the register — changes.

The I/O follows the PAN multi-author writing-style layout
(`problem-X.txt` / `truth-problem-X.json` / `solution-problem-X.json`,
macro-F1 over consecutive pairs). The files in `examples/documents/`
are **made-up exam answers**, not the PAN Reddit dumps.

This repository is intentionally dependency-free. The baseline is small
enough to read in one sitting and to defend in an oral exam: four named
voices, a personal cut-band, and a register change-point for the hard
case. Longer notes live in [`docs/`](docs/README.md).

This is personal exam work. There is no company code in the tree.

## Why this problem

If two people write a take-home together, or a student pastes a textbook
paragraph into an otherwise first-person script, you often **do not**
have candidate source documents. Authorship attribution then collapses
to an intrinsic question:

> Does the writing immediately before this point look unlike the writing
> immediately after it?

PAN editions of the task make the same point, and they control how much
**topic drift** you are allowed to lean on:

| level | what is allowed to change with the author |
| --- | --- |
| easy | topic *and* register |
| medium | mostly register; topic stays close |
| hard | register only; same topic |

The bundled stories use those three names, plus an `exam` mash-up
(student prose → pasted textbook → lecture notes) and a single-author
negative control.

## Install

Python 3.10 or newer. No third-party package is required to run the
detector.

```bash
git clone https://github.com/sapphireran/Language-Processing-Exam-Style-Change-Detection.git
cd Language-Processing-Exam-Style-Change-Detection
pip install -e .
```

For tests:

```bash
pip install -e ".[dev]"
pytest
```

If you do not want to install the package, the same commands work with
`PYTHONPATH=src` from the repo root, or as `python -m stylechange …`
after an editable install.

## 30-second demo

```bash
stylechange detect examples/documents/problem-exam-takehome.txt --explain
```

The file is a fake take-home: three student sentences, four textbook
sentences, three lines of lecture shorthand. The detector should print
two `CHANGE` marks, at the two joins:

```text
units:    10
changes:  [0, 0, 1, 0, 0, 0, 1, 0, 0]
authors~  3
voices:   ['student', 'student', 'student', 'textbook', 'textbook', 'textbook', 'textbook', 'notes', 'notes', 'notes']
```

`--explain` adds the local voice jump and the densest stylometric
deltas. The `changes` array is one shorter than the number of
sentences: label `i` is the join between sentence `i` and sentence
`i+1`.

Score every bundled file at once:

```bash
python examples/run_collection.py
```

On the current baseline that report is exact:

```text
id                               gold                         pred                         match F1
---------------------------------------------------------------------------------------------------
easy-kitchen-and-syntax          [0, 0, 1, 0, 0, 1, 0, 0]     [0, 0, 1, 0, 0, 1, 0, 0]     yes   1.000
exam-takehome                    [0, 0, 1, 0, 0, 0, 1, 0, 0]  [0, 0, 1, 0, 0, 0, 1, 0, 0]  yes   1.000
hard-we-vs-one                   [0, 0, 1, 0, 0]              [0, 0, 1, 0, 0]              yes   1.000
medium-embeddings                [0, 0, 1, 0, 0]              [0, 0, 1, 0, 0]              yes   1.000
notes-after-prose                [0, 0, 0, 1, 0, 0, 0]        [0, 0, 0, 1, 0, 0, 0]        yes   1.000
paragraph-gift                   [1, 1]                       [1, 1]                       yes   1.000
questions-vs-exposition          [0, 0, 1, 0, 0]              [0, 0, 1, 0, 0]              yes   1.000
single-author                    [0, 0, 0, 0, 0]              [0, 0, 0, 0, 0]              yes   1.000

collection macro-F1=1.000  accuracy=1.000  pairs=46  exact=8/8
```

That 1.000 is **not** a claim about PAN test data. It is a claim that
the baseline recovers the eight hand-written stories it was designed
around. Real shared-task numbers will be lower, especially on the hard
split.

## How the baseline works

Adjacent-sentence cosine over character n-grams is a bad exam answer.
Two sentences from the same person barely share 3-grams, so every
boundary looks like a change.

This baseline does three more opinionated things. The longer version is
[docs/baseline.md](docs/baseline.md).

### 1. A stylometric profile, not topic words

Each unit is a `FeatureVector` (`src/stylechange/features.py`):

- length and richness: log words, type–token, hapax, syllable estimate
- punctuation rates: comma, colon, dash, question, exclaim
- closed-class rates: function words, `I` / `we` / `you` / `one`,
  hedges, academic connectives, contractions, casual lexis
- notes flags: arrows (`->`), digits, uppercase productions

Lowercase `i` in `P(w_i)` is **not** treated as first person. English
`I` is.

### 2. Four voices, three cut-bands

`src/stylechange/voices.py` projects that profile onto:

| voice | high when the unit looks like… |
| --- | --- |
| **chat** | *yeah / don't / you*, questions, casual lexis |
| **student** | *I / I'm / I think*, hedges |
| **textbook** | *therefore / moreover*, long words, *we* or *one* |
| **notes** | colons, digits, `->`, missing function words |

`chat` and `student` share a **personal** band when we decide to cut.
A recipe that says "yeah" and then "I" is still one person. `--explain`
keeps the four names so you can talk about them.

A short labelled line (`CFG: S -> NP VP`, `CRF: P(y|x)`) is forced to
notes, so a formula cannot be read as chat because it contains a letter
`I`.

### 3. Blocks, not a coin-flip at every sentence

Exam answers are written in contiguous spans. The default detector
(`src/stylechange/detector.py`) therefore:

1. absorbs one-unit voice blips
2. marks a change when the *cut-band* jumps (personal / textbook / notes)
3. inside a long same-voice run, looks for one extra cut that maximises
   **register distance** (mean binary flags: `I`, `we`, `one`, informal,
   notes). That is the hard *we* vs *one* document.
4. refuses to span-cut a notes dump, so four lecture lines stay one author

Mean word length is *not* in the register distance. A single long
sentence would otherwise invent a fake author — the single-author
morphology file is the control.

## CLI

```bash
stylechange detect FILE [--explain] [--debug-voices] [--json]
stylechange evaluate examples/documents [--output DIR]
stylechange features FILE
stylechange voices FILE
python -m stylechange detect FILE --explain
```

Walkthrough scripts:

```bash
python examples/run_collection.py
python examples/explain_document.py
python examples/pan_roundtrip.py
python examples/mix_blocks.py
```

## Data format

See [examples/documents/README.md](examples/documents/README.md) for the
eight stories. In short:

| file | role |
| --- | --- |
| `problem-<id>.txt` | document, one sentence per line (or blank-line paragraphs) |
| `truth-problem-<id>.json` | gold `changes` plus human notes |
| `solution-problem-<id>.json` | what `evaluate --output` writes |

`changes` is always one shorter than the number of units.

## Layout

```text
docs/                  exam notes (task, stylometry, baseline, orals)
examples/documents/    eight PAN-shaped problems + gold files
examples/*.py          collection / explain / PAN round-trip / mixer
src/stylechange/       detector, voices, features, CLI
tests/                 gold locks + tokenizer / feature / CLI checks
```

## Limitations

- Eight hand-written documents, not a Reddit shared task.
- Voices are a closed inventory. A sarcastic textbook will fool them.
- One-sentence interpolations that are a *real* third author are
  absorbed on purpose (exam answers come in blocks).
- English-only lexicons.
- A windowed encoder would beat this on real PAN data and would be
  harder to defend on a whiteboard.

Those points are expanded in [docs/oral-exam.md](docs/oral-exam.md).
