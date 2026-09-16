# Oral cards

Say the bold line, then the one-sentence expansion. Numbers should
be refreshed from `scripts/run_curriculum.py` before the sitting.

## Card 1 — task

**For n sentences I emit n−1 bits; a 1 means the next sentence has
a different author.**
I never name the authors. I only mark seams. That is intrinsic
style-change detection.

## Card 2 — why closed class

**I put most of the weight on function words so a new topic is not
automatically a new author.**
`of`, `however`, and `you` travel with a writer. `vellum` travels
with a subject.

## Card 3 — Easy vs Hard

**If I only report Easy I have not shown stylometry.**
Easy aligns topic and author. Hard holds the topic still. The gap
between those two macro-F1s *is* the result.

## Card 4 — accuracy

**A never-fire detector can be 80% accurate and still score 0.44
macro-F1.**
I will put the four cells on the board if needed.
`macro_f1_from_cells(0, 0, 16, 4) == 0.444`.

## Card 5 — Delta

**Delta is mean absolute z-score difference on a closed list.**
Our z-scores are computed inside one short document, so the
estimate is noisier than Burrows' novel-scale figures. I still
use it because the coordinates stay interpretable.

## Card 6 — gift authorship

**A flagged seam is a hypothesis, not an accusation.**
I would show the pair, the channel breakdown, and a human the
full paragraph. I would not write a name in a margin.

## Card 7 — transformers

**A Siamese encoder is still intrinsic if it only compares
windows inside the document.**
The risk is topic leakage in the embedding space. I would demand
the Hard split before I believed the number.

## Card 8 — CUSUM

**CUSUM is how I explain structure; the official answer is still
a pairwise `changes` array.**
A long climb means a late block unlike the opening. A spike that
falls back is probably one odd sentence.

## Card 9 — short units

**I do not trust TTR on six tokens.**
If the gold seam sits on `Yes.` I expect `short_unit_noise` and I
will say I need a window, not a braver threshold.

## Card 10 — what I would do next

**I would add a POS pronoun/noun ratio and keep the closed list.**
I would not add an open content bag. I would re-run Easy vs Hard
after every feature I add.
