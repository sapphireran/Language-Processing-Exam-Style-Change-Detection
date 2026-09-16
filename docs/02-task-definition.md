# Task definition

## Informal statement

A document is a sequence of paragraphs \(p_1, p_2, \ldots, p_n\) written
in English. Each paragraph has exactly one author. Authors may repeat
later in the document. The job is **not** to name the authors. The job is
to emit a binary vector

\[
\mathbf{c} = (c_1, c_2, \ldots, c_{n-1})
\quad\text{where}\quad
c_i =
\begin{cases}
1 & \text{if author}(p_i) \neq \text{author}(p_{i+1}) \\
0 & \text{otherwise.}
\end{cases}
\]

A one-paragraph document has an empty change array. A four-paragraph
document always has exactly three labels.

## Why “intrinsic”

**Extrinsic** authorship analysis compares a questioned text to a set of
candidate authors who have already given you writing samples. **Intrinsic**
analysis is the no-candidates setting: the only evidence is internal
variation inside the document itself. Style change detection is the
intrinsic problem. That is why it is the right tool when you suspect
unattributed contribution or plagiarism but have no comparison corpus.

## Legal change sites

By construction of the exam (and of the PAN 2023-style setup these notes
follow):

- A change may occur only at a paragraph boundary.
- A paragraph is never mixed-author.
- The number of authors is unbounded and is **not** required as output.
- Topic and authorship may move together (Easy) or not (Hard).

If an exam question asks you to mark a change *inside* a sentence, the
answer is: the task forbids it. Tokenise, then snap to the nearest legal
boundary, or say the instance is ill-posed.

## File format

Problems live in a directory as UTF-8 text:

```
problem-001.txt
truth-problem-001.json
```

Read text with `open(path, "r", encoding="utf-8", newline="")` so that
blank-line boundaries survive. Paragraphs are blocks separated by a blank
line. Truth looks like:

```json
{
  "authors": 2,
  "changes": [0, 1, 0]
}
```

A system writes only the prediction:

```json
{
  "changes": [0, 1, 0]
}
```

`authors` is supervision for analysis, not a required output of the
detector. The baseline in this repo ignores it at prediction time.

## Difficulty split

The three-way split is not “more authors” versus “fewer authors”. It is
a **topic-control** gradient.

| Split | Topic structure | What a lazy model can use |
| --- | --- | --- |
| Easy | Adjacent authors often discuss different things | Content words, named entities, coarse embeddings |
| Medium | One situation, two registers | Some leftover topical cues plus style |
| Hard | One topic, similar registers | Style almost alone |

The control split in `examples/data/control/` is extra: single-author
documents used to measure **false-positive rate**. PAN-style test sets
include single-author texts; an exam answer that never mentions them is
incomplete.

## Worked length check

For `examples/data/easy/problem-001.txt`:

- 4 paragraphs
- truth `changes = [0, 1, 0]`
- authors = 2 (cooking voice, then planning voice)
- the `1` sits between leftover-pasta and municipal sidewalks

If your system emits 4 numbers, you have labelled paragraphs instead of
boundaries. That is the most common off-by-one in this task.

## What the task is not

| Nearby problem | Why it is different |
| --- | --- |
| Authorship attribution | Needs candidate authors and comparison texts |
| Authorship verification | Pair of documents, not a sequence of spans |
| Clustering paragraphs into author IDs | Stronger output; PAN has used it in other years |
| Plagiarism source retrieval | Needs an external collection |
| Topic segmentation (TextTiling, C99) | Optimises topical coherence, not habit |

You can *use* a topic segmenter as a baseline on Easy. You must not
*define* the task as topic segmentation.

## Output contract for software

A command-line tool should accept a directory of `problem-*.txt` files
and write one `solution-problem-*.json` per input. This repo:

```bash
python -m stylechange.cli detect examples/data/easy -o /tmp/easy-out
python -m stylechange.cli eval examples/data/easy
```

The second command scores against `truth-problem-*.json` in the same
folder. See [05-evaluation.md](05-evaluation.md) for the metric.
