# Walkthrough: press then notice

File: `problem-01-press-then-notice.txt`
Gold: `[0, 1, 0]`
Houses: press, press, notice, notice

## What I mark on paper

Paragraphs 0 and 1 are the compositor: "I locked the forme", "One
must", a wedding invitation, tympan cloth. Paragraphs 2 and 3 are the
clerk: "Members of the public are advised", shall, ordinance, a log of
press hours that is no longer a diary. The only hinge I want is 1→2.

## What I expect the channels to do

- NCD: press+press cheaper than press+notice, if the paragraphs are
  long enough (they are).
- Function words: `I` / `one` versus `shall` / `the` / `of`.
- Shape: mean sentence length stays long on both sides, so shape may
  not be the hero. Formal-marker rate should jump.
- Character 3-grams: ` the`, `sha`, `ll ` on the notice side.

## Oral sentence

> This is the easy split in miniature: the topic changes (shop diary
> to byelaw) *and* the house changes. A bag of words would pass. I
> still want the closed-class jump so I can say I did not *need* the
> topic leak.

## If the detector misses it

I have a bug, not a hard document. Recheck the splitter (two blank
lines?) and the threshold before I invent a story about Caslon.
