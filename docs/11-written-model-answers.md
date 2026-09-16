# Written model answers

These are the short essays I want to be able to write without
looking at the notes.

## 1. Define intrinsic style-change detection.

Intrinsic style-change detection asks whether the *writing
hand* changes inside a document when no comparison documents
are given. The shared-task form labels every pair of
consecutive sentences. The label is binary: same author or
new author. The problem is not "how many authors exist in
the world" and it is not "who wrote this". It is "where does
the dialect of this page jump".

Because the setting is intrinsic, a method that needs a
gallery of candidate authors is answering a different exam
question (attribution). Because the jump is local, a method
that only says "this file is multi-author" is answering the
2018 form of the task, not the sentence-level form.

## 2. Why are function words more honest than content words?

Content words follow the topic. If two authors take turns on
a kiln, the word *kiln* will not move. If one author writes
about a kiln and then about a millrace, *kiln* will fall off
a cliff. A model that rides that cliff is doing topic-change
detection. Function words (pronouns, auxiliaries, articles,
connectives, hedges) are habits of the hand. They are not
immune to genre, but they are the closest thing a short
document has to a dialect map that can stay still while the
nouns rotate.

## 3. Give a decision rule that is not a blended distance.

Estimate a small closed-class vector on each unit. At each
hinge compute a per-channel z-jump using the document's own
standard deviations. Mark a channel if the jump is above an
absolute silence floor and close to that channel's peak in
the file. Predict a change if at least k channels mark. The
rule is a vote over isoglosses. It refuses to let one loud
channel, or a bag of nouns, own the hinge.

## 4. Why is accuracy a liar here?

Style-change labels are sparse. A never-change predictor
matches the majority class and can look strong on accuracy
while scoring zero on the change class. The shared task
reports macro-F1 so both classes count. Any write-up that
quotes accuracy without the never-change baseline is
incomplete.

## 5. What goes wrong with Roll versus Brine?

Both houses are third-person and deontic. A blended register
axis that is mostly "formality" will see a small step. The
honest residual is *was/were* (minutes of a past meeting)
versus a pure *shall/must* statute, plus article stacking.
If those channels are weak in a short unit, the bundle
under-votes. The fix is to write the minutes with *it was
resolved* and the statute without past copula, not to add
the word *committee* to the feature list.
