# PAN-shaped I/O

The shared task is not this repo. I still copy its contract so an
exam answer can move from a toy file to a real one without
changing shape.

## Input

`problem-X.txt` is the document. Read it with
`open(path, "r", newline="")` so a Windows file does not grow
ghost breaks. `truth-problem-X.json` has at least:

```json
{
  "authors": 2,
  "changes": [0, 1, 0]
}
```

`changes[i]` is the hinge between unit `i` and unit `i+1`.
`0` is the same hand. `1` is a new hand. The array is always
one shorter than the unit list.

This lab's truth files also carry `houses`, `topics`,
`difficulty`, `holdout`. Those keys are for me. The detector
never reads them.

## Output

`solution-problem-X.json` is only:

```json
{
  "changes": [0, 1, 0]
}
```

The CLI copies the shared-task call:

```
python3 -m isogloss predict -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY
```

## Units in this lab

PAN asks for **sentences**. My original bank uses **blank-line
paragraphs** so a house can speak for fifty to ninety words. A
rate estimated on eight words is a twitch. A rate estimated on
sixty words is a map. If a file has no blank line, `split_units`
falls back to a conservative sentence split.

In an oral I say this out loud: the *decision* is still a hinge
between consecutive units. The unit is thicker than a sentence
because I wrote the bank, not because I think PAN is wrong.

## Difficulty bands (the real task)

- **Easy:** topic and author may move together. A bag-of-words
  cheat almost works. I still refuse nouns.
- **Medium:** less topical variety. Style has to do more.
- **Hard:** one topic. Nouns are a liar. Closed class is the job.

My bank mirrors those bands with *house* and *topic* tags I
control. A trap is the extra band I need for an exam: topic
moves, house does not.
