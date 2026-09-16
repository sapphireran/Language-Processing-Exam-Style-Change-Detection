# Calibration, and why leave-one-out lies here

The default threshold `τ = 0.30` and sure-fold `σ = 0.45` were picked
on **this** folder. That is circular. Say it.

## What a fair procedure would be

1. Freeze the feature definition (the six rates, the 108 function
   words, the blend weights).
2. Hold out whole documents, or whole *sites*.
3. Pick `τ` on the complement.
4. Report the hold-out site, especially hard and control.

`scripts/grid_thresholds.py` sweeps `τ` after the fact. Use it as a
sensitivity picture, not as a second training loop you pretend you
did not do.

## Leave-one-out on 26 toys

LOO here is optimistic for three reasons:

- every easy document is the same joke (stall/letter/chat → notice)
- the hard documents were edited until the detector missed them
- the threshold is coarse (0.05 steps) so LOO rarely moves it

If the examiner asks "how would you set τ on a real PAN collection,"
the answer is: on the published training split, maximising **macro-F1
on boundaries**, with a nested check that the topic-control documents
stay near zero false folds. Then freeze. Then touch the test zip
once.

## Adaptive is not a free lunch

`median + 0.85 MAD` with a floor of 0.22 is a per-document rule. It
does not leak other documents. It *does* leak the scores of the
document you are marking, including the gold hinge if one exists. On
a quiet control the floor dominates. On a collage the median is high
and almost every cut clears it. That is acceptable only because the
register floor (L1 ≥ 0.18) still sits on the six rates.
