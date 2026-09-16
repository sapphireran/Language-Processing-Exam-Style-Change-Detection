# Results on the synthetic study set

Live numbers from `python3 examples/compare_detectors.py` after the
contraction-tail fix. This is a **24-document toy set**. Quote it as a
revision check, not as a shared-task score.

Detectors were fit on the 15 `train` problems (all difficulties mixed)
and then scored on every document of each difficulty, including the
train rows of that folder. That is a debugging table, not a blind test.
For a stricter split, score only `split=test` in the manifest.

| split | detector | acc | f1_0 | f1_1 | macro-F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| easy | always0 | 0.737 | 0.848 | 0.000 | 0.424 |
| easy | unsupervised | 0.789 | 0.857 | 0.600 | 0.729 |
| easy | threshold | 0.772 | 0.840 | 0.606 | 0.723 |
| easy | logistic | 0.895 | 0.927 | 0.812 | 0.870 |
| easy | ensemble | 0.912 | 0.940 | 0.839 | 0.889 |
| medium | always0 | 0.674 | 0.805 | 0.000 | 0.403 |
| medium | unsupervised | 0.783 | 0.844 | 0.643 | 0.743 |
| medium | threshold | 0.804 | 0.857 | 0.690 | 0.773 |
| medium | logistic | 0.870 | 0.903 | 0.800 | 0.852 |
| medium | ensemble | 0.804 | 0.857 | 0.690 | 0.773 |
| hard | always0 | 0.698 | 0.822 | 0.000 | 0.411 |
| hard | unsupervised | 0.774 | 0.838 | 0.625 | 0.731 |
| hard | threshold | 0.755 | 0.817 | 0.629 | 0.723 |
| hard | logistic | 0.868 | 0.909 | 0.759 | 0.834 |
| hard | ensemble | 0.849 | 0.895 | 0.733 | 0.814 |

## What to say about this table in an exam booklet

1. `always0` keeps high accuracy and a dead `f1_1`. That is why the
   headline is macro-F1.
2. The unsupervised z-score jump already beats the baseline on the
   **hard** split (0.73 vs 0.41). Topic leakage is not the only signal.
3. Logistic pairwise regression is stronger still, but it has seen the
   train documents that sit inside these folders. Treat the jump from
   0.73 to 0.83 as “the features are linearly usable”, not as a
   generalisation claim.
4. Easy is not dramatically easier than hard for the style-only models.
   That is by design: the house authors were written with loud habits.
   A real hard set with similar registers would be harsher.

Re-generate:

```bash
python3 examples/compare_detectors.py
```
