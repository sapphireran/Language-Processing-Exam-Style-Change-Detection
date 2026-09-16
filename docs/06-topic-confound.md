# Topic is not style

## The 2023 point

Earlier PAN style-change sets were topically diverse. A model could
flag a change because the nouns changed. The 2023 organisers therefore
built three difficulties:

- **Easy.** Neighbouring paragraphs often differ in topic *and*
  author. Topic leakage is rewarded.
- **Medium.** Some topical variety remains, but not enough to sleep
  on.
- **Hard.** Every paragraph is about the same thing. Only style
  should move.

This is the most important conceptual question on the exam.

## How to demonstrate it with this kit

`examples/lab07_topic_confound.py` prints `topic` (content-word
Jaccard distance) next to Delta and formality.

- `02_easy_bikes_then_vellum` — bicycles then vellum. Topic and
  register jump together at P2→P3.
- `09_magnets_kid_vs_paper` — same facts, different audience. Topic
  distance is lower than on the bike/vellum cut; formality still
  jumps.
- `04_hard_circadian` — melatonin, two academic voices. Content words
  overlap; `we` vs `one` and hedge rate carry the decision.
- `01_single_ferns` — new nouns (bathroom, radiator) but one author.
  Topic distance can be high while style channels stay quiet.

## Neural models leak topic too

A fine-tuned transformer is not "pure style". Subreddit jargon, named
entities, and even Markdown leftovers (stripped in 2023, but the
lesson remains) become features. Contrastive paragraph training on
the easy split can become "are these the same thread?". The hard split
is the audit.

## What to do about it

1. Hold topic constant when you invent study documents (circadian,
   rent, magnets).
2. Keep content words out of the *style* vector.
3. Report easy and hard separately.
4. If you use TF-IDF, say what it measures.

Gift authorship (`05_gift_poster`) is a real-world mix: the abstract
and the lab confession share a project and still differ in person,
modality, and contraction rate. That is the example to give if asked
for an application rather than a benchmark.
