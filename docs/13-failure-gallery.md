# Failure gallery

Walk these documents with `python -m seamtrace inspect <file>`
before the oral. The filenames are the teaching set, not PAN.

## The topic trap — `problem-02-bikes-vellum.txt`

Easy. Author and subject change together. If this is your only
demo, you have shown a topic detector. Ask yourself: which channel
carried the hit, function words or trigrams-plus-nouns?

## The false friend — `problem-20-campus-return.txt`

Control. One writer, one afternoon, two scenes (kitchen, then the
S-train). A content model wants to fire in the middle. Gold is all
zeros. A false alarm here is `topic_confound` or
`single_author_drift`.

## The quiet seam — `problem-14-two-bakers.txt`

Hard. Same loaf, two bakers. Look at first person, hedging, and
imperatives. If the default cut misses, the tag should be
`register_only` or `threshold_near_miss`. This is the document you
want on the projector.

## The short yes — `problem-10-committee-slack.txt`

Medium. Minutes, then a chat paste that includes fragments.
`Yes.` and `lol ok` are legal sentences in this lab. TTR on those
lines is meaningless. Windowing would help; bravado will not.

## The gift abstract — `problem-11-gift-authorship.txt`

Medium. Formal we-voice methods, then a first-person "I just
wrote the figure caption." Ethically this is a *discussion
starter*. Do not write a misconduct sentence in the solution
file.

## The collage — `problem-21-housing-collage.txt`

Four voices, several returns. `sum(changes) + 1` is not the
author count if someone speaks twice. Check the manifest.

## The measurement flood — `problem-17-flora-walk.txt`

Hard-ish field notes. Digit rate and Latin binomials look like
style and are actually genre. Two botanists can share that genre.
Trust function words and sentence length more than `digit_rate`.

## The lyric rain — `problem-18-same-rain.txt`

Same shower, diary vs meteorological note. Easy to overfit to `!`
and imagery. A detector that only uses `exclaim_mark` will look
clever here and die on `problem-16-chess-endgame.txt`.
