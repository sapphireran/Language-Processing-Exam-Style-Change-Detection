# Language Processing Exam: Style Change Detection

Personal study repository for **intrinsic style-change detection**: given a
document, decide for every pair of consecutive paragraphs whether the writer
changed. The code, notes, and example documents here are original teaching
material. They are not a submission to a shared task and they do not include
third-party exam corpora.

This repo exists so I can rehearse the exam-style problem end to end:

1. split a document into paragraphs
2. extract stylometric and character-n-gram profiles
3. score adjacent paragraphs
4. emit a binary `changes` array
5. evaluate with macro-averaged F1

## Why the task is hard

Style is a weak, noisy signal. Topic, genre, and register move at the same
time as authorship. A detector that fires on every topic shift will look
strong on mixed-topic documents and collapse once every paragraph stays on
the same subject. The synthetic examples in `examples/sample_problems/` are
built around that confound:

| Split | What changes besides authorship |
| --- | --- |
| `easy/` | Topic and register both jump |
| `medium/` | Same broad topic, different register |
| `hard/` | Same topic, similar register, different habits |
| `single_author/` | Control documents with no author change |

## Quick start

The toolkit is standard-library Python 3.11+. No third-party packages are
required to run detectors, evaluation, or the CLI.

```bash
python3 -m pip install -e .
style-change predict -i examples/sample_problems/easy -o /tmp/style-out
style-change evaluate --gold examples/sample_problems/easy --pred /tmp/style-out
style-change features examples/sample_problems/easy/problem-001.txt
```

From a checkout without installing:

```bash
PYTHONPATH=src python3 -m style_change predict \
  -i examples/sample_problems/easy \
  -o /tmp/style-out
```

## Repository map

```
docs/                      study notes (task, features, metrics, walkthrough)
examples/sample_problems/  original synthetic documents + gold labels
examples/*.py              scripts that print feature tables and baseline scores
src/style_change/          detectors, I/O, evaluation
tests/                     unit tests for the exam-critical paths
```

## Predicted output format

For a document with `N` paragraphs the model writes `N-1` binary labels.
`1` means “style change between this paragraph and the next.”

```json
{
  "changes": [0, 1, 0, 1]
}
```

Gold files in this repo also record the author count so a walkthrough can
show how the `changes` array relates to speaker turns.

## Detectors

| Name | Signal |
| --- | --- |
| `stylometric` | Cosine distance on z-scored lexical / punctuation features |
| `char3` | Cosine distance on character 3-gram profiles |
| `function_word` | Jensen–Shannon divergence on function-word distributions |
| `ensemble` | Weighted mix of the three (default) |

Thresholds can be fixed or chosen adaptively per document. The walkthrough
in `docs/04-walkthrough.md` shows both, including the case where a
homogeneous document should stay all zeros.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`. Example documents are original text written for this
repository and may be reused under the same license.
