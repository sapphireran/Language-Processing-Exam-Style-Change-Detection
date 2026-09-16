# Task 3: From vectors to change points

The detector is unsupervised. It never sees a labelled author during
inference. That matches the exam setting: you are given a document and
asked what you would compute, not which pretrained checkpoint you would
download.

The pipeline is:

```
text → paragraphs → feature matrix X
     → 4-D style axes  (formality, address, rhythm, procedure)
     → adjacent Euclidean distances d_i
     → threshold τ  (floor, optionally raised into the first gap)
     → Task 1 / Task 2 from peaks
     → Task 3 from clustering
```

## Why not cosine on the full z-scored vector?

A closed function-word inventory is the right *linguistic* story and
the wrong *geometry* for a six-paragraph exam document. After
column-wise z-scoring, 100+ coordinates with five or six samples are
almost orthogonal: every adjacent pair looks equally far, including
two paragraphs by the same writer.

That is a point you can score marks for: **high-dimensional distances
need many observations**. Shared-task systems get those observations
from a corpus. A single document does not.

The toolkit therefore keeps the full vector for inspection
(`inspect_features.py`) and detects changes in a 4-D space whose axes
you can name:

| Axis | High when… | Built from |
| --- | --- | --- |
| **formality** | connectives, semicolons, no chat | `+infer +contrast +semicolon −contraction −person −casual −? −!` |
| **address** | the writer talks to someone | first person + second person + `?` + `!` |
| **rhythm** | sentences run long | words per sentence / 20 |
| **procedure** | lists, steps, numbers | colon rate + digit rate |

Weights are teaching defaults, not estimated parameters. Changing them
is a legitimate criticism.

## Euclidean distance on the axes

For paragraphs `i` and `i+1` with style vectors `u` and `v`:

```
d_i = ‖u − v‖₂
```

Euclidean is the right default in 4-D: the axes were scaled to be
roughly comparable, and a jump on formality should look like a jump.
Cosine on the same 4-D vectors is a valid alternative (it ignores how
*far* a paragraph sits from the origin). Adjacent distances still
ignore the rest of the document — correct for localising a cut,
incomplete for a returning author.

## Choosing a threshold

A fixed floor (`d_i ≥ 0.75`) is easy to explain and is the fallback.
When the sorted distances show a gap that *leaves* the below-floor
cluster, the detector raises `τ` into that gap:

```
sort d
find the first gap with  d_(k) < floor ≤ d_(k+1)  and  gap ≥ min_gap
τ = max(floor, midpoint of that gap)
```

Using the *largest* gap instead is a common mistake. In a three-author
document one cut can be much larger than the other; the largest gap
then sits among the already-large distances and the weaker cut is
lost. The implementation only looks at the jump out of the small
cluster.

You should be able to attack this choice:

- The floor is a magic number tuned on the study texts.
- A single-author document whose internal jitter crosses 0.75 will
  false-trigger; the casual study file is written to stay under it.
- A supervised model could replace `τ` with a classifier on
  `(d_i, local context)`.

## Task 1 and Task 2 from the same peaks

`changes[i] = (d_i ≥ τ)` is the Task 2 prediction: a style change after
paragraph `i`.

Task 1 is then almost free: `multi_author = any(changes)` or more than
one cluster. The extra cluster check exists for the rare case where
clustering splits the document without an adjacent peak (for example
two interleaved styles with moderate adjacent distances). On the study
texts this path is uncommon; it is there so the three tasks cannot
contradict each other silently.

## Task 3: blocks versus clusters

Walking the change vector produces contiguous author blocks:

```
A A A | B B B   →  0 0 0 1 1 1
```

That is sufficient when authors write in one stretch each. It fails on
`A A B B A`: the last block would be labelled `2` even though it
belongs with the first.

Average-linkage agglomerative clustering on the same Euclidean style
space compares every pair of paragraphs, not just neighbours. Clusters
merge while the average inter-cluster distance stays `≤ τ`, then stop.
If clustering finds *fewer* authors than the block walk (and more than
one), the document has a returning style and those labels are kept.
`examples/documents/mixed_return_author.txt` is the unit test for that
sentence.

Average linkage is a teaching default. Single linkage chains; complete
linkage splits elongated groups. Either alternative is a valid short
essay paragraph.

## Other methods you should be able to name

If a question asks for alternatives to adjacent distance, these are the
standard names:

- **Sliding windows.** Compare the left `w` paragraphs to the right `w`
  paragraphs with a divergence (Jensen–Shannon on term distributions,
  cosine on features). Smoother than a single-paragraph pair; worse at
  placing the exact cut.
- **CUSUM.** Project each paragraph onto the first principal direction
  of `X`, then look for a change in the cumulative sum. Classic in
  statistical change-point detection.
- **Bayesian change points.** A generative model over segment lengths
  and per-segment multinomials. Heavier, more principled.
- **Supervised sequence models.** Paragraph embeddings into a
  BiLSTM-CRF or a transformer that predicts a boundary tag.
  State-of-the-art on large labelled sets; opaque in a closed-book
  exam unless you only need the architecture name.
- **Text segmentation algorithms** (TextTiling, C99, topic Tiling).
  They optimise topical cohesion. Mention them to show you know why
  they are the wrong tool if the topic is held constant and the *writer*
  changes.

## Confounds the method cannot see

Write at least two of these if asked for limitations:

1. **Topic shift with one author.** Content leaks into some scalar
   features (`chars_per_word`, a few suffixes). A single author who
   switches from a narrative example to a definition block can trigger
   a false cut.
2. **Quoted material.** A paragraph of dialogue is a second voice by
   definition, but it is not a second author of the document.
3. **Length.** Short paragraphs have unstable rates. The code skips
   them; a shared-task submission would have to decide whether skipping
   is allowed.
4. **Language mixing and editing.** Machine translation and aggressive
   copy-edit can erase personal function-word rates.
5. **Threshold transport.** `floor = 0.75` will not travel to a new
   feature set or a new set of axis weights without retuning.

The honest one-sentence summary: this detector makes style *geometry*
visible. It does not understand writing.
