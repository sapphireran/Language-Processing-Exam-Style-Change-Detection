# Live results

Re-run:

```bash
python3 -m quoin report examples/corpus
python3 -m quoin baselines examples/corpus
```

The labs write a copy under `examples/reports/live-results.md`.

## What I will claim, and what I will not

I will claim that on **this original bank** the blended detector
beats never-fire and always-fire on macro-F1, that easy register
jumps usually light up, that the two single-author controls stay
dark, and that zlib NCD saturates (so the peak + register rule is
doing the deciding). I will not claim that zlib authorship is state
of the art, and I will not quote these numbers as if they were PAN
test scores. The peak margin and the absolute cutoff were fit on the
same files.

## Snapshot (this revision)

| predictor | macro-F1 | micro-F1 | mean acc |
| --- | ---: | ---: | ---: |
| never-fire | 0.179 | 0.000 | 0.667 |
| always-fire | 0.461 | 0.500 | 0.333 |
| quoin | **0.612** | **0.653** | 0.798 |

Per-band notes I will say out loud:

- **control** — both files F1 1.00 (all zeros, correctly).
- **easy** — five of six files perfect; the funicular/complaint file
  picks the louder intra-complaint hinge. Owned miss.
- **hard** — the workshop pairs (pewter, thatch, lantern, tram, cave)
  are where sentence length and mouth-feel actually move. This is the
  pleasant surprise, not a generalisation claim.
- **trap** — press-on-three-topics stays quiet. Notice and chat each
  pick one false peak. Gift-abstract is too even for the peak rule.
- **return / collage** — recall is partial; the peak rule wants one
  loud hinge.

Accuracy of never-fire is 0.667. That is the table I want on the
board before anyone quotes mine.
