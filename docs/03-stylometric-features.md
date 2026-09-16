# 3. Stylometric features

Style-change detection lives or dies on what you measure in each unit.
This note is the catalogue implemented in `scd.features` and the reason
each group exists. It is also the answer key for "list features that are
more authorial than topical".

## Authorial vs topical (the exam cut)

**More authorial (relatively stable across topics)**

- Function-word frequencies (*the, of, and, to, in, that, which, …*)
- Pronoun and contraction habits
- Punctuation rates and preferred sentence length
- Character n-gram profile (captures apostrophes, British/American
  spelling crumbs, and morphology without meaning the words)
- Type-token behaviour and short/long word mix

**More topical (dangerous on easy data, useless on hard data)**

- Content-word bag-of-words
- Named entities and rare nouns
- Embeddings of "what the sentence is about"
- Topic-model posteriors

A feature is not *purely* one or the other. Average word length moves
when you switch from "cat sat" to "photosynthesis". The point is
*relative* stability. On the hard band we try to keep topic fixed so
that leftover performance is closer to style.

## Unit-level scalar features

For a unit `u` the extractor computes a fixed-width vector. Pairwise
classification then uses differences and similarities, not the raw
vector of a single sentence alone.

### Length and richness

| Feature | Definition | Why it is style-ish |
|---------|------------|---------------------|
| `n_chars` | Character count | Some writers pack clauses; others don't |
| `n_words` | Whitespace tokens | Classic length habit |
| `avg_word_len` | Mean token characters | Latinate vs Germanic vocabulary |
| `short_word_rate` | Share of tokens with length ≤ 3 | Function-word heavy prose |
| `long_word_rate` | Share of tokens with length ≥ 7 | Academic / technical voice |
| `ttr` | `types / tokens` | Vocabulary diversity (unstable on very short units) |
| `hapax_rate` | Hapax legomena / tokens | Same caveat as TTR |

**Exam caveat.** TTR and hapax rates are **length-sensitive**. Two
writers with the same vocabulary will show different TTR if one writes
8-word sentences and the other writes 24-word sentences. Always
interpret them next to `n_words`, or use a length-robust alternative
(for example, average TTR over a sliding window of fixed token count).
On sentence-level data, treat TTR as a weak, noisy feature.

### Orthography and symbols

| Feature | Definition | Typical author habit |
|---------|------------|----------------------|
| `upper_rate` | `A-Z` / letters | Shouting, acronyms, title case |
| `digit_rate` | Digits / chars | Procedural / technical writers |
| `punct_rate` | Punctuation / chars | Dense vs bare sentences |

These are cheap and surprisingly useful once topic is controlled.

### Punctuation profile

Separate rates per character, each normalised by character count:

`comma`, `semi`, `colon`, `dash`, `qmark`, `exclaim`, `paren`, `quote`

Writers differ more in *how* they punctuate than in whether they know
the rules. Casual voices lean on `!`. Academic voices lean on `;` and
hedged commas. Technical voices use parentheses for asides and digits.

### Closed-class lexicon

A fixed list of function words is counted and divided by token count.
The list is in `scd.features.FUNCTION_WORDS`. It includes determiners,
prepositions, auxiliaries, common adverbs, and a few complementizers.

Why function words?

1. They are frequent, so a short unit still has a few.
2. Speakers are rarely aware of them, so they are hard to fake.
3. They are almost topic-invariant: you need *the* and *of* whether
   you are talking about bread or bytecode.

We also bucket:

- `first_person_rate`: I, me, my, mine, we, us, our, ours
- `second_person_rate`: you, your, yours
- `contraction_rate`: tokens containing `'` that match `n't, 're, 've, 'll, 'd, 'm, 's`

A formal synthetic author in this repo is forbidden contractions and
almost forbidden first person. A casual author does the opposite. That
is an exaggerated teaching device; real authors are milder.

## Pairwise features (what the classifier actually sees)

Let `a = f(u[i])` and `b = f(u[i+1])`. The pairwise vector is:

1. `|a - b|` — absolute difference of every scalar
2. `a + b` is *not* used (that would encode "how long is this region",
   which is not a change signal)
3. Cosine similarity of character 2-gram and 3-gram distributions
4. Jaccard similarity of the lowercase word sets
5. Length ratio `min(n_words_a, n_words_b) / max(...)`
6. Function-word cosine between the two closed-class histograms

The classifier is asked "how *different* are these two units?", so
symmetric features are appropriate. If you concatenated `[a; b]` you
would also let the model learn "the second sentence is casual, so this
is a change" — that can work on a tiny author set and fail when a new
casual author appears in second position. Absolute differences
generalise better.

### Character n-grams

For each unit, count character n-grams (letters, digits, punctuation,
spaces folded to a single space). L2-normalise. Cosine near 1 means
the two units "look like the same keyboard habits". This quietly
captures:

- British *-ise* vs *-ize*
- Apostrophe density
- `...` vs `.`
- Preferred capitalisation after commas (rare, but real)

Character n-grams are more robust than word unigrams on short
sentences because a 12-word sentence still has dozens of bigrams.

### Jaccard of words

```
|set(a) ∩ set(b)| / |set(a) ∪ set(b)|
```

On easy data this is a topic detector. On hard data it stays high
across a change (same nouns) and should *not* dominate. The trained
linear model can down-weight it if the hard band is in the training
mix. If you train only on easy data, Jaccard will hog the weights.
That is the experimental punchline of `examples/04_compare_difficulties.py`.

## What we deliberately do not implement

- POS tags and dependency trees (would need a tagger and a model file)
- BERT / DeBERTa pair classifiers (download, GPU, topic leakage)
- PMI function-word graphs, writeprints, or full Burrows' Delta
- Character 4-grams and spelling-error rates (useful, but diminishing
  returns on a toy corpus)

Burrows' Delta is worth knowing for the exam: it z-scores function-word
frequencies against a corpus mean and takes a Manhattan/Euclidean
distance between documents. It is an *extrinsic* nearest-author method.
You can fake a Delta-like pairwise score by z-scoring function-word
diffs against the training set; the library's function-word cosine is
the lightweight cousin.

## Feature hygiene

- Lowercase before word features; keep case for `upper_rate`.
- Do not strip punctuation before the punctuation profile.
- Empty units (can happen after a bad split) return a zero vector plus
  similarities of 0, not a crash.
- Do not TF-IDF content words and then claim you have a style model.

If you add features, add a test that they are finite, named, and of
fixed dimension. Pairwise dimension is part of the model contract.
