# 11 — Formula sheet

Write this from memory. If I cannot, I am not ready.

## CUSUM

```
μ      = (1/n) Σ x_i
S_0    = 0
S_i    = S_{i-1} + (x_i − μ)
```

Candidate cut: sustained slope reversal of `S`.

## Character 3-gram cosine

```
cos(a,b) = (a · b) / (‖a‖ ‖b‖)
dist     = 1 − cos(a,b)
```

## Function-word L1

```
p_w(A) = count_A(w) / |tokens_A|
L1     = Σ_w |p_w(A) − p_w(B)|
```

`w` ranges over a closed list. Open-class words stay out.

## Smoothed KL (windows, optional)

```
p'_k = (c_k + λ) / (N + λV)
KL(p‖q) = Σ p'_k log(p'_k / q'_k)
```

## Pair score I implemented

```
d = 0.42 dist_3gram
  + 0.28 clip(L1 / 1.4)
  + 0.20 clip(style_L2 / 1.1)
  + 0.10 |n1 − n2| / max(n1, n2)
```

Threshold: `max(floor, min(μ + kσ, midpoint of largest gap))`
if the gap is clean; else `max(floor, μ + kσ)`.
No cut if `max(d) < floor`.

## Macro-F1

```
P_c  = TP / (TP + FP)     (1 if both are 0)
R_c  = TP / (TP + FN)     (1 if both are 0)
F1_c = 2PR / (P + R)
macro = (F1_0 + F1_1) / 2
```

## Adjusted Rand index

```
ARI = (Index − Expected) / (Max − Expected)
```

Labels may be permuted. Pair F1 can be 1 when ARI is not.

## Output shapes

```
changes : length n − 1, binary, 1 = writer changed
authors : length n,     ints,   same int = same writer
```

## Words I must not mix

```
attribution  → name, needs candidates
verification → same person, two texts
style change → cuts, one text, intrinsic
topic        → not style
```
