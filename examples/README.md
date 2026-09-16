# Synthetic sample problems

These documents are original teaching examples. They are not scraped from
Reddit, not copied from a shared-task corpus, and not exam questions.

Each split mimics the usual difficulty story for intrinsic style-change
detection: topic and register can leak authorship, so a detector that only
notices “the subject changed” will look stronger than it is.

| Directory | Documents | What a detector is allowed to lean on |
| --- | ---: | --- |
| `easy/` | 2 | Topic jumps and register jumps, often together |
| `medium/` | 2 | Same broad topic, different register or genre |
| `hard/` | 2 | Same topic, closer registers, leftover habits |
| `single_author/` | 2 | Control: one voice, gold `changes` all zeros |

Every `problem-*.txt` is blank-line segmented. The matching
`truth-problem-*.json` stores:

```json
{
  "authors": 3,
  "changes": [0, 1, 0, 1]
}
```

`changes[i]` labels the boundary between paragraph `i+1` and paragraph
`i+2`. Length is always `n_paragraphs - 1`.

## Inventory

| File | Authors | Gold `changes` | Sketch |
| --- | ---: | --- | --- |
| `easy/problem-001` | 3 | `[0, 1, 0, 1]` | hiking chat → hydrology memo → recipe |
| `easy/problem-002` | 4 | `[1, 1, 1]` | recap → contract → nature journal → text |
| `medium/problem-001` | 2 | `[0, 1, 0]` | chatty bake, then process notes |
| `medium/problem-002` | 2 | `[1, 1]` | library memory, policy memo, memory |
| `hard/problem-001` | 2 | `[1, 1]` | rain garden, three registers on one topic |
| `hard/problem-002` | 2 | `[1, 1]` | same commute, long / clipped / long |
| `single_author/problem-001` | 1 | `[0, 0]` | houseplants, one voice |
| `single_author/problem-002` | 1 | `[0, 0]` | a walking week, one voice |

## How to run them

```bash
PYTHONPATH=src python3 -m style_change predict \
  -i examples/sample_problems/easy \
  -o /tmp/style-easy

PYTHONPATH=src python3 -m style_change evaluate \
  --gold examples/sample_problems/easy \
  --pred /tmp/style-easy
```

`examples/inspect_features.py` prints a feature table for one file.
`examples/compare_baselines.py` scores every detector on every split.
`examples/annotated/easy-001.md` is a paragraph-by-paragraph reading of
the first easy document.

## Design notes

- Paragraphs are long enough for type-token ratios and function-word
  rates to move. Two-sentence snippets make stylometry look random.
- Easy documents are allowed to cheat with topic. That is intentional:
  the walkthrough uses them to show a detector working, then medium/hard
  show where topic leakage stops helping.
- Single-author documents exist so “always predict change” cannot look
  like a serious baseline.
- Gold labels were written with the documents, not inferred from a model.
