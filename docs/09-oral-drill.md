# 09 — Oral drill

Sixty seconds each. I say the bold line first, then one caveat.

1. **What is the task?**
   Mark every adjacent pair where the writer changes, using only the
   document. Output a binary vector of length `n − 1`.

2. **Intrinsic or extrinsic?**
   Intrinsic. No reference authors. Extrinsic is attribution or
   retrieval in a cheap coat.

3. **Units?**
   Whatever the question specified. Paragraphs in older setups,
   sentences now. Align gold before I talk about F1.

4. **Why not bag-of-words?**
   Open-class words are topic. On an easy split they impersonate
   style. I want glue and shape.

5. **Best cheap feature?**
   Character 3-grams plus function-word L1. I can implement both
   without a library.

6. **Draw CUSUM.**
   `S_i = S_{i-1} + (x_i − μ)` on sentence length. Slope reversal is
   a candidate cut. Not a proof.

7. **Why a distance floor?**
   Short units have unstable profiles. Without a floor the gap
   heuristic invents a writer on a diary.

8. **Easy vs hard?**
   Easy lets topic move with authorship. Hard holds topic still.
   Quote the hard number.

9. **Metric?**
   Macro-F1 on pairs, both classes. Empty class: 0/0 → 1 so a clean
   single-author file scores 1.0.

10. **Accuracy?**
    A trap when changes are rare. Always-0 looks fine and is useless.

11. **Returning author?**
    Need memory or clustering. Pair F1 can be perfect while ARI is
    not.

12. **Gift authorship?**
    Same topic, different register and person. If I used project
    keywords I cheated.

13. **Neural pair model?**
    Works, encodes topic, opaque, needs a same-topic ablation.

14. **Twenty-minute plan?**
    Split, char-3grams, function words, gap threshold, mention two
    failures.

15. **What I will not claim?**
    That 1.0 on ten toy files is a shared-task result. It is a
    sanity check that the code matches the notes.

## If they hand me a document in the oral

I do this in order:

1. Read it once as a human. Where would *I* cut?
2. Say the grain (sentence or paragraph).
3. Point at two features that should move (length, `we`/`one`,
   contractions).
4. Only then talk about a model.

If I start with "I would fine-tune DeBERTa" I have not looked at the
text they handed me.
