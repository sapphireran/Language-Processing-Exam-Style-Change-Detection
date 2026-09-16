# Written model answers

Longer versions of the oral cards. I would cut these to the word limit
on the day; I am not pretending they are a finished script.

## 1. Define intrinsic style-change detection and say what the system
must output.

Intrinsic style-change detection asks, given only a document and no
external comparison corpus, at which paragraph boundaries the author
changes. A document of `n` paragraphs yields `n-1` binary decisions.
The conventional on-disk form is a JSON object whose `changes` array
holds those decisions in order. A `1` at index `i` means paragraphs
`i` and `i+1` are attributed to different authors. The task is not to
name the authors and not to cluster non-adjacent paragraphs, although
both are natural extensions. "Intrinsic" rules out building author
profiles from other documents; the evidence has to come from
contrasts inside the file. That is why the problem is the right
neighbour of intrinsic plagiarism detection and of gift-authorship
spotting, and the wrong neighbour of closed-set attribution.

## 2. Why is accuracy a misleading headline metric here?

Author changes are sparse. In a four-paragraph single-author document
the gold vector is `[0,0,0]`. A system that emits `[0,0,0]` for every
document will obtain high accuracy on any bank whose base rate of
change is low, and it will obtain a useless recall of zero on the
documents that actually contain a change. Shared-task evaluation
therefore uses F1, typically computed per document and then averaged
(macro). A complete comparison table should also include a never-fire
baseline and an always-fire baseline so that a reported F1 has
neighbours. I treat the all-zero / all-zero case as F1 = 1 so that a
correctly untouched control document is a success rather than an
undefined score.

## 3. Explain Normalized Compression Distance and its limits on this
task.

NCD estimates how much extra compressed length is needed to encode
`y` once `x` is known, normalised by the harder of the two separate
lengths. If a compressor is a decent approximation to Kolmogorov
complexity, strings that share regularities — including the half-
conscious regularities we call style — produce a low score. I use
zlib because it is in the standard library and I can print `C(x)`,
`C(y)`, and `C(xy)` in a lab. Limits: (i) short paragraphs spend most
of `C` on headers and a cold dictionary; (ii) topic words are
regularities too, so NCD will shrink when two authors discuss the
same objects; (iii) the compressor *is* the feature function, so a
different compressor is a different model. I therefore blend NCD with
character 3-gram cosine and a closed-class profile, and I refuse to
quote an easy-split score as evidence that the blend measured style.

## 4. How would you stop a system using topic as a proxy for
authorship?

At data level, evaluate on a slice where topic is held still (the
PAN hard split, or my same-topic workshop pairs) and on a slice where
author is held still while topic moves (my trap files). At feature
level, prefer closed-class frequencies, punctuation, and sentence
shape over content n-grams, or at least report an ablation that
removes the open class. At model level, do not tune only on easy
data. At rhetoric level, do not lead with the easy number. A
transformer does not get a free pass: pretraining is a topic model
with extra steps.

## 5. Sketch a baseline you can implement in an afternoon and say
how you would report it.

Split on blank lines. For each adjacent pair, compute a small vector:
zlib NCD, cosine distance on character 3-grams, L1 on function-word
relative frequencies, L1 on a handful of shape rates. Take a weighted
sum, threshold it, emit the bit vector. Report macro-F1, micro-F1,
accuracy, and the two constant baselines. Show one worked document
with a per-channel table. State that the threshold was fit on the
same toy bank you are quoting, so the number is a rehearsal. That is
the whole afternoon, and it is enough to have a conversation about
the task.
