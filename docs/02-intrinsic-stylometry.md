# Intrinsic stylometry

## Fingerprint, then compare

Every intrinsic method, neural or not, does the same two things:

1. Turn a span of text into a **style fingerprint**.
2. Decide whether two fingerprints are close enough to be one author.

The span here is a paragraph. That is short. Short spans are why
student systems overfit to topic and why function words matter: you
need features that fire often enough to be estimated from 40–80 tokens.

## Three feature families (name them)

**Lexical.** Character n-grams, word lengths, vocabulary richness
(TTR, hapax), contractions, digits. Character 3-grams are the modern
default because they see morphology (`-tion`, `-ing`), punctuation,
and pieces of function words without a tokenizer argument.

**Syntactic.** POS n-grams, punctuation rates, sentence length,
question rate. This kit fakes POS with suffix bins. Say that out loud
so the examiner knows you know it is a proxy.

**Structural / register.** Pronoun person, discourse connectives,
formality markers, line-breaking habits. These are not "style" in the
literary sense; they are habitual choices that survive a topic change.

Content words are a fourth family and a trap. They measure **topic**.
On the easy PAN split they look like authorship. On the hard split
they go quiet. Lab 07 prints both channels side by side.

## Closed-class words

Function words (`the`, `of`, `however`, `I`, `one`) are frequent,
topic-light, and hard to control consciously. That is the textbook
reason they dominate classical authorship. Burrows's Delta is just
"z-score those frequencies and take the mean absolute difference".

A paragraph of 50 tokens will have many zeros in an 80-word function
list. That sparsity is why we z-score *inside the document* and why
we also keep a coarse register score (contractions, `I` vs `one`).

## Intrinsic vs extrinsic, in one paragraph

Extrinsic authorship uses an external corpus: "here are 50 essays by
each suspect". Intrinsic authorship uses only the document under test.
Style-change detection at PAN 2023 is intrinsic. If you fine-tune
DeBERTa on the *training documents*, you have introduced a corpus —
that is allowed for the shared task, but it is no longer a purely
unsupervised intrinsic method. Be ready to draw that distinction.

## What "unsupervised" means in this repo

`scdkit` never sees gold labels at detection time. Thresholds were
chosen on the bundled examples (a form of cheating you must admit).
A cleaner story is: compute several adjacent distances, take a robust
centre (median), and flag outliers. The ensemble here uses fixed
floors *and* a two-vote rule so a single-author letter with one long
paragraph does not fire just because it is the local z-score maximum.
