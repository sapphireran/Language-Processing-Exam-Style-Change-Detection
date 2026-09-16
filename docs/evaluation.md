# Evaluation

PAN reports **macro-averaged F1** over the two labels `{0, 1}` so a
detector that never fires cannot hide behind the majority class.

Almost every pair in a real document is a `0`. Always predicting `0`
gives high accuracy and a terrible macro-F1. Always predicting `1` is
the adjacent-sentence 3-gram failure mode.

This repo implements that metric in `stylechange.evaluate.macro_f1` and
also reports pooled pair-accuracy and an exact-document count, because
on eight toy files you want to see *which* story broke.

## How to score the bundled folder

```bash
stylechange evaluate examples/documents
python examples/run_collection.py
python examples/pan_roundtrip.py
```

`evaluate` can write PAN-shaped `solution-problem-*.json` files:

```bash
stylechange evaluate examples/documents --output /tmp/stylechange-out
```

`pan_roundtrip.py` does the same thing into a temp directory and prints
the arrays it wrote. That is the submission shape: one solution file
per problem, no gold keys, just `changes`.

## What a 1.000 here means

On the current baseline the bundled collection is exact:

- 8 / 8 documents match their gold `changes`
- 46 / 46 pairs match
- collection macro-F1 = 1.000

That number is **not** a PAN test-set number. The documents were
written so that the voices and the *we* vs *one* contrast are audible.
Real shared-task documents (Reddit comments, same topic, same register)
will score lower, especially on the hard split. Say that out loud
before you show the table.

## Document-wise vs pooled

PAN editions have varied between "F1 per document, then average" and
"pool the pairs". We pool the pairs for the collection line and still
print a per-document F1 so a single broken file is obvious. With eight
files the two views agree whenever every file is exact.

## Length mismatches

If `len(pred) != len(gold)`, the document scores `F1 = 0` in the table.
That almost always means the segmenter picked paragraphs instead of
sentences (or the other way around). Pass `--granularity sentence` or
`paragraph` explicitly.
