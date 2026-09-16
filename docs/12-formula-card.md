# Formula card

One page I can rewrite from memory.

## Split score

\[
\mathrm{score}(k)=\lVert \mu(x_{1:k})-\mu(x_{k+1:n})\rVert_2
\sqrt{\frac{k(n-k)}{n}}
\]

Cut at \(\arg\max_k \mathrm{score}(k)\) if that value \(\ge \tau\).
Recurse with \(\tau' > \tau\).

## Adjacent step

\[
d_i=\lVert x_i-x_{i+1}\rVert_2
\]

Mark hinge \(i\) if \(d_i \ge \delta\) (absolute floor), even when
the first split diluted it.

## Hellinger (inspection, not the saw)

\[
H(p,q)=\frac{1}{\sqrt{2}}\lVert \sqrt{p}-\sqrt{q}\rVert_2
\quad\text{after }L_1\text{ normalising non-negative }p,q
\]

Useful if I am asked for a rate-space distance. The saw uses
weighted Euclidean on the fingerprint, which already includes
non-rate shape terms.

## Precision / recall / F1

\[
P=\frac{tp}{tp+fp},\quad
R=\frac{tp}{tp+fn},\quad
F_1=\frac{2PR}{P+R}
\]

Macro-F1: average of \(F_1\) on `change` and \(F_1\) on `same`.

## Never-fire / always-fire

Never-fire: \(tp=0, fp=0\), so \(F_1(\text{change})=0\),
\(F_1(\text{same})\) is high. Always-fire: \(tn=0, fn=0\), so
\(F_1(\text{same})=0\).

## Naive author count (and why it is wrong)

\[
\hat{a}=1+\sum_i c_i
\]

Equals the true number only if authors do not return.

## Frozen blade (this bank)

\(\tau=0.22\), \(\tau'=0.40\), \(\delta=0.40\).
