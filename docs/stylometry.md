# Stylometry notes (oral-exam crib)

Stylometry is the measurement of *how* someone writes, as opposed to
*what* they write about. The classical claim, going back at least to
Mosteller & Wallace on the Federalist Papers, is that **function words**
are a better fingerprint than content words:

- they are frequent, so estimates are less sparse
- they are topic-light, so "the" vs "and" does not mean "this paragraph
  is about cooking"
- they are hard to fake; people do not decide to stop saying *however*

That is why `src/stylechange/lexicon.py` is a closed-class list and not
a bag of nouns.

## Features that survive a 12-word sentence

A PAN sentence is short. Rates estimated on 12 tokens are noisy. The
inventory in `features.py` is therefore small and mostly *binary* when
we compare spans:

| cue | what it is a proxy for |
| --- | --- |
| `I / me / my` (capital I only) | student / diary |
| `we / our` | first-person-plural academic |
| `one / one may` | impersonal academic |
| `you` | tutorial / chat |
| contractions (`n't`, `'m`) | speech-like register |
| hedges (`maybe`, `basically`, `I think`) | student hedging |
| academic connectives (`therefore`, `moreover`) | textbook |
| colons, digits, `->` | lecture notes / productions |
| mean word length, type–token | richness (kept for display, not for the hard cut) |

Lowercase `i` in `P(w_i)` is **not** first person. English `I` is. That
distinction is tested.

## Register is not identity

Two people can share a register (both write textbook English) and still
have different habits (`we` vs `one`). One person can change register
without changing identity (a student who pastes a definition, then goes
back to "I think"). The baseline therefore:

1. names four *voices* for explanation (`chat`, `student`, `textbook`,
   `notes`)
2. collapses `chat` and `student` into one **personal** band when it
   decides to cut
3. only looks for a second cut inside a same-voice run if a binary
   register flag actually moves

If an examiner asks "is style the same thing as author?", the honest
answer is **no**, and this code makes that explicit.

## Topic is a confound, not a feature

A sudden jump from recipes to constituency trees *is* a style change in
the easy document, but the detector is not allowed to rely on the nouns
`oven` and `NP` as its only evidence. We count `chuck` / `messy` as
casual lexis and `->` as a notes flag. We do not embed the sentence and
cluster by cosine of content words. That choice is deliberate and
slightly costly on the easy split — and it is the choice you defend
when someone says "BERT would just work".

## What a neural model would do differently

A fine-tuned encoder (or a style embedding trained with a verification
loss) would compare contextual representations of adjacent *windows*,
not of single sentences, and would need a calibration set. It would
almost certainly beat this baseline on real PAN data. It would also be
a worse oral-exam artefact: you cannot point at the weight on `we`.
This repository is the inspectable baseline, not the shared-task entry.
