# Examples

Original documents, a voice sheet, numbered labs, and a few
walkthroughs I wrote after I had already marked the hinges on paper.

| path | what it is |
| --- | --- |
| [`corpus/`](corpus/README.md) | 28 PAN-style problems + truth |
| [`voices.md`](voices.md) | house labels used in the truth files |
| [`labs/`](labs/README.md) | revision scripts, 00–10 |
| [`walkthroughs/`](walkthroughs/README.md) | prose on five files |
| [`reports/`](reports/README.md) | generated score tables (gitignored except README) |

From the repo root, after `pip install -e ".[dev]"`:

```bash
python3 examples/labs/run_all.py
python3 -m quoin score examples/corpus
```
