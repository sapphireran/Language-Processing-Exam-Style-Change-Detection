# Formula card

## Hinge length

\[
n_{\text{hinges}} = n_{\text{units}} - 1
\]

## Returning-author trap

\[
n_{\text{from changes}} = 1 + \sum_i \text{changes}_i
\]

Equals the true writer count only if nobody returns.

## Smoothed function-word rate

\[
\hat{p}_w = \frac{c_w + k}{n + k\,|V|}
\quad k = 0.35
\]

## Cosine distance

\[
d_{\cos}(a,b) = 1 - \frac{a\cdot b}{\|a\|\,\|b\|}
\]

## Register gap

\[
\text{raw} = \sum_j w_j \frac{|x_j - y_j|}{s_j},
\quad
\text{gap} = \frac{\text{raw}}{1.15 + \text{raw}}
\]

## Blend

\[
\text{blend} = 0.72\,\text{gap} + 0.16\,d_{\text{fw}} + 0.06\,(0.45\,d_{\text{char}}) + 0.06\,\frac{\Delta}{1+\Delta}
\]

Cut at \(\tau = 0.30\) on this study set.

## Intra-document Delta

Z-score each function-word rate across units in the *same* document. Adjacent Delta is the mean absolute difference of those z-scores.

## CUSUM

\[
S_t = \sum_{i=1}^{t} (d_i - \bar{d})
\]

## Pair F1

\[
P = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}},\quad
R = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}},\quad
F_1 = \frac{2PR}{P+R}
\]

Macro-F1 is the unweighted mean of change-F1 and hold-F1.

## 16/4 trap

TN=16, FN=4, TP=0, FP=0 → acc=0.800, hold-F1=0.889, change-F1=0, macro-F1=0.444.
