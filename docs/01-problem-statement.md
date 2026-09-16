# Problem statement

## One-sentence version

Given a single English document segmented into sentences, label every
consecutive pair as **same author** (`0`) or **author change** (`1`).

## Formal version

Let a document be a sequence of sentences \(S = (s_1, s_2, \ldots, s_n)\),
\(n \ge 2\). A style-change detector is a function

\[
f(S) = (y_1, y_2, \ldots, y_{n-1}), \qquad y_i \in \{0, 1\}
\]

where \(y_i = 1\) if and only if \(s_i\) and \(s_{i+1}\) were written by
different authors. The detector is **intrinsic**: it may inspect \(S\) and any
statistics derived from \(S\), but it does not receive named candidate authors
or external reference corpora at test time. A supervised detector may of
course have been fit on *other* labeled documents beforehand.

## Constraints that matter on the exam

1. **Sentence integrity.** A sentence has exactly one author. Changes occur
   only at sentence boundaries.
2. **Unknown author count.** \(S\) may be single-author (the zero vector) or
   may contain an arbitrary number of switches.
3. **Unknown author identity.** Labels are *changes*, not author IDs. Two
   non-adjacent blocks can be the same person returning; the gold file in this
   repo happens to include `author_ids` for study, but a submitted solution
   must not be required to recover them.
4. **Topic is not style.** Easy data lets topic leak. Hard data forbids it.
   An answer that only discusses TF–IDF will lose marks on the hard split.
5. **Class imbalance.** Most adjacent pairs are `0`. Always predicting `0`
   can look accurate and still fail macro-F1.

## Three difficulty regimes

The synthetic set copies the pedagogical structure used in recent
multi-author writing-style analysis shared tasks, without using their text.

### Easy — topic and style move together

Author A writes three sentences about reef ecology. Author B writes three
sentences about a ruined dinner. A unigram model will fire on *coral* vs
*pan*. That is allowed on the easy split and forbidden as an explanation of
the hard split.

Use easy data to debug I/O, the sentence splitter, and the evaluation
script. Do not use it to claim that your features “capture style”.

### Medium — one subject, several angles

Everyone is writing about city cycling, but one author discusses frame
geometry, another describes a commute, a third writes a short scene at a
red light. Topic overlap is high; residual lexical cues remain
(*bottom bracket* vs *I nearly missed the light*).

Medium is the split where a mixed detector (style features + a little
content) looks tempting. The honest write-up says which signal did the
work.

### Hard — one subject, held still

Every sentence is about brewing a pour-over. Vocabulary is forced to
overlap: water, kettle, filter, bloom, mug. What remains is rhythm,
stance, hedging, punctuation, and pronoun habit.

If your detector dies here, it was a topic detector. That is the intended
lesson.

## Output contract

For each `problem-X.txt` produce `solution-problem-X.json`:

```json
{ "changes": [0, 0, 1, 0] }
```

Length must equal the number of sentence pairs. A length mismatch is an
I/O bug, not a modelling disagreement, and the evaluator treats it as a
hard failure for that document.

## What a full-mark exam answer usually contains

- A definition of the task that mentions *intrinsic* and *sentence pairs*.
- At least one baseline (majority class) and one non-trivial detector.
- A feature list that would still function if the topic were held constant.
- Macro-F1, with a one-line defence of why accuracy is insufficient.
- A limitation paragraph: short sentences, quoted speech, and a single
  author changing register (email vs essay) all look like author changes.

The rest of this folder expands each of those points.
