# Language Processing exam — style-change detection

Personal study lab for an intrinsic **style-change detection** exam
(sentence-level seams, PAN-shaped I/O, Easy / Medium / Hard intuition).
The repository is original notes, original teaching prose, and a small
stdlib toolkit named `seamtrace`. It is not a shared-task submission
and it does not contain company code or PAN Reddit text.

## What you can run

```bash
PYTHONPATH=src python3 -m pytest -q
PYTHONPATH=src python3 scripts/check_hand_calculation.py
PYTHONPATH=src python3 scripts/run_curriculum.py
PYTHONPATH=src python3 -m seamtrace inspect examples/corpus/problem-14-two-bakers.txt
```

Optional HTML pair reports:

```bash
PYTHONPATH=src python3 -m seamtrace report examples/corpus --out examples/reports
```

## Layout

| Path | What it is |
| --- | --- |
| `docs/` | Exam notes, oral cards, model answers, formula card |
| `examples/corpus/` | 22 original documents + gold `changes` arrays |
| `examples/walkthroughs/` | Live detector tables for four spotlight files |
| `src/seamtrace/` | Features, Delta, CUSUM, detectors, error taxonomy |
| `scripts/` | Curriculum table, threshold grid, walkthrough writer |
| `tests/` | Contract tests for the corpus and the metric |

Start with [`docs/README.md`](docs/README.md) or the
[revision circuit](docs/15-revision-circuit.md).

## The claim the lab is built to make

A detector that only works when **topic and author move together**
has not shown that it can see style. Easy files in `examples/corpus`
are allowed to look easy for a content model. This lab's default
blend is a *register* detector, so Medium (same domain, different
hands) is often the strongest slice and Hard stays close to the
majority baseline. Controls include a single-author day that still
changes rooms. Write the Easy / Medium / Hard gap down — that is
the result, not a failure to hide.

## Detector (teaching default)

Each consecutive pair gets a blended distance:

- 0.35 function-word cosine (lightly smoothed)
- 0.10 character-trigram cosine
- 0.40 register scalars (person, contractions, sentence-initial case)
- 0.15 bounded Burrows' Delta on the same closed list

A pair is a change if the blend is at least **0.42**. Adaptive and
ensemble voters live in the same CLI (`--detector adaptive|ensemble`).
The default window is one unit on each side so a labelled seam is
not smeared into its neighbours.

Evaluation is **macro-F1**. A never-fire baseline on 16 stay + 4
change pairs scores 0.80 accuracy and 0.444 macro-F1. That example
is executable: `python3 examples/never_fire_demo.py`.

## License

MIT. Teaching prose is original to this repo.
