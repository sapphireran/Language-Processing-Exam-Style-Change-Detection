# What the exam is actually asking

Style-change detection is an **intrinsic** authorship problem. You are
handed one document and no gallery of known writers. You have to say
whether the sheet was folded, and where.

Three questions show up in slightly different wording:

1. **Does this document contain a style change at all?**
2. **How many authors wrote it?**
3. **Between which units (sentences or paragraphs) did the voice change?**

This lab trains (3). If you can mark the folds, (1) is "were there any
folds?" and (2) is "how many faces did the sheet show?" — with a trap:
a returning author shows two faces and three or more folds.

## What a style change is not

It is not a new topic. A baker who writes about dough, then a night
bus, then a cat, in the same first-person contracted English, has not
folded the sheet. See `problem-19-stall-three-topics`.

It is not a new named entity. Switching from *Mira* to *Jan* is not a
fold.

It is not "the writing got more technical." Two bellfounders can both
be technical in the same hedged *we* and still be two people. The
default detector will **miss** that pair. That miss is the point of the
hard set, not a bug you should hide in the oral.

## What a style change is

A change in **register**: closed-class habits that survive a topic
swap. On this course the habits we count are:

- who is speaking (I / you / we)
- whether the writer contracts
- whether the writer installs *shall* / *must* / *hereby*
- whether the writer hedges

If those rates jump between adjacent units and the jump is a peak, we
call that a fold.

## The answer the examiner wants

A binary list one shorter than the unit list. `1` means "fold after
this unit." Plus, if asked, an author count that you can defend.

Do not lead with accuracy. Lead with the fold list and the named error
you expect on the hard pair.
