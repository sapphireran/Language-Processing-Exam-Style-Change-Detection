# Teaching corpus

Twenty-six original documents. Each file is **one sentence per line** so the gold `changes` array has an obvious length (`n_sentences - 1`).

Truth files live in `truth/` and follow a PAN-shaped contract:

```json
{
  "changes": [0, 0, 1, 0],
  "authors": [1, 1, 1, 2, 2]
}
```

`authors` is teaching metadata. A solution file only needs `changes`.

## Splits

| Split | What it is testing |
| --- | --- |
| `easy` | Topic and register jump together. A register detector should look clever. |
| `medium` | Topic is held. Only the house voice changes. |
| `hard` | Topic is held and the two voices are close. Honest misses are expected. |
| `control` | One writer, several topics. A topic detector false-alarms here. |
| `return` | A-B-A. `len(set(authors)) != 1 + sum(changes)`. |
| `collage` | Three or four house voices. |
| `gift` / `paste` | A block was dropped in, not co-written. |

## Spotlight files

- `problem-13-two-mycologists.txt` — hard same-topic pair; the oral takeaway.
- `problem-19-river-three-topics.txt` — control; topic is not style.
- `problem-22-canal-return.txt` — returning writer.
- `problem-25-tidepool-gift-abstract.txt` — gift authorship.

Regenerate from the sentence bank with:

```bash
python3 scripts/write_corpus.py
```
