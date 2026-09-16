# Calibration and leave-one-out

The default cut is **0.30**. That is a number that fits *this* study set. It is not a law of style.

## Grid

```bash
PYTHONPATH=src python3 -m hingemark calibrate examples/corpus
```

The grid walks τ from 0.18 to 0.70 and sorts by mean per-document macro-F1. On this revision the peak sits near 0.30. Nearby values (0.28, 0.32) tell the same story: easy/medium seams light up, hard same-register pairs stay dark, River/Quill controls stay quiet.

## Leave-one-document-out

```bash
PYTHONPATH=src python3 -m hingemark calibrate examples/corpus --loo
```

For each file, pick the best τ on the other twenty-five, then score the held-out file. This is the honest exam story:

- A cut that fits quince-and-letter may still miss two mycologists.
- A cut that is kind to chat controls may go blind on a quiet gift abstract.

If the oral asks "how did you choose the threshold?" do not say "0.30 felt right." Say "I grid-searched mean macro-F1 on the study documents and I checked leave-one-out so one loud file could not pick the cut."

## What not to do

- Do not tune τ on the same file you report.
- Do not tune τ to make hard files look solved. Hard files are in the corpus to stay hard.
- Do not average accuracy into the selection criterion. See the 16/4 trap.
