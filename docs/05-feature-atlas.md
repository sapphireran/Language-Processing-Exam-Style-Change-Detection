# Feature atlas

## The exam vector (count these)

For a span of units, let `T` be the number of word tokens
(`inkfold.tokenize.word_tokens`: letters plus `I'm`-style apostrophes).

| symbol | rate | membership |
| --- | --- | --- |
| I | first-person singular / T | I, me, my, I'm, I've, I'd, I'll, mine, myself |
| you | second person / T | you, your, yours, you're, … |
| ctr | contractions / T | don't, I'll, can't, it's, gonna, … |
| frm | formal / T | shall, must, hereby, pursuant, thereof, … |
| hdg | hedges / T | perhaps, approximately, consistent, seems, … |
| we | first-person plural / T | we, our, us, ours, ourselves |

```
r = (I, you, ctr, frm, hdg, we)
d(left, right) = || r_left - r_right ||_1
```

`inkfold hand` prints the raw counts so you can check a script by
pencil. If your hand count disagrees, you tokenised a hyphen or a
numeral differently. The lists live in `src/inkfold/lexicon.py` and
the function-word list is frozen at **108** items.

## Recorded but not in d

- **Mean unit length / 20.** On six-line documents a four-token swing
  outruns a *shall*. We still print it. We do not add it.
- **Vocatives** (yeah, lol, btw). Chat crumbs. Useful in an ablation,
  poisonous in a topic control.
- **Character 3-grams.** Contentful on short text. Kept in the explain
  table as a *leak*. Weight in the default blend is **0**.
- **Intra-document Delta.** Same function-word counts, Manhattan of
  z-scores with a floor. Recorded, not blended.

## The blend the program actually uses

```
hinge = 0.65 * adjacent + 0.35 * window_2
adjacent = 0.80 * squash(d, 0.20) + 0.20 * (1 - cos(fw))
```

`squash(x, s) = x / (x + s)`. An L1 of 0.25 becomes 0.56. Function
words are add-0.5 smoothed over the 108-word list.

If the oral asks "why not transformers," the answer is: a six-line
document has no right to a 110-million-parameter prior, and you cannot
hand-check one in an exam hall.
