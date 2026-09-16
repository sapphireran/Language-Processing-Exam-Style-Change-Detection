# NCD by hand

Normalized Compression Distance:

\[
\mathrm{NCD}(x,y)=\frac{C(xy)-\min(C(x),C(y))}{\max(C(x),C(y))}
\]

`C` is zlib length after I subtract the empty-input header, so two
empty strings are not infinitely far apart for a boring reason. The
score is theoretically near `[0,1]`; real compressors overshoot a
little, so the code clamps to `[0, 1.5]`.

Cross-compression gain is the same arithmetic flipped:

\[
\mathrm{gain}(x,y)=\frac{C(x)+C(y)-C(xy)}{C(x)+C(y)}
\]

High gain means the concatenation recovered budget. Low NCD and high
gain travel together.

## A worked pair from this bank

Take the first paragraph of `problem-01-press-then-notice.txt` as `x`
and the third as `y` (press versus notice). I do not copy the zlib
bytes here; I report what `python -m quoin ncd --files` says on those
two paragraphs after I split them.

The lab `examples/labs/02_ncd_by_hand.py` prints:

- word counts
- `C(x)`, `C(y)`, `C(xy)`
- NCD
- gain
- the same numbers for `x` against the *second* press paragraph
  (should be cheaper) and for `y` against the fourth notice paragraph

The qualitative result I want to be able to talk about without the
script: same-house pairs come back cheaper than cross-house pairs, and
the gap is visible even though zlib is a blunt instrument.

## Why I still add n-grams — and why NCD is often silent

On this bank, same-house and cross-house NCD both sit near 0.85. Each
paragraph is original, ~80–120 words, and zlib's cold dictionary does
not get a chance to reuse the compositor's semicolons. That is not a
bug in the formula; it is the short-text objection landing. I keep
computing NCD so I can *say* it saturated. The decision uses a
register axis (formality, sentence length, contractions) and a
within-document peak instead.

Character 3-grams are a *manual compressor*: they count the short
regularities zlib would have put in a dictionary if the string had
been longer. Cosine distance on those counts still moves when NCD
does not.

## Cross-entropy view, one paragraph

If I trained a tiny character model on `x` and evaluated it on `y`,
the cross-entropy would be low when `y` looks like `x`. Compression
length is a crude cross-entropy. That is the sentence that connects
this page to a language-modelling course without dragging in a neural
net.
