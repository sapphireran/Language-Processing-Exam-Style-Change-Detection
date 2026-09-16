# Formula sheet

## Type-token ratio

\[
TTR = \frac{|\{types\}|}{N}
\]

Unstable for small \(N\). Do not compare a 12-word note to a
120-word paragraph without comment.

## Yule's K

Let \(V(i)\) be the number of types that occur exactly \(i\) times,
and \(N\) the number of tokens.

\[
K = 10^{4}\,\frac{\sum_i i^{2} V(i) - N}{N^{2}}
\]

Higher \(K\) means more repetition.

## Flesch-like reading ease

\[
206.835 - 1.015 \left(\frac{words}{sentences}\right) - 84.6 \left(\frac{syllables}{words}\right)
\]

Syllable counts here are a vowel-group heuristic, not a lexicon.

## Z-score

\[
z_{j} = \frac{x_{j} - \mu}{\sigma}
\]

computed **across paragraphs of the current document** for each
feature \(j\).

## Cosine distance

\[
d_{\cos}(u,v) = 1 - \frac{u\cdot v}{\|u\|\,\|v\|}
\]

## Burrows-like Delta

\[
\Delta(u,v) = \frac{1}{M} \sum_{j=1}^{M} |z_j(u) - z_j(v)|
\]

for \(M\) function-word coordinates.

## Character n-gram profile

\[
p(g) = \frac{count(g)}{\sum_{g'} count(g')}
\]

then cosine distance on \(p\).

## CUSUM

\[
S_t = \sum_{i=1}^{t} (x_i - \bar x)
\]

## Precision, recall, F1

\[
P=\frac{TP}{TP+FP},\quad
R=\frac{TP}{TP+FN},\quad
F_1=\frac{2PR}{P+R}
\]

## Author lower bound

\[
\hat A \ge 1 + \sum_i changes_i
\]

Equality only if the system never reuses an author across a missed
or extra cut in a way that collapses the walk. Treat it as a lower
bound, not a clustering.

## Ensemble score (this kit)

\[
s = 3.0\,d_{\text{register}} + 0.15\,\Delta + 0.40\,\max(0, d_{3\text{-gram}}-0.45) + 0.05\,d_{\text{CUSUM}}
\]

A boundary is 1 if \(s\) is an intra-document outlier (median + 1.25
MAD) or \(s\) exceeds an absolute floor (default 0.55). Weights are
study defaults. Calibrate if you change the corpus.
