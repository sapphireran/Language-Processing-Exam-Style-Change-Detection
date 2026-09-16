# 06 — Oral answers

Say these out loud until they are boring. An examiner who hears the
first clause of each item will usually not need the rest.

## What is the task?

"Intrinsic paragraph-level style-change detection: for each adjacent
pair of paragraphs in one English document, decide whether the author
changed. No gallery. Output a bit vector of length n−1."

## Why not accuracy?

"Single-author documents are all zeros. A system that never predicts
a change scores perfect accuracy there and fails the actual joins.
Quote positive-class F1 and macro-F1."

## What is the easy/medium/hard split?

"Topic control. Easy lets topic change with author; hard holds topic
fixed so content features go quiet. It is not officially 'authors are
harder to tell apart', even if they sometimes are."

## Name three style families that are not topic.

"Function-word frequencies, character n-grams, and sentence-length
plus punctuation. Lexical richness is a fourth. Content-word Jaccard
is the thing you compute and then refuse to let vote."

## Why function words?

"Closed class, frequent, weakly coupled to topic, historically enough
to separate Hamilton from Madison. You can put the vector on paper."

## Why character n-grams?

"They capture affixes, contractions, and punctuation without a
tokeniser argument. They also leak topic, so they are not pure."

## What is Burrows's Delta?

"Mean absolute z-score difference across function-word (or other
closed-class) frequencies. Z-scoring is across the documents or
paragraphs you are comparing, so rare words do not dominate by raw
count."

## What is NCD?

"Normalised compression distance. If concatenating A and B compresses
almost as well as the better of A or B, they share structure. zlib is
a crude approximation of Kolmogorov complexity. Cheap, language-agnostic,
and not a syntactic theory."

## Intrinsic or extrinsic for gift authorship with no sample?

"Intrinsic. You have only the suspicious document. Extrinsic methods
need writing samples from the alleged authors."

## Does a 1 mean a *new* author or a *different* author?

"Different from the previous paragraph. Returning authors still flip
the bit to 1, then 1 again when they leave. The task does not
re-identify."

## Why split on blank lines, and why `newline=""`?

"PAN's paragraph boundary is a blank line. Opening with newline=''
stops Python converting CRLF and accidentally eating a boundary or
inventing one."

## What independence assumption does a pairwise threshold make?

"That the decision at boundary i does not depend on the run length
behind it or the rest of the document, except insofar as we z-score
features inside the document. A CUSUM or an HMM would relax that."

## Why will transformers win the real shared task?

"They see long-range lexical and syntactic cues jointly, and they
will quietly use topic unless you starve them of it. The lab exists
so I can still name the cues they are using."

## What would you do on PAN data that this lab does not?

"Fit the threshold on a validation split, not on the same twelve
documents I report. Add a sequential model. Consider a learned
representation *after* I can explain the baseline. Never tune on the
test directory."
