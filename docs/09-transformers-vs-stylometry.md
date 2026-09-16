# What to say about transformers

You will be asked whether you should have fine-tuned BERT. A grown-up
answer has three layers.

## Yes, they work

PAN 2023 systems that fine-tuned transformers on paragraph *pairs*
did well, especially when they also augmented data. A pair classifier
is a natural fit: the label is defined on `(paragraph_i, paragraph_{i+1})`.
You can concatenate the two paragraphs with a separator token and
train a binary head.

## They do not retire stylometry

Transformers are excellent topic models. That is the same sentence as
"they will ace the easy band." On the hard band you still need to
ask whether the model is using *shall* vs *will* or just a faint topic
drift the annotators failed to kill.

A feature-based baseline is how you prove that the neural net is doing
more than cosine-on-nouns. It is also how you debug a document in an
oral: you can point at a contraction rate. You cannot point at
dimension 387.

## Cost and exam honesty

This repository is a study kit. It has no GPU story and no hidden
PAN dump. If you built a transformer for the actual course project,
you would still owe:

- a stylometric baseline
- a threshold or decision rule
- easy / medium / hard scores
- an error analysis that includes a same-topic miss and a
  same-author false alarm
- a note on data (licence, whether extra Reddit was used)

## A pair of sentences that sound like you

> I would use a transformer pair classifier as the production model
> and keep function-word Delta plus character 3-grams as the explainer
> and the sanity baseline. If the neural net beats the baseline only
> on the easy split, I do not get to say I solved style change.

That is the whole section. Do not pretend you implemented RoBERTa in
this repo.
