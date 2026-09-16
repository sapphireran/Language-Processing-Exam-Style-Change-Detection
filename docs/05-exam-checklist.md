# Exam checklist

Short prompts you should be able to answer without opening the code.
Each item is a prompt, then the shape of a full-mark answer.

## Definitions

**Q. Define style change detection and name the three subtasks.**

A document is given; no candidate authors are named. Decide (1) whether
more than one writing style is present, (2) at which paragraph
boundaries the style changes, and (3) which paragraphs share a latent
author, allowing non-contiguous returns.

**Q. Contrast SCD with authorship attribution and with topic
segmentation.**

Attribution classifies into a closed author set using labelled history.
Topic segmentation cuts a document where *content* shifts. SCD cuts
where *stylistic habit* shifts, ideally while topic is held constant
or treated as a confound.

**Q. Why are function words better markers than nouns for this task?**

They are frequent, closed-class, and weakly determined by topic.
Writers repeat them unconsciously. Nouns track subject matter and will
fire on a single author who changes topic.

## Features

**Q. Give four feature families and one example from each.**

Length (words per sentence), richness (TTR or Yule's K), punctuation
(semicolon rate), closed class (frequency of `the` / `however` /
contractions), person (first vs second). Mention that all should be
normalised by paragraph length.

**Q. Why is TTR dangerous on short paragraphs?**

Vocabulary size cannot exceed token count, so short texts look
artificially rich. Compare paragraphs of similar length or use a
length-adjusted measure.

**Q. What does z-scoring the feature matrix achieve?**

It equalises scale so sentence length does not dominate a comparison
of raw features. The cost is unstable variances when the document has
only two or three paragraphs — which is why this baseline detects in
a 4-D style space instead of z-scored 100-D cosine.

## Methods

**Q. Describe an unsupervised baseline in four steps.**

Paragraph split; extract relative-frequency features; project onto a
small named style space (or otherwise reduce dimension — a 100-D
z-score on six paragraphs is not a distance); compute adjacent
distances; call a peak a change if it exceeds a floor or the first
small-to-large gap. Cluster non-adjacent paragraphs if a writer may
return.

**Q. Why is a returning author harder than a single cut?**

Adjacent peaks only produce contiguous blocks. `A B A` needs a
comparison between non-adjacent paragraphs (clustering, or matching
block centroids).

**Q. Give two alternatives to adjacent Euclidean distance on style axes.**

Sliding-window Jensen–Shannon; CUSUM on a 1-D projection; supervised
boundary tagging on paragraph embeddings. State one strength and one
weakness for whichever you pick.

## Evaluation

**Q. Why is label accuracy wrong for Task 3?**

Predicted ids are arbitrary. `{0,0,1}` and gold `{5,5,2}` agree
perfectly. Use ARI or BCubed.

**Q. Precision vs recall on boundaries.**

Precision drops when single-author variation is marked as a cut.
Recall drops when a real cut is below threshold or smoothed away.

**Q. Name two confounds.**

Quoted dialogue; headings and lists; topic shift; machine translation;
very short paragraphs.

## Practical "what would you do"

**Q. The detector splits a single-author essay at a long quotation.
What now?**

Do not just lower the threshold. Either detect quotes and mask them,
merge the quoted paragraph into its host for scoring, or add a feature
that marks quoted text so the distance can be interpreted as register
rather than authorship.

**Q. You may add one resource beyond this baseline. What do you add?**

A POS tagger (syntactic rates), character 3-grams (strong but less
interpretable), or a small supervised boundary classifier trained on
PAN-style labels. Pick one and say what problem it fixes.

**Q. How would you explain a prediction to a human?**

List the adjacent distance, the threshold, and the five features with
the largest z-score gap (`inspect_features.py`). If those features are
`contraction_ratio`, `first_person`, and `discourse_casual`, the story
is register. If they are `fw_enzyme`-style leaks, the story is topic
and the model is cheating.
