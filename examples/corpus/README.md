# Teaching corpus

Twenty-two original documents, written for this personal exam lab.
Nothing here is copied from PAN, Reddit, or a course handout.

Each `problem-*.txt` is one sentence per non-empty line. Gold lives in
`truth/truth-<stem>.json` and always satisfies

```
len(changes) == n_sentences - 1
```

`authors` is the number of distinct voices, not `1 + sum(changes)`.
Collage files return a writer, so those two numbers disagree on
purpose.

## Tiers

| Tier | Files | Exam use |
| --- | --- | --- |
| Easy | 02–06 | Topic and register move together |
| Medium | 07–13 | Same domain, different register |
| Hard | 14–18 | Same subject, close hands |
| Control | 01, 19, 20 | Single author; 20 also changes scene |
| Collage | 21–22 | More than two voices, with a return |

## How to score

```
PYTHONPATH=src python3 -m seamtrace score examples/corpus
PYTHONPATH=src python3 scripts/run_curriculum.py
```

`manifest.json` is the machine-readable contents list.
