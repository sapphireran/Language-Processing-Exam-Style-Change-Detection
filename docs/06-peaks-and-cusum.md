# Peaks, sure-folds, and a CUSUM sketch

## Adjacent comparison is the pencil method

At the cut after unit `i`, compare unit `i` to unit `i+1`. That is
what you can do in the margin of a script. Prefix-versus-suffix is a
pretty picture for a *single* hinge and a lie for a returning author
(both sides of a true fold are mixed).

The program's default score is 65% adjacent plus 35% a two-unit
window, so a one-line chat fragment does not decide the whole cut.

## Two firing rules

Let `s_i` be the hinge score at cut `i`, `τ = 0.30`, `σ = 0.45`.

1. **Sure fold:** `s_i ≥ σ` — fire even if a neighbour is slightly louder.
2. **Peak fold:** `s_i ≥ τ` and `s_i` is a local maximum.

A three-voice collage has three loud cuts; the middle one is often a
little quieter. Rule 1 is what lets it fire. Say this in the oral so
you do not sound like you only peak-picked.

The ensemble also refuses a fire whose register L1 is under 0.18. That
is the topic brake: function-word cosine can twitch when the subject
changes, the six rates should not.

## CUSUM is a picture, not a detector

Pick one rate, often first-person. Centre it (`x_i - mean`). Sum.
A slope change is a *candidate* fold.

```bash
PYTHONPATH=src python3 -m inkfold cusum examples/corpus/problem-01-kiln-then-notice.txt
```

CUSUM on first-person will also twitch when a stall voice simply
stops saying *I* for one line. Do not submit a CUSUM peak as an
answer unless you have checked the six-rate L1 at that cut.

## Adaptive threshold

`median + k * MAD` of the document's own scores, with a floor of
0.22. On a six-cut control document the MAD is small and the floor
does the work. On a collage the median is already high and adaptive
fires almost everything — which is correct.
