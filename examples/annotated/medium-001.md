# Medium document: same bake, two voices

Gold for `medium/problem-001`: two authors, `changes = [0, 1, 0]`.

This is the worksheet I would use after the easy hiking/climate example.
Nothing in the file leaves the kitchen. If a detector still finds the
seam, it found style. If it does not, it was using topic.

## Paragraphs 1–2 — home baker

First person, jokes (`dough like it owes me rent`), contractions, taste
and neighbours, the tap-the-bottom ritual. P2 continues the same loaf
without resetting the voice. A topic-segmenter might see “starter” then
“crust” and invent a boundary. Gold says no.

## Paragraphs 3–4 — process notes

Hydration percentages, autolyse, coil folds, oven spring, Maillard.
First person almost disappears. Connectives and measurements take over.
P4 stays in that lab notebook. The author change is P2→P3 only.

## Why this split exists

`easy/problem-001` lets you be right by noticing that hiking is not
hydrology. This file does not. Function-word rates, contraction rates,
and average word length should move at the seam; bag-of-content-words
overlap will stay high because both writers are talking about bread.

```bash
PYTHONPATH=src python3 -m style_change features \
  examples/sample_problems/medium/problem-001.txt
```

Compare `contraction_rate` and `digit_rate` on columns 1–2 versus 3–4.
That pair of columns is the whole argument of the medium split.
