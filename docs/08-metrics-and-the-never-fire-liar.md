# Metrics and the never-fire liar

This bank has 92 hinges and 23 changes. A predictor that never
fires is right on 69 / 92 hinges. That is about **75%
accuracy** and a **useless** system.

I will not quote accuracy unless I also quote the liar.

## Macro-F1

For each class `c ∈ {0, 1}`:

```
P_c = TP_c / (TP_c + FP_c)
R_c = TP_c / (TP_c + FN_c)
F1_c = 2 P_c R_c / (P_c + R_c)
```

Macro-F1 is `(F1_0 + F1_1) / 2`. The shared task uses this
(macro across sentence pairs). Never-fire has `F1_1 = 0`, so
macro-F1 collapses even when accuracy looks adult.

Always-fire has the opposite disease: it never sees a same-hand
hinge. On this bank it looks busy and scores worse than
never-fire on accuracy, which is the other way a student can
lie to themselves.

## What I put on the board

| predictor | what it proves |
| --- | --- |
| never-fire | the base rate |
| always-fire | the other base rate |
| isogloss | whether the bundle is doing work |

If isogloss cannot beat never-fire on macro-F1, I do not have
a detector. I have a story.

## Per-document honesty

A control should be all zeros. A trap should be all zeros. An
easy 2+2 should fire exactly once, at the join. An ABA should
fire twice. A collage of four houses should fire three times.
I would rather show one clean inspect table than a leaderboard.
