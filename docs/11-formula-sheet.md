# Formula sheet

**Change vector.** For paragraphs \(p_1,\ldots,p_n\),

\[
y_i = [\,\mathrm{author}(p_i) \neq \mathrm{author}(p_{i+1})\,],
\quad i = 1,\ldots,n-1.
\]

**Relative frequency.** \(f_p(w) = \mathrm{count}_p(w)\,/\,|p|\).

**Z-score.** \(z_p(w) = (f_p(w)-\mu_w)/\sigma_w\).

**Burrows Delta.**
\(\Delta(p,q)=\frac{1}{|V|}\sum_{w\in V}|z_p(w)-z_q(w)|\).

**Cosine distance.**
\(d_{\cos}(x,y)=1-\frac{x\cdot y}{\|x\|\|y\|}\).

**Jaccard distance.**
\(d_J(A,B)=1-|A\cap B|/|A\cup B|\).

**Damped TTR.** \(\mathrm{types}/\sqrt{n}\) (then scaled). Raw TTR
is \(|\mathrm{types}|/n\).

**CUSUM.** \(S_t=S_{t-1}+(x_t-\bar x)\), \(S_0=0\).

**Precision / recall / F1.**

\[
P=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}},\quad
R=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}},\quad
F_1=\frac{2PR}{P+R}.
\]

If TP=FP=FN=0, this kit sets \(P=R=F_1=1\).

**Macro-F1.** \(\frac{1}{D}\sum_{d=1}^{D} F_1^{(d)}\).

**Micro-F1.** F1 on the pooled confusion matrix.

**Ensemble rule.** Flag if \(\#\{\text{strong channels}\}\ge 1\) or
\(\#\{\text{channels above floor}\}\ge 2\).
