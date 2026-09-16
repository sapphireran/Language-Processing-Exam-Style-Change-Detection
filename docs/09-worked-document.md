# Worked document

Document **16** (`problem-16-stilling-caliper-then-seminar`) is the
one I will do on paper if asked. Same stilling well. Caliper for
two paragraphs, Seminar for two. Topic cannot help.

## The gold

```
changes = [0, 1, 0]
```

Hinge 1 is the only cut. Houses: Caliper, Caliper, Seminar, Seminar.

## What I compute by hand (sketch)

I do not compute the full saw vector in an oral. I compute the
three rates that actually move.

| para | house | *was* / *the* | *we* / *however* | *you* | mean sent (words) |
| --- | --- | --- | --- | ---: | ---: |
| 0 | Caliper | high | none | none | ~16 |
| 1 | Caliper | high | none | none | ~12 |
| 2 | Seminar | low | present | none | ~28 |
| 3 | Seminar | low | present | none | ~28 |

The left-right split after paragraph 1 groups two Caliper means
against two Seminar means. That is the loudest kerf. After
paragraph 0 I would be comparing one Caliper paragraph to a mix.
After paragraph 2 I would be comparing a mix to one Seminar
paragraph. The size weight also likes the balanced cut.

## What kerf prints

```bash
PYTHONPATH=src:. python3 -m kerf inspect \
  examples/corpus/problem-16-stilling-caliper-then-seminar.txt
```

Expect a high split at hinge 1, a high adjacent at hinge 1, and
`pred = [0, 1, 0]`. Reason: `split`.

## Why this is the hard band, not the easy band

Easy files also change the topic (well → booth, ice → filter).
Here both sides talk about a slipped chart drum and a peak that
might be a labelling event. A content model has almost nothing to
grip. The hedges and the *we* are the grip.

## A second file if they want a trap

Document **20** is the same Caliper hand on a well and then on a
booth. I can list the nouns that change (*float*, *xenon*) and the
function words that do not (*the*, *was*, *recorded*, no *you*,
no *we*). Gold is `[0, 0, 0]`. Kerf agrees.
