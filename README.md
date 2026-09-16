# Language-Processing-Exam-Style-Change-Detection

Personal exam lab. Not a PAN submission. Not company code. Not
shared-task data.

A dialect atlas does not declare a new dialect because one word
changes. It waits for a **bundle of isoglosses**. This repo treats
a style change the same way: each closed-class rate draws its own
1-D map, and a hinge fires only when several maps agree.

```
z_{i,f} = (x_{i,f} − x_{i+1,f}) / (max(s_f, prior_f) + ε)
mark_{i,f} = 1[ |z_{i,f}| ≥ max(ζ, ρ · peak_f) ]
change_i = 1[ votes_i ≥ k ]
```

Nouns never enter the map. Topic is not a dialect.

## Layout

| path | what it is |
| --- | --- |
| `src/isogloss/` | detector, PAN-shaped I/O, macro-F1 |
| `docs/` | exam notes, oral cards, formula card |
| `examples/corpus/` | 30 original documents, six houses |
| `examples/labs/` | revision scripts |
| `tests/` | unit tests and corpus smoke |

Houses: **Skiff, Roll, Twine, Vellum, Flint, Brine**. Crafts: eel
weir, hop oast, lime kiln, millrace, salt pan, peat, withy, coble,
cider, charcoal, granite setts, tide mill, hurdles. Holdout codes:
04 / 10 / 16 / 22 / 26 / 30.

## Commands

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest
python3 -m isogloss score examples/corpus
python3 -m isogloss inspect examples/corpus/problem-19-skiff-then-vellum-eel.txt --features
python3 -m isogloss holdout examples/corpus --ids 4,10,16,22,26,30
python3 -m isogloss predict -i examples/corpus -o /tmp/isogloss-out
cd examples/labs && python3 run_all.py
```

## What this is not

It is not the kerf saw (global mean-shift). It is not NCD. It is
not a blended register peak. Those are fine orals. This one is an
atlas.

See `docs/18-why-not-the-other-orals.md` and `docs/15-ethics.md`.
