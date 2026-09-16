# 06 — Topic as a confound

This is the paragraph that separates a pass from a good oral.

## The leak

If author changes and topic changes at the same time, **any**
representation that notices content will fire at the cut. Bag-of-words,
tf–idf, BERT, a prompt to a chat model: all of them get a free signal
they do not deserve.

The easy study file does this on purpose. Sentences 1–8 are a recipe.
Sentences 9–13 are food chemistry. A topical embedding looks like a
genius. It has noticed `onion` versus `melanoidin`.

## How shared tasks tried to close the leak

Later editions built difficulty bands:

| band | construction I need to remember |
| --- | --- |
| easy | author change often co-occurs with a topic change |
| medium | some topical drift, not a reliable cue |
| hard | units stay on roughly the same subject; style has to do the work |

The hard study file is my pocket version: both halves explain BPE.
If a method needs `tokenise` versus `pasta` to see the cut, it will
fail that file.

## How I test myself

I ask three questions of any feature:

1. Would this feature still move if I replaced every content noun with
   the word `widget`?
2. Would this feature move if I translated the same meaning into a
   more formal register?
3. Would a topical classifier fire here even if one person wrote both
   halves?

Function words, contractions, sentence length, and `we` versus `one`
survive (1). Character 3-grams mostly survive (1) because they lean on
glue and morphology, but they still see distinctive content stems.
Transformer cosine often fails (1) and (3).

## Gift authorship is a topic-controlled problem

A supervisor paragraph grafted onto a student abstract is usually
**about the same project**. That is why `06_gift_abstract` keeps the
subject (the detector) and changes the person and the nouns of
evaluation (`I built` versus `the contribution was to formalise`).
If I detect that cut with a keyword list of NLP terms, I cheated.

## What I write in the limitations paragraph

> Performance on easy data overstates style sensitivity whenever topic
> is allowed to move with authorship. A fair claim needs a same-topic
> split, short units, and a metric that does not reward always
> predicting "no change" on a sparse label vector.

I should be able to say that last sentence from memory.
