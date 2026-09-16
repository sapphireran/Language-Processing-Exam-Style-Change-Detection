# Language-Processing-Exam-Style-Change-Detection

Personal exam lab for **sentence-level style-change detection**. No company code, no shared-task dumps.

A document is a chain of sentences. Every neighbouring pair is a **hinge**. The hinge either holds or snaps. The official answer is a binary `changes` array. This repo fills that story with notes, twenty-six original documents, and a stdlib blender you can run.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 -m hingemark eval examples/corpus
PYTHONPATH=src python3 -m hingemark explain examples/corpus/problem-13-two-mycologists.txt
PYTHONPATH=src python3 examples/labs/run_all.py
```

On this revision the default cut (0.30) scores about **0.70 mean macro-F1** on the teaching set: strong on easy/medium register flips, honest on hard same-register pairs, quiet on the River and Quill topic controls. The Spark chat control still false-alarms. That gap is in `docs/15-live-results.md`, not hidden.

## Layout

| Path | What |
| --- | --- |
| `docs/` | Exam notes, oral cards, formula card, live table |
| `examples/corpus/` | 26 original one-sentence-per-line documents + gold |
| `examples/labs/` | Revision labs 00–10 |
| `src/hingemark/` | Split, features, hinges, detectors, CLI |
| `tests/` | Gold-length locks and the 16/4 accuracy trap |

## House voices

River (field journal), Quill (minutes), Spark (chat), Marble (catalog), Hearth (letter). Hard files use two close scientists (Quist / Vale) on the same topic. See `examples/voices.md`.

## Spotlight files

- `problem-08-quince-batch-then-letter` — same topic, register snap (should hit)
- `problem-13-two-mycologists` — same topic, same register (intended miss)
- `problem-19-river-three-topics` — one writer, three topics (should stay quiet)
- `problem-22-canal-return` — A-B-A; `1+sum(changes)` is wrong on purpose
- `problem-25-tidepool-gift-abstract` — student paragraph, pasted abstract

MIT. Teaching material only; not a forensic tool.
