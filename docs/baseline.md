# How the baseline decides to cut

The detector is `detect()` in `src/stylechange/detector.py`. There is no
training loop.

```
document
  → segment into units          (tokenize.py)
  → FeatureVector per unit      (features.py)
  → named voice per unit        (voices.py)
  → smooth + absorb 1-unit blips
  → mark voice-band jumps
  → maybe one register cut inside a long same-voice run
  → changes[]
```

## 1. Segmentation

`--granularity auto` (the default) does this:

- blank line in the file → paragraph units (PAN 2023)
- otherwise, if each line already looks like a sentence / production →
  one unit per line (the bundled sentence files)
- otherwise a light `.?!` splitter

You can force `--granularity sentence` or `paragraph`.

## 2. Four voices

Each unit is scored against four named voices. The winner has to beat
the runner-up by a small margin; otherwise the label is `mixed` and is
filled from a neighbour.

| voice | high when |
| --- | --- |
| **chat** | contractions, *you*, questions, casual lexis, short words |
| **student** | *I / me / my*, `I think`, hedges |
| **textbook** | academic connectives, long words, passives, *we* or *one* |
| **notes** | `->`, colons, digits, uppercase productions, missing function words |

A short line with a colon or an arrow (`CFG: S -> NP VP`, `CRF: P(y\|x)`)
is forced to **notes**. That stops a formula from being read as chat
because it happens to contain a letter `I` or a digit.

`chat` and `student` share a **personal** cut-band. A recipe that says
"yeah" and then "I" is still one person. The labels stay distinct in
`--explain` so you can talk about them.

## 3. Voice-band jumps are the easy/medium story

After smoothing, a jump `personal → textbook`, `textbook → notes`, or
`personal → notes` is a change. Isolated one-unit blips are absorbed
first (`merge_singleton_runs`), because exam answers are written in
blocks, not as a coin-flip at every sentence.

## 4. Register distance is the hard story

When a whole document is textbook-on-textbook (*we/our* vs *one/may*),
there is no voice jump. The detector then looks, inside that run, for
the cut that maximises **register distance**: the weighted L1 between
the *mean binary flags* on the left and on the right.

Flags are presence/absence, not rates:

`I`, `we`, `you`, `one`, hedge, informal/casual/contraction, notes-ish,
question.

Mean word length is **not** in this distance. A single long sentence
would otherwise invent a fake author. The default threshold is `1.00`.
On the bundled hard file the true *we* vs *one* cut scores about `1.93`;
the single-author morphology file scores ~`0` and is left uncut.

Lecture-note runs are not span-cut a second time. Notes are short and
their punctuation is chaotic.

## 5. What we refuse to do

- cosine of character 3-grams on adjacent sentences
- a per-pair logistic regression with no document context
- anything that needs `pip install` beyond the standard library
- anything that downloads a model

The CLI is `stylechange` (or `python -m stylechange`): `detect`,
`evaluate`, `features`, `voices`.
