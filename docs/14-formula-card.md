# Formula card

## Units and labels

- \(n\) units → \(n-1\) pair labels
- `changes[i] = 1` iff author(\(u_{i+1}\)) ≠ author(\(u_i\))

## Type-token ratio

\[
\mathrm{TTR}(u) = \frac{|\{types\}|}{|\{tokens\}|}
\]

Unreliable for \(|tokens| \lesssim 12\).

## Cosine distance

\[
\mathrm{cos\text{-}dist}(a,b) = 1 - \frac{a \cdot b}{\|a\|_2 \|b\|_2}
\]

If either vector is zero, Seamtrace returns 1.

## Burrows' Delta (lab form)

\[
\Delta(u,v) = \frac{1}{M}\sum_{j=1}^{M} |z_j(u) - z_j(v)|
\]

\(z_j\) uses the mean and population std of bin \(j\) across units
in the same document.

## Blended pair score

\[
s = 0.35\,d_{fw} + 0.10\,d_{tri} + 0.40\,d_{sc} + 0.15\,\Delta'
\]

where \(\Delta' = \Delta / (1+\Delta)\) keeps Delta in \((0,1)\).

## Detectors

- Threshold: \(\hat y = [s \ge \tau]\), default \(\tau = 0.42\)
- Adaptive: \(\tau = \max(0.22, \bar s + k \sigma)\), default \(k = 0.85\)
- Ensemble: change if either voter fires

## F1 and macro-F1

\[
F1_c = \frac{2 P_c R_c}{P_c + R_c},\qquad
\mathrm{macro\text{-}F1} = \frac{F1_0 + F1_1}{2}
\]

Never-fire example: \(TP=0,FP=0,TN=16,FN=4\) → macro-F1 \(= 0.444\),
accuracy \(= 0.80\).

## Content Jaccard (diagnostic only)

\[
\mathrm{topic\text{-}shift} = 1 - \frac{|A \cap B|}{|A \cup B|}
\]

\(A,B\) = tokens of length \(> 3\) that are not on the function-word
list.
