# Formula card

Write this from memory. If a symbol needs a speech, it is
the wrong symbol.

## Split

`n` units → `n−1` hinges.

## Rates

For a count channel, `x = count / n_words`.
Shape channels (`mean_word_len`, `n_words`, `question_rate`)
stay in their own units. They are still z-scored inside the
document, so they vote on the same scale.

## Document std

```
s_f = pstdev({ x_{1,f}, …, x_{n,f} })
```

Population std, not sample std. With four units I am not
pretending to know a degree of freedom.

## Jump

```
scale_f = max(s_f, prior_f)
z_{i,f} = (x_{i,f} − x_{i+1,f}) / (scale_f + 10^{-6})
```

`n_words` and `mean_word_len` do not vote.

## Mark

```
peak_f = max_i |z_{i,f}|
mark_{i,f} = [|z_{i,f}| ≥ max(ζ, ρ · peak_f)]
```

`ζ = 0.90`, `ρ = 0.70`.

## Bundle

```
votes_i = Σ_f mark_{i,f}
change_i = [votes_i ≥ k]
```

`k = 3`.

## Macro-F1

```
F1_c = 2 P_c R_c / (P_c + R_c)   c ∈ {same, change}
macro-F1 = (F1_same + F1_change) / 2
```

## Liars

```
never-fire:  change_i = 0
always-fire: change_i = 1
```

## Authors guess (not the task)

`1 + Σ change_i` is a walk count, not the number of unique
hands. ABA has two changes and two authors. I will not
confuse those in a written answer.

## PAN command

```
mySoftware -i INPUT -o OUTPUT
→ OUTPUT/solution-problem-X.json  {"changes":[…]}
```
