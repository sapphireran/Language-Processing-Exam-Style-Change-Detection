# Named errors

Give the miss a name in the oral. "It failed" is not an answer.

| name | what you see | house example |
| --- | --- | --- |
| `same_register_miss` | gold fold, predicted zeros, two notebooks | problem-13 … 18 |
| `topic_false_alarm` | gold zeros, a content model would fire | problem-19, 20 (we stay quiet) |
| `chat_jitter` | gold zeros, we fire anyway on wire units | problem-21 |
| `return_undercount` | folds correct, `authors` naive is 3 not 2 | problem-22 |
| `false_fold` | extra 1 next to a real hinge | none on this revision's easy/medium |
| `off_by_one` | peak on the neighbouring cut | a risk if length is put back in L1 |

## What we do *not* call an error

Missing a hard pair is the advertised behaviour of a closed-class
peak-picker. Do not apologise for it; explain it. Two bellfounders
share *we*, hedges, and the absence of contractions. `d` is small.
The gold hinge is a claim about identity, not about register.

## What we do call an error

If an easy kiln→notice document misses the middle cut, the blend is
broken. The corpus tests refuse that. If the stall topic-control
grows a fold, someone put char-3 or length back into `d`.

## Author count is a separate error

The detector's `authors` field is `1 + sum(predicted folds)`. It is
not a clusterer. On problem-22 the folds are exact and `author_ok`
is false. That is `return_undercount`, not a boundary miss.
