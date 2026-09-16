# 08 — Model answers (written mock)

I wrote this paper for myself. Timing: about 90 minutes. I do not
copy a shared-task abstract. I answer in the same voice I would use
in an exam hall.

---

## Q1. Define style-change detection and separate it from attribution and verification. (10)

**Answer.** Style-change detection is an *intrinsic* authorship problem:
given a single document and no reference set, mark the positions at
which the writer changes. Units are specified (paragraphs in older
setups, sentences in the current one). The usual output is a binary
vector of length `n − 1` in which a 1 means that unit `i+1` does not
share an author with unit `i`.

Authorship *attribution* assumes a closed candidate set and samples
from each candidate; the system names the writer of a text or of a
block. Authorship *verification* is given two texts and must decide
whether they share an author. Neither task is asked to find cuts
inside one unseen document, and both are allowed extrinsic evidence
that style-change detection does not get.

A short contrast: attribution asks "whose?", verification asks
"same person?", style change asks "where?".

---

## Q2. Why is the task intrinsic? When would extrinsic information help? (8)

**Answer.** It is intrinsic because the operational settings that
motivate it — gift authorship, silent collaborative edits, some
plagiarism, sockpuppets — do not come with a folder of comparison
texts. The detector may only look at the document.

Extrinsic information helps when a candidate set later appears: once
the cuts exist, each block can be attributed. It also helps, in a
weaker sense, when a training split is built from the same community
and a system retrieves similar paragraphs as pseudo-authors. That
trick inflates a leaderboard and does not travel to a single essay.
I would mention it as a caveat, not as my method.

---

## Q3. Name four feature families and one feature from each. Which family is most robust when topic is held still? (10)

**Answer.**

1. Character n-grams — overlapping character 3-gram cosine.
2. Closed-class lexical — function-word relative frequencies, L1.
3. Surface / complexity — mean word length, sentence length.
4. Register cues — contraction rate, first- vs second-person, hedges.

When topic is held still I trust (1) and (2) first. Character 3-grams
still leak some content stems, but they also carry morphology and
punctuation. Function words are the cleanest "glue" signal. Sentence
length helps when the two writers differ in rhythm and does nothing
when they do not. A topical embedding is the family I would *drop* on
a hard split.

---

## Q4. Explain why character n-grams work on short units. (8)

**Answer.** A six-word SMS does not support a stable word-unigram
distribution. Character 3-grams still observe contractions (`n't`),
emoticons, padding around punctuation, and morphological endings
(`ing`, `tion`). They do not require a tokenizer argument, so an
exam implementation stays small. The representation is a sparse
count vector; I compare two units with cosine and take `1 − cosine`
as a distance. The failure mode is shared boilerplate and very short
units with almost no gram mass, which is why I keep an absolute
distance floor.

---

## Q5. Compute a CUSUM by hand. Lengths: 4, 5, 4, 5, 18, 16, 17, 19. Where is the candidate cut? (12)

**Answer.** Mean `μ = 88/8 = 11`. Increments: `−7, −6, −7, −6, +7, +5, +6, +8`. Cumulative sum:

```
S = 0, −7, −13, −20, −26, −19, −14, −8, 0
```

The series decreases for four observations and then increases for
four. The slope reversal is after sentence 4, i.e. pair index 3. I
would only accept the reversal if both runs are long enough to rule
out a single noisy sentence; here each run has length 4, so I accept
it. I would still treat CUSUM as a cue, not as a complete detector,
because two writers with the same preferred length leave `S` flat.

---

## Q6. Gold `0 0 1 0 0`, prediction `0 1 1 0 0`. Macro-F1? State the empty-class convention. (10)

**Answer.** Class 1: `TP=1, FP=1, FN=0` so `P=0.5`, `R=1`, `F1=2/3`.
Class 0: `TP=3, FP=0, FN=1` so `P=1`, `R=0.75`, `F1=6/7`.
Macro-F1 `= (2/3 + 6/7)/2 = 16/21 ≈ 0.762`.

Convention: if a class never occurs in gold or prediction, I take
precision and recall as 1 rather than 0, so a perfect single-author
document scores 1.0 instead of 0.5.

---

## Q7. What is the topic confound, and how do easy / medium / hard splits try to control it? (8)

**Answer.** If authorship and topic change together, any content
feature fires at the cut and the system looks better than its style
sensitivity. Easy constructions allow that correlation. Medium
constructions add topical drift that is no longer a reliable cue.
Hard constructions keep units on roughly the same subject so the
system must use register, rhythm, and closed-class choice. A fair
claim therefore needs a same-topic number, not only an easy-split
number.

---

## Q8. Design a baseline you could implement in twenty minutes. (12)

**Answer.** Split the document into the required units. Score each unit
on a closed cue sheet I can recite (slang, imperative, formal notes,
``we`` versus ``one``, first person). Cut when the label changes;
reuse an id when a label returns. Keep character 3-grams and
function-word L1 as the explanation I show for a pair, but do not
threshold raw pair cosine on six-word sentences — they barely overlap
even inside one writer. Evaluate with pairwise macro-F1. I would not
fine-tune a transformer in twenty minutes, and I would write down that
the baseline will miss two careful academics who share register.

---

## Q9. A returning author appears after a third writer. What extra machinery do you need, and which metric notices if you skip it? (8)

**Answer.** Boundary detection only needs a yes/no at each pair.
Returning-author assignment needs a memory of previous centroids (or
a clustering step over all units). If I mint a new id at every cut I
can still score a perfect pairwise F1 and a poor ARI. The metric that
notices the skip is ARI (or BCubed), not boundary F1. Example:
`authors = [1,1,2,2,1,1]` versus `[1,1,2,2,3,3]`.

---

## Q10. Limitations of a neural sentence-pair classifier on this task. (8)

**Answer.** A fine-tuned pair classifier is a strong practical tool
and still has exam-relevant limits. It encodes topic extremely well,
so it overfits the easy leak unless the training data already
controls topic. Short units give it little style to work with. It
does not by itself assign returning-author ids. It is opaque in an
oral: I can say "the CLS cosine jumped" and I cannot show a function
word. Finally, a model trained on forum concatenations may not
transfer to exam scripts or scientific abstracts. I would use it in a
project with a same-topic ablation sitting next to it.

---

## How I mark myself

If an answer does not mention **units**, **intrinsic**, and **one
failure mode**, I have written a blog post. Q5 and Q6 are binary: the
numbers are right or I lost the marks. Q8 must be implementable, not
a shopping list of paper names.
