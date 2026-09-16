# Cheatsheet

- **Task**: intrinsic, one document, binary hinges.
- **Output**: `{"changes":[…]}` length `n-1`.
- **Return trap**: `1+sum(changes)` assumes no writer comes back. See problem-22.
- **Features**: register rates + smoothed function words. No nouns.
- **Blend**: 0.72 register, 0.16 fw, damped char, damped Delta. Cut **0.30**.
- **Metric**: macro-F1. Accuracy lies (16/4 → 0.800 acc, 0.444 macro-F1).
- **Topic**: 19 quiet, 08 loud. If that flips, you leaked topic.
- **Hard miss**: problem-13, `same_register_miss`.
- **Chat wiggle**: problem-21 false alarms.
- **Gift hit / paste miss**: 25 vs 26.
- **CLI**: `hingemark explain FILE`, `eval`, `calibrate --loo`, `trap`.
