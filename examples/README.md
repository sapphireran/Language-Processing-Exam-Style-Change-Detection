# Runnable examples

Scripts assume you are at the repository root and that `src/` is on
`PYTHONPATH` (the tests already set this; or run
`python3 -m splicefind ...`).

| Script | What it is for |
|--------|----------------|
| `00_split_and_count.py` | Prove you can see the paragraphs. |
| `01_feature_table.py` | Print the scalars an examiner can ask about. |
| `02_pairwise_scores.py` | Show the three distances on one document. |
| `03_cusum_trace.py` | Sparkline for sentence-length CUSUM. |
| `04_score_corpus.py` | F1 on all eighteen labelled documents. |
| `05_calibrate_threshold.py` | Sweep the ensemble cut-off. |
| `06_ablate_channels.py` | Drop Delta / n-grams / scalars one at a time. |
| `07_topic_confound.py` | Same author new topic vs new author same topic. |
| `08_pan_roundtrip.py` | Write and read PAN-shaped files in a temp dir. |
| `09_generate_synthetic.py` | Emit a tiny easy/medium/hard split. |
| `10_write_reports.py` | HTML + text reports for the corpus. |
| `run_all.py` | Run the above in order. |

Worked prose for document 14 lives in
`docs/10-worked-walkthrough.md`.
