# Calibration

A distance is not a decision. The Quoin score is a real number. The
exam format wants a bit. The number that turns one into the other is
a **threshold**.

I do not treat the default absolute cutoff `0.72` as a law. It is the
value that, together with a within-document peak margin of `0.08`,
stopped the never-fire / always-fire sandwich on *this* toy bank.
`python -m quoin calibrate` still grids an *absolute* threshold on
raw Quoin scores so I can see the accuracy trap in a table. The live
detector also marks a hinge that is the file's loudest score by
`rel_margin`, provided it clears a floor. If I add a document, I run
the grid and I look at the peak table in `explain`. If the winner
moves a lot, the bank was doing the work, not the method.

## How the grid works

For each threshold `t` in `[0.16, 0.60]` step `0.02`:

1. mark a hinge `1` iff `quoin >= t`
2. compute macro-F1 and micro-F1 on the whole bank
3. pick the `t` with the best macro-F1, breaking ties toward a
   middling threshold so I do not worship an edge spike

There is no cross-validation library. There is a loop. The honest
limitation: I am tuning and testing on the same 28 files. These
numbers are a rehearsal, not a generalisation claim. I will say that
in the oral before anyone else does.

## What I would do with real data

- tune on the official training split
- freeze `t`
- quote the test split once
- not wander back

I would also tune *per difficulty* if the shared task evaluates easy /
medium / hard separately, which it does. A threshold that is kind to
hard documents will look sleepy on easy ones.

## Weights

The blend that actually decides is `0.20 char-cosine + 0.15 function
L1 + 0.25 shape L1 + 0.40 register L1`. NCD is computed and printed
with weight `0` on this bank because it saturates. I can move the
weights; I cannot pretend they came from a theorem. The oral version:
"I kept the compressor in the lab so I could show when it stopped
helping."
