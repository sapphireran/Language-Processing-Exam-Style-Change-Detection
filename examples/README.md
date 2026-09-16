# Examples

Runnable walks over the original teaching corpus. No extra packages.
Put `src/` on `PYTHONPATH` or install the package editable.

```bash
export PYTHONPATH=src
python3 examples/walk_worked_example.py
python3 examples/compare_channels.py
python3 examples/run_lab.py
python3 examples/annotate_document.py examples/corpus/easy/problem-01-ferry-marsh-knit.txt
python3 -m scarfjoint eval examples/corpus
```

| Script | What it shows |
| --- | --- |
| `walk_worked_example.py` | The cosine / Yule K / F1 numbers locked in `docs/05-worked-example.md` |
| `compare_channels.py` | Formality jump vs topic Jaccard on every gold boundary |
| `run_lab.py` | Band-by-band eval plus the leakage switch |
| `annotate_document.py` | Paragraph preview + channel dump for one file |

Hand-written boundary notes for three documents live in [`annotated/`](annotated/).
The corpus itself is in [`corpus/`](corpus/README.md).
