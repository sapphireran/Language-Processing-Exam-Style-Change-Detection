# Walkthrough — Single author, kitchen then S-train

File: `problem-20-campus-return.txt`  ·  tier: **control**  ·  voices: campus_day

Default threshold detector (τ = 0.42): macro-F1 0.400, change-F1 0.000, stay-F1 0.800. Cells: tp=0 fp=3 fn=0 tn=6.

Numbers come from `seamtrace` on this revision. Re-run `scripts/write_walkthroughs.py` if you move the cut.

| i | gold | pred | score | fw | tri | Δ | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0.374 | 0.64 | 0.81 | 0.38 | genuine_stay |
| 1 | 0 | 1 | 0.428 | 0.66 | 0.83 | 0.60 | single_author_drift |
| 2 | 0 | 0 | 0.300 | 0.45 | 0.70 | 0.41 | genuine_stay |
| 3 | 0 | 1 | 0.424 | 0.67 | 0.90 | 0.58 | single_author_drift |
| 4 | 0 | 1 | 0.487 | 0.90 | 0.97 | 0.41 | single_author_drift |
| 5 | 0 | 0 | 0.326 | 0.38 | 0.72 | 0.72 | genuine_stay |
| 6 | 0 | 0 | 0.259 | 0.28 | 0.57 | 0.63 | genuine_stay |
| 7 | 0 | 0 | 0.267 | 0.35 | 0.74 | 0.44 | genuine_stay |
| 8 | 0 | 0 | 0.364 | 0.54 | 0.87 | 0.56 | genuine_stay |

## Boundaries

### Pair 0 — `genuine_stay`

- Score 0.374 (Predicted stay matches gold.)
- Left: I burnt the oats again and I ate them anyway because the morning had already spent its patience.
- Right: The kitchen window showed a courtyard that was trying to be spring and not quite succeeding.

### Pair 1 — `single_author_drift`

- Score 0.428 (False alarm: score cleared the cut without a labelled seam.)
- Left: The kitchen window showed a courtyard that was trying to be spring and not quite succeeding.
- Right: I packed the notes in the order I wish I had written them, which is not the order they exist.

### Pair 2 — `genuine_stay`

- Score 0.300 (Predicted stay matches gold.)
- Left: I packed the notes in the order I wish I had written them, which is not the order they exist.
- Right: On the S-train a child's shoe kept tapping the pole and I decided not to turn it into a metaphor.

### Pair 3 — `single_author_drift`

- Score 0.424 (False alarm: score cleared the cut without a labelled seam.)
- Left: On the S-train a child's shoe kept tapping the pole and I decided not to turn it into a metaphor.
- Right: Nørreport smelled like wet coats and pretzels, which is to say it smelled like itself.

### Pair 4 — `single_author_drift`

- Score 0.487 (False alarm: score cleared the cut without a labelled seam.)
- Left: Nørreport smelled like wet coats and pretzels, which is to say it smelled like itself.
- Right: I walked the last ten minutes because the air was cheaper than another carriage.

### Pair 5 — `genuine_stay`

- Score 0.326 (Predicted stay matches gold.)
- Left: I walked the last ten minutes because the air was cheaper than another carriage.
- Right: In the reading room I opened the same page I had opened at breakfast and I did not pretend the commute had improved it.

### Pair 6 — `genuine_stay`

- Score 0.259 (Predicted stay matches gold.)
- Left: In the reading room I opened the same page I had opened at breakfast and I did not pretend the commute had improved it.
- Right: The day changed rooms and I still used the same first person and the same short clauses.

### Pair 7 — `genuine_stay`

- Score 0.267 (Predicted stay matches gold.)
- Left: The day changed rooms and I still used the same first person and the same short clauses.
- Right: I made tea in the reading-room flask and it tasted of the oats I had already admitted were burnt.

### Pair 8 — `genuine_stay`

- Score 0.364 (Predicted stay matches gold.)
- Left: I made tea in the reading-room flask and it tasted of the oats I had already admitted were burnt.
- Right: I left when the page stopped moving, which is my usual honest time to go.

