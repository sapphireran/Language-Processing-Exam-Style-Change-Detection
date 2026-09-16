# Error taxonomy

Every pair that Seamtrace scores can carry a label. Use the label
in the oral instead of "it got that one wrong."

| Label | Gold / pred | Typical cause |
| --- | --- | --- |
| `genuine_hit` | 1 / 1 | Register or topic+register jump |
| `genuine_stay` | 0 / 0 | Same author, score below cut |
| `topic_confound` | 0 / 1 | Content nouns jumped; function words did not |
| `single_author_drift` | 0 / 1 | Score cleared the cut in a labelled stay |
| `short_unit_noise` | either miss | One side has ≤6 tokens |
| `threshold_near_miss` | 1 / 0 | Score sat close to the cut |
| `register_only` | 1 / 0 | Function-word / Delta moved; blend still missed |
| `unlabelled` | — | Test-style file, no gold |

## How to use this in a paragraph

> Pair 4 on the rye document is a `register_only` miss: first
> person and contractions drop, but the blended score is 0.31
> against a 0.42 cut. Raising the function-word weight would catch
> it and would also create a `topic_confound` on the vellum
> document's internal topic aside.

That paragraph scores marks. "We need a bigger model" does not.

## Do not overfit the taxonomy

The rules in `explain.py` are if-then heuristics. If both topic
and register move, a false alarm still might tag `topic_confound`.
Read the four channel numbers before you believe the tag.

## Suggested table for the write-up

Count labels over the whole corpus for the default threshold
detector. The interesting row is `topic_confound` vs
`register_only`. A stylometric system should have few of the first
and some of the second. A bag-of-words system is the other way
around.
