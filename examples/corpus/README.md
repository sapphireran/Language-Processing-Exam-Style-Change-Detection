# Original corpus

Thirty documents, six house voices, no PAN files, no scraped text.

| band | codes | what it tests |
| --- | --- | --- |
| control | 01–06 | one house, one topic, never fire |
| easy | 07–12 | house change *and* topic change |
| medium | 13–18 | house change, related craft |
| hard | 19–24 | house change, same topic |
| trap | 25–28 | same house, topic change — must not fire |
| return / collage | 29–30 | ABA, then four seams |

Holdout codes, unused while I stare at thresholds: **04, 10, 16, 22, 26, 30**.

Units are blank-line paragraphs. A house is allowed a short block so
the closed-class rates have enough words to be a map, not a twitch.

```bash
PYTHONPATH=src:. python3 -m examples.corpus.emit
python3 -m isogloss score examples/corpus
python3 -m isogloss inspect examples/corpus/problem-19-skiff-then-vellum-eel.txt --features
python3 -m isogloss holdout examples/corpus --ids 4,10,16,22,26,30
```

Houses are documented in `houses.md`. The detector never reads them.
`truth-problem-XX.json` carries extra keys (`houses`, `topics`,
`difficulty`) for labs. PAN only needs `changes`.
