# Executable revision examples

These scripts assume you are at the repository root and have installed
the toolkit (`python3 -m pip install -e .`).

| Script | What it shows |
| --- | --- |
| `feature_walkthrough.py` | Live feature tables for the Mira / Jules / Hale / Nell cards |
| `manual_pair_check.py` | Paper-vs-code check of the worked-example pairs |
| `compare_detectors.py` | always0 / unsupervised / threshold / logistic / ensemble on all splits |
| `revision_session.py` | A single sitting: explain one hard document, then score the split |

```bash
python3 examples/feature_walkthrough.py
python3 examples/manual_pair_check.py
python3 examples/compare_detectors.py
python3 examples/revision_session.py
```

Equivalent CLI:

```bash
stylechange explain --input data/synthetic/hard/problem-001.txt
stylechange demo --split hard
```

Nothing here talks to the network. Nothing here loads a shared-task dump.
