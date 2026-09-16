# Live results on this revision

Default detector: `EnsembleDetector(threshold=0.30, sure=0.45,
register_floor=0.18)`. Numbers from `python3 -m inkfold score` after
the corpus retune. If you edit a teaching sentence, rerun and replace
this page.

## Headlines

| row | accuracy | macro-F1 | fold F1 | N |
| --- | ---: | ---: | ---: | ---: |
| detector (pooled) | 0.932 | 0.898 | 0.840 | 117 |
| never-fire | 0.769 | 0.435 | 0.000 | 117 |
| mean per-document macro-F1 | — | 0.790 | — | 26 docs |

Never-fire is *more accurate* and a worse answer. That is the trap.

117 boundaries, 27 gold folds, 90 gold seams.

Detector: tp=21 fp=2 tn=88 fn=6.

The six false negatives are the six hard documents (one gold fold
each, all missed). The two false positives are both on
`problem-21-chat-three-topics`.

## By site

| site | acc | macro-F1 | fold F1 | what happened |
| --- | ---: | ---: | ---: | --- |
| easy | 1.000 | 1.000 | 1.000 | every register flip exact |
| medium | 1.000 | 1.000 | 1.000 | same topic, two genres, exact |
| hard | 0.800 | 0.444 | 0.000 | all six `same_register_miss` |
| control | 0.867 | 0.464 | 0.000 | stall+notice quiet; chat jitters |
| return | 1.000 | 1.000 | 1.000 | folds exact; naive authors = 3 |
| collage | 1.000 | 1.000 | 1.000 | three- and four-voice hits |
| gift | 1.000 | 1.000 | 1.000 | student → supervisor |
| paste | 1.000 | 1.000 | 1.000 | two exam answers |

Per-document macro-F1 on `problem-23` is 0.5 even though the change
list is exact: there are no seams, so seam-F1 is 0/0. The collage
*site* still reports 1.0 because problem-26 has seams.

## Documents the oral should name

- **Hit:** `problem-01-kiln-then-notice` — stall → notice after unit 3.
- **Miss:** `problem-13-two-bellfounders` — gold hinge, predicted zeros.
- **Topic quiet:** `problem-19-stall-three-topics` — dumplings / bus / cat.
- **Jitter:** `problem-21-chat-three-topics` — two false folds.
- **Return:** `problem-22-kiln-return` — exact folds, `author_ok` false.
- **Gift:** `problem-24-gift-abstract` — hedges out, shall/must in.

## What these numbers are not

They are not a PAN leaderboard score. They are a teaching folder
whose hard documents were written to be missed and whose easy
documents were written to be hit. Quote them as *this revision, this
folder,* not as "the method achieves 0.90 F1."
