# 6. Worked example (by hand)

This is the document in `examples/data/easy/problem-1.txt`, one sentence
per line. We will label it, compute a few features without the library,
and see why a pairwise model should fire between sentences 2 and 3.

## The text

| # | Sentence |
|---|----------|
| 1 | The souffle requires a precise fold of the egg whites into the batter. |
| 2 | Oven temperature should remain stable so the structure can set. |
| 3 | Yeah I'm just gonna chuck the frozen pizza in and hope for the best. |
| 4 | I'm not gonna overthink dinner tonight, seriously. |

Truth: `authors = 2`, `changes = [0, 1, 0]`.

Author A (formal recipe voice) writes 1–2. Author B (casual dinner
voice) writes 3–4. Topic also jumps from technique to convenience
food, so this is an *easy* item.

## Step 1 — units and pair count

Four sentences ⇒ three pairs: (1,2), (2,3), (3,4). Any system that
emits four bits has an off-by-one bug.

## Step 2 — features you can count on paper

Ignore character n-grams for a moment. Count tokens by splitting on
whitespace and stripping wrapping punctuation from tokens, but keep
internal apostrophes (`I'm`, `gonna` has none).

### Sentence 1

Tokens: `The, souffle, requires, a, precise, fold, of, the, egg, whites, into, the, batter` (13)

- Contractions: 0
- First person: 0
- Second person: 0
- `!` / `?`: 0
- Function-word-ish: The, a, of, the, into, the (6/13 ≈ 0.46)
- Average word length: souffle(7)+requires(8)+precise(7)+batter(6) pull this up
- Tone: imperative-adjacent but still declarative, Latinate *requires*, *precise*

### Sentence 2

Tokens: `Oven, temperature, should, remain, stable, so, the, structure, can, set` (10)

- Contractions: 0
- Modal *should* / *can*: hedging, instructional
- No first person
- Similar average word length to sentence 1
- Same kitchen-science topic

Pair (1,2) should look *same-style*: both contraction-free, both
mid-length, both third-person / existential, high function-word
overlap (*the*, *should*/*can* auxiliaries).

### Sentence 3

Tokens: `Yeah, I'm, just, gonna, chuck, the, frozen, pizza, in, and, hope, for, the, best` (14)

- Contractions: `I'm` (1+)
- Informal *gonna*, *Yeah*, *chuck*
- First person: `I'm`
- Still no `!`, but the lexicon is a different register
- Content nouns: pizza, not egg whites

### Sentence 4

Tokens: `I'm, not, gonna, overthink, dinner, tonight, seriously` (7)

- Contraction: `I'm`
- Informal *gonna* again
- First person: `I'm`
- Discourse adverb *seriously*
- Shorter than sentence 3, still the same casual register

Pair (3,4) is same author, but the length jump is large (14 vs 7).
A model that *only* looks at length will false-alarm here. That is
why we also keep contraction rate, first person, and informal
lexicon: those stay in the casual cluster.

Pair (2,3) differs on almost every authorial cue *and* on topic.
Even a topic-only model gets this one. A style-only model should
also get it (contractions appear, *Yeah*/*gonna*, first person).

## Step 3 — sketch of |a − b| for three cues

Rough rates (not the library's exact tokenisation — see example 5
for the programmatic numbers):

| Cue | s1 | s2 | s3 | s4 | \|s2−s3\| | \|s3−s4\| |
|-----|----|----|----|----|-----------|-----------|
| contraction_rate | 0 | 0 | ~0.07 | ~0.14 | onset from 0 | both casual |
| first_person | 0 | 0 | >0 | >0 | onset from 0 | both casual |
| n_words | 13 | 10 | 14 | 7 | small | large |

The change pair is not the one with the biggest length gap. That is
the whole lesson. Length is a feature, not the task.

## Step 4 — what a majority-0 baseline does

It predicts `[0, 0, 0]`. Accuracy 2/3, positive-class F1 = 0,
macro F1 = 0.5 if class-0 F1 is 0.8 and class-1 F1 is 0 — or
exactly 0.4 / 0.5 depending on rounding. Either way it did not
find the splice. Macro F1 exists to make that visible.

## Step 5 — reconstruct author runs from `changes`

Start `author = 1` at sentence 1. For each bit, keep the same
author on `0` and increment on `1`:

```
changes [0, 1, 0]
runs    A, A, B, B
```

`authors` in the truth file is 2, which matches. If the file had
said `"authors": 3` it would be inconsistent and the loader would
reject it.

## After you run the library

`python examples/05_hand_features.py` prints the *actual* pairwise
vector slice for this document. Use it to check that casual-register
onset (contraction / first person leaving zero) is pair (2,3), while
`n_words` moves most on pair (3,4). The worked example and the code
are meant to disagree only in rounding, not in story.
