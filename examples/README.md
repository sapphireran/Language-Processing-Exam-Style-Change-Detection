# Examples

- `corpus/` — thirty original documents, house sheet, emitter.
- `labs/` — short scripts I can run before an oral.
- `walkthroughs/` — one annotated hard document.
- `reports/` — generated score dumps (gitignored except the readme).

```bash
PYTHONPATH=src:. python3 examples/labs/run_all.py
python3 -m isogloss score examples/corpus
```
