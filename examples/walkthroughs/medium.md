# Walkthrough — Committee minutes then Slack

File: `problem-10-committee-slack.txt`  ·  tier: **medium**  ·  voices: minutes, slack

Default threshold detector (τ = 0.42): macro-F1 0.564, change-F1 0.400, stay-F1 0.727. Cells: tp=1 fp=3 fn=0 tn=4.

Numbers come from `seamtrace` on this revision. Re-run `scripts/write_walkthroughs.py` if you move the cut.

| i | gold | pred | score | fw | tri | Δ | label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0.241 | 0.38 | 0.79 | 0.14 | genuine_stay |
| 1 | 0 | 0 | 0.350 | 0.61 | 0.82 | 0.28 | genuine_stay |
| 2 | 0 | 0 | 0.335 | 0.55 | 0.83 | 0.27 | genuine_stay |
| 3 | 1 | 1 | 0.435 | 0.71 | 0.92 | 0.29 | genuine_hit |
| 4 | 0 | 1 | 0.468 | 0.89 | 0.91 | 0.38 | single_author_drift |
| 5 | 0 | 1 | 0.491 | 0.62 | 1.00 | 0.70 | short_unit_noise |
| 6 | 0 | 1 | 0.437 | 0.58 | 1.00 | 0.74 | short_unit_noise |
| 7 | 0 | 0 | 0.388 | 0.45 | 0.80 | 0.56 | genuine_stay |

## Boundaries

### Pair 0 — `genuine_stay`

- Score 0.241 (Predicted stay matches gold.)
- Left: The committee convened at 14:05 and noted that a quorum was present.
- Right: It was agreed that the fieldwork budget would remain ring-fenced pending the March forecast.

### Pair 1 — `genuine_stay`

- Score 0.350 (Predicted stay matches gold.)
- Left: It was agreed that the fieldwork budget would remain ring-fenced pending the March forecast.
- Right: Members received the draft timetable and were invited to send corrections by Friday noon.

### Pair 2 — `genuine_stay`

- Score 0.335 (Predicted stay matches gold.)
- Left: Members received the draft timetable and were invited to send corrections by Friday noon.
- Right: No other business was raised, and the meeting closed at 14:40.

### Pair 3 — `genuine_hit`

- Score 0.435 (Predicted change matches gold.)
- Left: No other business was raised, and the meeting closed at 14:40.
- Right: ok that was 35 minutes of "noted" for one actual decision

### Pair 4 — `single_author_drift`

- Score 0.468 (False alarm: score cleared the cut without a labelled seam.)
- Left: ok that was 35 minutes of "noted" for one actual decision
- Right: budget still frozen which means we cannot book the van, just so we are all equally annoyed

### Pair 5 — `short_unit_noise`

- Score 0.491 (A very short unit made the distance unstable.)
- Left: budget still frozen which means we cannot book the van, just so we are all equally annoyed
- Right: Yes.

### Pair 6 — `short_unit_noise`

- Score 0.437 (A very short unit made the distance unstable.)
- Left: Yes.
- Right: I will dump the timetable in the folder but if your name is spelled wrong that is a Friday-you problem

### Pair 7 — `genuine_stay`

- Score 0.388 (Predicted stay matches gold.)
- Left: I will dump the timetable in the folder but if your name is spelled wrong that is a Friday-you problem
- Right: lol ok see you never in that room again I hope

