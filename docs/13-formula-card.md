# Formula card

Write this on scrap paper at the start.

## Units

Problem file: one non-empty line = one unit. `n` units, `n-1` cuts.

## Tokens

`[A-Za-z]+(?:'[A-Za-z]+)?` and numerals. Lowercased. `I'm` is one token.

## Exam vector

```
r = (I, you, ctr, frm, hdg, we)
rate = count / T
d = |ΔI| + |Δyou| + |Δctr| + |Δfrm| + |Δhdg| + |Δwe|
```

Function-word list length = **108**. Smooth each bin by +0.5 before cosine.

```
cos(a,b) = (a·b) / (||a|| ||b||)
fw = 1 - cos
squash(x, s) = x / (x + s)          s = 0.20 for d
adjacent = 0.80 * squash(d, 0.20) + 0.20 * fw
hinge    = 0.65 * adjacent + 0.35 * window_2
```

## Firing

```
τ = 0.30     σ = 0.45     register floor = 0.18
fire if (hinge ≥ σ) or (hinge ≥ τ and local max)
     and (d ≥ 0.18)
authors_naive = 1 + sum(fires)     # wrong on returns
```

## Metrics

```
acc = (tp+tn) / N                  # do not lead with this
P+ = tp / (tp+fp)    R+ = tp / (tp+fn)
F1+ = 2 P+ R+ / (P+ + R+)
macro-F1 = (F1+ + F1-) / 2
```

On this folder, never-fire acc ≈ 0.77, never-fire macro-F1 ≈ 0.44.

## CUSUM (picture only)

```
x_i = rate on unit i
S_k = sum_{i=1..k} (x_i - mean(x))
```

A peak in `|S|` is a candidate, not an answer.

## Contract

```
len(changes) = n - 1
if not return_author: authors = 1 + sum(changes)
if return_author: that equality fails on purpose
```

## Length

Mean unit tokens / 20 is printed. **Not** in `d`.
