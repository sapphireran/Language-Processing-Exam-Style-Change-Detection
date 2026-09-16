# 02 — Intrinsic vs extrinsic

This is the distinction I always get asked after I define the task.

## Intrinsic

All of the evidence is **inside the document**.

I build a stylistic profile per unit and I look for a jump. I never
meet the authors. I never see their other essays. If the document is
six sentences long, I have six sentences. That is the whole dataset.

Consequences I need to say out loud:

- There is **no training pair** of (author, text) unless I manufacture
  one from other units in the same file.
- A method that needs "100 documents per author" is not available.
- I must prefer features that **stabilise on a handful of sentences**:
  character n-grams, function-word rates, length, punctuation. I must
  not estimate a 50,000-D word embedding from eight tokens and then
  z-score it.

CUSUM, adjacent cosine, and a tiny closed vector are intrinsic. So is a
transformer that only sees the current pair, if I refuse to retrieve
anything else.

## Extrinsic

I am allowed **other texts**.

Typical uses:

- A candidate set: "is this Hamilton or Madison?"
- A web index: "did this paragraph appear somewhere else?"
- A language model trained on other writers, used as a likelihood
  under each author.

Extrinsic methods can be stronger when the comparison texts exist.
They are a **different problem**. If the exam question says the
document is the only input, retrieval is cheating, not cleverness.

## Why the exam cares

Style-change detection is interesting *because* the comparison texts
are missing. That is the situation for:

- a thesis chapter a supervisor rewrote
- a Wikipedia article with silent editors
- a chat log with sockpuppets
- an exam script that changes register halfway, which may be
  collaboration or may be panic

I should say: intrinsic SCD is often a **preprocessing** step.
Once I have cuts, I can try attribution on each block if a candidate
set later appears.

## A clean oral contrast

> Attribution: I have a closed set of authors and samples from each.
> I assign the whole document, or each block, to a name.
>
> Verification: I have two texts and I ask if they share an author.
>
> Style change: I have one text and I ask where the writer changed.
> I may never learn the names.

If I can say that without looking at notes, the rest of the oral is
details.

## Hybrid systems I should mention, then set aside

Some shared-task entries retrieve similar paragraphs from the training
split and treat those as pseudo-authors. That is extrinsic information
smuggled in through the dataset. It helps when the training documents
were built from the same forum. It does not travel to a single unseen
essay. I will mention it as a reason why leaderboard numbers can look
better than the intrinsic story.
