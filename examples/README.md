# Examples

These files are original study texts, not a shared-task dump. Each paragraph
is long enough for closed-class frequencies to be less noisy than a slogan.

| File | Gold shape | Why it exists |
| --- | --- | --- |
| `documents/single_author_formal.txt` | A A A A A | False-positive check for a lecture voice |
| `documents/single_author_casual.txt` | A A A A A | False-positive check for a chatty voice |
| `documents/mixed_formal_casual.txt` | A A A B B B | One clean cut |
| `documents/mixed_three_authors.txt` | A A B B C C | Two cuts, three clusters |
| `documents/mixed_return_author.txt` | A A B B A | Two authors, three blocks |

Gold labels live in `documents/labels/`. Author ids are arbitrary integers;
only equality matters.

## Commands

From the repository root, after `pip install -e .`:

```bash
style-change detect examples/documents/mixed_formal_casual.txt
style-change evaluate examples/documents/mixed_formal_casual.txt \
    examples/documents/labels/mixed_formal_casual.json
python examples/run_demo.py
python examples/inspect_features.py examples/documents/mixed_three_authors.txt
```

`run_demo.py` also works without an editable install because it puts `src/`
on `sys.path`.
