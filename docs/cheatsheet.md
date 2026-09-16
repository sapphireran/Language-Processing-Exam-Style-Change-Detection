# Cheatsheet

- **Task:** n units → n−1 bits. 1 = author change at that boundary.
- **Intrinsic:** no reference authors. Compare the document to itself.
- **Trust:** function words, punctuation, contractions, char trigrams.
- **Do not trust:** content nouns, raw TTR on short units, accuracy.
- **Delta:** mean |z-diff| on a closed list. Sample = this document.
- **Score:** 0.35 fw + 0.10 trigram + 0.40 register scalars + 0.15 bounded Delta.
- **Default cut:** 0.42. Adaptive: mean + 0.85 std, floor 0.22.
- **Metric:** macro-F1. Never-fire 16/4 → 0.444 F1, 0.80 acc.
- **Easy vs Hard:** if only Easy works, you measured topic.
- **Ethics:** a seam is a hypothesis. No names in the JSON.
- **CLI:** `python -m seamtrace inspect FILE`
- **Table:** `python scripts/run_curriculum.py`
