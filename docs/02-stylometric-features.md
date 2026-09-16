# Task 2: A closed stylometric inventory

The feature extractor in `src/style_change/features.py` is intentionally
boring. Every coordinate has a name you can write on an exam paper.
There is no learned embedding and no character n-gram hash.

The vector has two blocks:

1. **Scalar rates** — length, richness, punctuation, person, suffixes,
   discourse markers.
2. **Function-word frequencies** — a fixed list of high-frequency
   closed-class items, each stored as count / word count.

Both blocks are *relative frequencies* (or simple functions of
frequencies). Absolute counts would make long paragraphs look different
from short ones even when the writer did not change.

## Length and rhythm

| Feature | What it captures | Typical failure |
| --- | --- | --- |
| `words_per_sentence` | Habitual sentence extent | Lists and headings collapse it |
| `std_words_per_sentence` | Mix of short and long sentences | One-sentence paragraphs make it 0 |
| `chars_per_word` | Latinate vs everyday vocabulary | Technical terms inflate it without a new author |
| `std_chars_per_word` | Mixture of short function words and long content words | Same |

Sentence length is one of the oldest stylometric numbers for a reason:
it is stable for a writer and cheap to compute. It is also the first
thing a quotation or a fragment destroys.

## Lexical richness

Type-token ratio (TTR) is vocabulary size divided by token count. It
shrinks as a text gets longer, so it is a poor document-level feature
and only barely acceptable at paragraph level if the paragraphs are
similarly long.

Hapax ratio (types that occur once / vocabulary) and dislegomena ratio
(types that occur twice) try to describe the shape of the frequency
spectrum. Yule's K summarises that spectrum in one number:

```
K = 10^4 * (Σ i² V_i − N) / N²
```

where `V_i` is the number of types with frequency `i` and `N` is the
token count. Larger K means a more repetitive vocabulary.

Honoré's R emphasises hapaxes:

```
R = 100 * ln(N) / (1 − V₁ / V)
```

Both statistics are noisy below a few dozen tokens. The code returns 0
rather than pretending a 8-word caption has a meaningful richness
score. In an exam essay, write that richness features need a minimum
length and that you would prefer a length-adjusted measure (for example
MTLD) if the paragraphs varied wildly in size.

## Punctuation as a fingerprint

People are surprisingly consistent about commas versus dashes, about
whether they use semicolons at all, and about how often they ask a
question. The extractor stores several punctuation marks as counts per
word, plus a catch-all `punct_per_word`.

Casual example text in this repo is rich in questions and contractions.
Formal text prefers commas and the occasional semicolon. The procedural
third voice uses colons. Those are deliberate teaching contrasts, not
universal laws.

## Person, modality, negation

Pronoun person is a register cue as much as an authorship cue:

- first person (`I`, `we`, `my`) is common in narrative and in the
  casual study texts
- second person (`you`) is common in instructions and in chatty
  explanation
- third person dominates impersonal academic prose

Modals (`can`, `should`, `would`) and negation (`not`, `never`, `n't`)
are included because they are frequent, closed-class, and only weakly
topical. They will not separate two biologists writing lab notes. They
will separate a lecture from a rant.

## Discourse markers

Three tiny lexicons are kept separate so you can see them in
`top_differences`:

- **contrast:** however, although, though, yet, nevertheless
- **inference:** therefore, thus, hence, accordingly
- **casual:** anyway, yeah, kinda, pretty, really, stuff

A real system would estimate these lists from data. For exam study,
named buckets are more useful than a mystery weight.

## Function words

The function-word list is the backbone. Mosteller and Wallace's
Federalist analysis is the historical reference: the rates of `by`,
`from`, `to`, and a few others separated Hamilton from Madison better
than any list of content words.

Properties that make them good SCD features:

- they are frequent, so paragraph-level estimates are not all zero
- writers rarely choose them consciously
- topic changes do not force them the way they force nouns

Properties that make them fragile:

- genre conventions can swamp author signal (a statute versus a letter)
- editing and house style can overwrite personal habit
- translation and heavy copy-editing flatten the rates

Each function word is stored as `fw_<word>`. When two adjacent
paragraphs differ, `FeatureTable.top_differences` will often surface a
handful of these alongside sentence length and contraction rate.

## What was left out on purpose

Character n-grams (especially 3-grams) are strong in attribution
competitions. They are omitted here because they are hard to interpret
in a short oral exam and because they leak topic through fragments of
content words.

POS tags, syntactic production frequencies, and readability indices
would be reasonable extensions. They need a tagger. This toolkit stays
runnable with `numpy` and the standard library so the examples remain
easy to execute.

Learned representations (BERT, style embeddings) can outperform this
inventory on large datasets. They also hide the linguistic story. If a
question asks for a *baseline*, start here and mention contextual
embeddings as a possible second stage.

## Normalisation before comparison

The full matrix is useful for *explanation*:
`FeatureTable.top_differences` z-scores columns so that a 0.04 swing
in contraction rate can outrank a 4-word swing in sentence length.

That same z-scored 100-D vector is a poor *distance* on a document
with five paragraphs (almost every pair is orthogonal). Detection
therefore leaves the full inventory behind and compares a 4-D style
projection instead. See [03-detection-methods.md](03-detection-methods.md).

If a question asks how you would compare two long, labelled collections
rather than one short document, z-score or tf-idf plus cosine on the
function-word block is the classical answer. The unit of observation
then becomes "many documents", not "six paragraphs".
