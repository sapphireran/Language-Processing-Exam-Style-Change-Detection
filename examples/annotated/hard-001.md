# Hard document: one rain garden, leftover habits

Gold for `hard/problem-001`: two authors, `changes = [1, 1]`.

Topic never leaves stormwater. Register gets closer than the medium
bake: all three paragraphs could appear in a homeowner pamphlet. The
seams are habits.

## Paragraph 1 — designer

Third person, `therefore`/`moreover` cadence, design constraints,
twenty-four to forty-eight hours, overflow as delay not dam.

## Paragraph 2 — second person how-to

`You can dig`, `You'll plant`, contractions, metres from the foundation,
weeding. Same object, different address and sentence length.

## Paragraph 3 — designer again

Back to siting constraints, infiltration tests, underdrain. Author A
returns; this is why the gold vector is `[1, 1]` and not `[1, 0]`.

## What success looks like here

A system may miss one of the two boundaries. I still want it to prefer
P1–P2 over a random pair, because that is the larger habit jump
(address: third person → `you`). Character 3-grams should feel the
apostrophes in P2. Function-word JS should feel `you`/`the`/`therefore`.

If the ensemble predicts `[0, 0]`, adaptive thresholding decided the
document was homogeneous. That is the honest failure mode of an
unsupervised cut, and it is why `docs/05-exam-notes.md` lists a
supervised pair classifier as the first upgrade.

```bash
PYTHONPATH=src python3 -m style_change features \
  examples/sample_problems/hard/problem-001.txt \
  --detector ensemble
```
