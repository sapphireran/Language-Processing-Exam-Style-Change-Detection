# Live results

Generated from `python3 -m kerf score examples/corpus` on this
revision. If the numbers here and the CLI disagree, the CLI is
right and this page is stale.

Blade: first-cut penalty 0.22, recurse 0.40, adjacent floor 0.40.
84 hinges across 28 documents.

## Stacked hinges

| predictor | macro-F1 | hinge acc | f1-change | f1-same | tp | fp | fn | tn |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| never-fire | 0.404 | 0.679 | 0.000 | 0.809 | 0 | 0 | 27 | 57 |
| always-fire | 0.243 | 0.321 | 0.486 | 0.000 | 27 | 57 | 0 | 0 |
| kerf | 0.986 | 0.988 | 0.981 | 0.991 | 26 | 0 | 1 | 57 |

Never-fire accuracy is 0.679 because 57 of 84 hinges are zeros.
That is the whole point of the metrics note.

Document-mean accuracy is 0.988. Document-mean macro-F1 is 0.80
because every all-zero control/trap file scores 0.50 (no change
class to hit). I do not headline that 0.80.

## In-band vs holdout

Holdout codes: 04, 10, 15, 19, 23, 26, 28.

| split | macro-F1 | hinge acc | tp | fp | fn | tn |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in-band (21 docs) | 0.981 | 0.984 | 18 | 0 | 1 | 44 |
| holdout (7 docs) | 1.000 | 1.000 | 8 | 0 | 0 | 13 |

The blade was not moved after looking at holdout. Perfect holdout
on a seven-file toy split is a quote, not a generalisation.

## By band

| band | macro-F1 | acc | tp | fp | fn | tn | note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| control | 0.500 | 1.000 | 0 | 0 | 0 | 12 | no positives, so change-F1 is 0 |
| easy | 1.000 | 1.000 | 6 | 0 | 0 | 12 | |
| medium | 1.000 | 1.000 | 5 | 0 | 0 | 10 | |
| hard | 1.000 | 1.000 | 4 | 0 | 0 | 8 | |
| trap | 0.500 | 1.000 | 0 | 0 | 0 | 12 | topic jumps, house stays |
| return | 1.000 | 1.000 | 6 | 0 | 0 | 3 | ABA recovered by the floor |
| collage | 0.455 | 0.833 | 5 | 0 | 1 | 0 | the live miss |

Collage macro-F1 looks grim because those files have almost no
true `same` hinges, so `f1-same` collapses. The actual event is
one missed hinge.

## The live miss

`problem-27-stilling-four-houses`, last hinge, Seminar → Pocket,
same stilling well. Adjacent step ≈ 0.30, inside the same-house
cloud (document 13's last same-house step is ≈ 0.32). See
[error taxonomy](13-error-taxonomy.md).
