# Worked walkthrough

Document: `examples/corpus/problem-14-grandma-and-landlord.txt`

Two authors describe the same kitchen leak. That is the point. If you
only needed topic, this document would look single-authored.

## Gold

```json
{
  "authors": 2,
  "changes": [0, 1, 0],
  "difficulty": "hard",
  "title": "same leak, two addressees"
}
```

Paragraphs 1–2 are a letter to a grandmother. Paragraphs 3–4 are a
notice to a landlord. Same pipes, different habits.

## What you should notice by hand

| Cue                 | Grandma letter                         | Landlord notice                          |
|---------------------|----------------------------------------|------------------------------------------|
| Person              | I, you, we                             | the undersigned, the tenancy, one        |
| Contractions        | don't, it's, I've                      | almost none                              |
| Sentence length     | short, sometimes stacked with *and*    | long, with *hereby* and *regarding*      |
| Punctuation         | commas, one exclamation                | semicolons, section-like asides          |
| Stance              | affection, apology                     | obligation, dates, receipts              |

## What the toolkit should do

```text
python3 -m splicefind report \
  examples/corpus/problem-14-grandma-and-landlord.txt \
  --truth examples/corpus/truth/truth-problem-14-grandma-and-landlord.json \
  --title "grandma vs landlord"
```

You want the middle boundary to be the only `CHANGE`. If the ensemble
also nicks one of the same-author boundaries, that is a useful oral
moment: intra-author variance is real. A letter can move from "how is
your hip?" to "the bucket is on the chair" without changing writer.

## Feature gaps worth quoting

Run:

```text
python3 -m splicefind features examples/corpus/problem-14-grandma-and-landlord.txt
```

Expect:

- first-person rate high, then collapsed
- contraction rate high, then collapsed
- impersonal / `the` mass up in the notice
- average sentence length up in the notice

If character 3-grams also jump, look at `n't` vs `the`, `ing` vs
`ancy` (*tenancy*), and `I ` vs `Th`. That is morphology plus
boilerplate, not magic.

## Why this document is in the kit

Gift authorship and "I pasted the formal paragraph from last year"
are the same geometry: a human seam inside one topic. The grandma /
landlord pair is just a friendlier story than a conference abstract.
