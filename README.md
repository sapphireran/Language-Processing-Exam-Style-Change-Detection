# Language Processing exam lab: style-change detection

Personal study kit for a Language Processing exam on **intrinsic style-change
detection** — the PAN-style job of marking every paragraph boundary where the
author of a document changes.

This repository is not a course hand-in and not a shared-task submission. It is
a private workbook I built so I could rehearse the oral and written questions
with original documents, a tiny detector I can defend on a whiteboard, and
numbers I actually computed.

The toolkit is called **quoin**. In a letterpress shop a quoin is the wedge
that locks type into the chase. Here it is a metaphor for the exam question:
do two neighbouring paragraphs *lock* as one voice, or is there a gap you can
drive a wedge into?

The detector is deliberately old-fashioned. It does **not** fine-tune a
transformer. It asks a compressor (zlib, standing in for Kolmogorov
complexity) whether two paragraphs share structure, then backs that guess
with closed-class stylometry so a topic shift cannot masquerade as an author
shift. That pairing is the whole oral-exam thesis.

## What the exam task is

Given a plain-text document whose paragraphs are separated by blank lines,
emit a JSON object:

```json
{"changes": [0, 1, 0, 0]}
```

Length of `changes` is `n_paragraphs - 1`. A `1` means "the author changed
between these two paragraphs." Evaluation is F1 on those bits, usually
macro-averaged across documents. PAN 2023/2024 split the data into easy /
medium / hard by how much *topic* is allowed to leak into the style signal.

I wrote the notes, the original corpus, and the code so I could answer:

- Why is this an *intrinsic* problem?
- Why does accuracy lie when most boundaries are `0`?
- Why does a topic change fool a bag-of-words model?
- What does Normalized Compression Distance actually measure?
- When would I throw this away and fine-tune a transformer?

## Layout

| Path | What it is |
| --- | --- |
| [`docs/`](docs/README.md) | Exam notes, formula card, oral cards, ethics |
| [`examples/`](examples/README.md) | Original documents, labs, walkthroughs |
| [`src/quoin/`](src/quoin) | Tokenizer, NCD, features, detector, CLI |
| [`tests/`](tests) | Unit and corpus smoke tests |

## Install and run

Python 3.10+ and the standard library. No torch, no transformers, no
downloaded weights.

```bash
python3 -m pip install -e ".[dev]"
python3 -m quoin score examples/corpus
python3 -m pytest
```

Useful commands:

```bash
python3 -m quoin explain examples/corpus/problem-01-press-then-notice.txt
python3 -m quoin features examples/corpus/problem-13-two-pewtersmiths.txt
python3 -m quoin calibrate examples/corpus
python3 -m quoin report examples/corpus --out examples/reports
python3 -m quoin baselines examples/corpus
```

Lab scripts under `examples/labs/` are the same material stepped for
revision (split a document, print a feature table, compute one NCD by hand,
score the bank, ablate channels, watch the topic confound).

## The detector in one paragraph

For paragraphs \(p_i\) and \(p_{i+1}\) the **Quoin score** is a weighted sum
of four distances: zlib Normalized Compression Distance, cosine distance on
character 3-grams, L1 on a closed-class function-word profile, and L1 on a
tiny punctuation / length-shape vector. A boundary is marked `1` when the
score clears a threshold calibrated on a held-out slice of this same toy
bank. Easy documents (register *and* topic jump) are supposed to light up.
Same-voice topic jumps are supposed to stay dark. Same-topic two-author
documents are the ones I expect to miss in an oral, and I wrote them that
way on purpose.

## What this is not

- Not the official PAN datasets (those are Reddit threads; I do not
  redistribute them).
- Not a claim that zlib authorship attribution is state of the art.
- Not advice for accusing a classmate, a colleague, or a stranger of
  plagiarism. See [`docs/15-ethics.md`](docs/15-ethics.md).

## Licence

MIT. Original notes and example documents are mine. The task definition
follows the publicly described PAN multi-author writing-style analysis
setup.
