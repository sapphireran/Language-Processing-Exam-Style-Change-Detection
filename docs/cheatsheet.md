# Last-minute cheatsheet

```
TASK
  input : one document, n sentences
  output: n-1 bits, 1 = author changed at that boundary
  setting: intrinsic (no named candidates at test)

DIFFICULTY
  easy  : topic + style move together
  medium: one subject, leftover lexical cues
  hard  : one subject, style only

METRIC
  macro-F1 = (F1_same + F1_change) / 2
  always-0 is the baseline; accuracy will flatter it

FEATURES TO NAME
  function words / pronouns
  punctuation ( ; — ! ' )
  hedges, intensifiers, contractions
  passives, nominalizations, length
  NOT content TF-IDF on the hard split

MODELS TO NAME
  majority baseline
  within-document z-score + distance threshold
  logistic regression on |x_i - x_{i+1}|

LIMITATIONS
  short sentences blow up TTR / Flesch
  one author, two registers looks like two authors
  splitter errors shift every later label
  pairwise models ignore run structure (A-B-A)

I/O
  problem-X.txt → solution-problem-X.json
  { "changes": [0,1,0,...] }
  open(..., newline="") if you mention PAN validators
```
