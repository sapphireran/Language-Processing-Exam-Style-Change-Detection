# Language Processing Exam: Style Change Detection

Personal study code for an intrinsic **writing-style change detection** task: given a document and no extra comparison texts, mark the sentence (or paragraph) boundaries where the author — or at least the register — changes.

The layout and labels follow the PAN multi-author writing-style analysis format (`problem-X.txt` / `truth-problem-X.json` / `solution-problem-X.json`, macro-F1 over consecutive pairs). The documents in `examples/documents/` are **made-up exam answers**, not the PAN Reddit dumps.

This repository is intentionally dependency-free. The baseline is small enough to read in one sitting and to discuss in an oral exam: stylometric features, three register axes, and binary segmentation of author blocks.

## Why this problem

If two people write a take-home answer together, or a student pastes a textbook paragraph into an otherwise first-person script, you often **do not** have candidate source documents. Authorship attribution then collapses to an intrinsic question:

> Does the writing immediately before this point look unlike the writing immediately after it?

That is also the only setting in which style-change detection can stand in for plagiarism detection, gift authorship, or “someone else finished question 3”.

PAN editions of the task make the same point, and they control how much **topic drift** you are allowed to lean on:

| level | what is allowed to change with the author |
| --- | --- |
| easy | topic *and* register |
| medium | mostly register; topic stays close |
| hard | register only; same topic |

The bundled examples use those three names, plus an `exam` mash-up (student prose → pasted textbook → lecture notes) and a single-author negative control.

## Install

Python 3.10 or newer. No third-party package is required to run the detector.

```bash
git clone https://github.com/sapphireran/Language-Processing-Exam-Style-Change-Detection.git
cd Language-Processing-Exam-Style-Change-Detection
pip install -e .
```

For the test extra:

```bash
pip install -e ".[dev]"
pytest
```

If you do not want to install the package, the same commands work with `PYTHONPATH=src` from the repo root.

## 30-second demo

```bash
stylechange detect examples/documents/problem-exam-answer-shift.txt --explain
```

The file is a fake exam script: three student sentences, four textbook sentences, three lines of lecture shorthand. The detector should print two `CHANGE` marks, at the two joins:

```text
units:    10
changes:  [0, 0, 1, 0, 0, 0, 1, 0, 0]
authors~  3
```

`--explain` adds, for each boundary, the local register jump (personal / academic / telegram) and the three densest stylometric deltas. The `changes` array is one shorter than the number of sentences: label `i` is the join between sentence `i` and sentence `i+1`.

Score every bundled file at once:

```bash
python examples/run_examples.py
```

On the current baseline that report is exact:

```text
id                           gold                         pred                         match
easy-mixed-topics            [0, 0, 1, 0, 0, 1, 0, 0]     [0, 0, 1, 0, 0, 1, 0, 0]       yes
exam-answer-shift            [0, 0, 1, 0, 0, 0, 1, 0, 0]  [0, 0, 1, 0, 0, 0, 1, 0, 0]    yes
hard-close-register          [0, 0, 0, 1, 0, 0, 0]        [0, 0, 0, 1, 0, 0, 0]          yes
medium-one-topic             [0, 0, 0, 1, 0, 0, 0]        [0, 0, 0, 1, 0, 0, 0]          yes
paragraph-gift-authorship    [1, 1]                       [1, 1]                         yes
single-author                [0, 0, 0, 0, 0]              [0, 0, 0, 0, 0]                yes

collection macro-F1=1.000  accuracy=1.000  pairs=38
```

That 1.000 is **not** a claim about PAN test data. It is a claim that the baseline recovers the six hand-written stories it was designed around. Real shared-task numbers will be lower, especially on the hard split.

## How the baseline works

Adjacent-sentence cosine over character n-grams is a bad exam answer. Two sentences from the same person barely share 3-grams, so every boundary looks like a change.

This baseline does three more opinionated things.

