# Error taxonomy

I want names for misses so I do not say "it felt off".

## False change (fp)

- **Wrinkle:** one channel (digits, `n_words`) jumped; votes
  still reached `k` because shape channels piled on. Fix:
  stop letting shape dominate, or thicken the units.
- **Topic twitch inside a house:** I under-wrote the house.
  Twine lost its hedges on the second craft. Fix the prose.
- **ABA middle:** should not happen with window 1. If it
  does, I accidentally wrote the middle house like a blend.

## False same (fn)

- **Near pair:** Roll ↔ Brine, or a shy Skiff ↔ Twine
  (both contract). Not enough maps moved.
- **Short unit:** Flint is allowed to be short; Vellum is
  not. If Vellum is forty words, *however* is one token and
  `s_f` is junk.
- **Coward k:** five honest marks that I refused because I
  set `k=5` after staring at a trap.
- **Peak theft:** ρ too high, ABA return quieter than the
  first cut, second seam unmarked.

## Errors I will not call errors

- Predicting change on a file where I, the writer, cannot
  say which channels should flip. That is a bank error.
- A transformer that rides *eel* / *hop* on an easy file
  and dies on document 19. That is the easy-band cheat.

## How I log one

```
problem-id  gold  pred  votes  top channels  name of the miss
```

The inspect table already has the middle columns. The last
column is the oral.
