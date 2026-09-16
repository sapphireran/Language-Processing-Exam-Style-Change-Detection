# Style-change detection — personal exam kit

Personal study repo. Not company code, not a PAN submission, not a
shared-task dump.

I use this folder to revise a language-processing exam on **intrinsic
style-change detection**: given only a document, mark every adjacent
pair of units where the writer changes. The notes are in `docs/`. The
toy documents are in `examples/documents/`. The dependency-free
baseline that matches the notes is the `examscd` package.

If I cannot explain a line of the detector in the oral, it does not
belong here.

## Thirty-second demo

```bash
python -m pip install -e ".[dev]"
python -m examscd detect examples/documents/02_recipe_then_maillard.txt --explain
python -m examscd cusum examples/documents/02_recipe_then_maillard.txt
python examples/walkthrough_cusum.py
python examples/walkthrough_f1.py
python examples/run_collection.py
pytest
```

The recipe file is eight short imperatives and then five long academic
sentences about the Maillard reaction. The baseline should emit a
single `1` after sentence 8.

## What the exam is asking

Three jobs get bundled under the same name. I still use the older
task numbers because they match how oral questions are phrased.

| job | output |
| --- | --- |
| Task 1 | one cut in a two-author text |
| Task 2 | every cut, plus author ids so a returning writer is reused |
| Task 3 | every cut at sentence grain |

Current wording is Task 3 with the topic leak tightened: a binary
`changes` array of length `n_sentences - 1`. The task is **intrinsic**.
No reference authors. No search.

A neighbouring question I must not answer by accident:

- attribution names a writer from a candidate set
- verification asks whether two texts share an author
- style change asks *where* the writer changed inside one text

## How the baseline decides

Short sentences share almost no character 3-grams even when one person
wrote both, so I do **not** threshold raw pair cosine. Each unit gets
a cue-sheet label (slang, imperative, formal, notes, we-academic,
one-academic, academic, personal, lab). A pair is a cut when the label
family changes. Author ids reuse a label when it returns — the chair
after the intern, the cook after the scientist.

`--explain` still prints the pair distances (character 3-grams,
function-word L1, the 16-D vector, length) and a CUSUM of word count
so I can show *why* a cut looks like a cut. Those numbers are the
oral; the label is the bit.

The same ideas, with the hand calculations, live in:

- [docs/01-exam-brief.md](docs/01-exam-brief.md)
- [docs/03-feature-inventory.md](docs/03-feature-inventory.md)
- [docs/04-cusum-and-windows.md](docs/04-cusum-and-windows.md)
- [docs/07-metrics.md](docs/07-metrics.md)
- [docs/08-model-answers.md](docs/08-model-answers.md)
- [docs/11-formula-sheet.md](docs/11-formula-sheet.md)

## Study documents

I wrote every file in `examples/documents/`. Gold labels are in
`examples/documents/truth/`. A score of 1.0 on this folder is a sanity
check that the code matches the notes, not a shared-task result.

| file | grain | gold story |
| --- | --- | --- |
| `01_single_commute` | sentence | one diary voice |
| `02_recipe_then_maillard` | sentence | recipe → food chemistry |
| `03_forum_three_voices` | sentence | slang / moderator / parent |
| `04_minutes_return` | sentence | chair → intern → chair |
| `05_same_topic_hard` | sentence | two academics on BPE |
| `06_gift_abstract` | paragraph | student + grafted supervisor |
| `07_collage_paragraphs` | paragraph | three cooks, two returns |
| `08_sms_essay_mix` | sentence | SMS → short essay |
| `09_lab_notebook` | paragraph | one lab voice |
| `10_exam_mashup` | sentence | notes / chat / textbook / notes |

## Commands

```
examscd detect FILE [--explain] [-g sentence|paragraph] [-o out.json]
examscd evaluate FILE TRUTH
examscd features FILE
examscd cusum FILE [--svg figure.svg]
examscd compare FILE TRUTH
```

`python -m examscd` is the same entry point.

## What I will say in the oral if they ask about limits

Character n-grams and function words are cheap and explainable. They
still miss two careful academics who share register, topic, and
length. They still fire on a language switch by one person. They
still treat a pasted quotation as a visitor. A transformer pair
classifier is stronger on forum concatenations and more willing to
use topic. I want the same-topic number either way.

## License

MIT, same as the original empty repo. Study notes and toy documents
are original personal material.
