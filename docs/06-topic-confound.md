# Why topic is a confound

A confound is a variable that correlates with the label and with the
features, so you can "solve" the label without measuring the thing you
claimed to measure.

In style-change detection the usual confound is **topic**.

```text
author A, lighthouses  -->  author B, tax law
```

Almost every open-class feature jumps. Character n-grams jump because
the named entities change. Even some function words jump because
expository tax prose uses `the` and `of` at different rates than a
travel paragraph. You can get a high easy-band F1 and still have a
system that cannot see authorship.

The 2023 hard band exists to punish that shortcut: every paragraph is
about the same thing. If your F1 collapses from easy to hard, you
were riding topic.

## A demo you can run

`examples/07_topic_confound.py` builds two toys:

1. **Same author, new topic.** One voice describes a balcony tomato
   plant, then the same voice describes a delayed train. Gold label:
   no change. A topic-sensitive model wants to fire.
2. **New author, same topic.** Two voices describe the same balcony
   tomato. Gold label: change. A topic-sensitive model wants to sleep.

A system that is actually measuring style should be quieter on (1)
than on (2). `splicefind`'s ensemble is not perfect; the script prints
the scores so you can talk about residual leakage.

## Practical hygiene

- Prefer closed-class rates and punctuation over nouns.
- If you use embeddings, report easy and hard separately.
- If you augment training data, do not only splice unrelated Reddit
  threads. That recreates the easy band.
- When you write synthetic exam documents, keep a same-topic pair and
  a same-author topic shift in the corpus on purpose.

The oral one-liner:

> Topic change is evidence of *a* change. It is not evidence of an
> *author* change unless I have shown the system still works when the
> topic is held still.
