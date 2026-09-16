# Personal exam corpus

Eighteen original documents written for this repository. They are
**not** PAN Reddit splices and they are not copied from other course
projects.

Each `problem-*.txt` is blank-line paragraphised. The matching
`truth/truth-problem-*.json` stores the gold `changes` vector plus a
short note about why the document exists.

## How to read a file

Open with `newline=""` if you are matching PAN's warning, or just
use the helpers:

```text
python3 -m splicefind detect examples/corpus/problem-14-grandma-and-landlord.txt
python3 -m splicefind score-corpus examples/corpus
```

## Designed traps

| Id | Trap |
|----|------|
| 01 | Single author. Any predicted change is a false alarm. |
| 04 | Same topic, two lecturers. Content features should starve. |
| 07 | Author A returns. A "one cut only" story fails. |
| 14 | Same kitchen leak, grandmother vs landlord. Worked walkthrough. |
| 15 | Tiny paragraphs, unstable rates. |
| 16 | One diarist, tomato then train. Topic models should false-alarm. |

`manifest.json` is the table of contents in machine form.
