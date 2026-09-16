# Example documents

These files follow the PAN multi-author writing-style layout:

| file | role |
| --- | --- |
| `problem-<id>.txt` | document text, **one sentence per line** (except the paragraph example) |
| `truth-problem-<id>.json` | gold `changes` array: `0` = same style, `1` = style change |

The gold files also carry extra keys (`difficulty`, `voices`, `note`) that the evaluator ignores. They are here so a human can read the intended story.

## What each problem is testing

| id | difficulty | intended story |
| --- | --- | --- |
| `easy-mixed-topics` | easy | textbook n-grams → casual POS answer → parsing lecture notes |
| `medium-one-topic` | medium | vector semantics in two registers, same topic |
| `hard-close-register` | hard | textbook parsing vs compact lecture notes |
| `exam-answer-shift` | exam | student prose, then a pasted textbook block, then shorthand |
| `single-author` | single | negative control, morphology textbook only |
| `paragraph-gift-authorship` | paragraph | same exam story, blank-line paragraphs |

`changes` is always one shorter than the number of units. For `easy-mixed-topics` there are 9 sentences and therefore 8 labels: `[0, 0, 1, 0, 0, 1, 0, 0]`.

## Running them

From the repository root, after `pip install -e .`:

```bash
stylechange detect examples/documents/problem-exam-answer-shift.txt --explain
stylechange evaluate examples/documents --output /tmp/stylechange-out
```

The paragraph document needs an explicit granularity:

```bash
stylechange detect examples/documents/problem-paragraph-gift-authorship.txt \
  --granularity paragraph --explain
```

The Python scripts in the parent folder (`explain_boundaries.py`, `run_examples.py`) print a longer walkthrough of the same files.
