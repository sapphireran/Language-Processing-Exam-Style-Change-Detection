# Stylometric features

Style features are measurements that should stay put when the topic
changes and jump when the writer changes. The catalogue below is exactly
the vector `stylechange.features.extract_sentence` returns. Every name is
stable: scripts, tests, and the `explain` command all use this list.

## Design rules

1. **Closed class over open class.** Prefer pronouns, articles, hedges, and
   punctuation. Do not count *kettle* or *coral*.
2. **Rates, not raw counts**, except for length itself. A 40-word sentence
   will have more commas; comma *rate* is the comparable quantity.
3. **No external lexicon beyond a short in-file list.** Function words,
   hedges, intensifiers, and a handful of Latinate suffixes live in
   `features.py`. Nothing is downloaded.
4. **Deterministic.** Same sentence → same vector. No sampling, no
   contextual embeddings.

## Feature catalogue

### Length and rhythm

| Feature | What it measures | Why it is stylistic |
| --- | --- | --- |
| `char_count` | Characters including spaces | Mira writes long; Hale writes short |
| `word_count` | Whitespace tokens | Primary scale feature |
| `avg_word_len` | Mean token length | Latinate vs Germanic vocabulary |
| `std_word_len` | Spread of token length | Mixed register vs monotone jargon |
| `long_word_rate` | Share of tokens with ≥6 letters | Academic / technical |
| `short_word_rate` | Share of tokens with ≤3 letters | Casual function-word rain |
| `type_token_ratio` | Unique / total tokens | Repetition habit (unstable on very short sents) |
| `hapax_ratio` | Hapax / tokens | Same caveat as TTR |

Length is the strongest *cheap* signal in the synthetic set because the
four house authors were written with different breath. It is also the
first feature to fail when a single author writes a heading and then a
paragraph. Treat it as necessary, not sufficient.

### Punctuation and orthography

| Feature | What it measures |
| --- | --- |
| `punct_rate` | Punctuation characters / chars |
| `comma_rate` | Commas / words |
| `semicolon_rate` | Semicolons / words — Nell’s tell |
| `colon_rate` | Colons / words — Hale’s lists |
| `question_rate` | `?` / words |
| `exclamation_rate` | `!` / words — Jules |
| `paren_rate` | Round brackets / words |
| `quote_rate` | Quotation marks / words |
| `dash_rate` | Em/en/hyphen dashes / words |
| `uppercase_rate` | Capitalised tokens / words |
| `digit_rate` | Digit characters / chars |

Punctuation is closer to motor habit than to topic. A writer who likes
semicolons will keep liking them on any subject. Quoted speech is the
trap: the *quoted* punctuation may belong to someone else.

### Function words and stance

| Feature | Closed class |
| --- | --- |
| `function_word_rate` | articles, auxiliaries, prepositions, pronouns, conjunctions |
| `first_person_rate` | I, me, my, mine, we, us, our, ours |
| `second_person_rate` | you, your, yours |
| `third_person_rate` | he, she, they, it, his, her, their, … |
| `article_rate` | a, an, the |
| `hedge_rate` | however, perhaps, somewhat, relatively, suggest, appear, … |
| `intensifier_rate` | very, really, extremely, quite, pretty |
| `coord_conj_rate` | and, but, or, nor, yet, so |
| `subord_marker_rate` | because, although, while, if, unless, whereas, since |
| `contraction_rate` | tokens containing `'` that look like `n't`, `'re`, `'ll`, … |

These are the features you should name first in an oral exam. They are
topic-resistant and they separate the house authors cleanly:

- Mira hedges and subordinates.
- Jules contracts and uses first person.
- Hale drops pronouns and writes *was measured*.
- Nell coordinates with dashes and semicolons, not hedges.

### Morphology and register

| Feature | Heuristic |
| --- | --- |
| `nominalization_rate` | tokens ending in `-tion`, `-sion`, `-ment`, `-ness`, `-ity` |
| `ly_adverb_rate` | tokens ending in `-ly` (with a tiny stoplist: *only*, *really*) |
| `passive_be_rate` | `be`/`been`/`being`/`is`/`are`/`was`/`were` near a `ed`/`en` token |
| `latinate_rate` | tokens with `-ate`, `-ive`, `-ous`, `-ence`, `-ance` |
| `avg_syllables` | vowel-group count per word |
| `flesch_reading_ease` | `206.835 - 1.015(words/sents) - 84.6(syllables/words)` |

The Flesch number on a *single* sentence is a stretched use of a
paragraph-level formula. It is included because exams still ask for it,
and because the relative ordering (Hale high / Mira low) is stable even
when the absolute number is meaningless.

## Pairwise transformation

A detector almost never classifies a sentence in isolation. For sentences
with vectors \(x_i, x_{i+1}\) the default pair map is

\[
d_i = |x_i - x_{i+1}|
\]

Optional concatenations live in `stylechange.pairwise`:

| Name | Vector | Use |
| --- | --- | --- |
| `absdiff` | \(\|x_i - x_{i+1}\|\) | Default; scale-sensitive |
| `signed` | \(x_i - x_{i+1}\) | Order-aware; rarely better |
| `stack` | \(x_i \oplus x_{i+1} \oplus \|x_i-x_{i+1}\|\) | Logistic, more parameters |
| `cosine_distance` | \(1 - \cos(x_i, x_{i+1})\) | Unsupervised / threshold |

Standardize columns on the *training pairs* before logistic regression.
The unsupervised detector instead standardizes *within the document* so
that a long-winded document does not explode every distance.

## Features you should not reach for first

- TF–IDF unigrams of content words (topic leakage)
- Named entities (topic leakage)
- Document embeddings from a general LM (work, but hide the mechanism)
- Type-token ratio on sentences shorter than ~8 tokens (noise)

If an exam question gives you two sentences about the same kettle and asks
which feature would fire, pick `contraction_rate`, `semicolon_rate`, or
`first_person_rate`, not `word_count` alone and not *kettle*.
