# 03 — Feature inventory

I am not allowed a mystery 768-D vector in a closed-book exam. This is
the list I actually use. Every item is a rate or a mean. The code that
matches this page is `examscd.features`.

## The rule I write at the top of the answer book

**Closed-class and shape first. Content last.**

Open-class words (`tokenise`, `raid`, `pasta`) tell me what the text is
about. Closed-class words (`of`, `one`, `we`, `however`) and character
shape tell me how it is written. Style-change detection that leans on
content is topic detection in a cheap suit.

## Family A — character n-grams

I take lowercase characters, pad with a space, and count overlapping
3-grams. Distance is `1 - cosine`.

Why they work on short units:

- they see punctuation (`"e. "`, `"! "`)
- they see morphology (`ing`, `tion`, `n't`)
- they see function-word shapes without a tokenizer argument

Why they fail:

- two writers on the same boilerplate still share 3-grams
- a quoted formula can dominate a short sentence

See [05-ngram-profiles.md](05-ngram-profiles.md).

## Family B — function-word distribution

I keep a closed list of about a hundred English function words and
compute a relative-frequency vector. Distance is L1.

This is the Mosteller–Wallace idea, not their Federalist word list
copied out. The claim I need is: **people differ in how they glue
sentences together**, and glue is reusable across topics.

On the hard study file both writers discuss BPE. Writer 1 leans on
`we` / `this` / `although`. Writer 2 leans on `one` / `may` / `the`.
That is a function-word cut, not a noun cut.

## Family C — the 16-D closed vector

I will recite these if asked to "name features".

| dim | what I count | why it moves at a cut |
| --- | --- | --- |
| mean word length | letters / word | academic vs chat |
| mean unit length | words / sentence or paragraph | recipe vs essay |
| type–token | unique / tokens | repetition, slang |
| function-word rate | closed class / words | glue density |
| punctuation rate | punct tokens / tokens | SMS vs prose |
| digit rate | numbers | lab notes |
| uppercase rate | capitals / letters | shouting, acronyms |
| first person | I/we family | diary, student abstract |
| second person | you family | instructions, chat |
| contraction rate | don't / I'm / gonna | register |
| question rate | `?` / sentence-enders | Socratic vs declarative |
| hedge rate | maybe, perhaps, might | academic caution |
| booster rate | very, really, totally | informal emphasis |
| connective rate | however, therefore, thus | planned prose |
| nominalisation | -tion / -ment / -ness / -ity | academic packing |
| imperative rate | first word in {stir, note, …} | recipes, lab steps |

I normalise most of these into roughly `[0, 1]` so L2 is not dominated
by raw word counts. I do **not** z-score them against a 10,000-document
training set at exam time. On eight sentences the sample σ is a coin
flip.

## Family D — length as a one-D series

Sentence length (word count) is the input to CUSUM. It is a weak
classifier by itself and a strong **picture**. See
[04-cusum-and-windows.md](04-cusum-and-windows.md).

## What I will not put in the inventory unless they ask

- POS n-grams (need a tagger; I will describe them, not implement them)
- constituency rewrites (classic, expensive, good oral colour)
- punctuation *sequences* as a separate graph feature
- transformer CLS cosine (works; I must then talk about topic)

## How I combine them

Adjacent pair score in `examscd`:

```
d = 0.42 * char3_cosine_dist
  + 0.28 * clip(func_L1 / 1.4)
  + 0.20 * clip(style_L2 / 1.1)
  + 0.10 * |len1 - len2| / max(len1, len2)
```

Then a CUSUM hit adds a small bonus. Then a gap heuristic with an
absolute floor. I can write those four weights on the board and defend
them as "n-grams first, function words second, toy extras last".
I will not pretend they were grid-searched on PAN.

## Short-document warning I will underline

A six-word SMS has almost no 3-gram mass. A forty-word academic
sentence has plenty. Pair scores are **not calibrated across lengths**.
That is why the absolute floor exists, and why I still miss polite
academic-to-academic cuts when both writers are careful.
