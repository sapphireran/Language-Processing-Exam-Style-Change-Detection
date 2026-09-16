# Examples

These scripts are the hands-on half of the [study notes](../docs/README.md).
They operate only on the synthetic corpus under `examples/data/` — no
Reddit dumps, no shared-task downloads, no company data.

Run them from the repository root after `pip install -e ".[dev]"`.

| Script | What it demonstrates |
|--------|----------------------|
| [`01_inspect_document.py`](01_inspect_document.py) | Units, truth bits, reconstructed author runs |
| [`02_train_baseline.py`](02_train_baseline.py) | Pooled logistic regression + readable weights |
| [`03_error_analysis.py`](03_error_analysis.py) | Hits, misses, near-misses, feature deltas |
| [`04_compare_difficulties.py`](04_compare_difficulties.py) | 3×3 train-band × test-band macro F1 |
| [`05_hand_features.py`](05_hand_features.py) | The souffle/pizza document, cue by cue |
| [`06_write_report.py`](06_write_report.py) | HTML author-run walk-throughs |

Problems 1–12 in each band are the **training** slice. Problems 13–18
are the **holdout** slice used by examples 02–04 so in-band F1 is not
train-set accuracy.

Regenerate the corpus (should be a no-op if you have not edited
`scd.generate`):

```bash
python3 -m scd.generate --out examples/data --seed 20260316
```

Write an HTML walk-through of problem 1:

```bash
python3 -m scd report \
  --problem examples/data/easy/problem-1.txt \
  --out /tmp/scd-easy-1.html
```

## What you should see

- Easy documents change *topic and register* together.
- Hard documents keep the same nouns and vary closed-class habits.
- A model trained only on easy data overfits word Jaccard.
- A pooled model still ranks contraction / function-word cues highly.
- Majority-0 looks fine on accuracy and poor on macro F1.

If a script ever prints a perfect 1.0 on the hard band, the toy corpus
has become too clean. That is a generator bug, not a breakthrough.
