# Language-Processing-Exam-Style-Change-Detection

Personal exam lab. A document is a sheet of paper. A **style change is a fold**.
Counting folds is not the same as counting authors if the sheet is folded back
onto an earlier voice.

This repository is a study kit: original teaching documents, a six-number
register vector you can count with a pencil, and a stdlib detector that is
honest about what it misses.

No shared-task text. No company code.

## Quick start

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -q
PYTHONPATH=src python3 -m inkfold validate
PYTHONPATH=src python3 -m inkfold score
PYTHONPATH=src python3 -m inkfold explain examples/corpus/problem-01-kiln-then-notice.txt
PYTHONPATH=src python3 -m inkfold hand examples/corpus/problem-01-kiln-then-notice.txt
PYTHONPATH=src python3 examples/labs/run_all.py
```

## What to revise

- `docs/` — exam notes, oral cards, model answers, formula card, live numbers
- `examples/corpus/` — twenty-six original documents (PAN `problem` + `truth`)
- `examples/labs/` — numbered revision labs
- `src/inkfold/` — tokenizer, register vector, peak-picking detector, CLI

## Intended takeaways

1. **Easy / medium register flips are loud.** Kiln daybook → fire notice is a clean hit.
2. **Hard same-register pairs are a miss.** Two bellfounders on one tenor stay quiet (`same_register_miss`).
3. **Topic is not style.** One stall voice on dumplings, a night bus, and a cat does not fold.
4. **Chat jitters.** Short wire units false-alarm (`chat_jitter`).
5. **Return authors break `authors == 1 + sum(changes)`.** See `problem-22-kiln-return`.
6. **Accuracy is a trap.** Never-fire is ~0.77 accurate here and a terrible answer.

Live numbers for this revision live in `docs/15-live-results.md`.
