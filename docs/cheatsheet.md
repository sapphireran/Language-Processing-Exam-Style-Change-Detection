# Cheatsheet

**Task.** Intrinsic SCD. Bits `y_i = 1[author_i ≠ author_{i+1}]`.
No gallery. Paragraphs are single-author. Changes only at blank lines.

**I/O.** `open(path, "r", newline="")`. `problem-X.txt` →
`solution-problem-X.json` with `{"changes":[…]}`. `|changes| = n−1`.

**Bands.** Easy: topic may track author. Medium: little topic
variety. Hard: same topic; style has to work.

**Style channels.** Function words, char 3-grams, Burrows's Delta,
JS on closed class, richness (Guiraud, hapax, Yule K, Honoré R),
sentence/word length, punctuation, person, contractions, hedges,
boosters, zlib NCD.

**Not style.** Content-word Jaccard, named entities, meaning
embeddings. Compute them; do not let them vote unless you are
showing leakage.

**Yule's K.** `10^4 (Σ i² V_i − N) / N²`. Larger ⇒ more repetition.

**Honoré's R.** `100 ln N / (1 − V1/V)`. Undefined if V1 = V.

**F1.** Positive class is `1`. Macro-F1 averages class 1 and class 0.
Accuracy lies on single-author pages.

**Pairwise independence.** Each boundary scored alone. CUSUM / HMM /
transformers relax this.

**This lab's rule.** Weighted sum, threshold 0.42, fit on the bundled
twelve documents. Not a PAN score.

**Oral core.** "I detect joins, I do not name authors, I distrust
topic, I report macro-F1."
