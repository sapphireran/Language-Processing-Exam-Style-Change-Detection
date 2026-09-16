# Synthetic voices

`splicefind.generate` stitches five original template voices. They
exist so you can emit a throwaway easy / medium / hard split without
touching PAN files.

| Voice                 | Habit                                      |
|-----------------------|--------------------------------------------|
| `casual_first`        | I / contractions / short clauses           |
| `formal_impersonal`   | *one may*, long sentences, no jokes        |
| `question_you`        | questions, *you*, fragments                |
| `lab_we`              | *we measured*, numbers, trials             |
| `telegram_notes`      | full stops as list glue, almost no verbs   |

```text
PYTHONPATH=src python3 -m splicefind generate -o examples/generated/synthetic-split
```

Do not treat the templates as a linguistic theory of personality.
They are exam props: stable enough that a distance should fire, small
enough that you can read every sentence aloud.
