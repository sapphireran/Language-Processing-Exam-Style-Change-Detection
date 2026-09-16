# False friends (single-author drift)

A false friend is a boundary that *looks* like a style change and is
not one. The control split exists to produce them on purpose.

## Control 001 — the same gardener, three moods

Gold `[0, 0]`. Baseline `[0, 1]`.

| Boundary | combined | What actually changed |
| --- | --- | --- |
| basil list → balcony tomatoes | 0.295 | same `I`, slightly longer words |
| tomatoes → “friends ask” | **0.443** | shorter sentences (15.8 → 10.2), more contractions, casualness −0.34 → +0.12 |

Paragraph 3 is still the same person joking about not having a system.
The feature vector reads it as a jump because the prose speeds up and
the first-person rate doubles (`i` goes to 0.207 of function words).
Intra-author mood is not authorship.

## Control 002 — catalogue voice, first paragraph vs later

Gold `[0, 0]`. Baseline `[1, 0]`. Combined 0.366 on the first
boundary: the opening paragraph is a bit more general (“Cataloguing a
personal reading list…”) and the next one is more concrete
(“abandoned books”). Same author, same punctuation habit, not enough
tokens for the function-word cosine to sit still.

## Why the default threshold does not “just go up”

Raising \(t\) from 0.33 to 0.40 would silence both control false
positives **and** Medium problem 002 (distances 0.337 / 0.377). That
is the precision–recall hinge for this toy corpus. An exam answer
that picks one \(t\) without naming the hinge is incomplete.

## Adaptive threshold is not a free fix

`AdaptiveDetector` compares each jump to the document’s own mean and
standard deviation. On a two-boundary control document, one slightly
larger intra-author hop becomes “the outlier” and is labelled a
change. Adaptive helps Hard documents that are uniformly formal; it
makes short single-author documents worse. Always report it as a
variant, not as the hero.

```bash
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/control
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/control --adaptive
```

## Exam sentence you can reuse

> Single-author documents still vary in sentence length, pronoun rate,
> and mood; a threshold tuned on multi-author Easy data will spend its
> false positives there.
