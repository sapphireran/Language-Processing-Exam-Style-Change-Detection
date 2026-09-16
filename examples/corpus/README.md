# Teaching corpus

Twenty-six original documents. One sentence per line. PAN-flavoured
`problem-*.txt` plus `truth/truth-*.json`.

Nothing here is from a shared-task dump. The topics (kiln, dumpling
stall, paper marbling, ice hut, stained glass, late-night radio,
climbing gym, seed library, cooperage, locksmith, bookbinding, harbour
minutes, bellfounding, map colouring, organ tuning, fog signals, night
clerk, gift abstract) were written for this exam lab.

## Sites

| site | what it tests | default detector |
| --- | --- | --- |
| easy | loud register fold (stall/letter/chat → notice) | should hit |
| medium | same topic, two genres | should hit |
| hard | two specialists, same notebook register | allowed miss (`same_register_miss`) |
| control | one author, three topics | should stay quiet; chat may jitter |
| return | A, B, A | folds ok; naive author count is wrong |
| collage | three or four house voices | should hit every fold |
| gift | student abstract then supervisor rewrite | should hit |
| paste | two exam answers | should hit |

## Contract

`len(changes) == n_units - 1`.

If `return_author` is false, `authors == 1 + sum(changes)`.

If `return_author` is true, that equality is *supposed* to fail. See
`problem-22-kiln-return`: two authors, two folds, naive count 3.

## Regenerate

```bash
PYTHONPATH=src python3 scripts/export_corpus.py
```

The bank is the source of truth. Do not edit a `problem-*.txt` by hand
and forget the bank.
