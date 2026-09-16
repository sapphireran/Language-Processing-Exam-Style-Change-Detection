# Stylometry features

Style, for this exam, is the leftover signal after you have tried not to
model *what is being said*. Good features are frequent, weakly referential,
and stable for one writer across topics.

## Closed-class words

Function words (`the`, `of`, `and`, `I`, `you`, `to`, …) are the classic
authorship cue (Mosteller and Wallace on the Federalist Papers; Burrows'
Delta). They are:

- frequent enough to estimate on a paragraph
- chosen half-automatically, so they encode habit
- only weakly tied to topic compared with nouns and verbs

The package stores a frozen English list in `stylechange.lexicon`. Rates
are relative frequencies so a 40-token paragraph can be compared with a
90-token one.

**Exam pitfall:** on very short paragraphs the function-word vector is
sparse. Cosine then jumps around even for the same author. That is why
the baseline also uses a handful of **scalar rates** and why Hard is
hard.

## Scalar register features

| Feature | Casual writing | Formal writing |
| --- | --- | --- |
| Mean word length | lower | higher |
| Mean sentence length | lower, more variable | higher, more even |
| Contraction rate (`it's`, `don't`) | high | ~0 |
| First-person singular (`I`, `me`, `my`) | high | low |
| Second person (`you`) | medium–high | low unless instructional |
| Hedge rate (`perhaps`, `tends`) | low | higher in academic prose |
| Nominalizations (`-tion`, `-ment`) | low | higher |
| `!` and `?` | more | rare |
| `;` | rare | more |

These are **not** magic. A formal writer can say `I`. A recipe can say
`you` without being casual. Features are evidence, not identity.

## The casualness axis

For the walkthroughs, scalars are collapsed into one signed score:

```
casualness =
    3.0 * contraction_ratio
  + 2.5 * first_person_sg_rate
  + 1.5 * second_person_rate
  + 2.0 * exclaim_rate
  + 0.8 * short_word_ratio
  - 2.0 * nominalization_rate
  - 1.5 * hedge_rate
  - 1.2 * semicolon_rate
  - 0.12 * avg_word_len
  - 0.015 * avg_sentence_len
```

It is a teaching device, not a published statistic. If an exam asks you
to invent a one-dimensional style axis, this is a legal shape: positive
weights on informal cues, negative weights on academic cues, plus a
gentle penalty on long words and long sentences.

## Character n-grams

Character 3-grams on a letters-and-spaces stream capture morphology and
punctuation-adjacent habits without a parser (` the`, `ion`, `n't`).
They also capture **topic** (`pasta`, `side`) if you are not careful.
The baseline down-weights them (0.10) for that reason.

## Features that look like style and are not

| Feature | Why it leaks |
| --- | --- |
| TF–IDF of content words | That is topic |
| Named entities | Topic and genre |
| Embedding cosine of whole paragraphs | Mixes topic and style |
| Sentiment | Genre / stance, not author |
| Readability grade alone | Correlates with education *and* with topic difficulty |

Use them only if the question explicitly allows a topic-aware baseline,
and flag the leak.

## Length effects

Type–token ratio and hapax rate fall as a text gets longer, even if the
author does not change. Two paragraphs of different length will disagree
on TTR for boring reasons. The baseline therefore **does not** put TTR
into the distance. It still *computes* TTR so you can inspect it.

If an exam question gives you raw TTR on a 12-word paragraph versus a
200-word paragraph, say that the comparison is invalid unless you
standardise (fixed window, moving average, or a length-corrected measure
such as MTLD).

## How two paragraphs become a number

For paragraphs \(p\) and \(q\):

1. Build style profiles \(S(p), S(q)\).
2. Scalar distance = mean relative difference
   \(|a-b|/(|a|+|b|+\varepsilon)\) on the core scalars.
3. Function-word, punctuation, and 3-gram views use cosine *distance*
   \(1 - \cos\).
4. Combined distance is a weighted sum
   \(0.55\,d_{\text{scalar}} + 0.25\,d_{\text{fw}} + 0.10\,d_{\text{3g}} + 0.10\,d_{\text{punct}}\).

A change is predicted if that number exceeds a threshold (default 0.33)
or an adaptive cut-off. Details in [04-methods.md](04-methods.md).

## Tiny inspection recipe

```bash
PYTHONPATH=src python -m stylechange.cli inspect examples/data/easy/problem-001.txt
```

You should see contractions and first person fire on paragraphs 1–2,
then collapse on paragraphs 3–4, while mean word length and
nominalizations move the other way. That opposing motion *is* the
style change.
