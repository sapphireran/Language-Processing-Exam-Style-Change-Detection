# House voices

The corpus is written in five puppets plus a hard pair. Cards also live in `examples/voices.md`.

## River

I-voice field notes. Short. Counts, weather, gates, jars. Almost no hedges.

Use when you need a control that changes *topic* (problem-19: greenhouse, quince, night bus) or an easy snap into Marble.

## Quill

Minutes and specifications. *It was noted*, *however*, *subsequently*, *shall*. Long. No person.

Use for medium snaps out of Spark (problem-12) and for a single-author agenda control (problem-20).

## Spark

Chat. Contractions, `you`/`we`, questions, the occasional lowercase start.

Use for medium snaps (miso, darkroom, tram) and for the noisy control (problem-21). Chat-internal punctuation is a known false-alarm source.

## Marble

Lots, specimens, invoices. Digits and semicolons. The object is the subject.

Use for easy snaps from River and for collage stove-catalog lines.

## Hearth

Letters. *Dearest*, *I remain*, *do write*, exclamations.

Use for medium snaps from Marble batch sheets (quince, honey, nocturne).

## Quist vs Vale (hard)

Both write like cautious field scientists on the same chanterelle walk (problem-13). Quist likes *however / which / towards / whilst*. Vale likes *but / that / toward / while*. Register barely moves. The default blender misses the seam. That miss is the point of the file, not a bug to hide.

## How to write a new document

1. Pick a split first (easy / medium / hard / control).
2. Pick voices that match the split. Do not "make hard" by using two Rivers.
3. Write the gold `authors` array, then derive `changes`.
4. If a writer returns, check that `1 + sum(changes)` is *wrong*.
5. Run `python3 scripts/write_corpus.py` and `hingemark explain` before you trust the file.
