# Features, cosine, and Burrows's Delta

## The paragraph vector

For each paragraph the kit stores:

| handle | intuition |
| --- | --- |
| mean word length | longer in formal / technical prose |
| mean sentence length | the cheapest syntax feature |
| damped TTR | richness; raw TTR is 1.0 on tiny paragraphs |
| contraction rate | register |
| `I` / `we` / `you` / `one` | person and stance |
| formal connectives | `however`, `therefore`, `consequently` |
| casual markers | `lol`, `gonna`, `yeah` |
| suffix bins | `-ing`, `-ed`, `-ly`, `-tion` … |
| function-word frequencies | closed-class histogram |
| character 3-gram profile | L2-normalised counts |
| content-word set | topic channel, *not* in the style vector |

Formality is a signed mix of the register handles. It is not a
validated psychometric scale. It is a teaching score: high on the
vellum paragraphs, low on the Slack recap.

## Cosine on character 3-grams

Let \(c_p\) be the count vector of lowercase character trigrams in
paragraph \(p\), after collapsing whitespace. Then

\[
\cos(p, q) = \frac{c_p \cdot c_q}{\|c_p\|\,\|c_q\|}, \qquad
d_{\text{char}}(p, q) = 1 - \cos(p, q).
\]

Sparse dicts are enough; you do not build a global vocabulary. The
distance is 0 for identical strings and near 1 for disjoint alphabets.

## Burrows's Delta, intrinsic version

1. For each function word \(w\) and paragraph \(p\), compute the
   relative frequency \(f_p(w)\).
2. Treat the paragraphs of *this* document as the sample. Compute
   \(\mu_w\) and \(\sigma_w\).
3. \(z_p(w) = (f_p(w) - \mu_w) / \sigma_w\) (0 if \(\sigma_w = 0\)).
4. \(\Delta(p, q) = \frac{1}{|V|} \sum_w |z_p(w) - z_q(w)|\).

Say the weakness: one odd paragraph moves \(\mu_w\). A corpus-level
Delta (the original) is more stable and is *extrinsic*.

## Dense numeric cosine

The remaining scalars are concatenated, z-scored the same way, and
compared with cosine. This channel exists so sentence length and
pronoun mix can vote even when the function-word histogram is too
sparse for Delta.

## Topic Jaccard (the confound)

\[
J(p, q) = \frac{|C_p \cap C_q|}{|C_p \cup C_q|}, \qquad
d_{\text{topic}} = 1 - J
\]

where \(C_p\) is the set of content types (tokens of length ≥ 3 that
are not on the function / casual / connective lists). High
\(d_{\text{topic}}\) with low \(\Delta\) is "same author, new nouns".
Low \(d_{\text{topic}}\) with high \(\Delta\) is the hard PAN case.

## CUSUM

For a scalar series \(x_1, \ldots, x_n\) (word length, sentence
length, formality):

\[
S_0 = 0, \qquad S_t = S_{t-1} + (x_t - \bar{x}).
\]

A change of author often appears as a change of slope. CUSUM is a
weak paragraph-level voter and a strong oral-exam diagram. Lab 04
writes the SVG.
