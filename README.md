# Language-Processing-Exam-Style-Change-Detection

Personal exam lab. I treat style change detection as a **change-point
cut**, not a pairwise hinge classifier.

This is not company code, not a PAN submission, and not anyone else's
text. The twenty-eight documents in `examples/corpus/` are original.

## Thesis

A document is a walk on a short closed-class fingerprint. A style
change is a place I would saw that walk. The kerf is the gap the
blade leaves. If the best kerf is narrower than the blade, I do not
cut.

Pairwise neighbour scores lie on short paragraphs, on ABA returns,
and on topic jumps. The split score uses every paragraph to the left
and every paragraph to the right. An absolute adjacent floor is the
second blade, for returns the first saw dilutes.

## Layout

| path | what |
| --- | --- |
| `src/kerf/` | stdlib detector, I/O, metrics, CLI |
| `docs/` | exam notes, oral cards, live results |
| `examples/corpus/` | 28 original PAN-shaped files |
| `examples/labs/` | scripts that print live numbers |
| `tests/` | unit tests plus corpus smoke |

## Run

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest
PYTHONPATH=src:. python3 -m kerf score examples/corpus
PYTHONPATH=src:. python3 -m kerf inspect \
  examples/corpus/problem-16-stilling-caliper-then-seminar.txt
PYTHONPATH=src:. python3 examples/labs/run_all.py
```

## Live quote (this revision)

Stacked hinges, 28 documents:

| predictor | macro-F1 | hinge acc |
| --- | ---: | ---: |
| never-fire | 0.404 | 0.679 |
| always-fire | 0.243 | 0.321 |
| kerf | 0.986 | 0.988 |

Zero false changes. One false same: document 27, Seminar → Pocket
on the same stilling well. Holdout (04, 10, 15, 19, 23, 26, 28) is
clean. Never-fire accuracy is the liar — most hinges are zeros.

Read `docs/README.md` first. The cheatsheet is one page.
