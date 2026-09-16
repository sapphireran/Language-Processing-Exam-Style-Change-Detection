# Examples

Runnable companions to the notes in `docs/`.

| script | what it is for |
| --- | --- |
| `run_collection.py` | detect + score every study file |
| `compare_collection.py` | eight exam-explainable baselines on each file |
| `walkthrough_cusum.py` | the hand calculation from `docs/04` |
| `walkthrough_f1.py` | the hand calculation from `docs/07` |
| `walkthrough_features.py` | print the closed vector at a known cut |
| `write_cusum_figures.py` | SVG figures for the recipe cut and the commute control (`figures/`) |

From the repo root, after `pip install -e .`:

```
python examples/run_collection.py
python examples/walkthrough_cusum.py
python -m examscd detect examples/documents/02_recipe_then_maillard.txt --explain
python -m examscd compare examples/documents/05_same_topic_hard.txt \
    examples/documents/truth/05_same_topic_hard.json
```
