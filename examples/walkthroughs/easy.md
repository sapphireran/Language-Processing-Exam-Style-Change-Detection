# Walkthrough — Nørrebro bikes then parchment repair

File: `problem-02-bikes-vellum.txt`  ·  tier: **easy**  ·  voices: cycle_chat, conservator

Default threshold detector (τ = 0.42): macro-F1 0.585, change-F1 0.400, stay-F1 0.769. Cells: tp=1 fp=3 fn=0 tn=5.

Numbers come from `seamtrace` on this revision. Re-run `scripts/write_walkthroughs.py` if you move the cut.

| i | gold | pred | score | fw | tri | Δ | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0.446 | 0.75 | 0.84 | 0.57 | single_author_drift |
| 1 | 0 | 1 | 0.425 | 0.81 | 0.93 | 0.26 | single_author_drift |
| 2 | 0 | 1 | 0.472 | 0.92 | 0.90 | 0.26 | single_author_drift |
| 3 | 0 | 0 | 0.379 | 0.51 | 0.82 | 0.61 | genuine_stay |
| 4 | 1 | 1 | 0.498 | 0.66 | 0.90 | 0.68 | genuine_hit |
| 5 | 0 | 0 | 0.346 | 0.59 | 0.74 | 0.36 | genuine_stay |
| 6 | 0 | 0 | 0.301 | 0.45 | 0.67 | 0.40 | genuine_stay |
| 7 | 0 | 0 | 0.367 | 0.52 | 0.80 | 0.58 | genuine_stay |
| 8 | 0 | 0 | 0.372 | 0.56 | 0.80 | 0.57 | genuine_stay |

## Boundaries

### Pair 0 — `single_author_drift`

- Score 0.446 (False alarm: score cleared the cut without a labelled seam.)
- Left: ok so the cycle track on nørrrebrogade is packed by eight and you just have to commit or someone in a cargo bike will eat your elbow
- Right: i still brake too late at the bakery corner because the cobbles get this greasy film after rain

### Pair 1 — `single_author_drift`

- Score 0.425 (False alarm: score cleared the cut without a labelled seam.)
- Left: i still brake too late at the bakery corner because the cobbles get this greasy film after rain
- Right: my lights died last tuesday and a guy shouted that i was a ghost which fair

### Pair 2 — `single_author_drift`

- Score 0.472 (False alarm: score cleared the cut without a labelled seam.)
- Left: my lights died last tuesday and a guy shouted that i was a ghost which fair
- Right: anyway if you take the side street past the cemetery it's slower but you don't play chicken with the 5A

### Pair 3 — `genuine_stay`

- Score 0.379 (Predicted stay matches gold.)
- Left: anyway if you take the side street past the cemetery it's slower but you don't play chicken with the 5A
- Right: that's the whole commuting philosophy really: stay visible, don't be precious about minutes, go home

### Pair 4 — `genuine_hit`

- Score 0.498 (Predicted change matches gold.)
- Left: that's the whole commuting philosophy really: stay visible, don't be precious about minutes, go home
- Right: In contrast, the repair of a medieval charter begins with a survey of the skin rather than with any desire for speed.

### Pair 5 — `genuine_stay`

- Score 0.346 (Predicted stay matches gold.)
- Left: In contrast, the repair of a medieval charter begins with a survey of the skin rather than with any desire for speed.
- Right: Vellum that has cockled from damp must be humidified evenly; a local wet patch will stain and the fibres will remember the insult.

### Pair 6 — `genuine_stay`

- Score 0.301 (Predicted stay matches gold.)
- Left: Vellum that has cockled from damp must be humidified evenly; a local wet patch will stain and the fibres will remember the insult.
- Right: We align the bifolium to the original ruling before we infill a loss, and we tint the new parchment so that the mend recedes under gallery light.

### Pair 7 — `genuine_stay`

- Score 0.367 (Predicted stay matches gold.)
- Left: We align the bifolium to the original ruling before we infill a loss, and we tint the new parchment so that the mend recedes under gallery light.
- Right: Adhesives are chosen for reversibility: a future conservator must be able to undo our patience without undoing the text.

### Pair 8 — `genuine_stay`

- Score 0.372 (Predicted stay matches gold.)
- Left: Adhesives are chosen for reversibility: a future conservator must be able to undo our patience without undoing the text.
- Right: The work is slow on purpose, because a charter is not a commute and the damage was already done centuries before we arrived.

