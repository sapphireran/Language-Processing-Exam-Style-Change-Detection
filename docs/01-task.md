# The task: find where the writer changes

Intrinsic style-change detection asks a narrow question. You are given
one document. You do not get candidate authors, comparison texts, or a
closed set of names. For every pair of consecutive paragraphs you answer
yes or no: did the writer change here?

If a document has paragraphs `P1, P2, P3, P4`, the answer is a vector of
length 3. That vector is the entire prediction.

```text
P1  --0-->  P2  --1-->  P3  --0-->  P4
```

The gold file in this repo writes that as `{"changes": [0, 1, 0]}`.

## What “intrinsic” rules out

Extrinsic authorship methods compare a disputed text to writing samples
with known authors. Those methods are powerful when the samples exist.
They are unavailable for the exam-style problem this repository studies:
the only evidence is variation inside the document.

That restriction is the point of the exercise. It is also why the task
shows up in discussions of plagiarism with no source, gift authorship,
and writing-support tools. If you cannot look the writer up, you have to
look at the seams.

## Units and assumptions

The examples here follow the usual exam / shared-task contract:

- A paragraph has one author. Changes happen at boundaries, not inside
  a paragraph.
- Documents are English.
- Author count is not fixed. A document may be one writer or several.
- Topic may or may not move when the author moves. That is a difficulty
  knob, not a promise.

The last bullet is the one that fools shallow systems. If hiking chat is
followed by a climate memo, almost any lexical detector will fire, and
it will be right for the wrong reason. Medium and hard examples keep the
topic still so the model has to notice register, function words, rhythm,
and punctuation habits instead.

## Input and output

Problem files are UTF-8 text. Blank lines separate paragraphs. Truth
files are JSON:

```json
{
  "authors": 2,
  "changes": [0, 1, 0]
}
```

`authors` is metadata for humans and for the walkthrough. The metric
only sees `changes`. A submitted solution file stores the same binary
array and nothing else:

```json
{
  "changes": [0, 1, 0]
}
```

The CLI in this repo writes `solution-problem-<id>.json` next to that
contract so a directory of predictions can be scored in one call.

## A pipeline that fits on an exam answer

1. Segment paragraphs.
2. Represent each paragraph (stylometric vector, character n-grams,
   function-word distribution, or all three).
3. Compute a distance between adjacent representations.
4. Threshold the distances. Adaptive thresholds matter: a single-author
   document should not be forced to produce a `1`.
5. Report macro-F1 over the two classes `{0, 1}`.

That is the whole system implemented under `src/style_change/`. Neural
encoders can replace step 2 later. They do not change the rest of the
diagram, and they are not required to understand the problem.

## Failure modes worth naming

- **Topic leakage.** The detector is a topic-segmenter in disguise.
- **Class imbalance.** Most boundaries in realistic data are `0`. Always
  predicting `0` can look decent on accuracy and terrible on macro-F1.
- **Short paragraphs.** Type-token ratio and hapax rate are noisy below
  a few dozen tokens. The sample documents are written long on purpose.
- **Global thresholds.** A cut that works on easy mixed-topic documents
  will over-fire on a homogeneous control if it is not allowed to adapt.

`docs/02-stylometry.md` lists the features. `docs/03-evaluation.md`
spells out the metric. `docs/04-walkthrough.md` runs the CLI on the
sample splits.
