# Examples

- `corpus/` — twenty-six original documents and their truth files
- `labs/` — numbered revision scripts
- `walkthroughs/` — `inkfold explain` dumps for the documents the oral names
- `voices.md` — one line per house voice
- `reports/` — HTML written by `inkfold report` (not committed)

```bash
PYTHONPATH=src python3 examples/labs/run_all.py
PYTHONPATH=src python3 -m inkfold report --walkthroughs examples/walkthroughs
```
