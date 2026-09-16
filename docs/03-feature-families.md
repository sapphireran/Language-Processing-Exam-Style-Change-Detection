# Feature families you can defend

`splicefind.features` extracts one vector per paragraph. You do not
need to memorise every name. You need a family, a reason, and a
failure mode.

## Length and rhythm

- Average and standard deviation of word length
- Average and standard deviation of sentence length
- Syllables per word and a Flesch-like score

These are cheap proxies for register. A lab note ("Shed latch. Sticky.")
and a committee minute live in different sentence-length regimes.
They fail when two authors share a house style, or when one author
writes both a list and a paragraph.

## Vocabulary concentration

- Type-token ratio
- Hapax ratio
- Yule's K

Short paragraphs make raw TTR lie: a 12-word paragraph can look
"rich" because almost every token is unique. If you mention TTR in
the oral, immediately say you would length-normalise or refuse to
compare paragraphs of very different sizes. Yule's K is less sensitive
to length because it uses the frequency-of-frequencies.

## Pronoun and address habits

- First person (`I`, `we`, `my`)
- Second person (`you`, `your`)
- Impersonal `one`

This family is the easiest demo in the corpus. A diary paragraph and
an exam-model paragraph about the *same leaky tap* still diverge here.

## Stance markers

- Contractions
- Hedges (`perhaps`, `maybe`, `somewhat`)
- Intensifiers (`very`, `really`, `so`)
- Question and exclamation rates

These are register features. They are not "personality". Do not claim
that hedges mean the author is unsure in real life. Claim that the
**text** suddenly started performing academic caution.

## Punctuation and surface form

- Punctuation rate
- Commas per sentence
- Digit rate
- Upper-case ratio

Useful for notes vs prose, patch notes vs reviews, and minutes vs
chat. Fragile under OCR and under social-media casing.

## Closed-class distribution

The function-word vector is a separate block so it can be z-scored and
fed to Delta. See [04](04-delta-and-ngrams.md).

## What I deliberately left out

- Full POS tags: they need a model and they make the oral longer than
  it needs to be.
- Topic embeddings: they solve the easy band and tempt you to ignore
  the hard band.
- Typeface, layout, timestamps: this is a text-only exam.

If you are asked "which three features would you keep on a desert
island?", a defensible trio is:

1. function-word rates
2. character 3-grams
3. sentence-length mean and variance

That trio covers habit, morphology/punctuation, and rhythm. Everything
else is commentary.
