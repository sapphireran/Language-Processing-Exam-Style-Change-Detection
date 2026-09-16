# Original example corpus

Twenty-eight short documents I wrote for revision. They are **not** PAN
data. They are not scraped. Each file is a PAN-style problem: paragraphs
separated by a blank line. Truth lives under `truth/` as
`truth-<stem>.json` with a `changes` array and, where it helps teaching,
an `authors` array.

`manifest.json` is the index the CLI reads.

## Bands

| band | what I planted | what a fair detector should do |
| --- | --- | --- |
| `control` | one voice, one house | all zeros |
| `easy` | voice *and* topic jump | light up the hinge |
| `medium` | nearby topics, different register | still find the hinge |
| `hard` | same topic, two close workshop voices | this is where I expect to miss |
| `trap` | same voice, different topics; or a gift paragraph | stay dark, or mark only the gift |
| `return` | author A leaves and comes back | two hinges, not a new third voice |
| `collage` | three or four houses in one file | several hinges |

## Voices

See [`../voices.md`](../voices.md). The short names in the truth files
(`press`, `notice`, `chat`, `claim`, …) match that sheet.

## Regenerating the text files

The prose is stored in [`bank.py`](bank.py). Re-emit with:

```bash
python3 -m examples.corpus.bank
```

Do not paste PAN Reddit threads into this folder.
