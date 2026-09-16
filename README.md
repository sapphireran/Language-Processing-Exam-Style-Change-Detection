# Language Processing Exam: Style Change Detection

Personal exam notes and a small, dependency-free stylometry baseline
for **intrinsic style change detection**. Given a document, decide for
every pair of consecutive paragraphs whether the author changed.

This is not a shared-task submission and it does not include anyone
else’s writing. The documents under `examples/data/` were written for
these notes. The math follows the paragraph-level PAN-style setup
(binary `changes` array, Easy / Medium / Hard topic control, F1).

## Why this repo exists

The original README was a title. These notes fill it in with:

- a formal task definition you can write from memory
- a feature catalogue that keeps topic out of “style”
- worked exam questions with arithmetic you can check
- a runnable baseline so the tables in `examples/` are real

Company code does not belong here. Neither does a scraped corpus.

## Layout

```
docs/                 exam notes, from overview to ethics
examples/             original PAN-format documents + walkthroughs
src/stylechange/      stdlib stylometry toolkit
scripts/              score every split; check the hand calculations
tests/                unit tests + corpus sanity checks
```

Start at [docs/01-exam-overview.md](docs/01-exam-overview.md) or
[examples/README.md](examples/README.md).

## Quick start

Python 3.10+ is enough. No runtime dependencies.

```bash
python3 -m pip install -e ".[dev]"   # optional; only needs pytest
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 -m stylechange.cli inspect examples/data/easy/problem-001.txt
PYTHONPATH=src python3 -m stylechange.cli eval examples/data/easy
PYTHONPATH=src python3 scripts/run_curriculum.py
PYTHONPATH=src python3 scripts/check_hand_calculation.py
```

`eval` expects `problem-*.txt` and `truth-problem-*.json` in the same
folder and prints per-document F1 plus macro / micro summaries.

## What the baseline does

1. Split on blank lines.
2. Build a style profile: function-word rates, punctuation, character
   3-grams, and a short register vector (contractions, pronouns,
   hedges, nominalizations, length, a signed casualness axis).
3. Score each boundary with a weighted distance.
4. Label a change if the distance is above 0.33 (or use `--adaptive`).

It is meant to be readable in an exam answer, not to win a leaderboard.
On the teaching corpus it is perfect on Easy and Medium and clearly
wrong on Hard and on single-author controls — that gap is documented
in the walkthroughs on purpose.

## Teaching scores (threshold 0.33)

| Split | macro-F1 | What to take from it |
| --- | --- | --- |
| Easy | 1.00 | Style and topic agree |
| Medium | 1.00 | Register is enough when the world stays put |
| Hard | 0.33 | Same topic, close voices; one win, two honest misses |
| Control | 0.00 | Intra-author mood still looks like a change |

The one table to memorise is Hard problem 001 in
[examples/topic_confound.md](examples/topic_confound.md): the largest
topic jump is *not* the author change.

## License

MIT. Copyright line in `LICENSE` is unchanged from the original
repository.
