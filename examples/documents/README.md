# Example documents

Hand-written exam-style problems, not PAN Reddit dumps. The layout is the
PAN multi-author writing-style layout:

| file | role |
| --- | --- |
| `problem-<id>.txt` | document text |
| `truth-problem-<id>.json` | gold `changes` array (`0` same style, `1` a cut) |

`changes` is always one shorter than the number of units. Extra JSON keys
(`difficulty`, `voices`, `note`) are for humans; the evaluator only reads
`changes`.

Sentence problems put **one unit per line**. The paragraph problem uses
blank lines, the way PAN 2023 did.

## What each problem is testing

| id | units | intended story |
| --- | ---: | --- |
| `easy-kitchen-and-syntax` | 9 sentences | recipe chat → syntax textbook → CFG notes |
| `medium-embeddings` | 6 sentences | same topic; student hedges vs academic prose |
| `hard-we-vs-one` | 6 sentences | same topic *and* register; *we/our* vs *one/may* |
| `exam-takehome` | 10 sentences | student revision → pasted textbook → lecture shorthand |
| `single-author` | 6 sentences | negative control, morphology textbook only |
| `paragraph-gift` | 3 paragraphs | same take-home story, PAN-2023 paragraph pairs |
| `questions-vs-exposition` | 6 sentences | Socratic questions vs declarative LM notes |
| `notes-after-prose` | 8 sentences | parsing textbook vs labelled lecture notes |

## Running them

From the repository root, after `pip install -e .`:

```bash
stylechange detect examples/documents/problem-exam-takehome.txt --explain
stylechange evaluate examples/documents
python examples/run_collection.py
```

The paragraph document is picked up by `--granularity auto` because it
contains blank lines. You can still force it:

```bash
stylechange detect examples/documents/problem-paragraph-gift.txt \
  --granularity paragraph --explain
```
