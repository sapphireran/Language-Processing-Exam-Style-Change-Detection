# 7. Exam study notes

Short answers you can reuse. Each block is one typical prompt plus
the points a marker usually wants. These are personal reconstruction
notes, not a leaked paper.

## Define intrinsic style-change detection

Identify the positions in a *single* document where writing style
(and therefore likely authorship) changes, using only evidence from
that document. No candidate authors, no reference corpus.

## Contrast with attribution and verification

- Attribution: closed set of candidates + samples → pick one.
- Verification: one claimed author + samples → same/different.
- Style change: one document → pairwise same/different between
  neighbours.

The first two are extrinsic. The third is intrinsic.

## Why sentence level is harder than paragraph level

Shorter units ⇒ noisier stylometric estimates (TTR, function-word
rates). More pairs per document ⇒ more chances to false-alarm.
Class imbalance usually gets worse. Topic cues may still dominate
on easy data, so the extra difficulty is not uniform across bands.

## Why easy / medium / hard exist

To stop topic segmentation from masquerading as stylometry. Easy
allows topical and authorial changes to coincide. Hard holds topic
nearly constant so leftover performance is closer to style.

## Name five authorial features

Function-word frequencies; contraction rate; punctuation profile;
average word length / sentence length; character n-gram cosine.
Honourable mentions: pronoun rates, hapax rate (with length caveat),
comma vs full-stop habits.

## Name two topical features that leak on easy data

Content-word TF-IDF cosine; named-entity overlap; embedding
similarity of "aboutness". Jaccard on word sets is a lightweight
version of the same leak.

## Why macro F1, not accuracy

Changes are rare. Always predicting "no change" has high accuracy
and zero useful detection. Macro F1 averages the two classes.

## Off-by-one

`n` units ⇒ `n-1` pairwise labels. The last unit has no successor.
Truth and prediction must use the same segmentation.

## Function words: why they work

Frequent, topic-stable, produced with low conscious control, hard
to fake consistently. Classic stylometry (Mosteller & Wallace,
Burrows) is built on them.

## Why TTR is a trap on sentences

Type-token ratio shrinks as a text gets longer even if the writer
does not change. Comparing an 5-word unit to a 25-word unit on TTR
is mostly a length comparison.

## Cluster then cut vs pairwise classify

Clustering units into k authors can recover a segmentation, but you
must choose k and the official metric still scores consecutive
pairs. Pairwise classification matches the label definition
directly. Clustering is a reasonable *system*, not a different
*task*.

## Transformer vs stylometry (essay skeleton)

Transformers win when pretraining + pair context capture topical
and semantic ruptures (easy band). They struggle when neighbouring
sentences share content words (hard band) unless fine-tuning data
forces attention onto closed-class cues. Stylometry is weaker on
easy data (less topical firepower) and more interpretable on hard
data. A fair comparison trains and tests on each band, not only
on easy.

## List assumptions of the official formulation

English; change only between units; a unit is single-authored;
labels are pairwise not author IDs; evaluation ignores author
names; extra training data must be released if used in the shared
task.

## What "intrinsic plagiarism detection" shares with this

Both look for a rupture inside one text. Plagiarism systems often
add a second stage: search the web for the deviant segment.
Style change stops at the rupture. Do not describe a web search
in an answer that asked for an *intrinsic* method.

## A 10-minute revision checklist

1. Draw a 6-sentence document and write `changes` of length 5.
2. Reconstruct author runs from that vector.
3. Compute macro F1 on a 4-pair confusion matrix (note 5).
4. Explain one easy-band leak and one hard-band failure.
5. List function-word vs content-word examples.
6. State the I/O filenames (`problem-X.txt` /
   `solution-problem-X.json`).
7. Say why class-weighted logistic regression is a fair baseline.
8. Say why training only on easy data poisons hard-data tests.

`examples/05_hand_features.py` is the interactive version of (1)–(4).
