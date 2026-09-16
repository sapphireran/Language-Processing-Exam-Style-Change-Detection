# Walkthrough: Hard

Hard keeps the topic still and moves only the habit. This is the split
that decides whether you have a style system.

## Success: sourdough (`problem-001`)

Gold `[0, 1, 0]`.

- P1–P2: hedged analytic (`usually`, `tends`, `it is worth noting`,
  `generally`). Casualness −0.78 then similar.
- P3–P4: direct second person (`You will`, `Do not`, `Keep notes`).
  Casualness climbs toward −0.48.

| Boundary | Gold | combined | topic | Pred |
| --- | --- | --- | --- | --- |
| 1–2 analytic → analytic | 0 | 0.233 | 0.960 | same |
| 2–3 analytic → “you will” | 1 | 0.394 | 0.838 | CHANGE |
| 3–4 “you will” → “if the sour” | 0 | 0.270 | 0.903 | same |

The **smallest** topic jump (0.838) is the **true style change**. A
content-word segmenter would put the cut in the wrong place. This one
row is the best single exam example in the repo. Memorise it.

## Failure: walking notes (`problem-002`)

Gold `[0, 1, 0]` (reflective third person, then imperative field notes).
The baseline emits `[0, 0, 1]`.

The missed change (P2→P3, combined 0.307) is a soft register move:
“It is possible, of course…” versus “Walk the block once…”. The false
change (P3→P4, 0.361) is two imperative paragraphs whose *length*
diverges — P4 is 47 tokens of staccato (“Note the interruptions.
Then decide…”) so function-word cosine blows up (0.578) even though
the author did not.

Short-span sparsity, not philosophy, caused the error. That is the
answer if a question asks “when do function-word features fail?”.

## Failure: single-author library (`problem-003`)

Gold `[0, 0, 0]`. Pred `[1, 0, 0]`. The opening boundary is a scene
change (late hours → noon) written by the same person. Combined 0.354
clears 0.33. Genre shift inside one author is indistinguishable from
authorship at this feature budget.

## Split score

```
macro-F1 = 0.333
micro: F1=0.400  P=0.333  R=0.500  acc=0.667
         tp=1 fp=2 fn=1 tn=5
```

Accuracy 0.667 would look almost respectable in a slide. F1 does not.
Quote F1.

## What a stronger Hard system would add

- More context than one paragraph (sliding windows).
- A supervised pair classifier trained on Hard, not Easy.
- An explicit length normalisation so 47-token staccato does not look
  like a new author.
- Refusal to emit a `1` unless *several* views agree, not just
  function-word cosine.

The baseline is left bad on Hard on purpose. Do not “fix” it until you
can explain the errors above.
