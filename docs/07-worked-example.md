# Worked example: bikes then vellum

Document `examples/documents/02_easy_bikes_then_vellum.txt` has four
paragraphs, gold `changes = [0, 1, 0]`.

## What you should see without a computer

- P1–P2: first person, contractions (`don't`, `I'd`), short
  sentences, concrete commute nouns.
- P3–P4: `however`, `consequently`, `one must`, long sentences,
  conservation vocabulary, no contractions.
- The only author change is P2→P3. Topic changes there too. This is
  the *easy* case.

## What the kit computes

Run:

```bash
python examples/lab02_feature_table.py examples/documents/02_easy_bikes_then_vellum.txt
python examples/lab03_pairwise.py examples/documents/02_easy_bikes_then_vellum.txt
```

You should see, qualitatively:

- contraction rate high, then near zero
- formality negative / low, then clearly positive
- Delta and char-3g distance small on 1→2 and 3→4, large on 2→3
- topic distance large on 2→3 (bikes vs parchment)

The ensemble needs either one strong channel or two ordinary votes.
On this document several channels fire at the same cut, so the bit is
not a close call.

## F1 on this document

Gold `[0, 1, 0]`. A perfect prediction is F1 = 1. If the system also
flags 1→2 (false alarm):

- TP=1, FP=1, FN=0, TN=1
- P=0.5, R=1, F1 ≈ 0.667

If it misses the real cut and stays silent: gold has one positive, so
R=0 and F1=0.

## The hard twin

Repeat the labs on `04_hard_circadian.txt` (gold `[1, 1, 1]`). The
story you want to tell is: *topic distance stays high for every pair
because the content vocabulary is shared; the votes now come from
`we`/`one`, hedges, and Delta.* If the ensemble drops a boundary
there, that is the honest limitation of a short academic paragraph.
