# Synthetic study set

24 original short documents for personal exam revision. They are **not**
PAN evaluation data and they are **not** scraped posts.

| Split | What varies | Intended use |
| --- | --- | --- |
| `easy/` | Author **and** topic | Debug I/O and evaluation |
| `medium/` | One subject (city cycling), leftover lexical cues | Mixed-signal discussion |
| `hard/` | One subject (pour-over coffee) | Style-only claims |

Each folder has `problem-XXX.txt` (one sentence per line) and
`truth-problem-XXX.json` (`changes`, `author_ids`, `split`, `topic`).
`manifest.json` repeats the inventory.

House authors are documented in [`docs/author-styles.md`](../../docs/author-styles.md):
`mira`, `jules`, `hale`, `nell`.

Regenerate from the committed source of truth:

```bash
python scripts/build_synthetic_corpus.py
```

Do not add third-party dumps to this folder. If you later attach an
external set, give it its own directory and licence file.
