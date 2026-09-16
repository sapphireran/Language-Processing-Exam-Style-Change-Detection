# Feature atlas

Seamtrace scores a unit with three families. You should be able to
name one feature from each family and one way that feature fails.

## 1. Scalar rates

| Feature | What it notices | How it fails |
| --- | --- | --- |
| Average word length | Latinate vs everyday diction | Topic words (`photosynthesis`) inflate it |
| Type-token ratio | Lexical diversity | Short units make TTR near 1.0 |
| Hapax rate | One-off words | Same short-unit problem |
| Punctuation / comma rate | Clause stacking | Quoted lists |
| `?` / `!` flags | Interrogative or excited register | A single mark dominates |
| Ellipsis rate | Chat / trailing off | Rare, so brittle |
| Digit rate | Patch notes, field notes, recipes | Any measurement-heavy topic |
| Uppercase rate | Headings, shouting, patch keys | `I` in first-person English |
| Pronoun / 1st / 2nd person | Diary vs memo vs explainer | Dialogue |
| Modal rate | Hedging and policy (`should`, `must`) | Tiny counts |
| Hedge rate | Academic caution | Domain lists (`probably` in weather) |
| Contraction rate | Speech-like register | Edited-out by a copy-editor |
| Long-word rate (≥7) | Nominal style | Scientific topic, not author |
| Sentence-initial lowercase | Chat / texting register | Quoted fragments |

Counts (`n_words`, `n_chars`) are stored for diagnostics but **not**
fed raw into the blended distance. A 40-word sentence would otherwise
always look unlike an 8-word sentence, even from the same writer.

## 2. Function-word vector

A closed list of 100 items (`src/seamtrace/lexicon.py`) is counted and
L1-normalised. Cosine distance on that vector is the default
topic-resistant channel.

Why closed-class? Because authors reuse `of` / `however` / `you` on
any subject, while they cannot reuse `vellum` once the topic has
moved on.

Failures:

- Two authors who both write "plain academic" share the same `of`/`the`
  profile.
- A unit with eight tokens cannot estimate 100 bins.
- Translators and heavy editors flatten the signal.

## 3. Character trigrams

`char_ngrams` lowercases, squeezes whitespace, and slides a window of
3. That picks up `n't`, ` —`, `...`, `!!`, British vs American
spacing, and the texture of very short function words.

Failures:

- Topic-specific stems (`photo-`, `circad-`) leak content.
- Code, URLs, and tables are trigram fireworks.

## What this lab does not use

- POS tags (no tagger in the dependency-free kit)
- Parse features
- Type-token curves over a whole novel
- Author-topic LDA

If an exam question asks for "richer features", say what you would
add **and** which leak you would then have to control. A POS
pronoun/noun ratio is a reasonable next step. A bag of all content
lemmas is not.
