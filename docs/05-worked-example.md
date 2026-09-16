# 05 — Worked example (numbers you can redo)

All figures below come from `python3 examples/walk_worked_example.py`.
If you change the tokeniser, this page must change with it.

## Two paragraphs

**P1** (casual, first person):

> I think we should take the late boat. I cannot stand the morning
> crowd on the pier.

**P2** (academic, third person):

> The analysis suggests that tidal delay should be treated as a
> structural constraint rather than a residual error.

Tokenised (lowercase, apostrophes kept):

```
P1 (17): i think we should take the late boat i cannot stand the
         morning crowd on the pier
P2 (18): the analysis suggests that tidal delay should be treated
         as a structural constraint rather than a residual error
```

## Function-word relative frequencies

Only dimensions that are non-zero in at least one paragraph:

| word | P1 count / 17 | P2 count / 18 |
| --- | ---: | ---: |
| a | 0 | 2/18 = 0.1111 |
| as | 0 | 1/18 = 0.0556 |
| be | 0 | 1/18 = 0.0556 |
| cannot | 1/17 = 0.0588 | 0 |
| i | 2/17 = 0.1176 | 0 |
| on | 1/17 = 0.0588 | 0 |
| rather | 0 | 1/18 = 0.0556 |
| should | 1/17 = 0.0588 | 1/18 = 0.0556 |
| than | 0 | 1/18 = 0.0556 |
| that | 0 | 1/18 = 0.0556 |
| the | 3/17 = 0.1765 | 1/18 = 0.0556 |
| we | 1/17 = 0.0588 | 0 |

Cosine on the **full** function-word basis:

```
cos(P1, P2) ≈ 0.293
cosine distance = 1 − cos ≈ 0.707
JS divergence ≈ 0.491
```

Shared mass is essentially `should` and `the`. Everything else is on
one side of the join. That is what a style change looks like when
genre also changes. On hard documents you will not get a 0.71 cosine
distance; you will get something like 0.2 and you will need the rest
of the ensemble.

## Cosine on a six-word subset (exam-script version)

Take only `i, the, that, should, a, as`.

```
P1 = [2/17, 3/17, 0, 1/17, 0, 0]
   ≈ [0.1176, 0.1765, 0, 0.0588, 0, 0]
P2 = [0, 1/18, 1/18, 1/18, 2/18, 1/18]
   ≈ [0, 0.0556, 0.0556, 0.0556, 0.1111, 0.0556]

dot     = 0.1176·0 + 0.1765·0.0556 + 0 + 0.0588·0.0556 + 0 + 0
        ≈ 0.01307
||P1||  ≈ 0.2201
||P2||  ≈ 0.1571
cos     ≈ 0.01307 / (0.2201 · 0.1571) ≈ 0.378
```

You would put this table on the script. The full-basis cosine (0.293)
is lower because extra dimensions (`we`, `cannot`, `rather`, …) are
orthogonal. Both numbers tell the same story: these paragraphs do not
share a closed-class profile.

## Register rates

| | P1 | P2 |
| --- | ---: | ---: |
| first person | 3/17 ≈ 0.176 (`i`,`i`,`we`) | 0 |
| academic markers | 0 | 2/18 ≈ 0.111 (`analysis`, `constraint`) |
| mean sentence length | 8.5 words | 18 words |
| Flesch proxy | ~104 | ~38 |

P2 is a single long sentence. P1 is two short ones. The Flesch proxy
moves because sentence length and syllable load both move. Quote it
as a proxy.

## Yule's K on a toy bag (fully by hand)

Bag: `the the boat the pier`

```
N = 5
the × 3, boat × 1, pier × 1
V1 = 2, V3 = 1
Σ i² V_i = 1²·2 + 3²·1 = 11
K = 10^4 · (11 − 5) / 5² = 10^4 · 6 / 25 = 2400
```

A paragraph that repeats `the` this hard is cartoonish. Real lab
paragraphs land around K ∈ [50, 400]. Direction still matters:
repetition-heavy casual prose tends to larger K than dense methods
prose of the same length.

## Confusion matrix (same numbers as the evaluation note)

```
gold = [0, 1, 0, 1]
pred = [0, 1, 1, 1]
F1 = 0.800
macro-F1 ≈ 0.733
accuracy = 0.750
```

See [04-evaluation.md](04-evaluation.md) for the cell-by-cell
arithmetic.
