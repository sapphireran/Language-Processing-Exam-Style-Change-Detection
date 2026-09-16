# Walkthrough: Medium

Medium documents stay inside one situation. If a system still finds the
cuts, it is using register, not a change of world.

## Coffee, two voices (`problem-001`)

Gold `[1, 1, 1]`: memoir / recipe / memoir / recipe.

| Paragraph | Voice | Casualness | Giveaway |
| --- | --- | --- | --- |
| 1 | memoir | −0.116 | `wasn't`, `I'm`, `I`, `!` |
| 2 | recipe | −0.362 | imperative, numbers, `;`, `you` |
| 3 | memoir | −0.050 | `don't`, `I'm`, `I`, `!` |
| 4 | recipe | −0.560 | no `I`, semicolon, “instrument” |

```
boundary 1  CHANGE  combined=0.421  topic=0.823
boundary 2  CHANGE  combined=0.573  topic=0.906
boundary 3  CHANGE  combined=0.485  topic=0.868
```

Topic distance is high (short paragraphs, few repeated nouns) but
*not* a clean 1.000: `coffee`, `cup`, `water`, `grind` leak across
voices. Style distance still peaks at the recipe↔memoir seams. That
is the Medium signature: leftover topical overlap, usable register.

## Dough and canal

`problem-002` (house loaf) and `problem-003` (canal walk) are the same
exercise in other furniture. Gold is `[1, 1]` in both. The baseline
emits `[1, 1]` with combined distances 0.34–0.47.

Medium-002 is the tightest: 0.337 and 0.377 sit just above the default
cut. If you raise `--threshold` to 0.40 to silence Control false
positives, this document is the first to die. Write that trade-off in
any answer that quotes a single \(t\).

## Split score

```
macro-F1 = 1.000
micro: F1=1.000  tp=7 fp=0 fn=0 tn=0
```

Every Medium boundary in this toy set is a true change. That is
deliberate (so you can see recall) and unrealistic (real Medium sets
include same-author pairs). Compare Control before you generalise.