### 1. Stylometric profile, not topic words

Each sentence is a `FeatureVector` (`src/stylechange/features.py`):

- length and richness: log chars/words, type–token, hapax, syllable estimate
- punctuation rates: comma, colon, dash, question, exclaim, unique types
- closed-class rates: function words, first/second/third person, hedges, academic connectives, contractions, informal lexis
- a function-word histogram and character 3-grams (kept for inspection; they are *not* the main pairwise metric)

Lowercase `i` in `P(w_i)` is **not** treated as first person. English `I` is.

### 2. Three register axes

`src/stylechange/register.py` projects that profile onto:

| axis | high when the unit looks like… |
| --- | --- |
| **personal** | *I / I'm / yeah / just*, questions |
| **academic** | *therefore / moreover*, long words, commas |
| **telegram** | colons, digits, dashes, missing function words |

A student-vs-textbook join moves personal and academic. A textbook-vs-notes join moves telegram. A single academic connective swinging inside one textbook does **not** count as a new author — the scorer down-weights single-axis academic cuts.

### 3. Binary segmentation of author blocks

Exam answers are written in contiguous spans, not a coin-flip at every sentence. The default `mode="segment"` detector (`src/stylechange/detector.py`) therefore:

1. searches for the most surprising cut in the current span (mean register on the left vs mean register on the right)
2. keeps it if the score is ≥ `threshold` (default `0.36`)
3. recurses on each side
4. refuses to recurse into a sentence span shorter than 6 units, so a four-line notes dump is not carved into “authors”

`mode="pairwise"` is the ablation: windowed thresholding of every adjacent pair, which over-triggers on short sentences.

```python
from stylechange import StyleChangeDetector

detector = StyleChangeDetector(granularity="sentence")
prediction = detector.predict(open("answer.txt", encoding="utf-8").read(), explain=True)
print(prediction.changes)
print(prediction.authors_estimate)
```

Paragraph granularity uses blank lines as units:

```bash
stylechange detect examples/documents/problem-paragraph-gift-authorship.txt \
  --granularity paragraph --explain
```

## Example documents

All files live in [`examples/documents/`](examples/documents/README.md). One sentence per line, except the paragraph file.

| id | difficulty | intended story |
| --- | --- | --- |
| `easy-mixed-topics` | easy | textbook n-grams → casual POS answer → parsing notes |
| `medium-one-topic` | medium | vector semantics, textbook then first-person riff |
| `hard-close-register` | hard | constituency parsing, textbook vs compact notes |
| `exam-answer-shift` | exam | original student prose, pasted textbook, lecture shorthand |
| `single-author` | single | morphology textbook only (negative control) |
| `paragraph-gift-authorship` | paragraph | the same exam story, three blank-line paragraphs |

Gold files keep extra keys (`voices`, `note`, `difficulty`) for humans. The evaluator only reads `changes`.

### Other scripts

| script | what it does |
| --- | --- |
| `examples/run_examples.py` | score every bundled file, print the table above |
| `examples/explain_boundaries.py` | walk one file, default `exam-answer-shift` |
| `examples/calibrate_on_synthetic.py` | fit a threshold on generated answers, then re-score the hand files |
| `examples/pan_roundtrip.py` | copy the sentence-level examples into a PAN-shaped directory and run `stylechange evaluate` |

Generate a fresh labelled answer (used by tests and calibration):

```bash
stylechange generate --difficulty medium --seed 4
```

Voices in the generator (`src/stylechange/generate.py`) are deliberately cartoonish: `textbook`, `student`, and `notes`. That is a feature for an oral exam, not a claim about real authors.

## CLI

```text
stylechange detect FILE [--explain] [--json] [--granularity sentence|paragraph]
                        [--threshold 0.36] [--window 2] [--mode segment|pairwise]

stylechange features FILE [--granularity sentence|paragraph]

stylechange evaluate INPUT-DIR [--output output]
stylechange generate [--difficulty easy|medium|hard|single] [--seed N]
```

