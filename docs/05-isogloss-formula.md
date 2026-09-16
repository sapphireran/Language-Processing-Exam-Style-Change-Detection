# The isogloss formula

Let `x_{i,f}` be channel `f` on unit `i`. Let `s_f` be the
population standard deviation of that channel inside this
document. Let `prior_f` be a floor I chose so a quiet
single-house file cannot manufacture sigma. Adjacent jump:

```
z_{i,f} = (x_{i,f} − x_{i+1,f}) / (max(s_f, prior_f) + ε)
```

`ε` is `1e-6` so a dead channel does not explode. A dead
channel with constant `x` still has `z = 0`. Shape channels
(`n_words`, `mean_word_len`) are shown on inspect tables and
**do not vote**.

Let `peak_f = max_j |z_{j,f}|`. Mark:

```
mark_{i,f} = 1[ |z_{i,f}| ≥ max(ζ, ρ · peak_f) ]
```

Decision:

```
change_i = 1[ Σ_f mark_{i,f} ≥ k ]
```

Defaults I will say out loud: `ζ = 0.90`, `ρ = 0.70`, `k = 3`.
Rate priors sit around `0.03`–`0.05`; `digit_rate` is `0.14`
because Flint twitches; `the_rate` is `0.08` because articles
wander.

## Why adjacent, not a window

A window of two on each side is a mini saw. It helps when a
unit is short. It lies in the middle of an ABA, where the
window straddles A and B on both sides. I keep the window at
**one unit** and I write units long enough to be maps. That is
a design choice I can defend: I would rather thicken the unit
than blur the hinge.

## Why not Mahalanobis

Mahalanobis on fifteen channels with four units is a toy
covariance. I would be fitting noise and calling it geometry.
Votes do not need a covariance. They need independence as a
*story*: person, deontic, hedge, digit are not the same
muscle. If they move together, something happened to the hand.

## MDL in one sentence

Two codebooks are cheaper than one when the bundle is real.
I do not fit a two-book description length in the detector
(short files, Dirichlet-multinomial, a penalty I would invent).
I keep it as an oral cousin: **a bundle is a place where the
document gets cheaper to tell as two dialects**.
