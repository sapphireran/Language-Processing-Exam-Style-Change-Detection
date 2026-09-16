# Examples

Hand-written documents and small labs for the personal exam, not a
shared-task drop.

- `corpus/` — twenty-eight original problems in PAN shape, plus the
  house-voice sheet and `bank.py`.
- `labs/` — scripts that print live numbers from `kerf` instead of
  remembered ones.

```bash
PYTHONPATH=src:. python3 -m kerf score examples/corpus
PYTHONPATH=src:. python3 examples/labs/run_all.py
```
