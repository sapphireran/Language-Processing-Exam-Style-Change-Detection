# Oral cards

Speak these. Do not recite the docs.

## Card 1 — Define the task

Style-change detection is intrinsic. One document, no suspects. I score every consecutive pair — a hinge — and I emit a binary array. The array records seams, not names. If a writer returns, `1 + sum(changes)` over-counts.

## Card 2 — Features

I trust closed-class rates and register flags: person, contractions, hedges, `shall`, vocatives, punctuation. I do not trust the nouns. Function-word cosine is smoothed because a ten-word sentence is a sparse histogram. Character 3-grams are damped; they mostly say the strings differ.

## Card 3 — Topic confound

Problem-19 is one gardener talking about a greenhouse, quince, and a night bus. If my detector fires, I have a topic feature. Problem-08 is two writers on the same quince paste. If my detector stays quiet, I have gone blind the other way.

## Card 4 — The 16/4 trap

Sixteen holds, four missed changes, never-fire detector. Accuracy 0.8. Change F1 0. Hold F1 0.889. Macro-F1 0.444. I will not quote accuracy as the headline.

## Card 5 — Hard miss

Problem-13, two mycologists, same transect. Gold hinge in the middle. Default cut is all zeros. That is a `same_register_miss`. I would say so, and I would not retune the study threshold just to catch it.

## Card 6 — Returning writer

Problem-22. River, catalog, River. Two writers, two snaps, three spans. Diarization would be the next model; the official label does not ask for it.

## Card 7 — Ethics

I will not run this on a classmate's essay to play policeman. Gift-authorship examples in the repo are fiction I wrote. Intrinsic stylometry is weak evidence on short text.

## Card 8 — Threshold

0.30 is a grid-search peak on these 26 files. Leave-one-out exists because one loud file should not own the cut.
