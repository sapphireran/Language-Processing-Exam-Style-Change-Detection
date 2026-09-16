# What the task actually asks

Style-change detection is an **intrinsic** authorship problem. You are
handed one document and no comparison texts. The question is not "who
wrote this?" It is "where does the writing habit change?"

PAN at CLEF 2023 stated the operational version used in this exam kit:

- Input: an English document whose paragraphs are the atomic units.
- Assumption: a paragraph has exactly one author. Cuts happen *between*
  paragraphs, never inside them.
- Output: for every pair of consecutive paragraphs, emit `0` (same
  author) or `1` (author change).
- Score: F1 on that binary vector, computed independently on easy,
  medium, and hard splits.

The three difficulty bands exist because earlier shared tasks leaked
**topic** as a cheap proxy for authorship. If paragraph 3 is about
lighthouses and paragraph 4 is about tax law, a bag-of-words model can
shout "change" without ever seeing style.

| Band   | Topic structure                         | What a fair system must do      |
|--------|-----------------------------------------|---------------------------------|
| Easy   | Adjacent authors often change topic     | Topic cues are allowed, not required |
| Medium | Topic variety is small                  | Style has to do real work       |
| Hard   | All paragraphs share one topic          | Style is the only honest signal |

## Files

For a problem id `X`:

| File                         | Role                                      |
|------------------------------|-------------------------------------------|
| `problem-X.txt`              | Raw text. Open with `newline=""` in Python |
| `truth-problem-X.json`       | Gold `changes` plus optional `authors`    |
| `solution-problem-X.json`    | What a system must write                  |

A four-paragraph document has **three** boundaries. If authors go
A, A, B, B the gold vector is `[0, 1, 0]`.

The CLI in this repo mimics the PAN command shape:

```text
python3 -m splicefind detect-dir -i INPUT-DIRECTORY -o OUTPUT-DIRECTORY
```

That is enough to talk about software submission on TIRA without
claiming this kit was ever submitted.

## What the task is *not*

- It is not author attribution. There is no candidate set.
- It is not plagiarism detection against a web index. There is no
  external collection.
- It is not topic segmentation, even though topic shifts often
  coincide with author shifts in the easy band.
- It is not a request to recover the true number of authors, although
  `1 + sum(changes)` is a lower bound if you never assign the same
  author on both sides of a missed cut.

If an examiner asks "why paragraph level?", a clean answer is: the
2023 task designers treated the paragraph as a unit that is long
enough to estimate a few rates and short enough that mixed authorship
inside it can be ignored by construction.
