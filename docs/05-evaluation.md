# Evaluation

## Unit of scoring

The unit is a **boundary**, not a document and not a token. For each
document you have two aligned binary arrays of length \(n-1\). From
those you count:

|  | pred 1 | pred 0 |
| --- | --- | --- |
| truth 1 | TP | FN |
| truth 0 | FP | TN |

\[
P = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}}
\quad
R = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}
\quad
F_1 = \frac{2PR}{P+R}
\]

Accuracy \((\mathrm{TP}+\mathrm{TN})/N\) is reported by the library
because it is a useful *warning*, not because it is the official story.

## Empty-class conventions

A single-author document has \(\mathrm{TP}+\mathrm{FN} = 0\). A system
that predicts all zeros should score perfectly on that document. The
implementation therefore uses:

- \(P = 1\) when \(\mathrm{TP}+\mathrm{FP} = 0\)
- \(R = 1\) when \(\mathrm{TP}+\mathrm{FN} = 0\)
- \(F_1 = 0\) only when both \(P\) and \(R\) are 0 (the \(P+R=0\) case)

So:

| truth | pred | P | R | F1 | acc |
| --- | --- | --- | --- | --- | --- |
| `000` | `000` | 1 | 1 | 1 | 1 |
| `000` | `111` | 0 | 1 | 0 | 0 |
| `00100` | `00000` | 1 | 0 | 0 | 0.8 |

The last row is the exam trap: 80% accuracy, zero F1. Write it out if
the question gives you a similar vector.

## Macro vs micro

PAN-style reporting scores **each document**, then aggregates. This repo
prints both:

- **macro-F1** = mean of per-document F1 (small documents count as much
  as large ones)
- **micro-F1** = pool every boundary in the split, then compute one F1

If one 12-boundary document dominates a split, micro and macro disagree.
Say which one you are quoting.

## Why splits are scored separately

A single number over Easy+Medium+Hard hides the topic leak. The honest
table is three F1s. On the teaching corpus (fixed threshold 0.33):

| Split | macro-F1 | What it means |
| --- | --- | --- |
| Easy | 1.00 | Register + topic are loud |
| Medium | 1.00 | Register still enough |
| Hard | 0.33 | Same topic, close registers; one control-like miss |
| Control | 0.00 | Intra-author drift still triggers false 1s |

Those Hard and Control numbers are *features* of the notes, not a bug
to hide. A constant-0 predictor would get Control = 1.00 and Easy ≈ 0.
There is no free lunch.

## Baseline you must beat

Always quote:

1. **All-zero.** High accuracy, terrible Easy recall.
2. **All-one.** High recall, destroyed precision on Control.
3. **Topic-only cosine + threshold.** Strong on Easy, weak on Hard.
4. **Your style-only system.**

If (4) does not beat (3) on Hard, you have not shown style.

## Off-by-one and format errors

The evaluator in this repo raises if the arrays differ in length. On a
real shared-task script that is usually a silent zero. Before you talk
about F1, check:

```
len(changes) == n_paragraphs - 1
every label is 0 or 1
one solution file per problem file
```

## Command

```bash
PYTHONPATH=src python -m stylechange.cli eval examples/data/easy
PYTHONPATH=src python -m stylechange.cli eval examples/data/hard --adaptive
```
