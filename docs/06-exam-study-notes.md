# Exam study notes

Short answers you can adapt. Keep the verbs; change the examples if the
paper gives you different sentences.

## Definitions

**Intrinsic authorship analysis.** Infer authorship structure from the
questioned document alone (and, if supervised, from other labeled
documents used only at training time). No candidate writer is named at
test time.

**Extrinsic authorship analysis.** Compare the questioned text to named
samples: attribution (“which of these people?”) or verification (“is
this the claimed person?”).

**Style change detection.** Intrinsic change-point labelling at a stated
granularity (here: sentence pairs). Output is a binary sequence, not a
name.

**Register vs author.** One writer can shift register (lab note → email →
story). That shift *looks* like a style change. Gold labels in this repo
are author IDs, so a single-author register shift would be a false
positive. Mention this whenever you claim high precision.

## Feature families worth memorising

1. **Lexical closed class** — function words, pronouns, articles.
2. **Character / punctuation** — comma, semicolon, contraction, digit.
3. **Syntactic cheap proxies** — subordination markers, passives, length.
4. **Morphological register** — nominalizations, `-ly` adverbs, Latinate
   suffixes.

If the paper asks for “two features robust to topic control”, pick one
from 1 and one from 2. Do not pick TF–IDF.

## Standard arguments

### Topic is a confound

Authors in the wild change subject when they change speaker. A classifier
that sees *coral* then *casserole* will predict a change and be right
for the wrong reason. The hard split exists to take that toy away. An
answer that never mentions topic control has not finished the question.

### Imbalance

Changes are rare. Report macro-F1. Quote the always-`0` baseline. If you
oversample class `1` at train time, say that the decision threshold may
need to move back toward the real prior at test time.

### Short sentences

TTR, hapax, and Flesch are unstable below ~8 tokens. Either drop those
features on short sentences, or smooth them toward the document mean.
The toolkit does not drop them; the notes tell you they are noisy so you
can say so.

### Evaluation granularity

Paragraph-level change detection is easier because each unit has more
text. Sentence-level is the stricter exam setting: less evidence per
unit, more pairs, more imbalance. If a question contrasts the two, this
is the contrast.

### Within-document normalisation

A change-point detector should ask “is this jump large *for this text*?”,
not “is this sentence unusual in the British National Corpus?”. That is
why the unsupervised detector z-scores inside the document.

## Sketch proofs / derivations

### Pairwise reduction

A document of \(n\) sentences yields \(n-1\) i.i.d.-looking pairs only
after you pretend the pairs are independent. They are not: a three-author
document has runs. Logistic regression ignores the run structure. A
sequence model (HMM, CRF, BiLSTM) would not. If asked “name a limitation
of the pairwise reduction”, say independence.

### Macro-F1 algebra

If class `1` never appears in the gold *or* in the prediction, \(F1_1=0\)
by the zero-denominator convention used here. Always-`0` on an all-`0`
document is a perfect document-level score and a misleading corpus-level
story if mixed with documents that do contain changes. Pool after
concatenating.

### Distance threshold

Let \(d_i = \|z(x_i) - z(x_{i+1})\|_2\). If features are independent
standard normal under “same author”, \(d_i^2\) is roughly \(\chi^2\) with
\(p\) degrees of freedom. We do **not** use that tail (features are
dependent and not Gaussian). The \(k\sigma\) rule is a heuristic. Do not
dress it up as a likelihood-ratio test unless you write the likelihood.

## Oral / short-question bank

**Q. Why not cluster sentences and cut between clusters?**
A. Clustering throws away order. Adjacent same-author sentences can land
in different clusters if one is short. Change-point methods respect
order. You can still cluster as a diagnostic.

**Q. Would a language-model perplexity jump work?**
A. Yes, as a feature: train or prompt a model on the prefix and measure
surprise at the next sentence. It is extrinsic in spirit (the LM is a
huge prior) and opaque. Fine for a systems paper; weak as the only exam
answer.

**Q. How do you handle a returning author A–B–A?**
A. Pairwise labels still work: `[1, 1]` around B. Recovering that the
third block is A again is a harder clustering / attribution problem and
is *not* required by the output contract.

**Q. What is the majority baseline’s macro-F1 if the change rate is 30%?**
A. Predict all `0`. \(R_0=1\), \(P_0=0.7\), \(F1_0 \approx 0.824\).
\(F1_1=0\). Macro-F1 \(\approx 0.412\).

**Q. Name an ethical issue.**
A. Style-change tools get sold as plagiarism oracles. On short texts they
are coin flips. A write-up should refuse over-claiming and should not be
used to accuse a person.

## Memory sheet

```
n sentences → n-1 labels
y=1 means author changed between i and i+1
intrinsic = no named candidates at test
hard split = topic held constant
macro-F1 = mean of per-class F1
always0 is the first row of the table
features: pronouns, punctuation, hedges, length, passives
unsupervised: z-score inside the document, threshold jumps
logistic: abs-diff pairs, train scaler, class weights
limitation: one author, two registers
```
