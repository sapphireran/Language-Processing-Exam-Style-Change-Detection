# One-page cheat

- Unit: blank-line paragraph here; sentence in the real task.
- Output: `changes` has length `n_units - 1`. `1` means a new hand.
- Features: person, contractions, deontics, hedges, formal/oral
  connectives, *the*, digits, shape. **No nouns.**
- Jump: `z_i,f = (x_i,f − x_{i+1,f}) / (s_f + ε)`
- Mark: `|z| ≥ max(ζ, ρ · peak_f)`
- Fire: at least `k` marks. Default `ζ=0.90`, `ρ=0.70`, `k=3`.
- Quote **macro-F1**, not accuracy. Never-fire lies.
- Easy: house and topic move. Hard: only the house. Trap: only the topic.
- Holdout: 04 / 10 / 16 / 22 / 26 / 30.
