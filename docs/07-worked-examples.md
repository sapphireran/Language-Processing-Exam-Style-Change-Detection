# Worked examples

These calculations are meant to be doable on paper. The toolkit should
agree up to floating-point noise; if it disagrees on a *count*, the
tokenizer is the first place to look.

## Example A — a clean Mira → Jules boundary

**Sentence 0 (Mira).**
`However, the bloom remains relatively unstable although the pour is slow.`

**Sentence 1 (Jules).**
`I don't wait that long; I just go for it!`

Gold: `changes = [1]`.

### Manual tokens

Mira, lowercased, words only:

```
however the bloom remains relatively unstable although the pour is slow
```

11 words. Contractions: 0. First-person: 0. Hedges: *however*,
*relatively*, *although* (the last is also a subordinating marker).
Nominalizations: 0. Digits: 0. Semicolons: 0. Exclamations: 0.

Jules:

```
i don't wait that long i just go for it
```

If we treat `don't` as one token: 9 words. Contractions: 1.
First-person: `I` → 1. Hedges: 0. Exclamations: 1. Semicolons: 1
(Jules borrowed Nell’s punctuation for one beat — that happens).

### Features that must jump

| Feature | Mira | Jules | \|diff\| |
| --- | --- | --- | --- |
| `contraction_rate` | 0 / 11 = 0.00 | 1 / 9 ≈ 0.11 | 0.11 |
| `first_person_rate` | 0.00 | 1 / 9 ≈ 0.11 | 0.11 |
| `hedge_rate` | 2 / 11 ≈ 0.18 | 0.00 | 0.18 |
| `subord_marker_rate` | 1 / 11 ≈ 0.09 | 0.00 | 0.09 |
| `exclamation_rate` | 0.00 | 1 / 9 ≈ 0.11 | 0.11 |
| `word_count` | 11 | 9 | 2 |

No content word (*bloom*, *pour*) appears in this table. That is the
point. A topic model sees two coffee sentences and stays asleep; a
style model sees stance and punctuation flip.

### What the unsupervised detector does with one pair

With only two sentences, within-document z-scoring is degenerate: each
feature has two values, mean in the middle, and the single distance is
always “the” jump. The detector therefore **always predicts a change**
on a 2-sentence document. That is acceptable (there is no other pair to
compare) and is why the synthetic set starts at 7 sentences.

Run:

```bash
stylechange explain --input data/synthetic/hard/problem-001.txt --pairs 0-2
```

## Example B — Hale’s digits next to Nell’s semicolon

**Sentence 0 (Hale).**
`Water mass was 15.0 g and bloom time was 45 s.`

**Sentence 1 (Nell).**
`The kettle ticked; the filter breathed a faint paper sweetness.`

### Counts

Hale words: `water mass was 15.0 g and bloom time was 45 s` → 11 tokens
if `15.0` and `45` stay intact. Digits appear in two tokens. Passives:
*was* … no clear `ed` participle, so `passive_be_rate` may stay 0 —
do not force the heuristic. `digit_rate` is the clean tell.

Nell words: 10. Semicolons: 1. Digits: 0. Contractions: 0.

| Feature | Hale | Nell | \|diff\| |
| --- | --- | --- | --- |
| `digit_rate` (chars) | 4 digits / ~40 chars ≈ 0.10 | 0 | 0.10 |
| `semicolon_rate` | 0 | 1 / 10 = 0.10 | 0.10 |
| `first_person_rate` | 0 | 0 | 0 |
| `contraction_rate` | 0 | 0 | 0 |

This pair is why you do not evaluate a detector on a single feature.
Hale → Nell is a **digit / punctuation** jump, not a pronoun jump.

## Example C — a same-author pair you should *not* flag

**Both Mira, hard topic.**

1. `A modest bloom suggests that degassing remains relatively active.`
2. `However, the subsequent drawdown appears somewhat slower than expected.`

Shared habits: hedge words, no contractions, no `I`, similar length.
`hedge_rate` is high on both, so the *difference* is small. The
unsupervised detector should stay quiet unless the rest of the document
is written by Hale and these two are the odd ones out — in which case
the jump is at the *entry* to Mira’s block, not between these two.

This is the pairwise independence trap: a pair can look “same author”
locally and still be the middle of a three-author sandwich. Labels care
only about the two neighbours.

## Example D — majority baseline arithmetic

Document gold: `[0, 0, 1, 0, 1, 0]` (6 pairs, change rate 1/3).
`always0` predicts `[0, 0, 0, 0, 0, 0]`.

Class 0: TP=4, FP=2, FN=0 → P=4/6, R=1, F1=0.80.
Class 1: TP=0, FP=0, FN=2 → P=0, R=0, F1=0.
Macro-F1 = 0.40.

Accuracy = 4/6 ≈ 0.67. If you only wrote 0.67 in the booklet you would
be describing a coin that never calls heads.

## Example E — returning author

Gold author ids: `mira, mira, hale, mira, mira`.
`changes` must be `[0, 1, 1, 0]`.
`authors` must be `2`, not `3`.

A detector that outputs author *names* could in principle say the last
block is Mira again. The official output cannot. If the exam asks
whether style-change detection recovers identity, the answer is no.

## Check your own work

```bash
python examples/feature_walkthrough.py
python examples/manual_pair_check.py
```

Those scripts reprint the tables above from the live extractor so a
mismatch between paper and code is visible.
