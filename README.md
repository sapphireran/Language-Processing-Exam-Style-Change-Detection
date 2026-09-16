# Style change detection — personal exam notes

Personal study repo for a language-processing exam: what style change
detection is, which stylometric features are worth naming, how a
simple unsupervised baseline works, and how to score it.

There is no shared-task data and no company code here. The example
documents were written for this repository so that a formal lecture
voice, a casual voice, and a terse procedural voice can be compared by
hand.

## The three questions

Given one document and no named authors:

1. Is more than one writing style present?
2. Between which paragraphs does the style change?
3. Which paragraphs share a latent author (including a writer who
   leaves and later returns)?

Notes live in `docs/`. Runnable baseline lives in `src/style_change/`.

| Note | Contents |
| --- | --- |
| [docs/01-task-and-problem.md](docs/01-task-and-problem.md) | SCD vs attribution vs topic cuts |
| [docs/02-stylometric-features.md](docs/02-stylometric-features.md) | Closed feature inventory |
| [docs/03-detection-methods.md](docs/03-detection-methods.md) | Distance, threshold, clustering |
| [docs/04-evaluation.md](docs/04-evaluation.md) | Boundary F1, ARI, BCubed |
| [docs/05-exam-checklist.md](docs/05-exam-checklist.md) | Short-answer prompts |
| [docs/06-worked-example.md](docs/06-worked-example.md) | Walk-through of a mixed file |

## Baseline in one paragraph

Split on blank lines (or one paragraph per line). Represent each
paragraph with length, richness, punctuation, person, discourse
markers, and a fixed function-word list. Project those rates onto four
named axes (formality, address, rhythm, procedure). Call a style
change wherever adjacent Euclidean distance clears a floor, optionally
raised into the first small-vs-large gap. Cluster with average linkage
so a returning author can reuse an id.

```text
paragraphs ──► features X ──► 4-D style axes ──► adjacent Euclidean d_i
                                                      │
                                                      ▼
                                                 d_i ≥ τ ──► boundaries
                                                      │
                                                      ▼
                                              agglomerative cut ──► author ids
```

## Setup

Python 3.10+ and `numpy`. Matplotlib is optional and only used for
`style-change plot`.

```bash
python -m pip install -e ".[dev]"
pytest
```

## Commands

```bash
style-change detect examples/documents/mixed_formal_casual.txt
style-change features examples/documents/mixed_formal_casual.txt
style-change evaluate examples/documents/mixed_formal_casual.txt \
    examples/documents/labels/mixed_formal_casual.json
style-change plot examples/documents/mixed_three_authors.txt -o /tmp/distances.png
python examples/run_demo.py
```

Without an editable install, `PYTHONPATH=src` works the same, and the
scripts under `examples/` add `src/` themselves.

## Example documents

See [examples/README.md](examples/README.md). Gold labels are JSON
objects with an `authors` list; ids are arbitrary.

## Tests

`tests/` covers tokenisation edge cases, feature names, distance
geometry, ARI/BCubed sanity checks, and the study documents' Task 1
labels plus the obvious mixed-document cuts.

## License

MIT. See `LICENSE`.
