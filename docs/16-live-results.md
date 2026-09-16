# Live results on the teaching corpus

Recomputed by `scripts/run_curriculum.py` on this revision. If you
move a weight or a threshold, replace these numbers before you quote
them.

Default **threshold** detector, \(\tau = 0.42\), window = 1.

| Slice | macro-F1 | F1-change | F1-stay | acc | tp | fp | fn | tn |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 0.550 | 0.300 | 0.800 | 0.689 | 3 | 12 | 2 | 28 |
| Medium | 0.604 | 0.414 | 0.795 | 0.696 | 6 | 16 | 1 | 33 |
| Hard | 0.543 | 0.200 | 0.886 | 0.800 | 1 | 4 | 4 | 31 |
| Control | 0.413 | 0.000 | 0.826 | 0.704 | 0 | 8 | 0 | 19 |
| Collage | 0.449 | 0.421 | 0.476 | 0.450 | 4 | 6 | 5 | 5 |
| All | 0.563 | 0.326 | 0.800 | 0.691 | 14 | 46 | 12 | 116 |

## How to read the table

- **Accuracy is the liar again.** Hard accuracy is 0.800 because the
  detector mostly stays quiet. Change-class F1 is 0.200. That is the
  16/4 story in miniature.
- **Medium beats Easy.** The blend is a register detector. Minutes
  versus Slack, or a formal letter versus WhatsApp, move person and
  contractions. Easy topic jumps only fire when register also moves
  (lowercase cycle chat versus a conservator's `we`).
- **Hard is the honest remainder.** `problem-14-two-bakers.txt`
  labels the I-voice → you-voice seam as `register_only`: score
  0.345 against a 0.42 cut. Say that sentence in the oral.
- **Control still false-alarms.** Eight false positives on
  single-author files, including scene changes. Topic is not gone;
  it is just no longer the only cue.

Adaptive and ensemble numbers are printed by the same script. They
trade a few more Hard hits for more Control false alarms. Name the
cost; do not hunt a single "best" row.
