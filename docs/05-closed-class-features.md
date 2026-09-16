# Closed-class features

Open-class words name the world: *tympan*, *brood*, *funicular*,
*smalti*. Closed-class words glue the world: *the*, *of*, *shall*,
*I*, *gonna*. Stylometry's oldest useful bet is that the glue is more
about the person and the open class is more about the day.

I use three closed-ish channels in Quoin:

1. **Function-word profile** — relative frequencies of a fixed list.
   L1 between two paragraphs. Topic-light by construction.
2. **Shape** — mean sentence length, comma / semicolon / question
   rates, contraction rate, informal-marker rate, formal-marker rate,
   type-token, mean word length.
3. **Character 3-grams** — not closed-class in the linguistic sense,
   but they catch `the `, `; I`, `'s `, `n't` without me listing every
   word.

## Why I will not pretend POS is free

A part-of-speech histogram is a good style feature. It is also a
dependency I cannot install in an oral. If they ask, I will say I
would add it, and that the tagger becomes part of the model.

## Burrows' Delta, in one breath

Delta compares an author's z-scored function-word frequencies to a
disputed text. It is extrinsic: you need a candidate set and a
background. I mention it so I can say why I am *not* using it. Quoin
compares two paragraphs to each other, not to a gallery. Pairwise L1
on raw relative frequencies is the intrinsic cousin.

## What I tally if they hand me a printed paragraph

- count of `;` and `?`
- count of `'t` / `'s` / `'m` contractions
- count of `shall` / `hereby` / `must`
- count of `gonna` / `kinda` / `idk`
- mean words per sentence (split on `.?!` and live with the damage)
- a handful of function words: `I`, `the`, `of`, `and`, `to`

That tally is enough to talk about press versus notice, or student
versus gift-abstract, without a laptop.
