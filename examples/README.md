# Runnable labs

These scripts are the practical half of `docs/`. They import `scdkit`
from `src/` via `_paths.py`, so you can run them without installing
the package.

```bash
python examples/lab01_split_and_count.py
python examples/lab02_feature_table.py examples/documents/04_hard_circadian.txt
python examples/lab03_pairwise.py
python examples/lab04_cusum.py
python examples/lab05_score_collection.py
python examples/lab06_ablation.py
python examples/lab07_topic_confound.py
python examples/walkthrough_f1.py
python examples/write_reports.py
python examples/run_all.py
```

After `pip install -e .` the same walks are available as commands:

```bash
scdkit detect examples/documents/05_gift_poster.txt --explain --preview
scdkit features examples/documents/03_medium_cph_rent.txt
scdkit eval examples/documents --truth examples/documents/truth
scdkit compare examples/documents --truth examples/documents/truth
scdkit mix examples/authors ABA --stem drill_aba
scdkit report examples/documents/07_return_ferry.txt \
  --truth examples/documents/truth/07_return_ferry.json \
  --out examples/reports/07_return_ferry.html
```

`documents/` holds the fourteen hand-written problems. `authors/` holds
restackable voice cards. Generated HTML lands in `reports/`.
