# Threshold calibration

Every pairwise detector in this kit returns a real score. A threshold
turns the score into the binary vector PAN wants.

That threshold is not a moral property of language. It is a number you
fit on labelled development data.

```text
python3 -m splicefind calibrate examples/corpus
```

The sweep prints macro F1, micro F1, precision, recall, and accuracy
for a grid of cut-offs. The starred row is the macro-F1 winner.

## What you should see conceptually

- Low threshold: many 1s, recall up, precision down.
- High threshold: many 0s, the "always same" costume returns.
- A useful operating point sits where F1 peaks, which is rarely where
  accuracy peaks.

## Relative scoring (the default)

`--method relative` (the CLI default) does not treat 0.55 as a sacred
global cut. It marks a boundary if the blend is high for *this*
document (median + 1.25 MAD, with a small floor) or if the raw score
clears an absolute minimum. That is how a four-paragraph allotment
diary avoids being labelled as three author changes just because
z-scores have nothing else to compare against.

`--method ensemble` is the older global-threshold story, useful when
you want the sweep to move in a straight line. `--method adaptive`
min-max normalises the blend and is a diagnostic, not a default: it
over-fires on single-author documents.

## Development hygiene

- Do not pick the threshold on the same documents you will quote as
  the final score. The corpus here is tiny, so the README treats the
  printed F1 as a **demo**, not a leaderboard.
- If you add a transformer later, calibrate it the same way. A softmax
  is also just a score.
- Report the threshold next to the F1. An F1 without an operating
  point is an incomplete sentence.

The written-exam version of this section is in
[12-written-answers.md](12-written-answers.md), question 4.
