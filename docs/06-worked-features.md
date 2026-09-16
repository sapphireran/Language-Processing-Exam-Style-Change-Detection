# Worked toy: two paragraphs, one feature vector, one distance

The other notes describe the system. This page does the arithmetic on a
pair of sentences short enough to finish by hand. The real sample
documents are longer; the formulas are the same.

## Texts

**P1.** `I don't want to wait. It's late.`

**P2.** `The committee therefore declines the proposal.`

## Tokens

A token here is a letter sequence with optional internal apostrophes,
lowercased — the same rule as `style_change.tokenize.words`.

P1 tokens (7): `i`, `don't`, `want`, `to`, `wait`, `it's`, `late`

P2 tokens (6): `the`, `committee`, `therefore`, `declines`, `the`, `proposal`

## Type-token ratio

TTR = unique types / tokens.

- P1: 7 types / 7 tokens = 1.00 (everything appears once)
- P2: 5 types / 6 tokens = 0.833 (`the` repeats)

Short paragraphs make TTR look extreme. That is why the sample corpus
uses longer blocks, and why the detector z-scores features across the
document instead of trusting a raw 1.00.

## Contraction rate

Contractions are tokens with an internal apostrophe.

- P1: `don't`, `it's` → 2/7 ≈ 0.286
- P2: none → 0.000

## Connective rate

Using the closed list in `lexicons.py`, `therefore` counts.

- P1: 0/7 = 0.000
- P2: 1/6 ≈ 0.167

## A two-dimensional cosine

Ignore every other feature and keep `[contraction_rate, connective_rate]`.

```text
v1 = [0.286, 0.000]
v2 = [0.000, 0.167]
```

Dot product = 0. Cosine similarity = 0. Cosine distance = 1.

A threshold anywhere below 1 labels this boundary as a change. That is
the easy-case cartoon: the two coordinates point in opposite directions.

On a real document the vector has ~30 stylometric coordinates plus a
character 3-gram profile. The cartoon still holds: same-author neighbours
should point roughly the same way; a register jump should not.

## Check it against the code

```bash
PYTHONPATH=src python3 - <<'PY'
from style_change.features import extract_profile
from style_change.distances import cosine_distance

p1 = extract_profile("I don't want to wait. It's late.")
p2 = extract_profile("The committee therefore declines the proposal.")
print("TTR", round(p1.type_token_ratio, 3), round(p2.type_token_ratio, 3))
print("contraction", round(p1.contraction_rate, 3), round(p2.contraction_rate, 3))
print("connective", round(p1.connective_rate, 3), round(p2.connective_rate, 3))
print("full-vector cosine distance", round(cosine_distance(p1.vector(), p2.vector()), 3))
PY
```

The printed contraction and connective rates should match the fractions
above. The full-vector distance will not be exactly 1, because the other
coordinates (sentence length, articles, …) are not orthogonal. That gap
between the cartoon and the full vector is the reason the ensemble also
listens to character 3-grams and function-word distributions rather than
betting on two rates.
