# Feature atlas

A hinge score is only as honest as the features. This lab splits them into channels on purpose.

## Register scalars

Rates, not raw counts, except length which is divided by a constant so a two-word jitter cannot win.

| Channel | What it hears |
| --- | --- |
| `i_rate` / `you_rate` / `we_rate` | Person. River vs Quill vs Spark. |
| `contraction_rate` | Spark, some Hearth. |
| `hedge_rate` | however, therefore, subsequently, perhaps, … |
| `shall_rate` | Quill specifications. |
| `vocative_rate` | dearest, hey, yo, ok. |
| `passive_rate` | was / were / been / being / is / are as a cheap stand-in. |
| `question_rate` / `exclaim_rate` | Spark and Hearth. |
| `digit_rate` / `semi_rate` | Marble. |
| `lower_start` | Spark lines that begin `ok` or `yo`. |
| `fw_ratio` | Closed-class density. Catalogs run low. |
| `informal_rate` | gonna, kinda, anyway. |
| `mean_word_len` | Weak, scaled by 8. |
| `words_per_unit` | Very weak, scaled by 25. |

The compare function takes a **weighted L1** of those channels and squashes it: `raw / (1.15 + raw)`. Older drafts min-maxed inside the document. On a four-sentence file that made an 11-vs-10 word pair look like a full-scale change. Do not do that.

## Function-word histogram

A fixed closed-class list (`hingemark.lexicon.FUNCTION_WORDS`). Additive smoothing (`k = 0.35`) is mandatory on teaching-length sentences. Without it, two River lines that share no article look orthogonal and the blender false-alarms.

This is the channel that *might* see Quist vs Vale. On problem-13 it still does not, because the two scientists share most of the list.

## Character 3-grams

Morphology and spelling flavour. On 12-word units the cosine is almost always high (the sentences are just different strings). The blender therefore damps this channel. Mention it in the oral as "too sharp for short units."

## What we refuse

- Nouns, named entities, and topical lemmas as a change signal.
- Anything trained on a shared-task dump.
- Document-level min-max of length.

If a feature fires on problem-19 (River talking about a greenhouse, then quince, then a bus), it is a topic feature wearing a style hat. Throw it out.
