# Metrics, and why accuracy lies

## The official number

PAN evaluates **macro-F1** over the two pair classes (stay = 0,
change = 1), pooling every pair in a split. Seamtrace reports the
same thing plus the confusion cells so you can see *which* class
died.

\[
P_c = \frac{TP_c}{TP_c + FP_c},\quad
R_c = \frac{TP_c}{TP_c + FN_c},\quad
F1_c = \frac{2 P_c R_c}{P_c + R_c}
\]

Macro-F1 is the unweighted mean of \(F1_0\) and \(F1_1\).

If a class has no predicted positives, its precision is 0 in this
lab (no silent 1.0). Say so if you compare against a scorer that
treats undefined precision as 1.

## A four-cell example

Suppose a folder has 20 pairs: 16 stays, 4 changes. A detector that
never fires scores:

- \(TP=0, FP=0, TN=16, FN=4\)
- \(F1_1 = 0\)
- \(F1_0 = 2 \cdot 1 \cdot 16/20 / (1 + 16/20) = 0.889\) (recall of
  stay is 1, precision of stay is 16/20)
- wait — precision of stay is \(TN / (TN + FN) = 16/20 = 0.8\),
  recall of stay is \(TN / (TN + FP) = 1\), so \(F1_0 = 2\cdot 0.8
  \cdot 1 / 1.8 = 0.889\)
- macro-F1 \(= 0.444\)
- **accuracy** \(= 0.80\)

That is the trap. The oral prompt is: "Our accuracy is 80 percent."
Your answer is the table above.

`seamtrace.handcalc.macro_f1_from_cells(0, 0, 16, 4)` reproduces
0.444.

## What to report in a write-up

Always:

- macro-F1
- F1 on the change class
- support of each class
- at least one named miss

Nice:

- Easy vs Hard gap
- false-alarm rate on Controls
- an ablation with the function-word weight set to 0

Never as the headline:

- accuracy
- "it felt like it worked on the examples I looked at"

## Document-level vs pair-level

A document can be "mostly right" and still miss the only seam that
mattered (gift authorship, exam paste). Pair-level macro-F1 will
punish that if you have enough change pairs in the pool. If your
teaching set is tiny, **also** report how many documents had their
first seam correct. That is not an official PAN number. It is an
honest exam number.
