# Annotation: hard-07 darkroom

Gold: `[0, 1, 0, 1, 0]` — one harbour negative, three printers.

## Why this is hard

Topic is pinned: developer, fixer, crane, safelight, tram vibration,
squeegee, fibre prints. All three authors write in the first person.
Neighbouring voices were written to share:

- the same objects;
- similar sentence length;
- overlapping function words (`I`, `the`, `and`, `a`);
- the same small ritual (test fixer with leader, pause for the tram).

What differs is slight:

- Printer A: contractions, short asides (`I don't mind the buzz`).
- Printer B: fewer contractions, a little more complete syntax,
  still `I`.
- Printer C: hedges (`I think`, `remains open`, `prudent`), slightly
  more self-conscious.

## What the baseline does

On this page it under-fires. Combined scores sit near the
same-author mass. That is not a bug in the gold labels. It is the
hard band: style exists, but a 60–100 word paragraph does not give
Yule's K enough room to say so with a pairwise threshold.

## What you would try next (oral)

1. Sequential model: CUSUM on the formality coordinate, so a small
   persistent shift alarms even when no single pair clears 0.345.
2. More text per author, which PAN sometimes has and this lab's
   hard pages deliberately do not.
3. A learned representation — after you can name why the baseline
   failed.

Do not "fix" this document until it is easy. Then it is no longer a
hard example.
