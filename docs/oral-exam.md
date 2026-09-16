# Oral-exam talking points

A 30-minute oral will not let you walk through eight files. Pick four
moves and stop.

## 1. Define the problem in one sentence

"Intrinsic style-change detection: given only this document, mark the
sentence (or paragraph) joins where the author — or at least the
register — changes. No comparison texts."

If they ask for the output shape, draw a 6-sentence document and write
`[0, 0, 1, 0, 0]` under the five joins.

## 2. Topic is the confound

Easy / medium / hard is not "small / medium / large data". It is "how
much topic drift am I allowed to lean on?" A TF–IDF cosine that jumps
when the nouns change is an easy-split detector. The hard split holds
the topic fixed on purpose.

## 3. Why not adjacent-sentence 3-grams?

Two sentences from the same person barely share character 3-grams, so
every boundary looks like a cut. Compare *blocks*, or at least windows.
This baseline names four voices, cuts on voice-band jumps, and only
then runs a change-point on binary register flags (`I`, `we`, `one`,
notes punctuation).

## 4. Register ≠ author

`chat` and `student` are different voices and the same personal band.
A student who writes "yeah" and then "I think" is one person. Two
textbook authors (*we* vs *one*) are one named voice and two people.
The hard file is the exhibit.

## 5. First-person `I` vs dummy `i`

`P(w_i)` is not a diary. The feature extractor only counts English
`I` / `I'm` / `I've`. There is a unit test for that, because it is an
easy way to look sloppy.

## 6. Evaluation

Macro-F1 over `{change, no-change}`. Accuracy is the wrong headline
because most pairs are `0`. A 1.000 on the bundled stories is a
sanity check, not a shared-task result.

## 7. Limitations (say these before they do)

- Eight hand-written documents, not Reddit.
- Voices are a closed inventory; a sarcastic textbook will fool them.
- No model of *how many* authors beyond `1 + sum(changes)`.
- No handling of a one-sentence interpolation that is a real third
  author (we deliberately absorb one-unit blips).
- English-only lexicons. A Danish take-home would need new lists.
- A fine-tuned encoder with a windowed verification loss would beat
  this on real PAN data and would be harder to defend on a whiteboard.

## 8. If they ask "what would you do next?"

In this order:

1. Keep the voice inventory, but estimate thresholds on a real
   validation split instead of on the stories themselves.
2. Replace the binary flags with a low-dimensional style embedding,
   still compared as *span means*, not as adjacent sentences.
3. Only then add a transformer. Do not start there; you will not be
   able to explain the first wrong cut.
