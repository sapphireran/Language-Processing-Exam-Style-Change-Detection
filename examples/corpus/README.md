# Original corpus

Twenty-eight documents I wrote for this exam repo. Not PAN data, not
Reddit, not a workplace corpus, not a shared-task dump.

| band    | ids        | what it is for                                      |
| ------- | ---------- | --------------------------------------------------- |
| control | 01–04      | one house; the saw must stay shut                   |
| easy    | 05–10      | house and topic jump together                       |
| medium  | 11–15      | same topic, different house                         |
| hard    | 16–19      | same topic, houses that share a register            |
| trap    | 20–23      | topic jumps, house stays                            |
| return  | 24–26      | ABA; two real hinges                                |
| collage | 27–28      | three or four houses                                |

Holdout codes: **04, 10, 15, 19, 23, 26, 28**. Tune the penalty on the
other twenty-one. Quote holdout last.

Each `problem-*.txt` is blank-line paragraphs. Each
`truth-problem-NN.json` has `changes`, `authors`, `houses`, `band`,
and `holdout`. House names are for me, not for the detector.

`bank.py` is the source. `python3 -m examples.corpus.emit` rewrites
the text, truth, and `manifest.json`.

See `houses.md` for the six voices.
