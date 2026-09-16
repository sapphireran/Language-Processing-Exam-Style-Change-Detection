# Revision circuit

A 90-minute loop that uses this repository instead of rereading
slides.

## 0–15 min — contract

Read [01](01-what-the-exam-asks.md) and [02](02-pan-io-contract.md).
On paper, write a `changes` array for a 7-sentence document with
a seam after sentence 3 and a return author at sentence 6.
Check: length 6, not 7.

## 15–35 min — features

Read [04](04-feature-atlas.md) and [06](06-delta-and-closed-class.md).
Run:

```
PYTHONPATH=src python3 -m seamtrace features examples/corpus/problem-14-two-bakers.txt
```

Write down first-person rate and contraction rate on each side of
the labelled seam. If they do not move, your intuition about the
document is wrong — reread the file.

## 35–55 min — curriculum table

```
PYTHONPATH=src python3 scripts/run_curriculum.py
```

Copy Easy / Medium / Hard / Control macro-F1 for `threshold`.
Read [07](07-topic-is-not-style.md) and [08](08-metrics-and-why-accuracy-lies.md)
with those numbers in the margin.

## 55–70 min — one miss

```
PYTHONPATH=src python3 -m seamtrace inspect examples/corpus/problem-14-two-bakers.txt
```

Pick a non-`genuine_*` row. Name it with the taxonomy. That is
your oral example.

## 70–80 min — ethics and limits

Read the gift-authorship card and Q5 in
[12-written-model-answers.md](12-written-model-answers.md).
Say out loud one sentence you will *not* write in a solution file.

## 80–90 min — formula card

Cover [14](14-formula-card.md) and reproduce the 16/4 never-fire
example from memory. Run
`PYTHONPATH=src python3 scripts/check_hand_calculation.py` if you
hesitate.

## After a break

Swap the detector:

```
PYTHONPATH=src python3 scripts/run_curriculum.py --detector adaptive
```

If Hard improves and Control collapses, you now have a calibration
story for [09](09-calibration.md).
