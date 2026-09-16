# Walkthrough: problem 19

Same eel weir. Two hands. Gold `[0, 1, 0]`.

## Before the command

Units 0–1 are Skiff: *I*, contractions, *so* / *then*.
Units 2–3 are Vellum: *we* / *one*, *however* / *therefore*,
no apostrophes, longer.

Hinge 1 should mark at least `i_rate`, `contraction_rate`,
`we_rate`, `formal_rate`. Hinges 0 and 2 should be quiet.

If `digit_rate` is loud I have written a numeral by mistake.

## Command

```bash
python3 -m isogloss inspect \
  examples/corpus/problem-19-skiff-then-vellum-eel.txt --features
```

## After

Fill in from the live table:

- votes at hinge 1:
- pred:
- any fp/fn:

This page is the oral for "show me a hard file".
