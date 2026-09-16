# Pitfalls

Mistakes that lose marks or silently wreck a detector. Each item is a
thing this repo has seen, not a theoretical list.

## Off-by-one in the label array

`n` sentences produce `n-1` labels. People emit `n` labels (one per
sentence) or `n-2` (they skip the last boundary). The evaluator in this
repo refuses to crop. If your score file shows `io_failures > 0`, look
here first.

Related: discussing “the change at sentence 3” without saying whether
that is `changes[2]` or `changes[3]`. Worked examples print both
indexes.

## Treating `authors` as the number of switches

`A A B A` has **two** authors and **two** switches. The `authors` field
is the size of the ID set. Counting `1`s in `changes` is the number of
boundaries, not the number of people.

## Debugging on the easy split and quoting it as style

If your write-up’s only number comes from `data/synthetic/easy`, you have
measured topic change. Quote `hard`, or quote both and say which signal
you think you used.

## Sentence splitter vs gold segmentation

Gold labels are defined on *the* segmentation the annotator used. If your
splitter merges two gold sentences, every later index slides and the
document becomes an I/O failure or a smear of false positives. The
synthetic set uses one sentence per line so this cannot happen during
revision. Running prose in an exam essay should mention the risk.

Abbreviations (`Dr.`, `e.g.`, `U.S.`) are the usual splitter bug. The
toolkit protects a small list; it will still break on `cf.` or `pp.`.

## Unstable features on short sentences

A five-word Hale sentence has TTR \(1.0\) and a wild Flesch number. Pair
it with a twelve-word Hale sentence and the unsupervised detector may
fire. Mitigations: drop TTR below a word-count floor, or shrink those
coordinates toward the document mean. The library currently does not;
tests document the instability so you can talk about it.

## Fitting the scaler on the test document (logistic)

The logistic model’s mean/variance belong to the **training pairs**.
Recomputing them on the test document silently changes every weight’s
effective scale. The unsupervised detector *should* recompute on the
test document. Mixing the two policies is a common implementation bug.

## Thresholding probability 0.5 after heavy class weighting

Inverse-frequency weights push \(p\) upward. On a realistic prior (few
changes) you will over-predict `1` unless you raise the threshold on the
val split. Report the threshold you used.

## Quoted speech and parentheticals

Jules quoting Mira will import Mira’s hedges inside quotation marks.
Features do not currently strip quotes. If a question gives you a
dialogue-heavy paragraph, say that quote-stripping is a missing
pre-process.

## Single-author register change

A lab report that ends in a joke is one author and a large feature jump.
Intrinsic detectors cannot tell “new person” from “same person, new
genre”. Gold labels that assume otherwise are a modelling fiction.

## Data leakage through filenames or extra JSON keys

`author_ids` in the truth file is study metadata. A detector that reads
it is cheating. The CLI evaluate path only opens truth files inside
`evaluate`. Keep it that way.

## Overfitting eight documents

`stack` pairwise features × 35 dimensions × 40 training pairs is enough
rope to hang a logistic model. If train macro-F1 is 0.99 and hard-test
is 0.50, you memorised Mira’s sentence length. Prefer `absdiff`, L2, and
the unsupervised detector as a sanity check.

## Claiming shared-task performance

This repository does not contain PAN corpora and does not report PAN
scores. Do not write as if it did. The format is compatible; the text is
not the same.
