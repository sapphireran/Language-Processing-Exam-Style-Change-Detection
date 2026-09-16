# 08 — CLI lab session

Python 3.10+, no extra packages.

```bash
export PYTHONPATH=src
python3 -m scarfjoint split examples/corpus/easy/problem-01-ferry-marsh-knit.txt
python3 -m scarfjoint features examples/corpus/easy/problem-01-ferry-marsh-knit.txt
python3 -m scarfjoint detect examples/corpus/easy/problem-01-ferry-marsh-knit.txt --explain
python3 -m scarfjoint eval examples/corpus
python3 examples/compare_channels.py
python3 examples/walk_worked_example.py
python3 -m unittest discover -s tests -v
```

## What to look at, in order

1. **Split.** Confirm blank lines became the paragraphs you think
   they did. If a document shows one giant paragraph, you lost the
   blank lines.
2. **Features.** First-person rate should drop when the voice goes
   academic. Guiraud should usually rise. If both stay flat across a
   gold join, you wrote two paragraphs in the same register.
3. **Detect --explain.** The line `topic-distance=… (not a vote)`
   should be high on easy joins and uninformative on hard ones.
4. **Eval.** Mean F1 on this collection is a lab number. Read the
   per-document exact/error flags before you believe the mean.
5. **compare_channels.py.** Prints style combined vs topic Jaccard
   for every gold boundary. Easy gold 1s should show both high; hard
   gold 1s should show style still moving after topic has flattened.
6. **Worked example.** If those printed numbers drift from
   `docs/05-worked-example.md`, the tokeniser changed and the notes
   are stale.

## PAN-shaped batch

```bash
python3 -m scarfjoint predict-dir examples/corpus/easy /tmp/scarfjoint-out
ls /tmp/scarfjoint-out
```

Each `problem-*.txt` becomes `solution-problem-*.json` with a
`changes` array and nothing else.

## Leakage switch

```bash
python3 -m scarfjoint eval examples/corpus
python3 -m scarfjoint eval examples/corpus --use-topic
```

The second run is allowed to use content-word Jaccard as a vote.
Write down both means. The story you want: easy improves more than
hard.
