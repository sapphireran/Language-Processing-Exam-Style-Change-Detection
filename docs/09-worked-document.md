# Worked document: 19, same weir, two hands

`examples/corpus/problem-19-skiff-then-vellum-eel.txt`

Four units. Gold: `[0, 1, 0]`. Topic is the eel weir the whole
way. If a noun model is required to find the hinge, I have
failed the hard band.

## Units in prose

1–2. Skiff. *I don't*, *I'll*, *so*, *then*. Short, first
person, no *however*.

3–4. Vellum. *We ought*, *one therefore*, *however*, *this
does not*. Long, no apostrophes.

## What should mark at hinge 1

| channel | direction |
| --- | --- |
| `i_rate` | down |
| `contraction_rate` | down |
| `oral_rate` | down |
| `we_rate` | up |
| `formal_rate` | up |
| `n_words` | up |

That is already more than `k=3`. Hinges 0 and 2 stay inside a
house, so peaks should sit at hinge 1 and the relative rule
should not spray marks onto the quiet seams.

## How I inspect it

```bash
python3 -m isogloss inspect \
  examples/corpus/problem-19-skiff-then-vellum-eel.txt --features
```

I want `CHANGE` only on `i=1`, with a vote count I can read
aloud, and top channels that match the table above. If
`digit_rate` is in the top four, I have a bug or I
accidentally wrote a numeral into Vellum.

## What I say if it misses

Either Vellum picked up an *I* (it must not), or the units
are too short for `s_f` to mean anything, or `k` is a coward.
I fix the prose or I admit the miss. I do not add *eel* to
the feature list.
