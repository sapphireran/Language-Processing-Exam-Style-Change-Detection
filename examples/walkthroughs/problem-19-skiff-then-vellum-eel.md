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

## After (live)

```
i votes  max|z|    pred   gold  top channels
0     0    0.74    same   same  the_rate, i_rate
1     4    2.25  CHANGE CHANGE  formal_rate, contraction_rate, oral_rate, i_rate
2     0    0.89    same   same  we_rate
```

pred `[0, 1, 0]`. Four maps at the join, none of them nouns.
This page is the oral for "show me a hard file".
