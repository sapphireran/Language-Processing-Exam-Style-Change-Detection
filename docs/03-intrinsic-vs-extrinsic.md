# Intrinsic versus extrinsic

**Extrinsic** authorship: you have a gallery. "Was this *Federalist*
essay Hamilton or Madison?" You train on known Hamilton and known
Madison, then classify the disputed text.

**Intrinsic** authorship: you have only the document. "Did more than
one person write this, and where did the voice change?" There is no
gallery. Every feature has to be estimated from the sheet in your
hand.

Style-change detection is intrinsic. That has three consequences the
exam likes:

1. **You cannot normalise against a corpus mean.** Burrows' classical
   Delta z-scores a word against many documents. Intra-document Delta,
   which this lab implements, only compares two *spans of the same
   sheet*. The z-score floor is a fudge. Say so.
2. **Short spans are the whole game.** A six-sentence document gives
   you three-sentence sides. Function-word estimates are noisy. That
   is why the exam vector is six rates, not a 10,000-dimensional
   character language model.
3. **A returning author is invisible to a gallery method that was
   never given the gallery.** Intrinsic methods still have to notice
   that segment 5 looks like segment 1. Ours does not cluster; it only
   marks folds. That is why author count is naive.

If a question says "you may assume a training set of labelled
documents exists," they have switched you into a supervised,
semi-extrinsic setting. Thresholds can be fit. That is the
calibration note, not the definition of the task.
