# Topic confound

A style-change system that is secretly a topic segmenter will look
brilliant on Easy and ordinary on Hard. This page is the numerical
version of that sentence.

Content vectors drop function words and tokens shorter than 4
characters (`stylechange.topic.content_vector`). Distance is
`1 - cosine`.

## Easy 001 — topic and style agree

| Boundary | Gold | style combined | topic distance |
| --- | --- | --- | --- |
| cooking → leftovers | 0 | 0.251 | 0.821 |
| leftovers → sidewalks | 1 | **0.528** | **1.000** |
| sidewalks → parking | 0 | 0.223 | 0.861 |

The gold `1` is the unique topic-distance of 1.000 *and* the unique
style-distance above 0.5. You cannot tell which signal the model used.

## Hard 001 — topic and style disagree

| Boundary | Gold | style combined | topic distance |
| --- | --- | --- | --- |
| analytic → analytic | 0 | 0.233 | **0.960** |
| analytic → “you will” | 1 | **0.394** | 0.838 |
| “you will” → “if the sour” | 0 | 0.270 | 0.903 |

The *largest* topic jump is a same-author pair (starter chemistry vs
bulk fermentation: different subtopics, same hedged voice). The *true*
author change is the *smallest* topic jump, because both writers are
still talking about dough.

If you only remember one table from this repo, remember this one.

## How to use this in an answer

1. Report Easy and Hard F1 separately.
2. Show a topic-only straw man (`topic_distance` + the same threshold).
3. Claim “style” only if you beat the straw man on Hard.

A topic-only straw man on Easy 001 with a cut at 0.95 would already
recover `[0, 1, 0]`. On Hard 001 the same cut would emit `[1, 0, 0]`,
the opposite of gold. That is the experiment in
[docs/06-worked-exam-questions.md](../docs/06-worked-exam-questions.md)
Q6, already computed.

## Reproduce

```bash
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from stylechange.detectors import ThresholdDetector
from stylechange.io import load_problem
from stylechange.topic import topic_distance

for rel in [
    "examples/data/easy/problem-001.txt",
    "examples/data/hard/problem-001.txt",
]:
    problem = load_problem(rel)
    det = ThresholdDetector().predict_paragraphs(problem.paragraphs)
    print(problem.path.name, "style", [round(x, 3) for x in det.distances])
    print(
        " " * 14,
        "topic",
        [
            round(topic_distance(a, b), 3)
            for a, b in zip(problem.paragraphs, problem.paragraphs[1:])
        ],
    )
PY
```
