# Written model answers

These are personal drafts, not official marking guides. They are
sized for a 20–30 minute written section.

## Q1. Define intrinsic style-change detection and state the 2023 output.

Intrinsic style-change detection asks whether a single document
contains more than one writing habit, and *where* those habits meet,
without access to candidate author corpora. PAN 2023 operationalises
the problem at paragraph level: a paragraph is assumed to have one
author, and a system emits a binary vector `changes` of length
\(k-1\) for a document of \(k\) paragraphs. A 1 marks an author
change between paragraph \(i\) and \(i+1\). Evaluation is F1 on that
vector, separately on easy, medium, and hard collections that control
how much topic is allowed to co-vary with authorship.

## Q2. Why are function-word rates a better default than bag-of-words?

Bag-of-words counts are dominated by topical nouns. When authorship
changes coincide with topic changes, a BOW cosine will look brilliant
and still be measuring aboutness. Function words are frequent enough
to estimate in a short paragraph, carry little referential content,
and are reused from topic to topic. Classic attribution work
(Mosteller and Wallace; Burrows) already treats them as the primary
coordinates. They are not unbreakable: register and genre move
pronouns too, and tiny paragraphs make every rate noisy. They are
simply the right *default* when the scientific claim is style rather
than subject.

## Q3. Give an algorithm for a non-neural baseline.

(1) Split on blank lines. (2) For each paragraph, compute length-
normalised rates: sentence length, word length, contractions,
pronouns, hedges, and a fixed function-word distribution, plus a
character 3-gram profile. (3) Z-score the numeric channels across
paragraphs of this document. (4) Score each adjacent pair with a
blend of cosine distance, Burrows-like Delta, and 3-gram cosine
distance. (5) Threshold the blend, choosing the cut-off on labelled
development data by macro F1. (6) Write `{"changes":[...]}`. Report
easy / medium / hard separately and include an always-0 dummy so the
F1 is interpretable.

## Q4. How do you choose a threshold, and what goes wrong if you do not?

The detector outputs a real score. PAN wants bits. A threshold is a
mapping from scores to bits and must be estimated on labelled
development documents that you will not quote as the final test
number. Sweeping the threshold traces a precision–recall curve; F1
usually peaks at a different place than accuracy, because accuracy
rewards the majority "no change" class. If you skip calibration you
either ship an arbitrary number (0.5 is not magic) or silently
optimise on the test stories you will later present as evidence.
Both are exam faults. If the corpus is tiny, say so and treat the
chosen cut as a demonstration.

## Q5. Describe a topic confound and a control.

A topic confound occurs when a change in subject matter is correlated
with the authorship label *and* with the features. Splicing a
lighthouse paragraph to a tax paragraph creates a label that any
content model can recover. Control: evaluate on a hard split where
all paragraphs share a topic, and include a synthetic pair where one
author changes topic (gold 0) beside a pair where two authors share a
topic (gold 1). A style system should be louder on the second pair.
If your easy F1 dwarfs your hard F1, you have not yet earned the word
"style".

## Q6. What would you add if you had a GPU and licensed training data?

A transformer pair classifier on concatenated paragraphs, trained
with the official `changes` labels, plus a stylometric baseline kept
as explainer. I would augment with same-topic splices rather than
only cross-topic splices, calibrate the decision threshold on a
development split, and do an error analysis that includes gift-style
register shifts and single-author genre shifts. I would not drop the
feature model: I need it to check that the network is not a noun
detector in a trench coat.
