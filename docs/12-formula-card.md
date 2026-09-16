# Formula card

## Hinges

\[
n_{\text{hinges}} = n_{\text{paragraphs}} - 1
\]

## NCD

\[
\mathrm{NCD}(x,y)=\frac{C(xy)-\min\bigl(C(x),C(y)\bigr)}{\max\bigl(C(x),C(y)\bigr)}
\]

`C` = zlib length minus the empty-input header.

## Cross-compression gain

\[
\mathrm{gain}(x,y)=\frac{C(x)+C(y)-C(xy)}{C(x)+C(y)}
\]

## Cosine distance

\[
d_{\cos}(u,v)=1-\frac{u\cdot v}{\|u\|\,\|v\|}
\]

Used on character 3-gram relative frequencies.

## Function-word L1

\[
d_{fw}(p,q)=\sum_{w\in L}\bigl|f_w(p)-f_w(q)\bigr|
\]

`f_w` is relative frequency. `L` is the closed list.

## Quoin score (decision blend)

\[
Q = 0.20\,d_{\cos} + 0.15\,d_{fw} + 0.25\,d_{\text{shape}} + 0.40\,d_{\text{register}}
\]

NCD is computed and reported; its weight on this bank is 0 because it
saturates on 80-word original paragraphs.

Predict `1` iff \(Q ≥ t_{\text{high}}\) **or** \(Q\) is the document
max and \(Q - \mathrm{median}(Q) ≥ t_{\text{rel}}\), and \(Q ≥ t_{\text{floor}}\).

Defaults: \(t_{\text{high}}=0.72\), \(t_{\text{rel}}=0.08\),
\(t_{\text{floor}}=0.40\).

## Precision, recall, F1

\[
P=\frac{tp}{tp+fp}\qquad R=\frac{tp}{tp+fn}\qquad F_1=\frac{2PR}{P+R}
\]

If `tp=fp=fn=0` then `F_1=1`.

## Macro / micro

Macro: mean of per-document `F_1`.
Micro: compute `tp,fp,fn` on the pooled hinges, then `F_1`.

## Type-token

\[
\mathrm{TTR}=\frac{\#\text{types}}{\#\text{tokens}}
\]

Useful in a tally sheet; unstable on very short paragraphs.
