# CUSUM as a visual, not a verdict

CUSUM (cumulative sum, sometimes QSUM in older forensic notes) tracks
how a scalar wanders around its document mean.

For values \(x_1, \ldots, x_n\) with mean \(\bar x\):

\[
S_0 = 0, \qquad S_t = S_{t-1} + (x_t - \bar x)
\]

The series ends near zero. A long climb or a long descent means a
block of values sat above or below the mean. A kink is a candidate
seam.

In this kit you can dump a sparkline:

```text
python3 -m splicefind cusum examples/corpus/problem-04-tidally-locked.txt
```

Two traces are worth rehearsing:

1. **Sentence length**, sentence by sentence. Good for "notes then
   prose" and "chat then minutes".
2. **Average sentence length per paragraph.** Aligned with the PAN
   boundaries, so it can be turned into a boundary score.

The boundary score used here is naive on purpose: the absolute
difference between the mean CUSUM *increment* to the left of a cut and
the mean increment to the right. It is a slope-change detector. It is
not a likelihood ratio.

## What to say if someone mentions forensic CUSUM

QSUM plots of sentence length were sold, in some forensic contexts, as
if a kink proved mixed authorship. That overclaim is a gift for an
examiner. Your answer:

- CUSUM is an exploratory plot.
- Sentence length is one feature, and it moves with genre, editing,
  and fatigue.
- A single-author essay with a quoted table will kink.
- I would never testify from a sparkline. I would treat CUSUM as a
  feature among others and evaluate it with labelled F1.

That paragraph is more important than the recursion.
