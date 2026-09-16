# Closed-class features

Content words track topic. Function words, pronouns, deontics, and
sentence geometry track habit. The exam wants the second list.

## The long vector

`kerf.features.extract` builds a wide rate vector: about ninety
function words, plus contractions, questions, dashes, digits, mean
sentence length, type-token ratio, person rates, hedges, and a cheap
passive heuristic (`was/were` + `*ed`).

I keep the long vector for *inspection*. If a hinge is ugly I can
print the top contributions and say which habit moved.

## The saw vector

The saw does not get the long vector. A wide Euclidean space lets
topic-adjacent leftovers (a few extra *the*, a slightly longer
sentence) look like a house. The saw uses a short fingerprint:

| cue | houses it names |
| --- | --- |
| `you` / `your` / second person | Placard |
| `shall` / `must` / `any` / `such` | Statute |
| `we` / `however` / hedges | Seminar |
| `I` / `my` / dashes | Pocket |
| contractions / `anyway` / `honestly` / questions | Bench |
| `the` / `was` / digits | Caliper |

Weights live in `SAW_WEIGHTS`. They are not fitted. They are a
statement about which habits I believe I wrote.

## The possessive trap

A first draft counted every `'s` as a contraction. Then `observer's`
and `yesterday's` made Caliper look like Bench. The oral version:
spoken contractions only — `n't`, `'re`, `'ve`, `'ll`, `'d`, `'m`,
and a short list of `'s` forms that are actually verbs (`it's`,
`that's`, …).

## The rule I will recite

If I can swap the topic and keep the author, and the feature moves, it
is not a style feature. That is why nouns never enter the saw.