`evaluate` matches the PAN software-submission shape: read `problem-*.txt` from an input directory, write `solution-problem-*.json` to an output directory, then print macro-F1 if gold files are present.

```bash
stylechange evaluate examples/documents --output /tmp/stylechange-out
```

## Data format

A problem directory looks like the PAN 2024–2026 style-change releases:

```text
problem-12.txt              # document, ideally one sentence per line
truth-problem-12.json       # training / validation only
```

```json
{
  "authors": 2,
  "changes": [0, 0, 1, 0]
}
```

`changes[i] == 1` means a style change between unit `i` and unit `i+1`. A document of *n* units therefore has *n − 1* labels. The detector writes `solution-problem-12.json` with the same `changes` key (and an `authors` estimate = `1 + sum(changes)`).

Read files with `open(path, "r", encoding="utf-8", newline="")` if you add your own I/O — that is the PAN note about Windows newlines, and `stylechange.io.load_problem` already does it.

## Evaluation

PAN reports **macro-F1** over every consecutive pair, treating “change” and “no change” as two classes. `stylechange.evaluate.evaluate_changes` does the same:

```python
from stylechange import evaluate_changes

result = evaluate_changes(gold_list_of_lists, pred_list_of_lists)
print(result.macro_f1, result.precision, result.recall, result.pairs)
```

A length mismatch between gold and prediction skips that document and increments `skipped` instead of crashing. That is the usual failure mode when a tokenizer disagrees with the gold sentence count.

## Project layout

```text
src/stylechange/
  tokenize.py    sentence / paragraph split, abbreviation-aware
  lexicon.py     function words, connectives, contractions, informal list
  features.py    FeatureVector + extract_features
  register.py    personal / academic / telegram axes
  detector.py    binary segmentation (default) and pairwise ablation
  evaluate.py    macro-F1
  io.py          PAN problem / truth / solution files
  generate.py    synthetic exam answers with known labels
  cli.py         stylechange detect|features|evaluate|generate
examples/
  documents/     six hand-written problems + gold JSON
  *.py           walkthroughs listed above
tests/           tokenizer, features, I/O, CLI, and the six examples
```

## Limitations (say these out loud)

- The baseline is **intrinsic and unsupervised**. There is no transformer and no training on PAN zips.
- Perfect scores on six toy documents do not transfer to the official easy/medium/hard Reddit sets. Topic-controlled hard data is the whole point of the later PAN editions.
- Author blocks are assumed to be contiguous. Sentence-level A/B/A/B switching will be under-segmented.
- Register axes are English-specific and exam-specific. They will not survive code-switching, heavy dialogue, or a document written entirely in lecture notes.
- Threshold calibration on the tiny synthetic generator will drift low and start splitting single-author textbooks. Prefer the default `0.36` unless you have a real validation split.
- The sentence splitter is a regex with an abbreviation list, not a dependency parse.

A reasonable next step, if you want a second model for the write-up, is a supervised pair classifier on PAN training files (two sentences in, binary change out) and an ensemble with this segmenter.

## References

- [PAN 2025 Multi-Author Writing Style Analysis](https://pan.webis.de/clef25/pan25-web/style-change-detection.html) — sentence-level `changes` array, easy/medium/hard topic control, macro-F1.
- [PAN 2024 task page](https://pan.webis.de/clef24/pan24-web/style-change-detection.html) — paragraph-level predecessor, same I/O idea.
- Zangerle et al., *Overview of the Multi-Author Writing Style Analysis Task at PAN 2025* — what participants actually submitted (mostly fine-tuned encoders).
- Stamatatos, “A survey of modern authorship attribution methods” (*JASIST*, 2009) — function words and other-than-topic stylometry.
- PAN software submission: `mySoftware -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY`.

## License

MIT. See [`LICENSE`](LICENSE). Personal project; not affiliated with PAN or CLEF.
