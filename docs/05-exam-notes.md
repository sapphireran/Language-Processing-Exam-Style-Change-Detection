# Exam notes I actually want in working memory

Short answers, written so I can reconstruct them under time pressure.
Longer explanations live in the other `docs/` files.

## One-sentence definition

Intrinsic style-change detection: label every paragraph boundary in a
single document as author-change or same-author, using only evidence
from that document.

## Diagram

```text
text → paragraphs → profiles → adjacent distances → threshold → {0,1}*
```

## Difficulty knob

- Easy: topic and author often move together.
- Medium: topic held roughly still; register still leaks.
- Hard: topic held still; register closer; leftover habits.
- Control: one author, gold all zeros.

If the oral question is “why three datasets?”, the answer is topic
confounding, not “to have more numbers”.

## Feature families to name out loud

1. Function words / closed class
2. Character n-grams
3. Lexical richness (TTR, hapax, Yule's K)
4. Sentence and word length
5. Punctuation and contractions

Then: “I z-score features inside the document so scales do not dominate
cosine distance.”

## Metric to name out loud

Macro-F1 on boundary labels, because class 0 dominates. Mention a
single-author control so always-predict-1 cannot pose as a system.

## Adaptive threshold, one line

Change iff distance is high *relative to that document*. If the range is
tiny, predict no changes.

## Classic traps

- Evaluating with accuracy
- Training on easy topic jumps and testing on same-topic hard data
- Using paragraphs so short that TTR is noise
- Forgetting that a paragraph is assumed single-author
- Silent length mismatches between gold and prediction

## Intrinsic vs extrinsic, one contrast

Extrinsic: compare to known writing samples.
Intrinsic: only internal variation. Needed when there is no candidate
set (unknown plagiarist, disputed sole authorship, no reference corpus).

## What I implemented here, honestly

A transparent baseline, not a SOTA model. Character 3-grams plus
stylometry plus function-word JS, mixed and thresholded. Neural
paragraph encoders would slot into the same adjacent-distance frame.

## Worked numbers I can redo on paper

Gold `[0, 0, 1, 0]`, pred `[0, 1, 1, 0]`:

- TP=1, FP=1, TN=2, FN=0
- F1_1 = 2/3, F1_0 = 0.8, macro-F1 ≈ 0.733

Same example is unit-tested in `tests/test_evaluate.py`.

## CLI I should remember

```bash
python3 -m style_change features <problem.txt>
python3 -m style_change predict -i <dir> -o <dir>
python3 -m style_change evaluate --gold <dir> --pred <dir>
```

## If they ask how I would improve it

1. Supervised classifier on paired features (concat, abs-diff, product)
   instead of an unsupervised cut.
2. Frozen sentence encoder as the paragraph profile.
3. Explicit topic model, used as a *covariate to partial out*, not as
   the detection signal.
4. Calibration on a validation split per difficulty, not one global
   threshold forever.
