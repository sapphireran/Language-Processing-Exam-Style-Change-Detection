# Author style cards

Four fictional house authors appear in every synthetic document. They are
not real people. The cards exist so you can predict, before running the
toolkit, which features should jump at a labelled boundary.

## Mira Chen — academic hedger

- Long sentences, often with a concessive clause.
- Loves *however*, *suggests*, *relatively*, *although*.
- Almost no contractions. Almost no `!`.
- Nominalizations: *association*, *observation*, *variation*.
- Third person or impersonal *one*; rare `I`.
- Punctuation: commas and the occasional colon; semicolons are rare.

**Should light up:** `hedge_rate`, `subord_marker_rate`,
`nominalization_rate`, `word_count`, `latinate_rate`.

**Sample (original):**

> A growing body of observational work suggests that late-evening
> surface temperatures remain relatively high when canopy cover is
> sparse, although the size of that association varies by street width.

## Jules Ortega — casual first person

- Short to medium sentences.
- Contractions: *don't*, *I'm*, *that's*.
- First person, occasional second person (*you know*).
- Intensifiers: *really*, *pretty*, *very*.
- Exclamation marks allowed but not every line.
- Concrete verbs, few nominalizations.

**Should light up:** `contraction_rate`, `first_person_rate`,
`intensifier_rate`, `exclamation_rate`, `short_word_rate`.

**Sample (original):**

> I keep meaning to grind the beans before I put the kettle on, and
> then I remember while the water's already roaring.

## Dr. Hale — technical terse

- Short declaratives. Numbers. Units.
- Passives: *was measured*, *were recorded*.
- Almost no pronouns. Almost no hedges.
- Colons before lists. Digits.
- Latinate technical nouns without Mira’s wrapping clauses.

**Should light up:** `digit_rate`, `passive_be_rate`, `colon_rate`,
`avg_word_len`, low `first_person_rate`, low `hedge_rate`.

**Sample (original):**

> Water mass was 15.0 g. Bloom time was 45 s. Drawdown was recorded at
> 3:10.

## Nell Avery — literary rhythm

- Sensory nouns, metaphors, semicolons, dashes.
- Varied sentence length; one fragment is allowed.
- Third person or a distant first person; few contractions.
- Almost no digits. Almost no hedges of Mira’s academic type.
- Coordination with *and* rather than *however*.

**Should light up:** `semicolon_rate`, `dash_rate`, `ly_adverb_rate`,
`std_word_len`, low `digit_rate`.

**Sample (original):**

> By the time the kettle clicked, the paper filter had taken on the
> faint sweet smell of a wet envelope; even the mug looked briefly
> ceremonial.

## Expected pairwise jumps

| Boundary | Features that should move |
| --- | --- |
| Mira → Jules | contractions, first person, hedges, length |
| Jules → Hale | digits, passives, pronouns, exclamations |
| Hale → Nell | digits down, semicolons up, passives down |
| Mira → Nell | hedges down, semicolons up, similar length (harder) |
| Jules → Nell | contractions down, imagery / semicolon up |
| Mira → Hale | length down, digits up, hedges down |

Mira → Nell is the hardest house pair: both write long, both avoid
contractions. Hard documents that use only those two are the honest
stress test. `problem-008` in the hard split is built that way on
purpose.

## Names in gold files

Truth files use the ids `mira`, `jules`, `hale`, `nell`. Detectors must
not read those ids. They are there so a human can sanity-check a
confusion: if the model keeps missing Mira → Nell, the card above
already told you why.
