# Walkthrough — Two bakers, one rye loaf

File: `problem-14-two-bakers.txt`  ·  tier: **hard**  ·  voices: baker_i, baker_you

Default threshold detector (τ = 0.42): macro-F1 0.467, change-F1 0.000, stay-F1 0.933. Cells: tp=0 fp=0 fn=1 tn=7.

Numbers come from `seamtrace` on this revision. Re-run `scripts/write_walkthroughs.py` if you move the cut.

| i | gold | pred | score | fw | tri | Δ | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0.256 | 0.31 | 0.75 | 0.45 | genuine_stay |
| 1 | 0 | 0 | 0.317 | 0.46 | 0.86 | 0.37 | genuine_stay |
| 2 | 0 | 0 | 0.374 | 0.59 | 0.86 | 0.47 | genuine_stay |
| 3 | 1 | 0 | 0.345 | 0.57 | 0.70 | 0.35 | register_only |
| 4 | 0 | 0 | 0.331 | 0.38 | 0.79 | 0.65 | genuine_stay |
| 5 | 0 | 0 | 0.362 | 0.58 | 0.89 | 0.41 | genuine_stay |
| 6 | 0 | 0 | 0.317 | 0.40 | 0.81 | 0.52 | genuine_stay |
| 7 | 0 | 0 | 0.388 | 0.70 | 0.91 | 0.25 | genuine_stay |

## Boundaries

### Pair 0 — `genuine_stay`

- Score 0.256 (Predicted stay matches gold.)
- Left: The rye prefers a long cool ferment; I give it twelve hours in the fridge and I do not rush the oven for guests.
- Right: I like the crumb a little wet so I hold back a spoon of flour even when the dough looks slack.

### Pair 1 — `genuine_stay`

- Score 0.317 (Predicted stay matches gold.)
- Left: I like the crumb a little wet so I hold back a spoon of flour even when the dough looks slack.
- Right: If the loaf sings I wait, because cutting early is how you get a gummy sermon about patience.

### Pair 2 — `genuine_stay`

- Score 0.374 (Predicted stay matches gold.)
- Left: If the loaf sings I wait, because cutting early is how you get a gummy sermon about patience.
- Right: Steam for the first fifteen minutes, then dry heat, then I tap the base and I listen more than I look.

### Pair 3 — `register_only`

- Score 0.345 (Register moved; the blended cut still missed it.)
- Left: Steam for the first fifteen minutes, then dry heat, then I tap the base and I listen more than I look.
- Right: You should mix until the dough just clears the bowl, then stop, or you will build a tough crumb and call it rustic.

### Pair 4 — `genuine_stay`

- Score 0.331 (Predicted stay matches gold.)
- Left: You should mix until the dough just clears the bowl, then stop, or you will build a tough crumb and call it rustic.
- Right: Keep the surface taut when you shape; slack shaping is the usual reason a rye spreads instead of lifting.

### Pair 5 — `genuine_stay`

- Score 0.362 (Predicted stay matches gold.)
- Left: Keep the surface taut when you shape; slack shaping is the usual reason a rye spreads instead of lifting.
- Right: Proof only until a floured finger leaves a dent that slowly returns — fully returned means you waited too long.

### Pair 6 — `genuine_stay`

- Score 0.317 (Predicted stay matches gold.)
- Left: Proof only until a floured finger leaves a dent that slowly returns — fully returned means you waited too long.
- Right: I would rather underproof slightly than bake a loaf that collapses into a story about humidity.

### Pair 7 — `genuine_stay`

- Score 0.388 (Predicted stay matches gold.)
- Left: I would rather underproof slightly than bake a loaf that collapses into a story about humidity.
- Right: Score the dough with one decisive stroke; hesitation is how a rye leaks sideways and then sulks.

