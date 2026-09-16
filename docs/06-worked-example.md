# Worked example: `mixed_formal_casual.txt`

The file has six paragraphs. The first three are a lecture voice. The
last three are a chatty voice. Gold labels:

```
authors  = [0, 0, 0, 1, 1, 1]
changes  = [false, false, true, false, false]
```

This page is the walk-through you would put on a whiteboard. The
numbers below are the *kind* of quantities the code prints; re-run
`style-change evaluate` if you need the exact floats after a parameter
change.

## Step 1 — split

`split_paragraphs` sees blank lines and yields six `Paragraph`
objects. Each stores sentences, alphabetic words, and surface tokens.
No paragraph in this file is below `min_words=8`, so all six are
scored.

## Step 2 — features you can see without a computer

Read the first sentence of paragraph 0 and of paragraph 3:

- P0: "Style change detection asks whether a document remains
  stylistically homogeneous..."
- P3: "Okay but that's the textbook version..."

Before any vector is computed you can already name the contrast:

| Cue | Formal block | Casual block |
| --- | --- | --- |
| Contractions | almost none | `that's`, `I'm`, `won't` |
| Person | none | `I`, `you`, `my` |
| Sentence length | long, subordinated | short, fragmented |
| Discourse | `First`, `Second`, `Third` as structure | `Okay`, `Look`, `Really` |
| Questions | none | several |

That table *is* the model. The feature extractor just turns each row
into a rate.

## Step 3 — full vectors, then four axes

Each paragraph still becomes the long closed-class vector (see
`feature_names()`). That table is what `inspect_features.py` prints.

Detection does **not** cosine-compare those rows. Six paragraphs cannot
support a 100-D z-scored geometry; every pair looks far. The detector
projects onto four named axes and compares those:

- formal blocks sit near formality ≈ 0, address ≈ 0, rhythm ≈ 0.8
- casual blocks sit near formality ≈ −1, address ≈ 0.1, rhythm ≈ 0.5

The projection is a weighted sum, not a learned embedding. You can
write the weights on an exam paper.

## Step 4 — adjacent distances

Five gaps, five Euclidean distances in that 4-D space. The teaching
shape (and the numbers this file currently produces) is:

```
d ≈  [ 0.39,  0.59,  1.24,  0.20,  0.24 ]
         P0-P1 P1-P2 P2-P3 P3-P4 P4-P5
```

The floor is 0.75. The first gap that leaves the below-floor cluster
sits between 0.59 and 1.24, so `τ` rises to about 0.91. Only the
formal→casual cut clears it.

Task 2 therefore marks a change after paragraph 2. Task 1 is true.
Task 3 walks the flags and produces `0 0 0 1 1 1`. Clustering agrees;
there is no returning author to recover.

## Step 5 — explain the LARGE gap

`inspect_features.py` ranks coordinates by absolute z-score
difference between P2 and P3. Expect some of:

- `contraction_ratio`
- `first_person` / `second_person`
- `discourse_casual`
- `question_per_word`
- `words_per_sentence`
- a few function words (`fw_i` is not in the list because `I` is
  handled via the person bucket; `fw_you`, `fw_but`, `fw_that` often
  appear)

If the top features were instead topical nouns, the example would be
invalid: we would have built a topic-segmentation toy and called it
style. These texts were written to keep the topic (the SCD problem
itself) stable while the register flips.

## Step 6 — score

Against the gold file:

- Task 1: one binary, should be a true positive
- Task 2: five binaries; the only true change is gap 2
- Task 3: ARI = 1 and BCubed F1 = 1 if the predicted partition is
  `{0,1,2}` vs `{3,4,5}`

A miss of one adjacent formal/casual pair usually means the threshold
floor is too high or a paragraph was skipped. A false cut inside the
formal block usually means a short or list-like paragraph survived
`min_words`.

## What to try next

1. Run the same steps on `mixed_return_author.txt`. Task 2 still wants
   two peaks; Task 3 wants *two* ids, not three.
2. Run `single_author_formal.txt`. Distances should stay below `τ`.
3. Delete the third formal paragraph and re-evaluate: Task 2 still has
   one gold cut, but the z-scores change because the formal class now
   has less mass. That is a useful reminder that within-document
   standardisation is document-dependent.

Commands:

```bash
style-change evaluate examples/documents/mixed_formal_casual.txt \
    examples/documents/labels/mixed_formal_casual.json
python examples/inspect_features.py examples/documents/mixed_formal_casual.txt
```
