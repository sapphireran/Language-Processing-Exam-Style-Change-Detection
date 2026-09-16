# 04 — CUSUM and sliding windows

This is the calculation I can do with a pen. If they ask for "a method
that does not need a neural net", I start here.

## The picture

Take a one-dimensional observation per unit. I use **word count**.

Let `x_1 … x_n` be those counts and `μ` their mean.

```
S_0 = 0
S_i = S_{i-1} + (x_i − μ)
```

If a writer prefers short units, the increments are negative and `S`
walks down. If the next writer prefers long units, the increments turn
positive and `S` walks up. **A slope reversal is the candidate cut.**

I still need a rule that ignores a single noisy sentence. In the code,
a reversal counts only when each side of the joint runs for at least
two units and travels at least 20% of the CUSUM range.

## Worked numbers (I memorise this series)

Suppose eight sentences with lengths

```
4, 5, 4, 5, 18, 16, 17, 19
```

Mean `μ = (4+5+4+5+18+16+17+19) / 8 = 88 / 8 = 11`.

Increments `x_i − 11`:

```
-7, -6, -7, -6, +7, +5, +6, +8
```

CUSUM `S`:

```
0, -7, -13, -20, -26, -19, -14, -8, 0
```

The walk goes down for four steps and up for four steps. The joint is
after sentence 4, which is pair index `3`. That is the cut.

This is exactly the shape of `02_recipe_then_maillard`: short
imperatives, then long academic sentences. Run:

```
python -m examscd cusum examples/documents/02_recipe_then_maillard.txt
```

and I should see the same elbow.

## What CUSUM is not

- It is not a proof of authorship. Two moods of the same writer can
  bend the line.
- It is not robust when both writers use the same sentence length.
  The hard BPE file is closer to that failure.
- The classical "QSUM" forensic chart that plots two series on one
  axis has been criticised as visually suggestive. I will mention the
  criticism if they mention QSUM. The cumulative-sum *idea* is still
  a fair exam sketch if I state the limitations.

## Sliding windows (the other pen-and-paper move)

If units are too short to estimate a 3-gram profile, I glue them.

- Window width `w = 3` sentences.
- Window `i` is the concatenation of units `i, i+1, i+2`.
- Distance `d_i` is between window `i` and window `i+1` (they overlap;
  the unique material is the sentence that left and the sentence that
  entered).

A cleaner variant compares **non-overlapping** blocks: sentences
`1–4` vs `5–8`. That is what I would draw on the board for the hard
file.

KL divergence on character 3-grams, with add-`0.5` smoothing:

```
KL(p || q) = Σ p_k log(p_k / q_k)
```

I use it in walkthroughs, not in the default detector. Cosine is
enough for the oral and it is symmetric.

## How I turn a CUSUM into a binary vector

The detector does **not** trust CUSUM alone. A hit adds `0.06` to the
combined pair score. The cut still has to clear the gap threshold.
That way a gentle slope on a single-author commute diary does not
invent a writer.

If they ask me to use CUSUM as the only method, I will emit a `1` at
each sustained slope reversal and `0` elsewhere. That baseline is in
the compare table as `CUSUM slope reverse`.
