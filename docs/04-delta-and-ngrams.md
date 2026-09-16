# Delta and character n-grams

Two classic tools, used here as **pairwise distances** rather than as
attribution engines.

## Burrows' Delta

Original setting: a questioned text and several author profiles, each
profile a vector of relative frequencies for a fixed list of function
words. Z-score each frequency using the mean and standard deviation
across authors. Delta is the mean absolute difference between the
questioned z-vector and a candidate z-vector. Smaller Delta means
"closer writer".

Exam adaptation:

1. Treat the paragraphs of *this* document as the population.
2. Z-score each function-word rate across those paragraphs.
3. Delta between paragraph `i` and `i+1` is the mean absolute
   difference of their z-vectors.
4. A large Delta is evidence for a seam.

This is not historically pure Burrows (he compared a text to authors,
not a paragraph to its neighbour). Say that out loud. The algebraic
object is the same; the experimental design is local.

### Why z-score?

Without z-scores, `the` dominates because it is frequent. After
z-scoring, a rare-but-stable habit (`upon`, `shall`, `one`) can outvote
a noisy swing in `the`. Inside a four-paragraph document the z-scores
are rough. That is acceptable for a demo and a reason to prefer more
paragraphs at training time.

## Character n-grams

A character 3-gram profile is the L1-normalised multiset of every
window of three characters, including spaces. Cosine distance between
adjacent profiles is the n-gram channel in `splicefind`.

Why they work on short text:

- There are more character trigrams than words, so the histogram is
  denser.
- They encode punctuation (`n. `, `! I`) and morphology (`ing`, `n't`)
  without a tokeniser argument.
- They survive some topic change because function-word skeletons
  (` the`, ` and`, ` to `) still fire.

Why they fail:

- They happily latch onto a repeated named entity. If both authors
  discuss *Copenhagen* the trigrams `cop`, `ope`, `pen` become a false
  "same author" glue. That is a topic confound in n-gram clothing.
- Very short paragraphs produce unstable profiles. A three-word note
  has almost no 3-gram mass.

## How the ensemble uses them

Default blend in `splicefind.detect` (then a **document-relative** cut):

| Channel                         | Weight | Job                          |
|---------------------------------|--------|------------------------------|
| bounded register gap            | 3.00   | pronouns, stance, sentence length |
| function-word Delta             | 0.15   | closed-class habit           |
| char-3gram *excess* over 0.45   | 0.40   | morphology and punctuation   |
| CUSUM slope gap                 | 0.05   | weak sequential hint         |

Z-scored cosine on a four-paragraph document makes every pair look
far in high dimension. The kit therefore scores a handful of rates
that already live in `[0, 1]`, and it marks a boundary if the blend
is an intra-document outlier (median + MAD) or above an absolute
floor. The weights are study choices. An oral answer that says "I
would sweep them on a development split" is better than an answer
that pretends 3.00 was derived from theory.
