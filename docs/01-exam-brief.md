# 01 — Exam brief

I keep losing marks when I answer a neighbouring question. This page is
the question they actually asked.

## The one-sentence version

Given **only the document**, mark every place where the **writer
changes**.

Not: who wrote it. Not: is this Shakespeare's. Not: did they copy
Wikipedia. Those are different exams.

## Three jobs that get bundled under the same name

Older shared-task write-ups split the work. I still use their numbers
because they match how oral questions are phrased.

| # | Job | Output I must produce |
| --- | --- | --- |
| Task 1 | Style-change **basic** | One cut in a two-author text (usually paragraph grain) |
| Task 2 | Style-change **advanced** | Every cut, **and** a label per unit so a returning author gets the same id |
| Task 3 | Style-change **real-world** | Every cut at **sentence** grain |

The current "multi-author writing style analysis" wording is Task 3 with
the topic leak tightened. If the paper says "for each pair of consecutive
sentences, assess whether there was a style change", that is a binary
vector of length `n_sentences - 1`.

PAN-shaped JSON looks like this:

```json
{ "changes": [0, 0, 1, 0, 0] }
```

A `1` means the author of unit `i+1` is not the author of unit `i`.
There is no "author 3" in that file. Task 2 adds an `authors` array of
length `n_units`.

## What I am allowed to look at

**Intrinsic.** The document is the evidence. No reference folder of
known authors, no search engine, no "find the original post".

That is why the problem is hard, and why it is the only authorship
problem that still works when the comparison texts do not exist:
ghost-writing, gift authorship, some plagiarism, some collaborative
edits.

## What I am not allowed to treat as a free lunch

- **Topic shift.** Easy constructions let the subject change when the
  writer changes. A topical embedding then impersonates style. See
  [06-topic-confound.md](06-topic-confound.md).
- **Length.** A 400-word Wikipedia paragraph next to an SMS is a style
  change *and* a genre change. Say so.
- **Gold grain.** If they labelled paragraphs and I emit sentence cuts,
  my F1 is not comparable. Align the units first.

## The answer shape I use in a written paper

1. Define the units (sentence or paragraph) and the output vector.
2. Name the feature families and say which one I trust when topic is
   held still.
3. Say how I turn adjacent distances into binary cuts (threshold, gap,
   or a supervised pair classifier).
4. Name the metric (macro-F1 on pairs). Mention the empty-class
   convention if the document is single-author.
5. List two failure modes (short units; topic leak).

If I skip step 5 I sound like a blog post.

## Twenty-minute baseline I would actually write

If they hand me a laptop and thirty minutes I will not fine-tune
DeBERTa.

1. Split into the units they specified.
2. Score each unit on a closed cue sheet (slang, imperative, formal,
   notes, we-academic, one-academic, diary, lab).
3. Cut when the cue label changes. Character 3-grams and function-word
   L1 stay in the report so I can show *why* the cut looks like a cut;
   I do not threshold raw pair cosine on six-word sentences.
4. If they want author ids, reuse a label when it returns (chair after
   the intern; cook after the scientist).

That is exactly what `examscd` does. It is a teaching baseline. I will
not claim it wins a shared task.

## Words I will not mix up

| Term | Means | Does not mean |
| --- | --- | --- |
| Attribution | Name the author from a candidate set | Find the cuts |
| Verification | Same person or not, given two texts | Count the authors |
| Profiling | Infer age / gender / personality | Mark boundaries |
| Intrinsic plagiarism | Style outlier inside one document | Google the sentence |
| Style change | Boundary between writers | Boundary between topics |

If the question says "detect style change" and I spend a page on
tf–idf retrieval against a candidate set, I have answered attribution.
