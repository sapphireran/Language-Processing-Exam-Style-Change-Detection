# 10 — Failure modes

I lose easy marks when I only praise the method. This is the list I
recite at the end of an answer.

## 1. Short units

A six-word SMS does not have a stable 3-gram profile or a meaningful
function-word distribution. Pair distances become noise. Mitigation:
windows, or refuse to cut below an absolute floor.

## 2. Topic leak

See [06-topic-confound.md](06-topic-confound.md). Easy numbers lie.
Mitigation: a same-topic split and features that survive noun
replacement.

## 3. Same-register academics

Two careful writers on the same subject, both using `however` and
long sentences, will not move CUSUM or contractions. The hard file
is a mild version of this. A real thesis chapter is worse.
Mitigation: more text per unit, or accept that intrinsic SCD has a
ceiling.

## 4. Quoted material and formulae

A student who pastes a definition inherits someone else's 3-grams
for one sentence. The detector sees a cut, or worse, sees a return
to the source. Mitigation: strip quotes if the format allows; say
so if it does not.

## 5. The always-0 prior

Changes are rare. A timid threshold looks strong on accuracy and
misses the only cut that mattered. Mitigation: report class-1 F1,
not accuracy.

## 6. The always-1 prior

The opposite sin on a collage. Macro-F1 still punishes it, but a
confused implementation that thresholds at 0 will emit it.
Mitigation: the absolute floor.

## 7. Returning authors

Boundary F1 does not check ids. I can "solve" Task 2 by incrementing
a counter and still fail ARI. Mitigation: keep centroids; say when I
did not.

## 8. Grain mismatch

Evaluating sentence cuts against paragraph gold is not a method
problem, it is a bookkeeping problem. I will lose the marks anyway.

## 9. Language and code-switching

The closed function-word list is English. A Danish/English mix (I
have written those emails) will look like a cut at every switch even
when the writer did not change. Mitigation: say the inventory is
language-specific.

## 10. Overfitting the study folder

These ten files were written to be detectable. A detector that
scores 1.0 here and 0.4 on unseen polite prose is a teaching toy.
I will say that in the README and in the oral.

## The sentence I close with

> Intrinsic style-change detection is the right tool when comparison
> texts do not exist, and it is a weak tool when the writers share
> register, topic, and length. My baseline is for the first case. I
> will not sell it as the second.
