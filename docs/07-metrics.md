# Metrics, and why accuracy lies

Most hinges in a real document are `0`. A person does not change at
every paragraph. A system that predicts all zeros — **never-fire** —
therefore looks accurate and finds nothing.

PAN reports F1. I report four numbers every time I score the bank:

- **per-document F1**, with a special case: if gold and pred are both
  all zeros, F1 is 1.0 (a single-author document correctly left alone)
- **macro-F1** — unweighted mean of those per-document scores
- **micro-F1** — pool every hinge, then F1
- **accuracy** — so I can point at it and tell it to sit down

## The special case, written out

```
tp, fp, fn = usual counts of change-bits
if tp == fp == fn == 0: F1 = 1
else: F1 = 2PR / (P+R) with the usual zeros
```

Without that clause, a correct control document is `undefined` or
`0`, and the never-fire baseline cannot be discussed honestly.

## Macro versus micro

Macro treats a four-hinge control document as equal to a four-hinge
collage. That is what I want for an exam: each *document situation*
gets a vote. Micro lets a bank with many easy hinges dominate. I print
both. I quote macro unless someone asks.

## The table I always show

```
predictor              macro-F1   micro-F1   mean acc
never-fire (all 0)     low-ish    low-ish    high
always-fire (all 1)    worse      worse      low
quoin                  higher     higher     whatever
```

If never-fire wins on accuracy, the point is made. If it also wins on
F1, my detector is not doing its job and I will say so.

`python -m quoin baselines` prints this table on the live bank.
