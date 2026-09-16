# 03 — Feature families

Short paragraphs starve statistics. Every feature below is chosen
because it still moves on 60–90 words, and because you can explain it
without a GPU.

## 1. Function-word frequencies

A closed list of ~160 items (`the`, `of`, `i`, `however`, …). Each
paragraph becomes a relative-frequency vector in that basis.

Why they are style:

- they are hard to copy deliberately;
- they are weakly coupled to topic (not zero — "I" vs "the analysis"
  still correlates with genre);
- Mosteller and Wallace already used them on the Federalist papers.

Distance: cosine, Jensen–Shannon, or Burrows's Delta (mean absolute
z-score difference across the function-word dimensions).

On paper, drop to a handful of dimensions (`i`, `the`, `that`,
`should`, `a`, `as`) and compute cosine on that subset. The lab's
worked example does exactly this.

## 2. Character 3-grams

Slide a window of three characters across a lowercased,
whitespace-collapsed paragraph. Typical signals:

- `n't`, `'re`, `'ve` (contraction morphology);
- `ing`, `tion`, `ness` (suffix mix);
- ` ;`, `—`, `...` (punctuation);
- British `-our` vs `-or` if it ever appears.

Character n-grams survive OCR noise and do not need a tokeniser that
agrees with anyone else. They also pick up topic (`bee`, `ink`,
`gym`), which is why they are strong on easy data and slightly dirty
on hard data.

## 3. Lexical richness

Raw type-token ratio `V/N` collapses on short texts because `V`
cannot exceed `N`. Use length-adjusted cousins:

| Statistic | Formula | Intuition |
| --- | --- | --- |
| Guiraud's R | `V / sqrt(N)` | TTR with a softer length penalty |
| Hapax ratio | `V1 / V` | fraction of types that occur once |
| Yule's K | `10^4 (Σ i² V_i − N) / N²` | 0 if every word is unique; grows with repetition |
| Honoré's R | `100 ln N / (1 − V1/V)` | undefined / capped when every type is a hapax |

A chatty paragraph that repeats `I`, `the`, `and` will show a larger
K than a dense methods paragraph that barely repeats anything. That
is a style cue, not a quality judgement.

## 4. Rhythm and readability proxies

- mean and std of word length;
- mean and std of sentence length;
- punctuation rates (comma, period, `?`, `!`, `;`, `:`, dash,
  apostrophe);
- syllables per word (a vowel-run heuristic, not a dictionary);
- a Flesch-like linear combination `206.835 − 1.015·ASL − 84.6·ASW`.

The Flesch number in this lab is a *proxy*. Do not quote it as a
published readability score. It exists so an oral answer can say
"sentence length and syllable load jointly shift".

## 5. Register markers (tiny lexicons)

| Lexicon | What it catches |
| --- | --- |
| First / second / third person | diary vs instructions vs report |
| Contractions | `I'm`, `don't`, `can't` |
| Hedges | `perhaps`, `likely`, `suggests` |
| Boosters | `clearly`, `very`, `always` |
| Academic verbs / connectives | `however`, `therefore`, `empirical` |
| Informal residue | `yeah`, `kinda`, `stuff` |
| Imperative hints | `measure`, `avoid`, `rinse` |

These lists are teaching scaffolds. They are not a tagger.

## Dense vector

All of the numeric rates above are concatenated, then z-scored
*within the document* before Euclidean distance is taken. Document-level
z-scoring is important: a globally "formal" document should not flag
every pair just because both paragraphs are formal. You care about
*jumps*.

## What must not vote

Content-word Jaccard:

```
distance = 1 − |A ∩ B| / |A ∪ B|
```

where `A`, `B` are lowercased tokens after dropping the function-word
list. On easy documents this distance spikes at the same places as
authorship. That is leakage. `scarfjoint detect --explain` always
prints `topic-distance=… (not a vote)`. Pass `--use-topic` only when
you are demonstrating the leak.

## Ensemble used here

```
combined =
    0.28 · cosine_dist(function words)
  + 0.22 · cosine_dist(char 3-grams)
  + 0.18 · scaled Euclidean(dense z-vector)
  + 0.14 · scaled JS(function words)
  + 0.10 · scaled Burrows Delta
  + 0.08 · zlib NCD
```

Flag a change if `combined ≥ 0.42`.

Those numbers were swept on the twelve bundled documents. They will
not transfer to PAN. If an examiner asks "why 0.42?", the honest
answer is "it was the threshold that split this teaching set; I would
refit on a validation split of real data."
