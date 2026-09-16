# Paragraph-level reading of `easy/problem-001`

Gold: three authors, `changes = [0, 1, 0, 1]`.

The file is the one I would put on an exam worksheet. The first two
paragraphs share a voice, the middle two share a different voice, and the
last paragraph is a third person walking in with dinner.

## Paragraph 1 — author A, trail chat

Casual first person, contractions (`you're`, `don't`), concrete objects
(sandwich, shoes, creek), and short evaluations (`wrecked me in the best
way`, `ridiculous`). Sentence length jumps around. Punctuation is almost
only commas and periods.

Exam tell: high first-person rate, high contraction rate, short words.

## Paragraph 2 — still author A

Same parking-lot story, same jokes, same `I` + `again` cadence. If a
system fires a change here it is reacting to new entities (cash, bugs,
sock), not to style. Topic shifted inside the hike; authorship did not.

Gold boundary after P2: `0`.

## Paragraph 3 — author B, hydrology memo

Third person, Latinate nouns (`observational syntheses`, `climatologies`),
almost no contractions. Connectives arrive in P4 (`therefore`); P3
already sounds like a paper (`further suggest`). This is the first
actual style change.

Boundaries in this file:

- P1–P2: `0`
- P2–P3: `1`  ← first author change
- P3–P4: `0`
- P4–P5: `1`

## Paragraph 4 — still author B

Policy continuation of the same memo. `therefore`, `scenario ensembles`,
`systematically`. A topic-only detector might think “now it is planning,
not climate” and fire. A style detector should see the same academic
register and stay quiet.

Gold boundary after P4: `0`.

## Paragraph 5 — author C, weeknight cooking

Second-person recipe voice, fragments, humour, concrete food words.
Nothing in P3–P4 prepared this register. This is the second author change.

Gold boundary after P4: `1`.

## What I want a model to get right

1. Do not fire inside A (P1–P2) or inside B (P3–P4).
2. Do fire at A→B and B→C.
3. If it only fires at A→B because the topic jumped from hiking to
   runoff, it will still luck into the right label here — and then fail
   `medium/problem-001`, where baking stays baking.

Worked CLI:

```bash
PYTHONPATH=src python3 -m style_change features \
  examples/sample_problems/easy/problem-001.txt
```

Look at `first_person_rate`, `contraction_rate`, `connective_rate`, and
`avg_word_len` across the five columns. A and C should look like people
talking. B should look like a paper.
