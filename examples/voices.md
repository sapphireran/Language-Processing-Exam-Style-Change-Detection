# House voices

These are exam puppets, not people. Keep them consistent when you write a new document.

## River

Field journal. First person, short sentences, almost no hedges, almost no questions. Counts and weather. Typical openers: *I walked*, *I counted*, *I wrote*.

Register flags: high `i_rate`, low `hedge_rate`, low `question_rate`.

## Quill

Minutes and specifications. Third person or dummy subject (*it was noted*). Long sentences, `however` / `therefore` / `subsequently` / `accordingly`, passives, `shall`.

Register flags: high `hedge_rate` and `passive_rate`, near-zero person.

## Spark

Group chat. Contractions, `you` / `we`, questions, exclamations, occasional lowercase start, `anyway` / `gonna` / `kinda`.

Register flags: `contraction_rate`, `you_rate`, `question_rate`, `lower_start`.

## Marble

Object labels and invoices. Measurements, lot numbers, semicolons, no person. The thing is the subject.

Register flags: `digit_rate`, `semi_rate`, low `fw_ratio`.

## Hearth

Letters. *Dearest*, *I remain*, *do write*, warm adjectives, exclamations, coordinated clauses.

Register flags: `you_rate` plus `exclaim_rate`, some `i_rate`, almost no digits.

## Hard pair: Quist and Vale

Both write like cautious field scientists. Quist prefers *however / which / towards / whilst*. Vale prefers *but / that / toward / while*. Topic words stay shared on purpose. Function-word cosine is the channel that *might* see them; register often does not.
