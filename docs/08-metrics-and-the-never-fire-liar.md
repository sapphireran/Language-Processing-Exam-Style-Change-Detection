# Metrics and the never-fire liar

Most hinges in this bank are zeros. A predictor that never fires
is accurate and useless.

On the current stacked hinges:

| predictor | macro-F1 | hinge acc | f1-change | f1-same |
| --- | ---: | ---: | ---: | ---: |
| never-fire | low | high | 0 | high |
| always-fire | low | low | modest | 0 |
| kerf | high | high | high | high |

Exact live numbers live in [14-live-results.md](14-live-results.md)
and in `python3 -m kerf score examples/corpus`. I refuse to
duplicate a table here that will rot.

## Macro-F1 as I will write it

Treat each hinge as a binary item. Compute F1 on the `change`
class and F1 on the `same` class. Average them. That is the PAN
instinct and it stops never-fire from looking like a genius.

I also print a *document-mean* F1. That number is a liar in a
different way: a three-zero control scores 0.50 macro-F1
(F1-change is 0, F1-same is 1). I mention it so I am not surprised
when the CLI and a "mean over files" notebook disagree.

## Length mismatch is a crash

If a prediction has the wrong number of hinges, `kerf.metrics`
raises. Silently padding would invent a score. I would rather fail
the script than pass the exam with a padded zero.

## Accuracy is allowed in one sentence

Accuracy is allowed as a *secondary* number, after I have said
what the class balance is. It is not allowed as a headline.
