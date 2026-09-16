# Delta, n-grams, and CUSUM

Three supporting pictures. None of them is the default cut.

## Intra-document Delta

Classic Burrows' Delta z-scores function-word rates against a **reference corpus**, then takes a mean absolute difference. Inside one exam document there is no reference corpus, so we z-score each function word across the document's own units and compare neighbours.

On an 8-unit file the z-score is brittle: a word that appears once gets a huge z. The blender therefore squashs Delta with `d / (1 + d)` and keeps its weight small (0.06).

Say in the oral: "Delta wants a corpus. A document is not a corpus."

## Character n-grams

Useful when units are long enough to share morphology (*-tion*, *ing*, British *-our*). On this corpus they mostly measure "these two strings are not the same," which is not authorship. Damped.

## CUSUM

Plot `sum(score_i - mean)` along the hinge axis. A persistent new writer often changes the slope. A single loud hinge is a spike, not a new slope.

CUSUM on six hinges is a cartoon. Use it as a picture in `hingemark explain` (the peak index is printed). Do not submit a CUSUM cut as your only answer. Problem-26 exists so you can say that out loud: the student answer prefers pairwise, the pasted academic answer still likes CUSUM as a diagnostic.

## Default blend

```
blend = 0.72 * register_gap
      + 0.16 * (1 - cosine_smoothed_fw)
      + 0.06 * (0.45 * char_cosine_distance)
      + 0.06 * (delta / (1 + delta))
```

Register carries the lab. The other three are allowed to argue, not to drive.
