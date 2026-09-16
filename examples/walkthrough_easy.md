# Walkthrough: Easy

Easy documents let a lazy model cheat with topic *and* let an honest
model succeed with register. The point of this page is to watch both
signals fire at the same boundary.

Gold for `data/easy/problem-001.txt` is `[0, 1, 0]`.

```bash
PYTHONPATH=src python3 -m stylechange.cli inspect examples/data/easy/problem-001.txt
```

## The four paragraphs

1. **Casual cooking.** Contractions (`pasta's`, `It's`, `wasn't`), `I` /
   `you`, an exclamation, mean word length 4.29, mean sentence length
   12.3. Casualness ≈ −0.03.
2. **Same cook, leftovers.** Still contractions (`I'm`, `it's`,
   `That's`) and `!`. Casualness ≈ −0.16. Same author, slightly
   shorter.
3. **Formal planning.** No contractions, no first person, a semicolon,
   hedges (`often`), nominalizations (`distribution`, `implementation`
   arrives in p4), mean word length 5.40, mean sentence length 24.3.
   Casualness ≈ −0.87.
4. **Same planner.** Parking, sidewalk, corridor. Casualness ≈ −0.79.

The casualness axis drops by about 0.7 at the gold change and barely
moves on the same-author sides. That is what “register shift” looks
like as a number.

## Distances

| Boundary | Gold | combined | scalar | fw | topic | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1–2 cooking → leftovers | 0 | 0.251 | 0.261 | 0.261 | 0.821 | same |
| 2–3 leftovers → sidewalks | 1 | 0.528 | 0.669 | 0.325 | 1.000 | CHANGE |
| 3–4 sidewalks → parking | 0 | 0.223 | 0.195 | 0.270 | 0.861 | same |

The middle jump is largest on **every** style view and on topic. Easy
is easy because the two stories agree.

Topic distance 1.000 means the content-word vectors share no types of
length ≥ 4. Pasta / garlic / leftovers do not overlap sidewalk /
pedestrian / corridor. A bag-of-nouns segmenter would also put a cut
there. That is not a style result until you look at Hard.

## The rest of the Easy split

| ID | Gold | Pred | Story |
| --- | --- | --- | --- |
| 001 | `[0,1,0]` | `[0,1,0]` | cooking then planning |
| 002 | `[1,1,1]` | `[1,1,1]` | bike / ecology / bike / freehub |
| 003 | `[1,1]` | `[1,1]` | same board-game night, designer voice in the middle |

Problem 002 is the A–B–A–C pattern: the casual cyclist returns. Both
returns are labelled `1`. Combined distances stay high (0.56–0.64)
because ecology prose and workshop prose do not share a register with
“Classic! I oiled the chain”.

Problem 003 keeps the topic (tabletop games) and still yields two
changes. That is already halfway to Medium: topic overlap is not zero
(0.89 / 0.95) and style still clears 0.33.

## Split score

```
macro-F1 = 1.000
micro: F1=1.000  tp=6 fp=0 fn=0 tn=2
```

Do not quote this number as “stylometry works”. Quote it as “the
teaching Easy set is linearly separable at \(t=0.33\)”.
