# What the exam asks

A document arrives as an ordered list of units. In the PAN 2025 framing
those units are **sentences**. In earlier editions they were often
**paragraphs**. The exam question is the same either way:

> For each boundary between consecutive units, did the author change?

You do **not** name the authors. You do **not** get a reference folder
of known writing. You only see the document in front of you. That is
why the task is called *intrinsic*.

## Three numbers you must keep straight

For a document with \(n\) units there are exactly \(n-1\) boundaries.
The gold file stores those boundaries as a binary array called
`changes`. A `1` at index \(i\) means the author of unit \(i+1\) is
not the author of unit \(i\).

The number of authors is *not* `sum(changes)`. It is `1 + sum(changes)`
only if every change introduces a *new* author. Real documents can
return to an earlier writer. The teaching corpus marks both patterns.

## What "style" is allowed to mean

Style, for this exam, is a habit that survives a topic change:

- closed-class words (`of`, `however`, `you`)
- punctuation and contraction rate
- sentence length and hedging
- character n-grams that encode spelling and spacing

Style is **not**:

- the nouns that name the topic
- a single rare word
- a heading, a URL, or a number that any author would copy

If your detector lights up because the text moved from bicycles to
vellum, you have a topic detector. Easy documents reward that shortcut.
Hard documents punish it. The oral will ask you which one you built.

## Difficulty tiers (teaching version)

The shared task publishes Easy / Medium / Hard splits that control how
much topic moves with authorship. This repo copies the *idea*, not the
data.

| Tier | What moves | What you should trust |
| --- | --- | --- |
| Easy | Topic and register together | Register still has to move; topic alone is a cheat |
| Medium | Same domain, different register | Function words, punctuation |
| Hard | Same topic, close registers | Closed-class + n-grams; expect misses |
| Control | Nothing labelled as a change | False-alarm rate |

The takeaway sentence for the oral: **a system that only works on Easy
has not shown that it can see style.**

## What a complete answer looks like

A mark-winning answer does four things:

1. States the I/O contract (`n` units → `n-1` bits).
2. Names the features and why they are (or are not) topic-resistant.
3. Names the decision rule (fixed cut, adaptive cut, CUSUM, ensemble).
4. Reports **macro-F1**, not accuracy, and explains one miss with the
   error taxonomy in [10-error-taxonomy.md](10-error-taxonomy.md).

"We fine-tuned a transformer" is not an answer unless you can say what
the model is using as a cue and how you would tell topic from register.
